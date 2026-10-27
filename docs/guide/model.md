# The model: `CsnArr` values, not Csound arrays

A csnum array is a value of type `:CsnArr;`: the variable owns its data, and
opcodes exchange these values, never Csound `k[]`/`i[]` arrays:

```csound
values:i[]  = fillarray(4, 1, 3, 2)
data:CsnArr = csnfromarray(values) // Csound array -> CsnArr
back:i[]    = csntoarray(data)     // CsnArr -> Csound array
```

`csnfromarray` / `csnfromftable` are the way in, `csntoarray` / `csntoftable` the
way out; on the audio path the pairs are `csnfromaudio` / `csntoaudio` and
`csnpack` / `csnunpack`. Everything in between stays in csnum arrays, so a chain
of twenty operations copies data no more than the operations themselves require.

Assignment copies: after `B = A`, writing `A` leaves `B` as it was. `csncopy(A)`
also makes an independent copy. If `A` is a valid set array, both copies retain
its set classification.

The data is released with the variable that owns it: a local at the end of its
note, an `@global` one, shared across instruments, when Csound releases its
globals.

```csound
shape@global:i[]     = fillarray(1024)
buffer@global:CsnArr = csnzeros(shape)
```

(In the orchestra header an inline `array(...)` argument is still empty when the
opcode reads it, so bind the shape to a named i-array first, as above.)

Arrays carry up to 8 dimensions and at most 2^28 elements. Shape and strides are
kept in the array, so a reshape or a transpose is a layout change, not a copy.

## Arithmetic operators

`CsnArr` supports `+`, `-`, `*`, `/` and `^` directly in Csound expressions.
They act elementwise on two arrays; `^` raises each element to the corresponding
power. Each operator also accepts a real scalar on either side, or a complex
scalar. Array shapes broadcast from the right as in NumPy, and mixing real and
complex operands produces a complex array. `*` is elementwise multiplication;
use `csnmatmul` for matrix multiplication.

```csound
instr 1
    iA[] = fillarray(2, 4, 6)
    iB[] = fillarray(1, 2, 3)
    A:CsnArr = csnfromarray(iA)
    B:CsnArr = csnfromarray(iB)

    sum:CsnArr        = A + B    // [3, 6, 9]
    difference:CsnArr = A - B    // [1, 2, 3]
    product:CsnArr    = A * B    // [2, 8, 18]
    ratio:CsnArr      = A / B    // [2, 2, 2]
    shift:CsnArr      = 10 - B   // [9, 8, 7]
    squares:CsnArr    = B ^ 2    // [1, 4, 9]

    A += B                       // [3, 6, 9]
    A -= B                       // [2, 4, 6]
    A *= 2                       // [4, 8, 12]
    A /= 2                       // [2, 4, 6]
endin
```

