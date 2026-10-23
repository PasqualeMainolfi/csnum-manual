---
hide:
  - navigation
  - toc
---

<div class="csn-hero" markdown>

# csnum

NumPy-style arrays for Csound 7: n-dimensional real and complex arrays, with
{{opcodes}} opcodes in {{families}} families and no dependencies beyond Csound.
{ .csn-tagline }

[Get started](guide/requirements.md){ .md-button .md-button--primary }
[Opcode reference](reference/index.md){ .md-button }
[Source on GitHub](https://github.com/PasqualeMainolfi/csound-numeric){ .md-button }

</div>

<!-- csnum:note -->

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

<!-- csnum:intro -->

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

<!-- csnum:families -->
