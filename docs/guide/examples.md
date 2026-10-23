# Examples

Sort and reduce, entirely at i-time:

```csound
data:CsnArr     = csnfromarray(array(4, 1, 3, 2))
sorted:CsnArr   = csnsort(data)
sorted_back:i[] = csntoarray(sorted) // 1 2 3 4
peak:i          = csnmax(data) // 4
```

Count integer bins, with an optional weight per input element:

```csound
bins:CsnArr     = csnfromarray(array(0, 1, 1, 3))
counts:CsnArr   = csnbincount(bins) // 1 2 0 1
weights:CsnArr  = csnfromarray(array(0.5, 1, 2, 4))
weighted:CsnArr = csnbincount(bins, weights) // 0.5 3 0 4
```

Find where values can be inserted without disturbing ascending order:

```csound
sorted:CsnArr = csnfromarray(array(1, 3, 3, 5))
wanted:CsnArr = csnfromarray(array(0, 3, 4, 6))
left:CsnArr   = csnsearchsorted(sorted, wanted)    // 0 1 3 4
right:CsnArr  = csnsearchsorted(sorted, wanted, 1) // 0 3 3 4
```

Reshape to 2×3 and reduce along an axis:

```csound
shape:i[]   = fillarray(2, 3)
mat:CsnArr  = csnreshape(csnfromarray(array(1, 2, 3, 4, 5, 6)), shape)
cols:CsnArr = csnsum(mat, 0) // 5 7 9 (one value per column)
```

Complex arrays use the same opcodes, and a single element reads back as a
`:Complex;`:

```csound
z:CsnArr    = csntocomplex(data)
conj:CsnArr = csnconj(z)
cell:i[]    = fillarray(0)
w:Complex   = csnget(conj, cell)
```

Interpolate one value on a breakpoint table, then resample a curve:

```csound
X:CsnArr  = csnfromarray(array(0, 1, 2, 3))
Y:CsnArr  = csnfromarray(array(0, 10, 20, 30))
at:i      = csninterp(1.5, X, Y, 0, 1) // 15 (linear, clamped at the ends)
up:CsnArr = csnresample(Y, 7, 0, 1) // 0 5 10 15 20 25 30
```

At k-rate, with a trigger: the work runs on the triggered passes, and the
opcodes keep their previous result on all the others.

```csound
instr 1
    trig:k        = metro(200)
    scaled:CsnArr = csnmul(buffer, 0.5, trig)
    peak:k        = csnmax(scaled, trig)
    printf("peak=%.1f\n", trig, peak)
endin
```

In place, when a new array would be waste:

```csound
csnnormalize(data) // rewrites data; downstream consumers see a new generation
```