`+=`, `-=`, `*=` and `/=` update the left array. Assignment and the earlier
results remain independent copies. The operators take no trigger: they follow
the rates of their operands, so the i-rate example above runs during
initialization, while an operation with a k-rate operand runs on each control
period. To make an operator run at k on arrays built at init, cast one of them
with `csnk` (see [Choosing the rate](#choosing-the-rate-named-opcodes-take-a-trigger-operators-a-cast)). To inspect the result during performance, use
`csnprint(A, kTrig)` with a non-zero k-rate trigger; `csnprint(A)` reads it only
at initialization. Inside an instrument, passing `array(...)` directly to
`csnfromarray` selects its k-rate overload; use a named `i[]` built with
`fillarray` when the compound result is needed during initialization. An
operation that would overwrite values it still needs,
or change the target's layout, is refused. The corresponding named opcodes
(`csnadd`, `csnsubtract`, `csnmul`, `csndiv`, `csnpow`) remain available, including
their trigger forms.

An audio signal can be an operand too, on either side of `+`, `-`, `*`, `/` and
`^`: it takes part as its block of `ksmps` samples, an array of shape `(ksmps,)`,
as `csnfromaudio` would give, and the result is k-rate and marked as a
real-time path. A matrix of shape `(channels, 1)` therefore broadcasts a signal
into one row per channel, which `csnunpack` turns back into signals, sample
for sample at any `ksmps`:

```csound
mat:CsnArr = csnfromarray([1, -1])
csnreshape(mat, [2, 1])
y:CsnArr = x + mat * (ap * g)    // (2, ksmps): x + ap*g and x - ap*g
ys:a[]   = csnunpack(y)
```

The signal is computed only during performance, so the init pass lays the
result out and the first pass computes it.

On `CsnStr`, `+` joins elementwise, two arrays with broadcasting or an `S` on
either side, and `*` repeats each string by a count on either side, as
`csnstradd` and `csnstrmul` do; `+=` and `*=` update the left array. A string
operand has no rate, so an operator on an i-rate array runs again at perf
when its `S` changes, and `X += Sv` on an i-rate `X` appends once per change.
On one `S`, `+` and `*` join and repeat strings (`S1 + S2`, `S * 3`, `Sx +=
Sy`, `Sx *= n`); Csound has no arithmetic on strings, so these operators exist
only with csnum loaded. An `S` has no rate, so they compute at init and at perf
again only when an operand changed. See [string arrays](../reference/string-arrays.md#operators).

## Indexing with `[]`

`v[i][j]` reads and writes one element, one index per dimension, and
`v[start:end, step, axis]` reads a slice. The end of a slice is included, as in
Csound's own `slicearray`, and the axis is 0 unless given.

```csound
iShape[] = fillarray(2, 3)
M:CsnArr = csnreshape(csnarange(0, 6, 1), iShape)  // [[0, 1, 2], [3, 4, 5]]

iValue = M[1][2]             // 5
M[0][0] = 10                 // [[10, 1, 2], [3, 4, 5]]
Cols:CsnArr = M[1:2, 1, 1]   // [[1, 2], [4, 5]]
```

A write with only i arguments runs once, at init; a k value or index makes it
run on every control period, and the array k-rate. `[]` needs Csound 7.0,
which lets a plugin type provide it (csound PR #3363). See
[Indexing and slicing with `[]`](../reference/indexing.md) for the rules, including
what the slice syntax cannot express.

## Choosing the rate: named opcodes take a trigger, operators a cast

**The rule is one per kind of call, and it never mixes:**

| | How the rate is chosen | i-rate | k-rate |
| --- | --- | --- | --- |
| **Named opcodes** (`csnadd`, `csnsum`, `csntranspose`, ...) | the trigger, written in the call | no trigger: `csnadd(A, B)` | a trigger: `csnadd(A, B, kTrig)` |
| **Operators** (`+`, `-`, `*`, `/`, `^`, `+=`, ...) | the rate of the operands, set with a cast | i-rate operands: `A + B` | a k-rate operand: `csnk A`, then `A + B`, or `csnk(A) + B` |

For a named opcode the trigger must be written to get the k-rate form: Csound
picks the overload at compile time from the arguments of the call, and the form
without the trigger is the init-time one, whatever the rate of the arrays you
pass it. The cast has no effect there. An operator cannot take a trigger, so it
reads the rate of its operands instead, and `csnk`/`csni` are the way to set it.

An array carries its rate: i-rate when an i-rate opcode built it, k-rate once a
k-rate opcode produces or writes it. An operator runs on every control period
only while one of its operands is k-rate, so with i-rate operands it runs once,
at init. Two casts choose the rate at the point where it matters, as `k()` and
`i()` do for scalars:

```csound
instr 1
    iShape[] = fillarray(3)
    step:CsnArr = csnfull(iShape, 0.5)
    acc:CsnArr  = csnzeros(iShape)  // i-rate: built from i arguments

    csnk acc                        // in place: acc lives at k from here on
    acc += step                     // 0.5, 1, 1.5, ... on every pass

    base:CsnArr  = csnfull(iShape, 10)
    moved:CsnArr = csnk(base) + step  // only this expression is k-rate
    first:CsnArr = csni(acc)          // acc frozen at its init value
endin
```

| You want | Write |
| --- | --- |
| an array that operators keep updating | `csnk A` before using it |
| one expression at k, the operands untouched | `csnk(A) + B` |
| the init value of a k-rate array | `csni(A)` |

Running at k does not mean recomputing on every pass: a k-rate operation skips
its work while its operands and its result are unchanged, and only an operation
written over its own operand, as `A += B`, applies on every pass. Cast before
use: an operator that met `A` still i-rate has already applied once at init.

The casts reach the operators only: `csnadd(A, B)` still runs once, at init,
even after `csnk A`, because the call without a trigger is the init-time form.
Write `csnadd(A, B, kTrig)` for k.

## Empty arrays

An array with no elements is an ordinary value here, not an error case.
`csnempty` reserves a shape without publishing any element: `csnsize` reports 0
and `csnisempty` reports 1, while `csnshape` still reports the extents that were
reserved. That reservation is the capacity `csnpush` fills, so an array built up
element by element only reallocates when it outgrows what was reserved.

```csound
cap@global:i[] = fillarray(4)
buf:CsnArr     = csnempty(cap) // size 0, room for 4
csnpush(buf, 10)
csnpush(buf, 20) // size 2
last:i = csnpop(buf) // 20, size back to 1
```

Empty arrays travel through the rest of the suite instead of stopping it: the
shape transforms return an empty result of the right rank, concatenation with an
empty operand yields the other one, and `csnsum` over an empty array is 0 rather
than an error. The item type is an i-argument, so an array can also be declared
empty *and* complex from the start with `csnempty(cap, 1)`.

## Set arrays and their invariant

A set array is a one-dimensional real array kept in ascending, duplicate-free
form. `csnlikeset` establishes that invariant; the set operations and the
in-place `csnsetinsert` / `csnsetremove` operations preserve it.

Generic array operations do **not** guarantee the set invariant. In particular,
a generic in-place write or transformation may leave the values unsorted or
duplicated. A later set operation rejects such an array rather than silently
using binary search on invalid data. Pass the modified array through
`csnlikeset` again to produce a normalized set. `csnunlikeset` instead removes
the set classification when ordinary array semantics are intended. See
[Set arrays and their invariant](../reference/set-arrays.md) for the complete contract.

```csound
a:CsnArr = csnlikeset(csnfromarray(array(3, 1, 2, 2)))
b:CsnArr = csnlikeset(csnfromarray(array(2, 4)))
both:CsnArr = csnsetunion(a, b)       // [1, 2, 3, 4]
csnsetinsert both, 5                  // [1, 2, 3, 4, 5]
has3:i = csnsetcontains(both, 3)      // 1
```

The API also provides intersection, difference, symmetric difference, removal,
and subset, superset, disjointness, and equality predicates. Each opcode has a
runnable example in the [set-operation reference](../reference/index.md#sorting-and-sets).

## String arrays: `CsnStr`

A `CsnStr` is an array of strings with the layout of a `CsnArr`: a value that
owns its strings, copied by `B = A`, released with its variable. It is a type
of its own, so the numeric opcodes refuse it when the orchestra is compiled;
the ones that also make sense on strings have a `:CsnStr;` overload, and
`csntype` reports `2` for one.

```csound
labels:S[]  = fillarray("kick", "snare", "hat", "tom")
grid:CsnStr = csnfromarray(labels)
grid[3]     = "crash"                     // [] stores a copy
first:S     = grid[0]                     // "kick"
csnsave(grid, "labels.npy")               // np.load gives dtype <U5
```

Creation (`csnempty`, `csnfull`, `csnlike`, `csnfromarray`), the way out
(`csntoarray` to `S[]`, `csnprint`), elements and slices (`csnget`, `csnset`,
`[]`, `csngetslice`, `csnsetslice`, `csntake`), the queries, the layout
opcodes (`csnreshape`, `csnflatten`, `csntranspose`, `csnflip`, `csnroll`,
`csnreverse`), `csnframe`, `csnconcat`, `csnstack` and `csnpad` with a string fill,
`csnpush`, `csnpop`, `csninsert`, `csnremove`, `csntruncate`, `csnhead`,
`csnresize`, `csncopy`, `csnshuffle`, the masks (`csnwhere`, `csnputmask`,
`csncompress`, `csnselect`), the elementwise `csnstradd`, `csnstrmul`,
`csnstrupper`, `csnstrlower`, `csnstrcapitalize`, `csnstrswapcase`,
`csnstrtitle`, `csnstrstrip`, `csnstrlstrip`, `csnstrrstrip`, `csnstrcenter`,
`csnstrljust`, `csnstrrjust`, `csnstrreplace` and `csnstrsubstr`, the string
queries `csnstrlen`, `csnstrfind`, `csnstrrfind`, `csnstrstartswith`,
`csnstrendswith`, `csnstrisalpha`, `csnstrisdigit`, `csnstrisalnum` and
`csnstrisspace` (to a real array), the conversions `csnstrtonum` and
`csnnumtostr`, the join `csnstrjoin` (to one `S`), the splits `csnstrsplit`,
`csnstrrsplit`, `csnstrpartition` and `csnstrrpartition` (from one `S`), the
byte conversions `csnstrchr`, `csnstrord`, `csnstrtoascii` and
`csnstrfromascii`, the UTF-8 ones `csnstrencode`, `csnstrdecode`,
`csnstrtocodepoints` and `csnstrfromcodepoints`, the lists `csnstraslist`
and `csnlistasstr`, the number bases
`csntobinary`, `csnfrombinary`, `csntohex`, `csnfromhex`, `csnbinstrtoarr`
and `csnhexstrtoarr`, the base64
`csntobase64` and `csnfrombase64`, the byte buffers `csntobuffer` and
`csnfrombuffer` (a dtype `S`), the rate casts
`csni` and `csnk`, and
`csnsave` / `csnload` (`.npy` as `<U` or `|S`, `.csn`) take one today. A
string has no k form, so their k forms take an explicit trigger. Each element
keeps the buffer of its string, so on a [real-time path](real-time.md#real-time-paths) a k
pass writes into the room the init pass gave it and stops only at a string
that does not fit. See [String arrays](../reference/string-arrays.md) for the list, the
file formats, the real-time rule and a runnable example.

## Printing arrays

`csnprint` writes the shape, element type and values directly to Csound's message
stream. Values use five significant digits and nested arrays follow numpy's
bracket and indentation style:

```csound
values:i[] = fillarray(1.234567, 2, 3, 4)
shape:i[]  = fillarray(2, 2)
mat:CsnArr = csnreshape(csnfromarray(values), shape)
csnprint(mat)
```

```text
CsnArr(shape=(2, 2), dtype=float64)
[[1.2346 2]
 [3 4]]
```

Arrays with more than 1000 elements are summarized with their first and last
three entries along every long dimension. The k-rate form,
`csnprint(data, trig)`, prints on a non-zero trigger and emits nothing when the
trigger is zero. See the full [csnprint reference](../reference/csnprint.md).

---
