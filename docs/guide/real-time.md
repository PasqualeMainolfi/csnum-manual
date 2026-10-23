# Real-time paths

## Why perf time is different

Csound runs every opcode of every active note once per control period, on the
same thread that fills the audio buffer. In real time that thread works against a
deadline: the next buffer is due whether or not the orchestra has finished
computing it. At 48 kHz with `ksmps = 32` a control period lasts two thirds of a
millisecond.

A call into the allocator has no bounded running time. `malloc` and `realloc`
can take a lock another thread holds, walk long free lists, or ask the operating
system for fresh pages. Most calls return quickly, but it only takes one slow
call to miss the deadline, and a missed deadline is a dropout: a click in the
output, intermittent, and hard to trace back to its cause. That is why
real-time audio code allocates what it needs up front and never on the audio
thread.

csnum arrays are dynamic by design. Most k-rate opcodes can change the shape of
what they publish from one pass to the next, and a larger shape needs new
storage. Offline, or on a chain that only feeds analysis, that is harmless. On a
chain that ends in the speakers it is exactly the kind of allocation real-time
code must not do. The real-time mark is how you tell csnum which arrays are on
such a chain.

## What the mark guarantees

A marked array, and every buffer an opcode keeps to produce or rewrite it,
never takes new storage during performance. Init time is unrestricted, and it
is where the storage is taken. Writing new values, and changing the layout
within the storage already there, stay allowed at any time, so a marked array
can be reshaped, truncated, or resized back up to its capacity.

When a pass would need more storage than a marked array has, the opcode does
not allocate. It raises a performance error that names the array, which stops
the note:

```
PERF ERROR in instr 1 (opcode csnpad) line 36: [csnarray] Array is on a
real-time path and cannot grow from 64 to 96 elements at perf time; clear the
mark with csnrtunlock, or pass irt=0 at the audio source it descends from
```

That error is the point of the mark. A performance error stops the note the
moment the chain does something it cannot afford, and it tells you which array
did it. A dropout gives no such report.

## How arrays get marked

Every way of marking sets the same flag on an array:

| Source of the mark | When it applies | What it covers |
| --- | --- | --- |
| `csnfromaudio`, `csnpack`, `csnsnap` (`irt = 1`, the default) | when the array is published | the audio frame and everything derived from it |
| `csnrtlock data` | at init, or on a triggered k-rate pass | that one array |
| `csnrtlockstart` ... `csnrtlockend` | while the section is open | every array the current note creates in between; the note ending also ends the section |
| `csnrtlockall` | from its line in the orchestra header onward | every array created for the rest of the performance, with no way to switch it off |

An array derived from a marked operand inherits the mark when it is created, so
marking the source of a chain marks the chain. The mark belongs to the array it
is set on:

- locking a source later does not reach the arrays already derived from it;
- `csnrtunlock` clears one array and nothing else, so a branch that only feeds
  analysis can be released while the rest of the chain stays marked;
- `csnrtlock(data, 0)` is an inactive k-rate trigger, not an unlock.

```csound
instr 1
    trig:k          = 1
    win:k           = 5
    src:CsnArr      = csnzeros(fillarray(64))
    csnrtlock src
    smooth:CsnArr   = csnmovmedian(src, win, -1, trig)  ; inherits the mark

    csnrtlockstart
    frame:CsnArr    = csnzeros(fillarray(256))          ; marked by the section
    spectrum:CsnArr = csnrfft(frame, 256, -1, trig)     ; marked by the section
    csnrtlockend
endin
```

## What it covers

The mark is enforced wherever storage could grow during performance, not only
where an opcode publishes a result:

- **Published outputs.** An output keeps the storage it was created with, room
  for twice its initial element count, and reuses it for any later shape that
  fits. A marked output can therefore shrink, grow back, or change its count
  with the data (`csncompress`, `csnselect`, `csnunique`, the set operations)
  without new storage; only a shape that needs more than that room is
  refused.
- **Arrays rewritten in place.** `csnpush`, `csninsert`, `csnsetinsert`, and
  `csnpad` or `csnresize` without an output refuse to grow a marked array past
  its capacity.
- **Working buffers.** The scratch an opcode keeps for itself, the sort buffer
  of a median or the sorted window of `csnmovmedian` for instance, is reserved
  at init for the most the array it serves can hold. A window that grows
  mid-note, or a lock applied after the opcode, therefore never needs the
  allocator. Where a buffer would still have to grow, the opcode refuses in the
  same way.
- **Transforms.** The FFT convolutions and correlations refuse a new transform
  size on a marked path before the FFT setup is allocated. Their transform
  buffers follow the output's mark, which the output took from its operands at
  init, so `csnrtunlock` on the output releases them as well.
- **Csound arrays.** The k-rate forms of `csntoarray` and `csnshape` reserve
  their output at init, so a marked source that moves within its capacity never
  makes Csound grow the output array.
- **Strings.** Each element of a `CsnStr` keeps the buffer of its string, and a
  k form writes its strings into those buffers. On a marked string array a
  pass runs as long as every string fits the room its element already holds,
  and the first string that does not fit stops it with a performance error
  (`A string needs 22 bytes, its slot holds 4, ...`). The room is set at init:
  a marked output gets room for the longest string its operands hold, and the
  forms that make new strings (`csnstradd`, `csnstrmul`, a fill) size it from
  what they compute there. Writes in place (`csnset`, `csnsetslice`,
  `csnputmask`, a one-string `csnpush`) check every element first, so a pass
  that stops changes nothing. `csnload` and the in-place `csnpad` and block
  `csninsert` rebuild their strings on every pass and stay refused. See
  [String arrays](../reference/string-arrays.md#real-time-paths).

Two things stay outside the guarantee. `csnsave`, `csnload` and `csnprint` do
file or console I/O on the performance thread, which no mark can make real-time
safe. Csound's own copy-on-write of an output array that has been shared with
another variable is Csound's to perform.

## Building a chain that never trips it

- **Settle shapes at init.** Every derived opcode sizes its output from its
  source at init, so a chain fed by an array of fixed shape allocates once per
  note and never again. A shape that depends on a k scalar (a pad width, a
  slice, a k axis) is not known at init (see
  [What the init pass computes](k-rate.md#what-the-init-pass-computes)): give it as a
  constant or an i variable when it does not move, or start its k variable at
  the largest value with `init`, which `csnpad` takes as the room to reserve.
- **Reserve what has to grow.** An array can grow up to its capacity without
  new storage. A derived output has room for twice the element count it had at
  init; one that has to vary further should start at init from the largest
  shape it will take. `csnempty` reserves a shape without publishing any
  element, which gives `csnpush` and an in-place resize room to grow into.
- **Give strings their longest value at init.** A marked string array writes
  into the room its elements took at init, so build it there with strings at
  least as long as the ones its k forms will write.
- **Unmark what does not go back out.** Frames harvested only for analysis do
  not need the guarantee: pass `irt = 0` at the audio source, or `csnrtunlock`
  the branch.

---
