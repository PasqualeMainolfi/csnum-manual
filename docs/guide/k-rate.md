# k-rate performance: array versioning

The interesting part of csnum is what happens when these opcodes run inside the
k-rate loop, thousands of times per second, on arrays that usually have not
changed since the last pass.

Every array carries four counters, data, shape, ndim and item type, bumped only
by a writer that actually changed that aspect. A k-rate opcode records the
version of its source, and of the output it writes, at the end of a pass that
did real work. On the next pass it compares:

- the **source** version, including its array identity, so a different array
  with the same counters is not mistaken for the previous input;
- the **output** version, so an opcode that finds its result untouched
  can reuse it instead of recomputing it;
- the **request**, shape, ndim, item type and any scalar parameter it depends
  on, such as an axis or a window size.

If all of them match, the opcode keeps last pass's result and returns. No
allocation, no copy, no arithmetic. A chain of csnum opcodes driven by a source
that moves once every few hundred k-cycles therefore costs almost nothing on the
passes in between, and the saving compounds along the chain: a consumer sees its
own input as unchanged precisely because the producer upstream skipped its work.

Three details make this safe rather than merely fast:

- **The output array is reused.** A k-rate producer writes into its
  destination variable for the life of the note. The array is created with room for
  twice its initial element count, and a later shape that fits that room
  reuses it; new storage is taken only when the requested shape no longer
  fits.
- **In-place opcodes publish their write.** They bump the data version *and*
  record it as their own, so the next pass recognizes its own handiwork and
  leaves it alone, while every other consumer still sees a new generation.
- **Self-aliasing is checked per operation.** Elementwise operations can read
  and write the same cell in place when shape and type stay the same. Layout
  changes and operations with their own safe in-place algorithm also allow it.
  Operations that would overwrite input they still need refuse the alias.

Scratch buffers are per-opcode-instance and reserved at init from the capacity
of the array they serve, so a k-rate pass allocates nothing in steady state.
Off a real-time path they may still grow, geometrically, when an array outgrows
that capacity; on one they may not (see [Real-time paths](real-time.md#real-time-paths)).

One limit is worth stating plainly, because it is easy to read the counters as
promising more than they do. A bumped data version means **a producer wrote this
array on that pass**, not that the contents differ from the pass before. A k-rate
producer may rewrite its output on every pass it runs, so anything downstream that
tries to answer "has a new value arrived?" from the version alone will hear yes
on every pass as soon as a single k-rate opcode sits in between. That is fine
for skipping work, which is what the counters are for — a false "changed" costs
a recomputation and nothing else. It is not enough for an opcode that must act
exactly once per arrival: `csnstream` counts hops on a phase accumulator of its
own and uses the version only to notice a producer that has stopped.

## What the init pass computes

A k-rate opcode also runs an init pass, and it computes its result there only
when every argument the result depends on is known at init: a constant, an i
variable or an array. A k scalar is not: an ordinary k variable still reads 0
during the init pass, so a result computed from it would be wrong, and nothing
downstream could tell. With such an argument the init only lays the output out
and the first triggered pass computes it:

- an opcode that keeps the rank (`csngetslice`, `csnpad`, `csnconcat`,
  `csntranspose`, `csnreshape`) gives the source's layout, reserved but empty;
- one whose shape the k argument decides (a reduction or `csndiff` along a k
  axis, `csnmedfilt1d`) gives an empty 1-D array;
- an elementwise one (`csnclip`, `csngt` and the comparisons) keeps the
  source's shape with values not computed yet; `csnrotmat` gives a zero matrix.

```csound
instr 1
    trig:k        = metro(10)
    axis:k        = 0
    fixed:CsnArr  = csnsum(mat, trig, 0)    // reduced at init and on each trigger
    moving:CsnArr = csnsum(mat, trig, axis) // empty until the first trigger
endin
```

An output written over its own operand (`X = csnclip(X, lo, hi, trig)`) is not
computed at init either: every pass applies it, so the first one does. A
consumer that cannot take an empty array belongs behind the same trigger; the
k-rate `csntoarray` accepts one at init and converts from the first pass.

---
