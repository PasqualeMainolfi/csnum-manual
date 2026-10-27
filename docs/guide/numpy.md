# NumPy correspondence

The names follow NumPy wherever the operation is the same one. The table below
maps every opcode to the NumPy call it stands for, family by family, so a
function you already know can be found under its Csound name. The mapping is by
*intent*, not by signature: csnum opcodes exchange `CsnArr` values, take their shape
arguments as Csound i-arrays, and have no keyword arguments, so the NumPy column
is what the opcode computes, not a transliteration of its call.

Four differences apply throughout and are not repeated in every row:

- **Axis.** As in NumPy, a supplied negative axis counts from the end, so `-1`
  always means the last axis. Axis omission is represented by a separate
  overload and may mean flat, all axes, or last axis according to the operation.
- **Booleans.** csnum has no boolean element type. The comparisons, the `is*`
  predicates and the logical operations return a real array of `0` and `1` where
  NumPy returns `bool_`, and any of them is accepted as a mask.
- **Index results.** `csnindexof`, `csnargmin`, `csnargmax`, `csnargsort`,
  `csnargwhere` and friends return **coordinates**, one per source dimension,
  where NumPy often returns flat indices unless you call `np.unravel_index`.
- **Broadcasting.** Elementwise binary arithmetic, comparisons and logical
  operations broadcast array shapes from the right, as in NumPy; an extent of
  `1` can expand to its partner's extent. `csnmatmul` broadcasts batch axes.
  Operations with different semantics, such as `csnstack`, `csnpairdist` and
  `csnwhere`, still have their own exact-shape requirements.

An em dash in the NumPy column means there is no NumPy counterpart; a `scipy.`
entry means the operation lives outside NumPy proper.

## Creation

| csnum | NumPy | Notes |
| --- | --- | --- |
| `csnempty` | `np.empty` | Reserves capacity: size is 0, not the reserved extent. `csnpush` fills it. |
| `csnzeros` | `np.zeros` | |
| `csnones` | `np.ones` | |
| `csnfull` | `np.full` | |
| `csnlike` | `np.full_like` | Also covers `zeros_like` / `ones_like` via the fill value. |
| `csnidentity` | `np.identity` | |
| `csnarange` | `np.arange` | |
| `csnlinspace` | `np.linspace` | |
| `csnlogspace` | `np.logspace` | |
| `csngeomspace` | `np.geomspace` | |
| `csnrand` | `np.random.uniform` | |
| `csnrandint` | `np.random.randint` | |
| `csnseed` | `np.random.seed` | |

## Conversion, lifetime and queries

| csnum | NumPy | Notes |
| --- | --- | --- |
| `csnfromarray` | `np.array` | From a Csound `i[]` / `k[]`. |
| `csntoarray` | `ndarray.tolist` | The only way back out to a Csound array. |
| `csnfromftable` | — | Csound function table in. |
| `csntoftable` | — | Csound function table out. |
| `csncopy` | `np.copy` | |
| `csntype` | `ndarray.dtype` | `0` real, `1` complex, `2` string. |
| `csndims` | `ndarray.ndim` | |
| `csnsize` | `ndarray.size` | |
| `csnshape` | `ndarray.shape` | |
| `csnisempty` | `a.size == 0` | |
| `csnprint` | `print(a)` | Same bracket and indentation layout, same 1000-element summarization. |

## Persistence

| csnum | NumPy | Notes |
| --- | --- | --- |
| `csnsave` | `np.save` | A `.npy` path writes a NumPy file (`float64`, `complex128`, or `<U` for a `CsnStr`); `.csn` writes csnum's own format. |
| `csnload` | `np.load` | A `.npy` path reads supported numeric dtypes, or `<U` / `\|S` into a `CsnStr`, in C or Fortran order; `.csn` reads csnum's own format. |
| `csnloadaudiofile` | `librosa.load(path, sr=None, mono=False)` | Reads `.wav`, `.mp3` or `.flac`, one row per channel, and returns the file's sample rate; never resamples. |
| `csnsaveaudiofile` | `soundfile.write` | Writes `.wav` as 32-bit float, one channel per row. |

## Shape and layout

| csnum | NumPy | Notes |
| --- | --- | --- |
| `csnreshape` | `np.reshape` | |
| `csnflatten` | `np.ravel` | |
| `csntranspose` | `np.transpose` | Layout change, no copy. |
| `csnflip` | `np.flip` | |
| `csnroll` | `np.roll` | |
| `csnreverse` | `a[::-1]` | Flat element order. |
| `csnpad` | `np.pad` | Constant fill only. |
| `csntruncate` | `a[:n]` | One axis or every axis. |
| `csnhead` | `a[:n]` | 1-D only. |
| `csnresize` | `ndarray.resize` | Zero-fills what it grows, like the method. `np.resize` repeats instead. |
| `csnconcat` | `np.concatenate` | |
| `csnstack` | `np.stack` | |
| `csnframe` | `np.moveaxis(sliding_window_view(x, frame, axis)[..., ::hop, ...], -1, axis + 1)` | Frames and their positions take the framed axis's place; on the last axis, `sliding_window_view(x, frame)[..., ::hop, :]`. A copy; the tail that does not fill a frame is dropped. |
| `csninsert` | `np.insert` | |
| `csnremove` | `np.delete` | |
| `csnpush` | `np.append` | In place, into reserved capacity. |
| `csnpop` | `a[-1]` + `np.delete` | Returns the element and shortens the array. |

