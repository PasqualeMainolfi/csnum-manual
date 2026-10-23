---
hide:
  - navigation
  - toc
---

<div class="csn-hero" markdown>

# csnum

NumPy-style arrays for Csound 7: n-dimensional real and complex arrays, with
359 opcodes in 24 families and no dependencies beyond Csound.
{ .csn-tagline }

[Get started](guide/requirements.md){ .md-button .md-button--primary }
[Opcode reference](reference/index.md){ .md-button }
[Source on GitHub](https://github.com/PasqualeMainolfi/csound-numeric){ .md-button }

</div>

!!! note

    csound-numeric is currently in the testing phase. Bug reports, feedback, suggestions, and reports of unexpected behavior are very welcome and greatly appreciated, as they help improve the library and make it more stable and reliable.

## A first look

Build a matrix, transform it with ordinary operators, reduce it along an axis
and read one element back with `[]`:

```csound-document
<CsoundSynthesizer>
<CsOptions>
-n -d
</CsOptions>
<CsInstruments>

sr = 44100
ksmps = 32
0dbfs = 1

instr 1
    ; a 2x3 matrix from a flat list
    shape:i[]  = fillarray(2, 3)
    m:CsnArr   = csnreshape(csnfromarray(fillarray(3, 1, 2, 9, 7, 8)), shape)

    ; arithmetic with operators, reductions along an axis
    scaled:CsnArr = m * 2 + 1
    cols:CsnArr   = csnsum(scaled, 0)
    peak:i        = csnmax(scaled)

    csnprint(scaled)
    csnprint(cols)
    prints("peak = %g\n", peak)

    ; element read with []
    prints("m[1][2] = %g\n", m[1][2])
    turnoff
endin

</CsInstruments>
<CsScore>
i 1 0 0.1
</CsScore>
</CsoundSynthesizer>
```

```text
CsnArr(shape=(2, 3), dtype=float64)
[[7 3 5]
 [19 15 17]]
CsnArr(shape=(3,), dtype=float64)
[26 18 22]
peak = 19
m[1][2] = 8
```

Run it with the plugin in place, or install the plugin first
([Building](guide/building.md)):

```sh
csound --opcode-dir=path/to/csound-numeric/build first.csd
```

## What it is

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


## Understand the model

<div class="grid cards" markdown>

-   :material-cube-outline: **[The CsnArr model](guide/model.md)**

    ---

    Arrays as values, not Csound arrays: operators, `[]` indexing, empty,
    set and string arrays.

-   :material-timer-outline: **[k-rate performance](guide/k-rate.md)**

    ---

    Triggers, array versioning and what the init pass computes.

-   :material-lightning-bolt-outline: **[Real-time paths](guide/real-time.md)**

    ---

    Chains that never reallocate during performance, and how to build them.

-   :material-waveform: **[Audio](guide/audio.md)**

    ---

    Moving blocks of samples between audio signals and arrays.

-   :material-content-save-outline: **[Saving and loading](guide/saving-loading.md)**

    ---

    Arrays to disk and back.

-   :material-language-python: **[NumPy correspondence](guide/numpy.md)**

    ---

    Every opcode next to the NumPy call it stands for.

</div>

## Opcode families

<div class="grid cards" markdown>

-   **[Creation](reference/index.md#creation)** · 13

    ---

    [csnempty](reference/csnempty.md), [csnzeros](reference/csnzeros.md), [csnones](reference/csnones.md), [csnfull](reference/csnfull.md), [csnlike](reference/csnlike.md) and 8 more

-   **[Conversion, lifetime and queries](reference/index.md#conversion-lifetime-and-queries)** · 13

    ---

    [csnfromarray](reference/csnfromarray.md), [csntoarray](reference/csntoarray.md), [csnfromftable](reference/csnfromftable.md), [csntoftable](reference/csntoftable.md), [csncopy](reference/csncopy.md) and 8 more

-   **[Persistence](reference/index.md#persistence)** · 4

    ---

    [csnsave](reference/csnsave.md), [csnload](reference/csnload.md), [csnsaveaudiofile](reference/csnsaveaudiofile.md), [csnloadaudiofile](reference/csnloadaudiofile.md)

-   **[Shape and layout](reference/index.md#shape-and-layout)** · 16

    ---

    [csnreshape](reference/csnreshape.md), [csnflatten](reference/csnflatten.md), [csntranspose](reference/csntranspose.md), [csnflip](reference/csnflip.md), [csnroll](reference/csnroll.md) and 11 more

-   **[Indexing and selection](reference/index.md#indexing-and-selection)** · 18

    ---

    [csnget](reference/csnget.md), [csngetrow](reference/csngetrow.md), [csngetcol](reference/csngetcol.md), [csnset](reference/csnset.md), [csngetslice](reference/csngetslice.md) and 13 more

-   **[Elementwise arithmetic](reference/index.md#elementwise-arithmetic)** · 68

    ---

    [csnadd](reference/csnadd.md), [csnsubtract](reference/csnsubtract.md), [csnmul](reference/csnmul.md), [csndiv](reference/csndiv.md), [csnpow](reference/csnpow.md) and 63 more

-   **[Transcendental functions](reference/index.md#transcendental-functions)** · 15

    ---

    [csnexp](reference/csnexp.md), [csnsqrt](reference/csnsqrt.md), [csncbrt](reference/csncbrt.md), [csnsin](reference/csnsin.md), [csncos](reference/csncos.md) and 10 more

-   **[Angles and phase](reference/index.md#angles-and-phase)** · 5

    ---

    [csndegtorad](reference/csndegtorad.md), [csnradtodeg](reference/csnradtodeg.md), [csnatan2](reference/csnatan2.md), [csnwrap](reference/csnwrap.md), [csnunwrap](reference/csnunwrap.md)

-   **[Comparison and logic](reference/index.md#comparison-and-logic)** · 17

    ---

    [csngt](reference/csngt.md), [csnlt](reference/csnlt.md), [csnge](reference/csnge.md), [csnle](reference/csnle.md), [csneq](reference/csneq.md) and 12 more

-   **[Reductions and statistics](reference/index.md#reductions-and-statistics)** · 26

    ---

    [csnsum](reference/csnsum.md), [csnprod](reference/csnprod.md), [csnsub](reference/csnsub.md), [csnmean](reference/csnmean.md), [csnmin](reference/csnmin.md) and 21 more

-   **[Sorting and sets](reference/index.md#sorting-and-sets)** · 18

    ---

    [csnshuffle](reference/csnshuffle.md), [csnsort](reference/csnsort.md), [csnargsort](reference/csnargsort.md), [csnunique](reference/csnunique.md), [csnargunique](reference/csnargunique.md) and 13 more

-   **[Linear algebra and geometry](reference/index.md#linear-algebra-and-geometry)** · 20

    ---

    [csndot](reference/csndot.md), [csninner](reference/csninner.md), [csnouter](reference/csnouter.md), [csnmatmul](reference/csnmatmul.md), [csntrace](reference/csntrace.md) and 15 more

-   **[Complex arrays](reference/index.md#complex-arrays)** · 6

    ---

    [csnreal](reference/csnreal.md), [csnimag](reference/csnimag.md), [csnangle](reference/csnangle.md), [csnconj](reference/csnconj.md), [csntocomplex](reference/csntocomplex.md) and 1 more

-   **[Fourier analysis](reference/index.md#fourier-analysis)** · 21

    ---

    [csnfft](reference/csnfft.md), [csnrfft](reference/csnrfft.md), [csnifft](reference/csnifft.md), [csnirfft](reference/csnirfft.md), [csnfft2](reference/csnfft2.md) and 16 more

-   **[Cepstral and mel analysis](reference/index.md#cepstral-and-mel-analysis)** · 3

    ---

    [csnmfcc](reference/csnmfcc.md), [csnmfbank](reference/csnmfbank.md), [csnmlogfbank](reference/csnmlogfbank.md)

-   **[Convolution and correlation](reference/index.md#convolution-and-correlation)** · 16

    ---

    [csnconvolve1d](reference/csnconvolve1d.md), [csncorrelate1d](reference/csncorrelate1d.md), [csnconvolve](reference/csnconvolve.md), [csncorrelate](reference/csncorrelate.md), [csnfftconvolve1d](reference/csnfftconvolve1d.md) and 11 more

-   **[Interpolation and resampling](reference/index.md#interpolation-and-resampling)** · 4

    ---

    [csninterp](reference/csninterp.md), [csnresample](reference/csnresample.md), [csnlagrange](reference/csnlagrange.md), [csnroots](reference/csnroots.md)

-   **[Filter design](reference/index.md#filter-design)** · 29

    ---

    [csnlptolpzpk](reference/csnlptolpzpk.md), [csnlptohpzpk](reference/csnlptohpzpk.md), [csnlptobpzpk](reference/csnlptobpzpk.md), [csnlptobszpk](reference/csnlptobszpk.md), [csnbilinearzpk](reference/csnbilinearzpk.md) and 24 more

-   **[Windows](reference/index.md#windows)** · 5

    ---

    [csnhanning](reference/csnhanning.md), [csnhamming](reference/csnhamming.md), [csnbartlett](reference/csnbartlett.md), [csnblackman](reference/csnblackman.md), [csnkaiser](reference/csnkaiser.md)

-   **[Coordinate systems](reference/index.md#coordinate-systems)** · 16

    ---

    [csnpoltocar](reference/csnpoltocar.md), [csncartopol](reference/csncartopol.md), [csncyltocar](reference/csncyltocar.md), [csncartocyl](reference/csncartocyl.md), [csnsphtocar](reference/csnsphtocar.md) and 11 more

-   **[Special functions](reference/index.md#special-functions)** · 3

    ---

    [csnlegendre](reference/csnlegendre.md), [csnsphharm](reference/csnsphharm.md), [csnsphharmacn](reference/csnsphharmacn.md)

-   **[Room acoustics](reference/index.md#room-acoustics)** · 7

    ---

    [csnt60sab](reference/csnt60sab.md), [csnt60eyr](reference/csnt60eyr.md), [csnrt60absp](reference/csnrt60absp.md), [csnfschrd](reference/csnfschrd.md), [csnfpqr](reference/csnfpqr.md) and 2 more

-   **[Levels and time conversion](reference/index.md#levels-and-time-conversion)** · 5

    ---

    [csndbsum](reference/csndbsum.md), [csnsamptomillis](reference/csnsamptomillis.md), [csnsamptosec](reference/csnsamptosec.md), [csnmillistosamp](reference/csnmillistosamp.md), [csnsectosamp](reference/csnsectosamp.md)

-   **[Audio bridge](reference/index.md#audio-bridge)** · 11

    ---

    [csnfromaudio](reference/csnfromaudio.md), [csntoaudio](reference/csntoaudio.md), [csnpack](reference/csnpack.md), [csnunpack](reference/csnunpack.md), [csnsnap](reference/csnsnap.md) and 6 more

</div>
