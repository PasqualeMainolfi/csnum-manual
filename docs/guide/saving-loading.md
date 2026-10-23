# Saving and loading

`csnsave` and `csnload` select the file format from the path extension. Use
`.csn` for csnum's own format or `.npy` to exchange arrays with NumPy. Other
extensions are rejected before a file is opened; the same i-rate and k-rate
opcode forms work with both formats.

The `.csn` format has a fixed 64-byte `CSDN` header followed by the raw array
payload. It records the version, element type, dimension count, shape, element
count and byte count. The loader checks these fields and restores the original
shape and real/complex type.

For `.npy`, `csnsave` writes a NumPy 3.0 file containing C-order `float64` or
`complex128` values. NumPy's `np.load` can read it. `csnload` accepts `.npy`
versions 1.0, 2.0 and 3.0 with numeric `bool`, signed/unsigned integers of
1/2/4/8 bytes, `float16`/`float32`/`float64`, or `complex64`/`complex128`.
It handles little, big and native byte order and converts Fortran-order payloads
to csnum's C-order layout. Real values become `double`; complex values become
pairs of `double`. Integer values beyond the exact range of `double` can lose
precision. Structured/object dtypes, scalar arrays with `shape=()`, and headers
over 10,000 bytes are not supported; csnum arrays have at most eight dimensions.
As with `.csn`, the element count must match the shape; an empty array with a
nonzero reserved shape cannot be saved as `.npy`.

Malformed headers, unsupported dtypes and incomplete payloads are rejected.
The [csnsave](../reference/csnsave.md) and [csnload](../reference/csnload.md) references give the
full argument and trigger behavior.

At k-rate the trigger is the whole contract: it fires, the file is read. There
is deliberately no caching between triggers, not even on an unchanged path.
`csnload` reads a file it does not own, so the path proves nothing about the
bytes behind it, and a stat-based stamp would only narrow the window — on HFS+,
SMB/NFS and FAT the mtime granularity is one to two seconds, wide enough for a
same-size rewrite to hide in. Re-reading a small file already in the page cache
is cheap; silently handing back stale data is not.

```csound
data:CsnArr = csnfromarray(array(1, 2, 3, 4, 5, 6))
csnsave(data, "analysis.csn")

back:CsnArr = csnload("analysis.csn")
values:i[]  = csntoarray(back) // 1 2 3 4 5 6

csnsave(data, "analysis.npy") // np.load("analysis.npy") can read this file
from_numpy:CsnArr = csnload("analysis.npy")
```

NumPy can also write the input file:

```python
import numpy as np
values = np.asfortranarray(np.array([[1, 2, 3], [4, 5, 6]], dtype=np.float32))
np.save("incoming.npy", values)
```

`csnload("incoming.npy")` returns the same 2×3 shape with C-order `double`
values.

At k-rate, reloading a file another process keeps rewriting. Until the first
trigger fires the output still holds the empty array the init pass published,
so a consumer that cannot read an empty extent belongs behind the trigger too:

```csound
instr 1
    trig:k       = metro(10)
    table:CsnArr = csnload("live.npy", trig)
    n:k          = csnsize(table)
endin
```

---