## Indexing and selection

| csnum | NumPy | Notes |
| --- | --- | --- |
| `a[i][j]` | `a[i, j]` | One index per dimension; also `a[i][j] = v`. |
| `a[start:end, step, axis]` | `np.take(a, range(start, end + 1, step), axis)` | End included, as Csound's `slicearray`; axis 0 by default. |
| `csnget` | `a[i, j]` | Coordinates come in as an i-array. |
| `csnset` | `a[i, j] = v` | |
| `csngetrow` | `a[i, :]` | |
| `csngetcol` | `a[:, j]` | |
| `csngetslice` | `a[start:stop:step]` | Along one axis. |
| `csnsetslice` | `a[start:stop:step] = v` | |
| `csntake` | `np.take` | Drops the indexed axis. |
| `csnwhere` | `np.where` | |
| `csnputmask` | `np.putmask` | |
| `csncompress` | `np.compress` | |
| `csnselect` | `np.extract` | `a[mask]`, flattened. |
| `csnindexof` | `np.argwhere(a == value)[0]` | First matching coordinate; an empty array when no element matches. |
| `csnbincount` | `np.bincount` | 1-D non-negative integer source; optional weights, but no `minlength`. |
| `csnsearchsorted` | `np.searchsorted` | Ascending 1-D real source; `side` is `0` for left and `1` for right; no `sorter`. |
| `csnargwhere` | `np.argwhere(np.isin(a, v))` | Coordinates of the elements matching a value array. |
| `csnargnonzero` | `np.argwhere(a)` | |
| `csnargisnan` | `np.argwhere(np.isnan(a))` | |

## Elementwise arithmetic

| csnum | NumPy | Notes |
| --- | --- | --- |
| `csnadd` | `np.add` | |
| `csnsubtract` | `np.subtract` | |
| `csnmul` | `np.multiply` | |
| `csndiv` | `np.divide` | |
| `csnpow` | `np.power` | |
| `csnlog` | `np.log(a) / np.log(base)` | Arbitrary base in one call. |
| `csndivmod` | `np.divmod` | Two arrays out. |
| `csnhypot` | `np.hypot` | |
| `csnminimum` | `np.minimum` | |
| `csnmaximum` | `np.maximum` | |
| `csnclip` | `np.clip` | |
| `csnabs` | `np.abs` | Magnitude for complex. |
| `csnsign` | `np.sign` | |
| `csnfloor` | `np.floor` | |
| `csnceil` | `np.ceil` | |
| `csnround` | `np.round` | Halves go to the even neighbour, as in NumPy and Csound's scalar `round`; Csound's `round` over an array sends them away from zero. |

## Transcendental functions

| csnum | NumPy | Notes |
| --- | --- | --- |
| `csnexp` | `np.exp` | |
| `csnsqrt` | `np.sqrt` | |
| `csncbrt` | `np.cbrt` | |
| `csnsin` `csncos` `csntan` | `np.sin` `np.cos` `np.tan` | |
| `csnasin` `csnacos` `csnatan` | `np.arcsin` `np.arccos` `np.arctan` | |
| `csnsinh` `csncosh` `csntanh` | `np.sinh` `np.cosh` `np.tanh` | |
| `csnasinh` `csnacosh` `csnatanh` | `np.arcsinh` `np.arccosh` `np.arctanh` | |

## Angles and phase

| csnum | NumPy | Notes |
| --- | --- | --- |
| `csndegtorad` | `np.deg2rad` | |
| `csnradtodeg` | `np.rad2deg` | |
| `csnatan2` | `np.arctan2` | |
| `csnwrap` | `np.mod` | Folds into one period centred on zero, `[-period/2, period/2)`. |
| `csnunwrap` | `np.unwrap` | |

## Comparison and logic

| csnum | NumPy | Notes |
| --- | --- | --- |
| `csngt` | `np.greater` | 0/1 real array out. |
| `csnlt` | `np.less` | |
| `csnge` | `np.greater_equal` | |
| `csnle` | `np.less_equal` | |
| `csneq` | `np.equal` | |
| `csnne` | `np.not_equal` | |
| `csnisnan` | `np.isnan` | |
| `csnisinf` | `np.isinf` | |
| `csnisfin` | `np.isfinite` | |
| `csnlogicand` | `np.logical_and` | |
| `csnlogicor` | `np.logical_or` | |
| `csnlogicnot` | `np.logical_not` | |
| `csnall` | `np.all` | |
| `csnany` | `np.any` | |
| `csncnteq` | `np.count_nonzero(a == v)` | |
| `csncntnz` | `np.count_nonzero` | |
| `csncntnan` | `np.count_nonzero(np.isnan(a))` | |

## Reductions and statistics

