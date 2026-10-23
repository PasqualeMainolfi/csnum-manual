# csnum: numpy-style array opcodes for Csound 7

**NOTE:** *csound-numeric is currently in the testing phase.
Bug reports, feedback, suggestions, and reports of unexpected behavior
are very welcome and greatly appreciated, as they help improve the
library and make it more stable and reliable.*

`csnum` is a Csound 7 plugin that brings a numpy-shaped array vocabulary into the
orchestra language: n-dimensional arrays with a shape and strides, elementwise
math, axis-wise reductions, slicing, sorting, statistics, linear-algebra
primitives, convolution, matrix solving, interpolation and resampling. `CsnArr`
values can also be combined with the orchestra's arithmetic operators, and read
and written with `[]`: `v[i][j]` for one element, `v[start:end]` for a slice.

The suite is deliberately narrow: it covers **array work only**. There is no
signal generation and no GUI. Two doors lead out of that: `csnsave` / `csnload`
persist an array to disk, and the audio bridge moves blocks of samples between
Csound's audio signals and csnum arrays, so an analysis chain can be written
with array operations and sent back out as sound.

Arrays hold either **real** values (one double per element) or **complex** values
(two doubles per element). Both are first class: creation, conversion, indexing,
reshaping, arithmetic, the reductions and the linear-algebra primitives take
either, and promote a real operand to complex when an operation mixes the two.
Operations with no meaning over the complex field, ordering comparisons,
sorting, rounding, the window functions, interpolation, are real-only and say
so when handed a complex array.

There are **no external library dependencies** beyond Csound and the C standard
library. The plugin builds from C11 sources against the Csound plugin headers.

---
