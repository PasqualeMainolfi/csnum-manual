# Audio

Six opcodes connect the array vocabulary to Csound's audio signals. They run at
performance time, but an a-rate opcode's perf function is called once per control
period, not once per sample, so they cost what a k-rate opcode costs.

`csnfromaudio` captures one control period into an array of `ksmps` elements and
`csntoaudio` sends one back out. In between, the whole suite applies:

```csound
instr 1
    gain:k       = 0.5
    sig:a        = oscili(0.5, 440)
    block:CsnArr = csnfromaudio(sig)
    out:a        = csntoaudio(csnmul(block, gain))
endin
```

`csntoaudio` checks the element count, not the shape, so an array reshaped to a
matrix comes back out without an intervening flatten. For multichannel material
`csnpack` folds a whole `a[]` into one `channels x ksmps` array and `csnunpack`
takes it apart again — an `a[]` stores each channel as a whole `ksmps`-long
block, so the pair is a transpose of layout, not a copy of samples.

## Frames independent of ksmps

`csnsnap` slices the stream into frames of a size you choose and publishes one
every `ihop` samples, raising a ready flag on the control period where that
happens. `csnstream` overlap-adds them back:

```csound
instr 1
    sig:a               = oscili(0.5, 440)
    frame:CsnArr, new:k = csnsnap(sig, 1024, 256)
    spectrum:CsnArr     = csnrfft(frame, 1024, -1, new)
    magnitude:CsnArr    = csnabs(spectrum, new)
    out:a, ready:k      = csnstream(frame, 256)
endin
```

Here `nfft` is the 1024-sample frame size, independent of `ksmps`. `csnsnap`
marks the frame as a real-time path by default, and the FFT outputs inherit the
mark; an extra `csnrtlock` call is not required.

The hop must be at least `ksmps`: one `CsnArr` variable holds one frame, so at most one
frame can be published per control period, and a smaller hop would overwrite a
frame before any consumer could read it. It is refused at init rather than
silently dropping frames. The default hop is the frame size, which gives
contiguous frames with no overlap.

`csnstream` folds in one frame per hop of output, counted on a phase accumulator
of its own, so any number of k-rate opcodes may sit between the two ends without
changing the result. With a rectangular window and `ihop` equal to the frame
length the reconstruction is exact; at 50% overlap every sample is covered twice,
so a real chain applies a window whose overlapped copies sum to one.

## Audio arrays are real-time paths

An array published by `csnfromaudio`, `csnpack` or `csnsnap` is marked as a
real-time path, and every array derived from it inherits the mark when it is
created. A chain whose shapes are settled at init, which is the ordinary case since
`csnfromaudio` fixes its shape at `ksmps`, allocates once per note and never
again. Where the frames are harvested for analysis rather than sent back out,
`irt = 0` at the source lifts the restriction for everything derived from it.
[Real-time paths](real-time.md#real-time-paths) covers the mark in full.

---