| csnum | NumPy | Notes |
| --- | --- | --- |
| `csnsum` | `np.sum` | |
| `csnprod` | `np.prod` | |
| `csnsub` | `np.subtract.reduce` | Every element subtracted from the first. |
| `csnmean` | `np.mean` | |
| `csnmin` | `np.min` | |
| `csnmax` | `np.max` | |
| `csnmedian` | `np.median` | |
| `csnrms` | `np.sqrt(np.mean(a ** 2))` | |
| `csnstd` | `np.std` | |
| `csnvar` | `np.var` | |
| `csnpercentile` | `np.percentile` | |
| `csnquantile` | `np.quantile` | |
| `csnargmin` | `np.argmin` | Coordinates, not a flat index. |
| `csnargmax` | `np.argmax` | Coordinates, not a flat index. |
| `csncumsum` | `np.cumsum` | |
| `csncumprod` | `np.cumprod` | |
| `csndiff` | `np.diff` | |
| `csngrad` | `np.gradient` | |
| `csnmovmean` | — | `pandas.Series.rolling(w, center=True, min_periods=1).mean()`: the window is centred and shorter near the ends, and every moving statistic below uses it. `np.convolve` with a box agrees away from the edges. |
| `csnmovmedian` | — | `rolling(...).median()`; a NaN in the window gives NaN, as `np.median` does. |
| `csnmedfilt1d` | — | `scipy.signal.medfilt` along one axis: the same centred window, padded with zeros instead of shortened at the ends. |
| `csnmedfilt` | — | `scipy.signal.medfilt` over a box of one size per axis, `scipy.signal.medfilt2d` for a 2-D pair. |
| `csnmovmin` | — | `rolling(...).min()`. |
| `csnmovmax` | — | `rolling(...).max()`. |
| `csnmovstd` | — | `rolling(...).std(ddof=0)`, the population deviation; pandas defaults to `ddof=1`. |
| `csnmovvar` | — | `rolling(...).var(ddof=0)`. |

## Sorting and sets

NumPy's set functions take any array and sort it on the way through. csnum
splits that in two: `csnlikeset` normalizes once and marks the array, and the
set operations then require the mark, so they can rely on binary search instead
of re-sorting on every k-rate pass.

| csnum | NumPy | Notes |
| --- | --- | --- |
| `csnshuffle` | `np.random.shuffle` | In place. |
| `csnperm` | `np.array(list(itertools.permutations(a)))` | 1-D; the same rows in Heap's order; an optional count takes the first ones. |
| `csnsort` | `np.sort` | |
| `csnargsort` | `np.argsort` | Coordinates. |
| `csnunique` | `np.unique` | |
| `csnargunique` | `np.unique(a, return_index=True)` | |
| `csnlikeset` | `np.unique` | Plus the set mark the operations below require. |
| `csnunlikeset` | — | Drops the mark, keeps the values. |
| `csnsetinsert` | — | In place, invariant preserving. |
| `csnsetremove` | — | In place, invariant preserving. |
| `csnsetcontains` | `np.isin` | Single value. |
| `csnsetunion` | `np.union1d` | |
| `csnsetintersect` | `np.intersect1d` | |
| `csnsetdiff` | `np.setdiff1d` | |
| `csnsetsymdiff` | `np.setxor1d` | |
| `csnsetissubset` | `np.isin(a, b).all()` | |
| `csnsetissuperset` | `np.isin(b, a).all()` | |
| `csnsetisdisjoint` | `np.intersect1d(a, b).size == 0` | |
| `csnsetisequal` | `np.array_equal(a, b)` | On normalized sets. |

## Linear algebra and geometry

| csnum | NumPy | Notes |
| --- | --- | --- |
| `csndot` | `np.dot` | |
| `csninner` | `np.inner` | |
| `csnouter` | `np.outer` | |
| `csnmatmul` | `np.matmul` | |
| `csntrace` | `np.trace` | |
| `csndiag` | `np.diag` | Both directions, as in NumPy. |
| `csnnorm` | `np.linalg.norm` | |
| `csnnormalize` | `a / np.linalg.norm(a, ord)` | Default order is the sum of magnitudes. |
| `csncross` | `np.cross` | 3-element vectors. |
| `csndist` | `np.linalg.norm(a - b, ord)` | Minkowski distance. |
| `csnpairdist` | `np.abs(a - b)` | Elementwise, same shape. |
| `csnangledist` | — | `arccos(dot(a, b) / (norm(a) * norm(b)))`. |
| `csnproject` | — | `dot(a, b) / dot(b, b) * b`. |
| `csnreject` | — | `a - project(a, b)`. |
| `csnreflect` | — | `a - 2 * project(a, b)`. |
| `csnsolve` | `np.linalg.solve` | One factorization, any number of right-hand sides. |
| `csninv` | `np.linalg.inv` | |
| `csndet` | `np.linalg.det` | Zero for a singular matrix, as NumPy's does; `csninv` and `csnsolve` refuse one. |
| `csnhilbertmat` | `scipy.linalg.hilbert` | The matrix, not a transform. |
| `csnsavgol` | `scipy.signal.savgol_coeffs` | Every derivative order at once, one per row; apply it with `csncorrelate1d`. |

## Complex arrays

| csnum | NumPy | Notes |
| --- | --- | --- |
| `csnreal` | `np.real` | |
| `csnimag` | `np.imag` | |
| `csnangle` | `np.angle` | |
| `csnconj` | `np.conj` | |
| `csntocomplex` | `a.astype(complex)` | |
| `csntoreal` | `a.real` | Keeps the real parts. |

## String arrays

A `CsnStr` stands for a NumPy array of dtype `str` (`<U`). These are the
overloads that take one; the numeric opcodes refuse it at compile time.

