# What is covered

Grouped by what they do, rather than listed one by one. The full list, with a
one-line description and the rates each opcode supports, is in
[`OPS_INDEX.md`](../reference/ops-index.md); one page per opcode, with every overload, the
meaning of each argument and a runnable example, is under
[`doc/`](../reference/index.md). Coming from NumPy, the table in
[NumPy correspondence](numpy.md#numpy-correspondence) maps every opcode to the call it
stands for. The examples are also standalone `.csd` files in
[`example/`](https://github.com/PasqualeMainolfi/csound-numeric/tree/main/example), and all of them run:

```sh
csound --opcode-dir=build example/csnsort.csd
```

- **Creation**: empty / zeros / ones / full / identity, `csnlike` to build one
  shaped like an array you already have, `arange`, `linspace`, `logspace`,
  `geomspace`, seeded random arrays.
- **Conversion, lifetime and inspection**: to and from Csound arrays and
  function tables, copy, type and shape queries, and numpy-style printing.
- **Shape and layout**: reshape, flatten, transpose, flip, roll, pad, truncate,
  head, resize, concat, insert, remove, push, pop.
- **Indexing**: element get/set, also as `v[i][j]`, slices, also as
  `v[start:end, step, axis]`, gathers, integer-bin counting
  (`bincount`), insertion-point search (`searchsorted`), and the
  index-returning searches (`indexof`, `argwhere`, `argnonzero`, `argisnan`).
- **Elementwise math**: the four operations plus power, log, divmod, hypot; the
  usual transcendental and rounding functions; degree/radian conversion; phase
  wrap and unwrap.
- **Comparison and logic**: the six comparisons, logical and/or/not, counters
  (`cnteq`, `cntnz`, `cntnan`), `all` / `any`.
- **Reductions and statistics**: sum, prod, mean, min, max, median, variance,
  standard deviation, percentile, quantile, argmin/argmax, cumulative sums and
  products, differences, gradient, and moving-window statistics.
- **Sorting and sets**: permutations, sort, argsort, unique, argunique, set conversion,
  membership, union, intersection, difference and set predicates.
- **Linear algebra and geometry**: dot, inner, outer, matmul, trace, diagonal,
  norms, normalize, cross product, distances, angular distance, vector
  projection and rejection, reflection, the three matrix operations that need
  a factorization — `csnsolve`, `csninv`, `csndet` — and `csnsavgol`, which
  builds a Savitzky-Golay filter for `csncorrelate1d` to apply.
- **Complex**: real / imaginary parts, angle, conjugate, conversion to and from
  real arrays, and scalar arithmetic on a `:Complex;` value — `csnadd`,
  `csnsubtract`, `csnmul`, `csndiv`, `csnpow`, `csnsqrt` with two complex
  operands or one complex and one real, plus `csnabs`, `csnangle` and `csnconj`
  on a single one.
- **Fourier analysis**: full and real FFT/IFFT along one axis or across a 2-D
  matrix, STFT/ISTFT, frequency-coordinate arrays, FFT shift/unshift, and the
  DCT-I/II and DST-I/II at any length, the analytic signal in one and two
  dimensions and the Hilbert transform on its own.
- **Cepstral and mel analysis**: mel-frequency cepstral coefficients in one
  opcode, and the triangular mel filterbank itself, linear or logarithmic.
- **Convolution and correlation**: convolution and cross-correlation, with a
  1-D kernel flat or along one axis, or with a kernel shaped like the source,
  over NumPy's FULL / SAME / VALID spans — computed directly, or through
  Fourier transforms for the kernels long enough to make that pay.
- **Interpolation and resampling**: `csninterp` (linear, nearest, previous,
  next, monotone cubic PCHIP, with error / clamp / fill / extrapolate boundary
  policies), `csnresample`, `csnlagrange` for the coefficients of the
  polynomial through a set of points, and `csnroots` for the roots of a
  polynomial, one per slice along an axis.
- **Filter design**: digital Butterworth, Chebyshev type I and II and
  elliptic filters as sections or coefficients (`csnbuttersos`,
  `csncheby1sos`, `csncheby2sos`, `csnellipsos` and their `ba` forms), applied
  to arrays or audio with `csnsosfilter` and `csnlfilter`, or with an explicit
  state through `csnzsosfilter` and `csnzlfilter`, the same four families on
  audio with a k-rate cutoff or band, redesigned every control period without
  allocating (`csnrtbutter`, `csnrtcheby1`, `csnrtcheby2`, `csnrtellip`), the analog
  Butterworth prototype (`csnbuttap`), the transforms of a lowpass prototype to lowpass,
  highpass, bandpass and bandstop, on transfer-function coefficients or on
  zeros, poles and gain, the bilinear transform to a
  digital filter, and `csntftozpk` / `csnzpktotf` between transfer-function
  coefficients and zeros, poles and gain, and `csnzpktosos` into second-order
  sections.
- **Windows**: Hann, Hamming, Bartlett, Blackman, Kaiser.
- **Persistence**: `csnsave` and `csnload` use `.csn` for csnum's own format or
  `.npy` for NumPy interoperability, preserving shape and real/complex type.
- **Coordinate systems**: conversions between cartesian coordinates and the
  polar, cylindrical and spherical systems, each pair named for its own; the
  spherical order is `(r, theta, phi)` with `theta` the inclination from `+z`,
  and an optional flag takes or answers the angles in degrees. `csndegtorad` and
  `csnradtodeg` also convert a single number.
- **Special functions**: the associated Legendre functions and the real
  spherical harmonics of the AmbiX convention (ACN, SN3D), one at a time or the
  whole set up to an order, at one direction or as a channels x directions
  matrix to build a decoder from. Neither carries the Condon-Shortley phase.
- **Room acoustics**: reverberation time by Sabine and by Eyring-Norris from a
  volume and its absorbing surfaces, the absorption a target time demands, the
  Schroeder frequency that separates a room's modal region from its diffuse one,
  and the modal frequencies of a rectangular room. Either operand may be an
  array, so a set of rooms or a range of targets is one call. `csnt60tofbg` and
  `csnfbgtot60` cross from the room to the reverb that models it: the feedback
  gain a comb of a given delay needs to decay by 60 dB in a given time, and the
  decay time a gain actually produces.
- **Levels and time conversion**: `csndbsum` adds levels in dB by adding their
  powers — over a pair, a whole array, or one axis — and the four sample/time
  conversions take the sample rate as an argument rather than reading the
  orchestra's, so material carrying a rate of its own converts against it.
- **Audio bridge**: `csnfromaudio` / `csntoaudio` move one control period between
  an audio signal and an array, `csnpack` / `csnunpack` do the same for a whole
  `a[]` as a `channels x ksmps` matrix, and `csnsnap` / `csnstream` slice a stream
  into overlapping frames of a size independent of `ksmps` and overlap-add them
  back. Arrays on an audio path refuse to reallocate during performance.

## Conventions shared by the whole suite

- **Axis argument.** Explicit axes follow NumPy indexing: `0` is the first axis,
  `-1` the last, `-2` the penultimate, and valid values run from `-ndim` to
  `ndim - 1`. Omitting the axis is a separate operation, never an alias for
  passing `-1`: depending on the opcode it means flatten first, operate on all
  axes, use the last axis, or is not allowed. Each opcode documents its default.
  The broad families are: flat for global reductions, cumulative operations,
  normalisation, moving statistics, interpolation/resampling and 1-D
  convolution; all axes for flip, pad and truncate; last axis for FFT-like
  transforms, difference and sorting. Structural operations such as take,
  slice and stack require an axis; the slice syntax `v[start:end]` is the
  exception, along axis 0 unless an axis follows the step.
- **In-place forms.** Where it makes sense, the opcode that produces a new
  array also has a sibling under the same name that writes back into its source
  and returns nothing: `csnnormalize(data)` normalizes in place, while
  `Norm:CsnArr = csnnormalize(data)` leaves the source alone.
- **Choosing the rate.** Named opcodes are chosen by their trigger, which must
  be written to get the k-rate form: without it the call is the init-time form,
  whatever the rate of its operands. The operators take no trigger and follow
  the rate of their operands, which `csnk` and `csni` set; see
  [Choosing the rate](model.md#choosing-the-rate-named-opcodes-take-a-trigger-operators-a-cast).
  The i-rate and k-rate forms of a named opcode share its name; Csound picks the
  overload from the arguments you pass.
- **Trigger.** Most k-rate forms take a trigger. When an axis may be omitted,
  the no-axis overload ends with the trigger and the explicit-axis overload is
  written `..., trigger, axis`; this keeps omission distinct from `axis = -1`.
  A zero trigger skips the pass entirely and keeps the previous result. Where
  the trigger is the only k-rate argument, as in `csnprint`, it is required so
  Csound can distinguish the performance overload from the init-time one.
  `csnprint`, `csnsave` and `csnload` have no previous computed result to
  keep, so a zero trigger simply performs no side effect.
- **Real-time paths.** An array on a live signal chain can be marked so that
  nothing reallocates it, or any buffer serving it, during performance. The
  audio sources mark what they publish by default (`irt = 1`); `csnrtlock` marks
  one array, `csnrtlockstart` / `csnrtlockend` everything a note creates
  between the two, and `csnrtlockall` everything for the whole performance.
  [Real-time paths](real-time.md#real-time-paths) explains how the mark works and why it
  matters.

---