| csnum | NumPy | Notes |
| --- | --- | --- |
| `csnempty` | `np.empty(shape, dtype=str)` | Reserved and empty, as for numbers. |
| `csnfull` | `np.full(shape, "s")` | |
| `csnlike` | `np.full_like(a, "s")` | The k form takes a trigger. |
| `csnfromarray` | `np.array(list_of_str)` | From an `S[]`; the k form takes a trigger. |
| `csntoarray` | `ndarray.tolist` | To an `S[]`; the k form takes a trigger. |
| `csnget` / `csnset` | `a[i, j]` / `a[i, j] = "s"` | Also `v[i][j]`. |
| `csngetslice` | `a[start:stop:step]` along an axis | Also `v[start:end]`; the slice owns its strings. |
| `csnsetslice` | `a[start:stop:step] = b` along an axis | Each slot takes a copy; an unchanged slot allocates nothing. |
| `csntake` | `np.take(a, i, axis)` / `a.flat[i]` | Along an axis to a `CsnStr`, flat to an `S`. |
| `csnsize`, `csndims`, `csnshape`, `csnisempty`, `csntype` | `a.size`, `a.ndim`, `a.shape`, `a.size == 0`, `a.dtype` | `csntype` is `2`. |
| `csnreshape`, `csnflatten` | `np.reshape`, `np.ravel` | In place: `a.shape = ...`, `a.shape = (a.size,)`. |
| `csntranspose`, `csnflip`, `csnroll`, `csnreverse` | `np.transpose`, `np.flip`, `np.roll`, `a[::-1]` | A copy owns its strings; in place nothing is allocated. |
| `csnconcat` | `np.concatenate` | Two `CsnStr`; flat without an axis. |
| `csnstack` | `np.stack` | Two or more `CsnStr`, all of the same shape. |
| `csnframe` | `sliding_window_view(a, frame)[..., ::hop, :]` | Each string copied into every frame that holds it. |
| `csnpad` | `np.pad(a, w, constant_values="s")` | The fill string is required; the k form in place is refused on a real-time path. |
| `csnpush`, `csninsert` | `np.append`, `np.insert` | In place, one `S` or a `CsnStr` block; the block k form is refused on a real-time path. |
| `csnpop`, `csnremove` | `a[-1]` + `np.delete`, `np.delete` | One element comes back as an `S`, allowed on a real-time path; a removed block is a new `CsnStr`. |
| `csntruncate`, `csnhead` | `a[:n]` | In place the strings are only moved, so the k form is allowed on a real-time path. |
| `csnresize` | `ndarray.resize` | What it adds is `""`. |
| `csncopy`, `csni`, `csnk` | `np.copy` | Each copy owns its strings. |
| `csnshuffle` | `np.random.shuffle` | The same permutation as a numeric array after the same `csnseed`; allowed on a real-time path. |
| `csnwhere` | `np.where(mask, a, b)` | Real mask; `b` a `CsnStr` or one `S`. |
| `csnputmask` | `np.putmask(dest, mask, values)` | Destination first, unlike the numeric form; unchanged elements are not rewritten. |
| `csncompress`, `csnselect` | `np.compress`, `a[mask]` | Real mask; the kept strings are copies. |
| `csnstradd` | `np.strings.add` | Two `CsnStr` with broadcasting, or one `S` before or after every element. |
| `csnstrmul` | `np.strings.multiply` | One count or a real `CsnArr` of counts; whole numbers, below 0 gives `""`. |
| `csnstrupper`, `csnstrlower` | `np.strings.upper`, `np.strings.lower` | ASCII letters only, as on a bytes (`S`) array: bytes from 0x80 up stay, so UTF-8 survives. Also in place. |
| `csnstrcapitalize` | `np.strings.capitalize` | First character up, the rest down; ASCII only, as on a bytes (`S`) array. Also in place. |
| `csnstrtitle` | `np.strings.title` | As on a bytes (`S`) array: ASCII letters only, and digits and UTF-8 bytes are not letters (`"1st"` gives `"1St"`, `"Cafés"` gives `"CaféS"`). Also in place. |
| `csnstrstrip`, `csnstrlstrip`, `csnstrrstrip` | `np.strings.strip`, `lstrip`, `rstrip` | ASCII whitespace only, as on a bytes (`S`) array, so UTF-8 survives. `chars` is a set of bytes, as on a bytes array: a multibyte character stands for each of its bytes. Also in place. Also on one `S` (Python's `str.strip`, `lstrip`, `rstrip`, no in-place form). |
| `csnstrcenter`, `csnstrljust`, `csnstrrjust` | `np.strings.center`, `ljust`, `rjust` | Width in bytes, as on a bytes (`S`) array; center splits an odd margin as CPython does. A negative width is refused rather than ignored; `fillchar` (here `fill`) must be one byte. Also in place. |
| `csnstrreplace` | `np.strings.replace` | Bytes, as on a bytes (`S`) array; an empty `old` matches between bytes. `count` optional, any negative for all. Also in place, and on one `S` (Python's `str.replace`, no in-place form). |
| `csnstrsubstr` | `np.strings.slice` | Bytes, stop excluded, clamped to each string. Indices as `csngetslice`: whole, from 0, start no greater than stop, step at least 1; no negative indices or steps. Also in place. |
| `csnstrlen` | `np.strings.str_len` | Bytes, as on a bytes (`S`) array: a UTF-8 character counts each of its bytes. |
| `csnstrfind`, `csnstrrfind` | `np.strings.find`, `rfind` | Bytes; `-1` where missing; rfind counts overlapping matches, an empty `sub` is found at the start of the range by find and at its end by rfind. `start`, `end` as `s[start:end]`, `end` `-1` (default) for the end of the string; whole, from 0, start no greater than end, no negative indices. |
| `csnstrstartswith`, `csnstrendswith` | `np.strings.startswith`, `endswith` | Bytes; 0/1 mask; the empty prefix or suffix matches any range that starts inside the string. `start`, `end` as for `csnstrfind`. |
| `csnstrisalpha`, `csnstrisdigit`, `csnstrisalnum`, `csnstrisspace` | `np.strings.isalpha`, `isdigit`, `isalnum`, `isspace` | ASCII only, as on a bytes (`S`) array, whatever the locale; 0/1 mask; an empty string gives 0. |
| `csnstrtonum` | `a.astype(float)` | As Python's `float()`, the point `.` whatever the locale; a string that is not a number gives `NaN` where NumPy raises, and digit underscores (`"1_000"`) are not a number. |
| `csnstrjoin` | `sep.join(a.flat)` | No NumPy join over an array: Python's `str.join` on the elements in row-major order; one `S` out. |
| `csnstrsplit`, `csnstrrsplit` | `s.split(sep, maxsplit)`, `s.rsplit(sep, maxsplit)` | Python's `str` methods on one `S`, to a 1-D `CsnStr` (NumPy's `np.strings.split` gives lists in an object array). `sep` required and not empty; no split on runs of whitespace. |
| `csnstrpartition`, `csnstrrpartition` | `s.partition(sep)`, `s.rpartition(sep)` | On one `S`, to a `CsnStr` of 3 where NumPy gives three arrays. `sep` not empty. |
| `csnstrchr`, `csnstrord` | `chr(n)`, `ord(c)` | On one `S`: chr takes ASCII codes 1 to 127 only, ord a one-byte string, 0 to 255. |
| `csnstrtoascii`, `csnstrfromascii` | `list(s.encode())`, `bytes(codes).decode()` | One `S` to its bytes as a real array (0 to 255) and back from ASCII codes (1 to 127). |
| `csnstrencode`, `csnstrdecode` | `s.encode()`, `bytes(b).decode()` | UTF-8 only, Python's strict rules (no overlong forms, no surrogates, U+10FFFF at most); the first bad byte is named. No NUL. |
| `csnstrtocodepoints`, `csnstrfromcodepoints` | `[ord(c) for c in s]`, `''.join(map(chr, p))` | Code points of a UTF-8 `S`, 1 to U+10FFFF, no surrogates. |
| `csnstraslist`, `csnlistasstr` | `np.array(list(s))`, `sep.join(map(str, a.tolist()))` | One UTF-8 `S` split by code point, text that is not UTF-8 refused; a real 1-D array written as `csnnumtostr` writes each number (`"1.0"`, `"0.1"`) and joined by `sep`. `""` and an empty array give an empty result. |
| `csntobinary`, `csntohex` | `np.binary_repr(n, width)`, `np.base_repr(n, 16).zfill(width)` | `width` optional. Whole numbers from 0 to 2^64 excluded: a negative one is refused, where `binary_repr` writes `-101`, or two's complement with a width. Hex upper case, no prefix; a width shorter than the digits keeps them all, where `binary_repr` raises. A `CsnArr` goes elementwise to a `CsnStr`. |
| `csnfrombinary`, `csnfromhex` | `int(s, 2)`, `int(s, 16)` | An optional `0b` / `0x` prefix, then digits only: no sign, blank or `_`. Below 2^64, above 2^53 to the nearest double. A `CsnStr` goes elementwise to a real `CsnArr`. |
| `csnbinstrtoarr`, `csnhexstrtoarr` | `np.array(list(s.removeprefix('0b')), float)`, `np.array(list(s.removeprefix('0x')))` | One `S` split into its digits, an optional `0b` / `0x` prefix skipped (`0B` / `0X` too); binary to a real array of 0 and 1, hex to a `CsnStr` keeping each digit's case. `""` gives an empty array; a non-digit is refused. |
| `csntobase64`, `csnfrombase64` | `base64.b64encode(a.astype(np.uint8).tobytes())`, `np.frombuffer(base64.b64decode(s), np.uint8)` | One `S` or a real 1-D array of bytes (0 to 255) to padded RFC 4648 text, and back to an `S` (no zero byte) or an array. Decoding is strict: no blank, `=` only at the end, the unused bits zero (`b64decode` takes `"TWF="`); no URL-safe alphabet. |
| `csntobuffer`, `csnfrombuffer` | `a.astype(dtype).tobytes()`, `np.frombuffer(b, dtype)` | The bytes as a real 1-D array of 0 to 255, a source of any shape flattened in row-major order. `dtype` one of `\|u1`, `\|i1`, then `<` or `>` before `u2`, `i2`, `u4`, `i4`, `f4`, `f8`: no native `=`, no shorthand without byte order, no `i8` or complex. A value the dtype cannot hold is refused where `astype` wraps or truncates (`300` to `\|u1`, `3.5` to `<i2`), NaN and infinities too; `f4` rounds to the nearest float. frombuffer takes a 1-D array, its length a multiple of the dtype's width; floats come back with NaN and infinities as they are. |
| `csnnumtostr` | `a.astype(str)` | Python's `repr`: the shortest digits that read back, `"1.0"`, `"1e-05"`, `"1e+16"`; the point `.` whatever the locale. Real arrays only. |
| `csnstrswapcase` | `np.strings.swapcase` | ASCII letters only, as on a bytes (`S`) array. Also in place; `X = csnstrswapcase(X, k)` swaps again on every pass. |
| `csnprint` | `print(a)` | `CsnStr(shape=..., dtype=str)`, elements quoted. |
| `csnsave` / `csnload` | `np.save` / `np.load` | `.npy` as `<U` (UTF-8 decoded to code points), loads `<U` and `\|S`; `.csn` dtype `3`. |

## Fourier analysis

| csnum | NumPy | Notes |
| --- | --- | --- |
| `csnfft` | `np.fft.fft` | Length is a fixed i-rate power of two. |
| `csnifft` | `np.fft.ifft` | |
| `csnrfft` | `np.fft.rfft` | |
| `csnirfft` | `np.fft.irfft` | |
| `csnfft2` | `np.fft.fft2` | |
| `csnifft2` | `np.fft.ifft2` | |
| `csnrfft2` | `np.fft.rfft2` | |
| `csnirfft2` | `np.fft.irfft2` | |
| `csnfftfreq` | `np.fft.fftfreq` | |
| `csnrfftfreq` | `np.fft.rfftfreq` | |
| `csnfftshift` | `np.fft.fftshift` | |
| `csnifftshift` | `np.fft.ifftshift` | |
| `csnstft` | `scipy.signal.stft` | Frames and their coordinates. |
| `csnistft` | `scipy.signal.istft` | |
| `csndctone1d` | `scipy.fft.dct(x, type=1)` | `norm=None`. Any length. |
| `csndcttwo1d` | `scipy.fft.dct(x, type=2)` | `norm=None`. Any length. |
| `csndstone1d` | `scipy.fft.dst(x, type=1)` | `norm=None`. Any length. |
| `csndsttwo1d` | `scipy.fft.dst(x, type=2)` | `norm=None`. Any length. |
| `csnhilbert1d` | `scipy.signal.hilbert` | The analytic signal, as scipy returns. Even length. |
| `csnhilbert1dr` | `np.imag(scipy.signal.hilbert(x))` | The transform alone, computed with two real FFTs. |
| `csnhilbert2` | `scipy.signal.hilbert2` | |

## Cepstral and mel analysis

| csnum | NumPy | Notes |
| --- | --- | --- |
| `csnmfcc` | `librosa.feature.mfcc` | HTK mel scale, Slaney-normalized bands, natural log. One argument sets both band and coefficient count. |
| `csnmfbank` | `librosa.filters.mel` | The matrix itself, `(bands, nfft / 2 + 1)`. |
| `csnmlogfbank` | — | The same matrix in logarithmic scale. |

## Audio features

| csnum | NumPy | Notes |
| --- | --- | --- |
| `csnzcr` | `librosa.feature.zero_crossing_rate(y, center=False)` | On a 1-D signal a number; along an axis one value per frame of `csnframe`. Defaults as librosa's: `\|x\| <= 1e-10` is 0, 0 counts as positive, crossings over `N`. |
| `csnamdf` | `[np.mean(np.abs(x[:n - t] - x[t:])) for t in range(maxlag + 1)]` | The curve along an axis, replaced by `maxlag + 1` lags; divided by `N - tau`. The pitch is the caller's: search a lag range, `D(0)` is always 0. |

## Convolution and correlation

| csnum | NumPy | Notes |
| --- | --- | --- |
| `csnconvolve1d` | `np.convolve` | Plus an axis: every lane along it is convolved on its own. |
| `csncorrelate1d` | `np.correlate` | Same kernel conjugation as NumPy's. |
| `csnconvolve` | `scipy.signal.convolve` | Kernel shaped like the source, flipped on every axis. |
| `csncorrelate` | `scipy.signal.correlate` | The same, unflipped and conjugated. |
| `csnfftconvolve1d` | `scipy.signal.fftconvolve` | Plus an axis. |
| `csnfftcorrelate1d` | `scipy.signal.correlate(..., method='fft')` | Plus an axis. |
| `csnfftconvolve` | `scipy.signal.fftconvolve` | N-D, kernel shaped like the source. |
| `csnfftcorrelate` | `scipy.signal.correlate(..., method='fft')` | N-D. |
| `csndeconvolve1d` | `scipy.signal.deconvolve` | The quotient, plus an axis. Undoes a FULL `csnconvolve1d`. |
| `csndecorrelate1d` | `scipy.signal.deconvolve(c, np.conj(h[::-1]))` | Undoes a FULL `csncorrelate1d`. Plus an axis. |
| `csndeconvolve` | — | N-D, kernel shaped like the source. |
| `csndecorrelate` | — | N-D. |
| `csnfftdeconvolve1d` | `np.fft.ifft(np.fft.fft(x, n) / np.fft.fft(h, n))[:len(x) - len(h) + 1]` | Plus an axis; `n` the next power of two at or above `len(x)`. |
| `csnfftdecorrelate1d` | the same with `np.conj(np.fft.fft(h, n))`, read from `len(h) - 1` | Plus an axis. |
| `csnfftdeconvolve` | the `fftn` form of the same | N-D. |
| `csnfftdecorrelate` | the `fftn` form of the same | N-D. |

The `csnfft*` four are the same operations as the four above them, computed by
padding to a power of two and multiplying in the spectrum: same arguments, same
lengths, same answers to within rounding. SciPy picks between the two methods
for you when you ask for `method='auto'`; here the choice is the opcode you
call.

The `edges` argument is NumPy's `mode` under another name: `0` FULL, `1` SAME,
`2` VALID, with the same lengths. Unlike NumPy's, it is an i-rate argument on
every overload, along with the axis, because the pair of them fixes the shape
of the output and a k-rate pass must not have to reallocate.

The deconvolve and decorrelate forms have no `edges` argument: they undo the
FULL span, the only one that keeps everything the source contributed, and
answer `x - h + 1` on each axis. The direct forms run the convolution sum
backwards, dividing by `h[0]` (deconvolution) or `conj(h[last])`
(decorrelation), which must be non-zero, and are stable only on a minimum-phase
kernel (reversed, for a decorrelation). The `csnfft*` forms divide spectra, have
no phase condition, and refuse a kernel with a spectral zero on the transform
grid, such as `[1, 1]` at Nyquist. The two routes agree when the input really is
a FULL convolution or correlation; otherwise the direct form returns the
quotient of a polynomial division and the transform a circular one.

## Interpolation, resampling and windows

| csnum | NumPy | Notes |
| --- | --- | --- |
| `csninterp` | `np.interp` | Linear matches; nearest / previous / next / PCHIP are `scipy.interpolate`. Boundary policy is explicit rather than a fill value. |
| `csnresample` | `scipy.signal.resample` | Interpolating resample along one axis, not Fourier. |
| `csnlagrange` | `scipy.interpolate.lagrange` | The coefficients, highest degree first, as `np.poly1d` takes them. Distinct `x` only. |
| `csnroots` | `np.roots` | Same coefficient order. Always complex, in no set order; one polynomial per slice along an optional axis. A leading zero is refused, not stripped. |
| `csnhanning` | `np.hanning` | |
| `csnhamming` | `np.hamming` | |
| `csnbartlett` | `np.bartlett` | |
| `csnblackman` | `np.blackman` | |
| `csnkaiser` | `np.kaiser` | |

## Filter design

| csnum | NumPy | Notes |
| --- | --- | --- |
| `csnlptolpzpk` | `scipy.signal.lp2lp_zpk` | |
| `csnlptohpzpk` | `scipy.signal.lp2hp_zpk` | A root at the origin is refused. |
| `csnlptobpzpk` | `scipy.signal.lp2bp_zpk` | The two roots of each pair are stored next to each other, not in two halves. |
| `csnlptobszpk` | `scipy.signal.lp2bs_zpk` | Same pair order; a root at the origin is refused. |
| `csnbilinearzpk` | `scipy.signal.bilinear_zpk` | `fs` in Hz, greater than zero. |
| `csntftozpk` | `scipy.signal.tf2zpk` | Real coefficients only. Roots in no set order. |
| `csnzpktotf` | `scipy.signal.zpk2tf` | 1-D zeros only. Real coefficients when the roots come in conjugate pairs, up to `1e-12` of the largest. |
| `csnlptolp` | `scipy.signal.lp2lp` | |
| `csnlptohp` | `scipy.signal.lp2hp` | |
| `csnlptobp` | `scipy.signal.lp2bp` | |
| `csnlptobs` | `scipy.signal.lp2bs` | |
| `csnzpktosos` | `scipy.signal.zpk2sos` | Digital, `pairing='nearest'` only. |
| `csnbuttap` | `scipy.signal.buttap` | |
| `csnbutterba` | `scipy.signal.butter` | Digital, `output='ba'`, frequencies in Hz with `fs` given; type `0` low, `1` high, `2` band, `3` stop. |
| `csnbuttersos` | `scipy.signal.butter` | The same with `output='sos'`; the form to use beyond the lowest orders. |
| `csncheby1ba` | `scipy.signal.cheby1` | `output='ba'`; `rp` after the cutoff, not before it. |
| `csncheby1sos` | `scipy.signal.cheby1` | `output='sos'`; `rp` after the cutoff, not before it. |
| `csncheby2ba` | `scipy.signal.cheby2` | `output='ba'`; `rs` after the cutoff, not before it. |
| `csncheby2sos` | `scipy.signal.cheby2` | `output='sos'`; `rs` after the cutoff, not before it. |
| `csnellipba` | `scipy.signal.ellip` | `output='ba'`; `rp`, `rs` after the cutoff, not before it. |
| `csnellipsos` | `scipy.signal.ellip` | `output='sos'`; `rp`, `rs` after the cutoff, not before it. |
| `csnlfilter` | `scipy.signal.lfilter` | Transposed direct form II along an axis; k-rate keeps each slice's state between passes, as `zi = zf`; audio form too. |
| `csnsosfilter` | `scipy.signal.sosfilt` | The same with second-order sections; `sos[:, 3]` must be 1. |
| `csnzlfilter` | `scipy.signal.lfilter(..., zi=zi)` | Returns `(y, zf)`; `zi` in scipy's layout, the source's shape with the axis replaced by the order. |
| `csnzsosfilter` | `scipy.signal.sosfilt(..., zi=zi)` | Returns `(y, zf)`; `zi` is `(n_sections, ...)` with the axis replaced by 2. |
| `csnrtbutter` | `scipy.signal.butter(..., output='sos')` + `sosfilt` | Audio only, redesigned every control period from a k-rate cutoff, the state kept; a band is centre and width in Hz, `[fc - bw/2, fc + bw/2]`. |
| `csnrtcheby1` | `scipy.signal.cheby1(..., output='sos')` + `sosfilt` | The same; `rp` after the cutoff (and width). |
| `csnrtcheby2` | `scipy.signal.cheby2(..., output='sos')` + `sosfilt` | The same; `rs` after the cutoff (and width). |
| `csnrtellip` | `scipy.signal.ellip(..., output='sos')` + `sosfilt` | The same; `rp`, `rs` after the cutoff (and width). |

## Special functions

| csnum | NumPy | Notes |
| --- | --- | --- |
| `csnlegendre` | `scipy.special.lpmv` | Arguments `(n, m, x)`, not `(m, n, x)`, and no Condon-Shortley phase: `lpmv(m, n, x) == (-1)^m * csnlegendre(n, m, x)`. `m >= 0` only. |
| `csnsphharm` | — | The real AmbiX harmonic, SN3D, no phase, no `1/sqrt(4 pi)`. `scipy.special.sph_harm` is the complex, orthonormal one with the phase: for `m != 0` this one is the real or imaginary part of that, renormalised, not a rescaling of the same value. |
| `csnsphharmacn` | — | Every harmonic up to an order, by ACN, at one direction or as a `channels x directions` matrix. |

## No NumPy counterpart

These exist because the arrays live inside a running orchestra, which is the one
thing NumPy never has to deal with:

| csnum | What it does |
| --- | --- |
| `csnfromaudio` / `csntoaudio` | One control period between an audio signal and an array. |
| `csnk` / `csni` | Rate casts: an array made k-rate in place or as a k-rate copy, or frozen at its init value. NumPy has no rates. |
| `csnpack` / `csnunpack` | A whole `a[]` as a `channels x ksmps` matrix, and back. |
| `csnsnap` / `csnstream` | Frames of a size independent of `ksmps`, and their overlap-add. |
| `csnrtlock` / `csnrtunlock` | Mark an array as a real-time path, forbidding reallocation at perf time. |
| `csnrtlockstart` / `csnrtlockend` | The same mark on every array a note creates between the two. |
| `csnrtlockall` | The same for the whole performance, declared in the orchestra header. |
| `csnforeach` | Maps a Csound opcode over every element, in place. Nearest idea is `np.vectorize`, but the callback is an orchestra opcode. |
| `csnnext` | Walks an array one element per control period. An iterator paced by the control rate, which NumPy has no notion of. |
| `csnt60sab` / `csnt60eyr` | Reverberation time of a room, Sabine and Eyring-Norris. |
| `csnrt60absp` | The absorption a room needs to reach a target reverberation time. |
| `csnfschrd` | Schroeder frequency: where a room stops being modal and becomes diffuse. |
| `csnfpqr` | Resonant frequency of a rectangular room for one modal index triple. |
| `csnt60tofbg` / `csnfbgtot60` | Comb feedback gain from a decay time, and the decay time back. |
| `csndbsum` | Adds levels in dB by adding their powers, over a pair, an array or one axis. |
| `csnsamptomillis` / `csnsamptosec` | Sample counts into milliseconds or seconds at a given rate. |
| `csnmillistosamp` / `csnsectosamp` | Milliseconds or seconds into sample counts at a given rate. |
| `csnpoltocar` / `csncartopol` | Polar and cartesian coordinates, in the plane. |
| `csncyltocar` / `csncartocyl` | Cylindrical and cartesian coordinates. |
| `csnsphtocar` / `csncartosph` | Spherical and cartesian coordinates, `(r, theta, phi)`. |
| `csnhoatocar` / `csncartohoa` | Ambisonics direction and cartesian, `(distance, azimuth, elevation)` in the AmbiX frame. The elevation is measured from the horizon, not from `+z`. |
| `csnrotmat` | A 3 x 3 rotation matrix about a basis axis or an arbitrary direction, for `csnmatmul`. |
| `csnrotmatypr` | The same, composing a yaw, a pitch and a roll in the audio convention, in the one order that is meant. |
| `csnnmtoacn` / `csnacntonm` | Ambisonics channel index from an order and a degree, and back. ACN ordering. |
| `csnhoaordtochnls` / `csnchnlstohoaord` | Channels in a complete 3-D set of a given order, and back. A count that is not a perfect square is refused. |
| `csnsn3dton3d` / `csnn3dtosn3d` | The per-channel gain vector between the SN3D and N3D normalisations, indexed by ACN. |
| `csnfromftable` / `csntoftable` | Csound function table in and out. |
| `csnunlikeset` | Drops the set classification. |

---
