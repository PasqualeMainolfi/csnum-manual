# csnum opcode index

One line per opcode, grouped by family. Overloads are not listed: an opcode
appears once under its plain name, whatever the number of type and rate
variants behind it. The parentheses carry two things: the rate, `i, k` for the
opcodes with both an i-time and a performance-time form, `i` for the ones that
only run at init, `k` for the ones that only act at performance time, and the
element types accepted, `real, complex` or
`real only`. The five opcodes that read a complex array and hand back its parts
are marked `complex only`, since a real input has nothing for them to do.
`string` marks the opcodes that also take a `CsnStr`, an array of strings
(`string in place` when only the in-place form does); see
[String arrays](string-arrays.md).

Conventions that apply throughout: explicit negative axes count from the end,
so `-1` is always the last axis; omitting an axis selects the opcode's documented
flat, all-axes, or last-axis default; opcodes that produce a new array usually have
an in-place sibling under the same name that writes back into its source and
returns nothing; k-rate forms put the trigger before an explicit optional axis, and a zero
trigger republishes the previous result instead of recomputing. A trigger that
is the only k-rate argument is required to select the performance overload;
side-effecting opcodes simply do nothing when it is zero; where an i-time and a
k-rate form take the same arguments (`csntranspose`, `csnflatten`, `csnlikeset`),
omitting the trigger selects the i-time form.
**The rate of a named opcode is chosen by its trigger, which must be written for
the k-rate form; the operators take no trigger and follow the rate of their
operands, which `csnk` and `csni` set.** A k-rate form computes during its
init pass only from arguments known there, constants, i variables and arrays;
with a k scalar among them the output is laid out empty or reserved and the
first triggered pass computes it. See the README for the `CsnArr` value model,
the k-rate versioning and what the init pass computes.

## Creation

- [**csnempty**](csnempty.md) - reserves a shape without publishing any element (i, k — real, complex, string)
- [**csnzeros**](csnzeros.md) - array of zeros (i, k — real, complex)
- [**csnones**](csnones.md) - array of ones (i, k — real, complex)
- [**csnfull**](csnfull.md) - array filled with one value (i, k — real, complex, string)
- [**csnlike**](csnlike.md) - array shaped and typed like another, filled with a value (i, k — real, complex, string)
- [**csnidentity**](csnidentity.md) - identity matrix (i, k — real, complex)
- [**csnarange**](csnarange.md) - evenly spaced values from start to stop by step (i, k — real only)
- [**csnlinspace**](csnlinspace.md) - n values evenly spaced between two bounds (i, k — real only)
- [**csnlogspace**](csnlogspace.md) - n values evenly spaced on a logarithmic scale (i, k — real only)
- [**csngeomspace**](csngeomspace.md) - n values in geometric progression (i, k — real only)
- [**csnrand**](csnrand.md) - uniform random values in a range (i, k — real only)
- [**csnrandint**](csnrandint.md) - uniform random integers in a half-open range (i, k — real only)
- [**csnseed**](csnseed.md) - seeds the random generator (i)

## Conversion, lifetime and queries

- [**csnfromarray**](csnfromarray.md) - Csound array to `CsnArr` (i, k — real, complex, string)
- [**csntoarray**](csntoarray.md) - `CsnArr` to Csound array (i, k — real, complex, string)
- [**csnfromftable**](csnfromftable.md) - function table to `CsnArr` (i — real only)
- [**csntoftable**](csntoftable.md) - `CsnArr` to function table, optionally resizing it (i — real only)
- [**csncopy**](csncopy.md) - independent copy of an array (i, k — real, complex, string)
- [**csnk**](csnk.md) - makes an array k-rate, in place or as a k-rate copy in an expression, so the operators on it run at performance time (i, k — real, complex, string)
- [**csni**](csni.md) - copy of an array frozen at its init value, the counterpart of `i()` (i — real, complex, string)
- [**csntype**](csntype.md) - item type: 0 real, 1 complex, 2 string (i, k — real, complex, string)
- [**csndims**](csndims.md) - number of dimensions (i, k — real, complex, string)
- [**csnsize**](csnsize.md) - number of elements (i, k — real, complex, string)
- [**csnshape**](csnshape.md) - extents, one per dimension (i, k — real, complex, string)
- [**csnisempty**](csnisempty.md) - 1 when the array holds no element (i, k — real, complex, string)
- [**csnprint**](csnprint.md) - prints shape, dtype and values in a NumPy-style layout (i, k — real, complex, string)

## Persistence

Both accept `.csn` (csnum's own format) or `.npy` (NumPy format), selected by
the path extension. `.npy` writes `float64` or `complex128`; the loader also
converts supported boolean, integer and lower-precision floating/complex dtypes,
including Fortran-order files. A zero trigger does not touch the disk.

- [**csnsave**](csnsave.md) - writes an array to a `.csn` or `.npy` file (i, k — real, complex, string)
- [**csnload**](csnload.md) - reads a `.csn` or supported `.npy` file (i, k — real, complex, string)

## Shape and layout

- [**csnreshape**](csnreshape.md) - same elements under a new shape (i, k — real, complex, string)
- [**csnflatten**](csnflatten.md) - collapses every dimension into one (i, k — real, complex, string)
- [**csntranspose**](csntranspose.md) - permutes the axes (i, k — real, complex, string)
- [**csnflip**](csnflip.md) - reverses the order along an axis (i, k — real, complex, string)
- [**csnroll**](csnroll.md) - circular shift, whole array or along an axis (i, k — real, complex, string)
- [**csnreverse**](csnreverse.md) - reverses the flat element order (i, k — real, complex, string)
- [**csnpad**](csnpad.md) - adds elements before and after, filled with a value (i, k — real, complex, string)
- [**csntruncate**](csntruncate.md) - shortens one axis, or every axis, to a length (i, k — real, complex, string)
- [**csnhead**](csnhead.md) - keeps the first n elements of a 1-D array (i, k — real, complex, string)
- [**csnresize**](csnresize.md) - reshapes to any size, zero-filling what it grows (i, k — real, complex, string)
- [**csnconcat**](csnconcat.md) - joins two arrays, flat or along an axis (i, k — real, complex, string)
- [**csnstack**](csnstack.md) - inserts a new axis and stacks two or more equal-shaped arrays (i, k — real, complex, string)
- [**csnframe**](csnframe.md) - cuts an axis into overlapping frames of a length every hop, one more dimension (i, k — real, complex, string)
- [**csninsert**](csninsert.md) - inserts elements or a block at a position (i, k — real, complex, string)
- [**csnremove**](csnremove.md) - removes elements or a block at a position (i, k — real, complex, string)
- [**csnpush**](csnpush.md) - appends one element at the end (i, k — real, complex, string)
- [**csnpop**](csnpop.md) - removes the last element and returns it (i, k — real, complex, string)

## Indexing and selection

`CsnArr` also takes `[]`: `v[i][j]` reads and writes one element, one index per
dimension (a complex element is written, and read with `csnget`), and
`v[start:end, step, axis]` reads a slice, end included as in Csound's
`slicearray`, along axis 0 by default (i, k — real, complex, string). See
[Indexing and slicing with `[]`](indexing.md).

- [**csnget**](csnget.md) - reads one element by coordinates (i, k — real, complex, string)
- [**csngetrow**](csngetrow.md) - extracts one row of a 2-D array as a vector (i, k — real, complex)
- [**csngetcol**](csngetcol.md) - extracts one column of a 2-D array as a vector (i, k — real, complex)
- [**csnset**](csnset.md) - writes one element by coordinates (i, k — real, complex, string)
- [**csngetslice**](csngetslice.md) - extracts a strided slice along an axis (i, k — real, complex, string)
- [**csnsetslice**](csnsetslice.md) - writes into a strided slice along an axis (i, k — real, complex, string)
- [**csntake**](csntake.md) - picks one index along an axis, dropping that axis (i, k — real, complex, string)
- [**csnwhere**](csnwhere.md) - picks from two arrays element by element, driven by a mask (i, k — real, string)
- [**csnputmask**](csnputmask.md) - the same choice made in place, the array being its own mask; for strings, writes values where a mask is set (i, k — real, string)
- [**csncompress**](csncompress.md) - keeps the entries a 1-D mask marks, along an axis or flat (i, k — real, complex, string)
- [**csnselect**](csnselect.md) - keeps the elements a mask marks, as a flat array (i, k — real, complex, string)
- [**csnindexof**](csnindexof.md) - coordinates of the first element equal to a scalar, or an empty array (i, k — real only)
- [**csnbincount**](csnbincount.md) - counts every non-negative integer bin, optionally accumulating weights (i, k — real only)
- [**csnsearchsorted**](csnsearchsorted.md) - insertion indices in an ascending 1-D array, left or right of equal values (i, k — real only)
- [**csnargwhere**](csnargwhere.md) - coordinates of the elements matching a value array (i, k — real only)
- [**csnargnonzero**](csnargnonzero.md) - coordinates of the non-zero elements (i, k — real only)
- [**csnargisnan**](csnargisnan.md) - coordinates of the NaN elements (i, k — real only)
- [**csnnext**](csnnext.md) - hands back one element per control period, walking the array flat (k — real, complex)

## Elementwise arithmetic

`CsnArr` also takes the operators `+`, `-`, `*`, `/` and `^`, between two arrays
or an array and a real or `:Complex;` scalar on either side, the compound `+=`,
`-=`, `*=` and `/=`, and unary minus. They are the named opcodes below without a
trigger, and follow the rates of their operands: with i-rate operands they run
once, at init; `csnk` makes an operand k-rate so that they run on every control
period. An audio signal on either side of `+`, `-`, `*`, `/` and `^` takes part
as its block of `ksmps` samples, shape `(ksmps,)`; the result is k-rate.

- [**csnadd**](csnadd.md) - addition, array with array or with a scalar (i, k — real, complex)
- [**csnsubtract**](csnsubtract.md) - subtraction, array with array or with a scalar (i, k — real, complex)
- [**csnmul**](csnmul.md) - multiplication, array with array or with a scalar (i, k — real, complex)
- [**csndiv**](csndiv.md) - division, array with array or with a scalar (i, k — real, complex)
- [**csnpow**](csnpow.md) - power, array with array or with a scalar (i, k — real, complex)
- [**csnlog**](csnlog.md) - logarithm in an arbitrary base (i, k — real, complex)
- [**csndivmod**](csndivmod.md) - quotient and remainder in one pass, as two arrays (i, k — real only)
- [**csnhypot**](csnhypot.md) - hypotenuse of two arrays, elementwise (i, k — real only)
- [**csnminimum**](csnminimum.md) - elementwise minimum of two arrays, or of an array and a scalar (i, k — real only)
- [**csnmaximum**](csnmaximum.md) - elementwise maximum of two arrays, or of an array and a scalar (i, k — real only)
- [**csnclip**](csnclip.md) - clamps every element between two bounds (i, k — real only)
- [**csnstradd**](csnstradd.md) - joins strings elementwise, two arrays with broadcasting or an array and one string on either side; on two S, and as S + S (i, k — string)
- [**csnstrmul**](csnstrmul.md) - repeats each string a number of times, one count or an array of counts; on one S, and as S * n (i, k — string)
- [**csnstrupper**](csnstrupper.md) - converts the ASCII letters of each string to upper case, as a copy or in place (i, k — string)
- [**csnstrlower**](csnstrlower.md) - converts the ASCII letters of each string to lower case, as a copy or in place (i, k — string)
- [**csnstrcapitalize**](csnstrcapitalize.md) - raises the first character of each string and lowers the rest, ASCII only, as a copy or in place (i, k — string)
- [**csnstrswapcase**](csnstrswapcase.md) - turns every ASCII letter of each string into the other case, as a copy or in place (i, k — string)
- [**csnstrtitle**](csnstrtitle.md) - puts each string in title case, a letter up after a non-letter and down after a letter, ASCII only, as a copy or in place (i, k — string)
- [**csnstrstrip**](csnstrstrip.md) - removes ASCII whitespace, or the bytes of `chars`, at both ends of each string, as a copy or in place; on one S as Python's str.strip (i, k — string)
- [**csnstrlstrip**](csnstrlstrip.md) - removes ASCII whitespace, or the bytes of `chars`, at the start of each string, as a copy or in place; on one S as Python's str.lstrip (i, k — string)
- [**csnstrrstrip**](csnstrrstrip.md) - removes ASCII whitespace, or the bytes of `chars`, at the end of each string, as a copy or in place; on one S as Python's str.rstrip (i, k — string)
- [**csnstrcenter**](csnstrcenter.md) - pads each string with spaces, or a fill character, on both sides to a width in bytes, as a copy or in place (i, k — string)
- [**csnstrljust**](csnstrljust.md) - pads each string with spaces, or a fill character, on the right to a width in bytes, as a copy or in place (i, k — string)
- [**csnstrrjust**](csnstrrjust.md) - pads each string with spaces, or a fill character, on the left to a width in bytes, as a copy or in place (i, k — string)
- [**csnstrreplace**](csnstrreplace.md) - replaces the occurrences of a substring in each string, all or the first count, as a copy or in place; on one S as Python's str.replace (i, k — string)
- [**csnstrsubstr**](csnstrsubstr.md) - keeps the bytes of each string from start up to stop, every step-th, as a copy or in place (i, k — string)
- [**csnstrlen**](csnstrlen.md) - the length in bytes of each string, as a real array (i, k — string)
- [**csnstrfind**](csnstrfind.md) - the lowest index of a substring in each string, optionally between start and end, -1 where it is missing (i, k — string)
- [**csnstrrfind**](csnstrrfind.md) - the highest index of a substring in each string, optionally between start and end, -1 where it is missing (i, k — string)
- [**csnstrstartswith**](csnstrstartswith.md) - 1 where a string begins with a prefix, otherwise 0 (i, k — string)
- [**csnstrendswith**](csnstrendswith.md) - 1 where a string ends with a suffix, otherwise 0 (i, k — string)
- [**csnstrisalpha**](csnstrisalpha.md) - 1 where a non-empty string holds ASCII letters only, otherwise 0 (i, k — string)
- [**csnstrisdigit**](csnstrisdigit.md) - 1 where a non-empty string holds ASCII digits only, otherwise 0 (i, k — string)
- [**csnstrisalnum**](csnstrisalnum.md) - 1 where a non-empty string holds ASCII letters and digits only, otherwise 0 (i, k — string)
- [**csnstrisspace**](csnstrisspace.md) - 1 where a non-empty string holds ASCII whitespace only, otherwise 0 (i, k — string)
- [**csnstrtonum**](csnstrtonum.md) - reads each string as a number, as Python's float(), NaN where it is not one, as a real array (i, k — string)
- [**csnnumtostr**](csnnumtostr.md) - writes each number of a real array as a string, as NumPy's astype(str) (i, k — real only)
- [**csnstrjoin**](csnstrjoin.md) - joins every string of an array, of any rank in row-major order, into one S with a separator, as Python's sep.join (i, k — string)
- [**csnstrsplit**](csnstrsplit.md) - splits one S at a separator into a 1-D string array, at most maxsplit cuts from the left, as Python's str.split (i, k — string)
- [**csnstrrsplit**](csnstrrsplit.md) - splits one S at a separator into a 1-D string array, at most maxsplit cuts from the right, as Python's str.rsplit (i, k — string)
- [**csnstrpartition**](csnstrpartition.md) - splits one S at the first separator into [head, sep, tail], as Python's str.partition (i, k — string)
- [**csnstrrpartition**](csnstrrpartition.md) - splits one S at the last separator into [head, sep, tail], as Python's str.rpartition (i, k — string)
- [**csnstrchr**](csnstrchr.md) - the one-byte S of an ASCII code, 1 to 127, as Python's chr on ASCII (i, k — string)
- [**csnstrord**](csnstrord.md) - the byte of a one-byte S, 0 to 255, as Python's ord on bytes (i, k — string)
- [**csnstrtoascii**](csnstrtoascii.md) - the bytes of one S as a real 1-D array, 0 to 255 (i, k — string)
- [**csnstrfromascii**](csnstrfromascii.md) - one S from a real 1-D array of ASCII codes, 1 to 127 (i, k — string)
- [**csnstrencode**](csnstrencode.md) - the UTF-8 bytes of one S as a real 1-D array, the S checked as UTF-8, as Python's s.encode() (i, k — string)
- [**csnstrdecode**](csnstrdecode.md) - one S from a real 1-D array of UTF-8 bytes, checked strictly, as Python's bytes.decode() (i, k — string)
- [**csnstrtocodepoints**](csnstrtocodepoints.md) - the code points of one UTF-8 S as a real 1-D array, as [ord(c) for c in s] (i, k — string)
- [**csnstrfromcodepoints**](csnstrfromcodepoints.md) - one UTF-8 S from a real 1-D array of code points, U+10FFFF at most, no surrogates (i, k — string)
- [**csnstraslist**](csnstraslist.md) - the characters of one UTF-8 S as a 1-D CsnStr, as Python's list(s) (i, k — string)
- [**csnlistasstr**](csnlistasstr.md) - the numbers of a real 1-D array as one S joined by a separator, as Python's sep.join(map(str, a)) (i, k — real only)
- [**csntobinary**](csntobinary.md) - the binary digits of a whole number, 0 to 2^64, zero-padded to a width, as Python's format(n, 'b') (i, k — real only)
- [**csnfrombinary**](csnfrombinary.md) - the number of a string of binary digits, optional 0b prefix, as Python's int(s, 2) (i, k — string)
- [**csntohex**](csntohex.md) - the upper-case hex digits of a whole number, 0 to 2^64, zero-padded to a width, as Python's format(n, 'X') (i, k — real only)
- [**csnfromhex**](csnfromhex.md) - the number of a string of hex digits, optional 0x prefix, as Python's int(s, 16) (i, k — string)
- [**csnbinstrtoarr**](csnbinstrtoarr.md) - the binary digits of one S as a real 1-D array of 0 and 1, optional 0b prefix (i, k — string)
- [**csnhexstrtoarr**](csnhexstrtoarr.md) - the hex digits of one S as a 1-D CsnStr, one digit each, optional 0x prefix (i, k — string)
- [**csntobase64**](csntobase64.md) - the padded base64 text of the bytes of one S or of a real 1-D array of bytes, as Python's base64.b64encode (i, k — string)
- [**csnfrombase64**](csnfrombase64.md) - the bytes of canonical base64 text, as one S or a real 1-D array, as Python's base64.b64decode (i, k — string)
- [**csntobuffer**](csntobuffer.md) - the bytes of a real array, flattened, in a NumPy dtype with explicit byte order (|u1 to <f8), as a real 1-D array of 0 to 255, as NumPy's a.astype(dtype).tobytes() (i, k — real only)
- [**csnfrombuffer**](csnfrombuffer.md) - a real 1-D array from bytes, a real 1-D array of 0 to 255, read in a NumPy dtype, as NumPy's np.frombuffer(b, dtype) (i, k — real only)
- [**csnabs**](csnabs.md) - absolute value, or magnitude for a complex array (i, k — real, complex)
- [**csnsign**](csnsign.md) - -1, 0 or 1 by the sign of each element (i, k — real, complex)
- [**csnfloor**](csnfloor.md) - rounds each element down (i, k — real only)
- [**csnceil**](csnceil.md) - rounds each element up (i, k — real only)
- [**csnround**](csnround.md) - rounds each element to the nearest integer, halves to even as in NumPy (i, k — real only)
- [**csnforeach**](csnforeach.md) - maps a user-defined opcode over every element, in place (k — real only)

## Transcendental functions

- [**csnexp**](csnexp.md) - exponential (i, k — real, complex)
- [**csnsqrt**](csnsqrt.md) - square root (i, k — real, complex)
- [**csncbrt**](csncbrt.md) - cube root (i, k — real, complex)
- [**csnsin**](csnsin.md) - sine (i, k — real, complex)
- [**csncos**](csncos.md) - cosine (i, k — real, complex)
- [**csntan**](csntan.md) - tangent (i, k — real, complex)
- [**csnasin**](csnasin.md) - arcsine (i, k — real, complex)
- [**csnacos**](csnacos.md) - arccosine (i, k — real, complex)
- [**csnatan**](csnatan.md) - arctangent (i, k — real, complex)
- [**csnsinh**](csnsinh.md) - hyperbolic sine (i, k — real, complex)
- [**csncosh**](csncosh.md) - hyperbolic cosine (i, k — real, complex)
- [**csntanh**](csntanh.md) - hyperbolic tangent (i, k — real, complex)
- [**csnasinh**](csnasinh.md) - inverse hyperbolic sine (i, k — real, complex)
- [**csnacosh**](csnacosh.md) - inverse hyperbolic cosine (i, k — real, complex)
- [**csnatanh**](csnatanh.md) - inverse hyperbolic tangent (i, k — real, complex)

## Angles and phase

- [**csndegtorad**](csndegtorad.md) - degrees to radians (i, k — real only)
- [**csnradtodeg**](csnradtodeg.md) - radians to degrees (i, k — real only)
- [**csnatan2**](csnatan2.md) - two-argument arctangent, quadrant aware (i, k — real only)
- [**csnwrap**](csnwrap.md) - wraps values into one period (i, k — real, complex)
- [**csnunwrap**](csnunwrap.md) - removes the jumps left by wrapping, along an axis (i, k — real, complex)

## Comparison and logic

- [**csngt**](csngt.md) - elementwise greater than, as a 0/1 array (i, k — real only)
- [**csnlt**](csnlt.md) - elementwise less than, as a 0/1 array (i, k — real only)
- [**csnge**](csnge.md) - elementwise greater or equal, as a 0/1 array (i, k — real only)
- [**csnle**](csnle.md) - elementwise less or equal, as a 0/1 array (i, k — real only)
- [**csneq**](csneq.md) - elementwise equality, as a 0/1 array (i, k — real only)
- [**csnne**](csnne.md) - elementwise inequality, as a 0/1 array (i, k — real only)
- [**csnisnan**](csnisnan.md) - 1 where an element is NaN, otherwise 0 (i, k — real only)
- [**csnisinf**](csnisinf.md) - 1 where an element is positive or negative infinity, otherwise 0 (i, k — real only)
- [**csnisfin**](csnisfin.md) - 1 where an element is finite, otherwise 0 (i, k — real only)
- [**csnlogicand**](csnlogicand.md) - logical and of two arrays, or of an array and a scalar (i, k — real only)
- [**csnlogicor**](csnlogicor.md) - logical or of two arrays, or of an array and a scalar (i, k — real only)
- [**csnlogicnot**](csnlogicnot.md) - logical negation (i, k — real only)
- [**csnall**](csnall.md) - 1 when every element is non-zero (i, k — real, complex)
- [**csnany**](csnany.md) - 1 when at least one element is non-zero (i, k — real, complex)
- [**csncnteq**](csncnteq.md) - counts the elements equal to a value (i, k — real only)
- [**csncntnz**](csncntnz.md) - counts the non-zero elements (i, k — real only)
- [**csncntnan**](csncntnan.md) - counts the NaN elements (i, k — real only)

## Reductions and statistics

- [**csnsum**](csnsum.md) - sum, over everything or along an axis (i, k — real, complex)
- [**csnprod**](csnprod.md) - product, over everything or along an axis (i, k — real, complex)
- [**csnsub**](csnsub.md) - running subtraction of every element from the first (i, k — real, complex)
- [**csnmean**](csnmean.md) - arithmetic mean (i, k — real, complex)
- [**csnmin**](csnmin.md) - smallest element (i, k — real only)
- [**csnmax**](csnmax.md) - largest element (i, k — real only)
- [**csnmedian**](csnmedian.md) - median (i, k — real only)
- [**csnrms**](csnrms.md) - root mean square, over everything or along an axis (i, k — real only)
- [**csnstd**](csnstd.md) - standard deviation (i, k — real, complex)
- [**csnvar**](csnvar.md) - variance (i, k — real, complex)
- [**csnpercentile**](csnpercentile.md) - percentile, from 0 to 100 (i, k — real only)
- [**csnquantile**](csnquantile.md) - quantile, from 0 to 1 (i, k — real only)
- [**csnargmin**](csnargmin.md) - coordinates of the smallest element (i, k — real only)
- [**csnargmax**](csnargmax.md) - coordinates of the largest element (i, k — real only)
- [**csncumsum**](csncumsum.md) - cumulative sum (i, k — real, complex)
- [**csncumprod**](csncumprod.md) - cumulative product (i, k — real, complex)
- [**csndiff**](csndiff.md) - differences between consecutive elements (i, k — real, complex)
- [**csngrad**](csngrad.md) - central-difference gradient (i, k — real only)
- [**csnmovmean**](csnmovmean.md) - moving average over a window (i, k — real, complex)
- [**csnmovmedian**](csnmovmedian.md) - moving median over a window (i, k — real only)
- [**csnmedfilt1d**](csnmedfilt1d.md) - median filter along one axis, zero-padded edges (i, k — real only)
- [**csnmedfilt**](csnmedfilt.md) - N-D median filter over a box, zero-padded edges (i, k — real only)
- [**csnmovmin**](csnmovmin.md) - moving minimum over a window (i, k — real only)
- [**csnmovmax**](csnmovmax.md) - moving maximum over a window (i, k — real only)
- [**csnmovstd**](csnmovstd.md) - moving standard deviation over a window (i, k — real, complex)
- [**csnmovvar**](csnmovvar.md) - moving variance over a window (i, k — real, complex)

## Sorting and sets

A set array is one-dimensional, real, sorted and duplicate-free. Only the set
API preserves that invariant. Generic array operations do not; normalize their
result with **csnlikeset** before using it as a set again. See
[the set-array contract](set-arrays.md).

- [**csnshuffle**](csnshuffle.md) - randomly permutes the flat element order in place (i, k — real, string)
- [**csnperm**](csnperm.md) - every permutation of a 1-D array, or the first few, one per row (i, k — real only)
- [**csnsort**](csnsort.md) - sorts, over everything or along an axis (i, k — real only)
- [**csnargsort**](csnargsort.md) - the coordinates that would sort the array (i, k — real only)
- [**csnunique**](csnunique.md) - the distinct values, in order (i, k — real only)
- [**csnargunique**](csnargunique.md) - coordinates of the first occurrence of each value (i, k — real only)
- [**csnlikeset**](csnlikeset.md) - normalizes an array as a sorted, duplicate-free set (i, k — real only)
- [**csnunlikeset**](csnunlikeset.md) - removes the set classification without changing the values (i, k — real only)
- [**csnsetinsert**](csnsetinsert.md) - inserts a value while preserving the set invariant (i, k — real only)
- [**csnsetremove**](csnsetremove.md) - removes a value while preserving the set invariant (i, k — real only)
- [**csnsetcontains**](csnsetcontains.md) - tests membership (i, k — real only)
- [**csnsetunion**](csnsetunion.md) - union of two sets (i, k — real only)
- [**csnsetintersect**](csnsetintersect.md) - intersection of two sets (i, k — real only)
- [**csnsetdiff**](csnsetdiff.md) - values in the first set but not the second (i, k — real only)
- [**csnsetsymdiff**](csnsetsymdiff.md) - values belonging to exactly one set (i, k — real only)
- [**csnsetissubset**](csnsetissubset.md) - tests whether the first set is a subset of the second (i, k — real only)
- [**csnsetissuperset**](csnsetissuperset.md) - tests whether the first set is a superset of the second (i, k — real only)
- [**csnsetisdisjoint**](csnsetisdisjoint.md) - tests whether two sets have no common value (i, k — real only)
- [**csnsetisequal**](csnsetisequal.md) - tests whether two sets contain the same values (i, k — real only)

## Linear algebra and geometry

- [**csndot**](csndot.md) - NumPy-style dot: scalar product of vectors, matrix product of matrices (i, k — real, complex)
- [**csninner**](csninner.md) - inner product: sum over the last axis of both operands (i, k — real, complex)
- [**csnouter**](csnouter.md) - outer product of two vectors (i, k — real, complex)
- [**csnmatmul**](csnmatmul.md) - matrix multiplication (i, k — real, complex)
- [**csntrace**](csntrace.md) - sum of the diagonal (i, k — real, complex)
- [**csndiag**](csndiag.md) - diagonal of a matrix, or a matrix from a diagonal (i, k — real, complex)
- [**csnnorm**](csnnorm.md) - vector or matrix norm of a given order (i, k — real, complex)
- [**csnnormalize**](csnnormalize.md) - divides by its own norm of a given order (sum of magnitudes by default) (i, k — real, complex)
- [**csncross**](csncross.md) - cross product of two 3-element vectors (i, k — real only)
- [**csndist**](csndist.md) - Minkowski distance between two arrays, of a given order (i, k — real, complex)
- [**csnpairdist**](csnpairdist.md) - elementwise distance between two arrays of the same shape (i, k — real, complex)
- [**csnangledist**](csnangledist.md) - angle between two vectors (i, k — real, complex)
- [**csnproject**](csnproject.md) - component of one vector along another (i, k — real only)
- [**csnreject**](csnreject.md) - component of one vector orthogonal to another (i, k — real only)
- [**csnreflect**](csnreflect.md) - reflects a vector about another (i, k — real, complex)
- [**csnsolve**](csnsolve.md) - solves a linear system A x = B, any number of right-hand sides (i, k — real, complex)
- [**csninv**](csninv.md) - inverse of a square matrix (i, k — real, complex)
- [**csndet**](csndet.md) - determinant of a square matrix (i, k — real, complex)
- [**csnsavgol**](csnsavgol.md) - Savitzky-Golay coefficient matrix, one row per derivative order (i — real only)
- [**csnhilbertmat**](csnhilbertmat.md) - the Hilbert matrix, 1 / (i + j + 1) (i, k — real output)

The three matrix operations share one LU decomposition with partial pivoting.
A pivot counts as zero when it falls at or below `n * DBL_EPSILON` times the
largest magnitude in the matrix, so a matrix that is singular only to within
rounding is caught too. `csninv` and `csnsolve` refuse a singular matrix;
`csndet` answers zero, since that is the determinant and asking for it is how
one tests for singularity.

`csnsavgol` only builds the filter; applying it is `csncorrelate1d`, on the row
for the derivative wanted. Correlation, not convolution: the rows come out in
natural order, and convolution would reverse them, which flips the sign of
every odd-order row.

## Complex arrays
`csnadd`, `csnsubtract`, `csnmul`, `csndiv`, `csnpow` and `csnsqrt` also take
scalar `:Complex;` operands, and `csnabs`, `csnangle` and `csnconj` a single
one, with no array operand and no trigger involved. Those forms are listed on the
opcode's own page rather than as separate entries here.

- [**csnreal**](csnreal.md) - real parts, as a real array (i, k — complex only)
- [**csnimag**](csnimag.md) - imaginary parts, as a real array (i, k — complex only)
- [**csnangle**](csnangle.md) - argument of each element (i, k — complex only)
- [**csnconj**](csnconj.md) - complex conjugate (i, k — complex only)
- [**csntocomplex**](csntocomplex.md) - real array to complex, imaginary parts at zero (i, k — real only)
- [**csntoreal**](csntoreal.md) - complex array to real, keeping the real parts (i, k — complex only)

## Fourier analysis

Transform lengths are fixed i-rate parameters and must be positive powers of
two. The k-rate forms observe source changes while their trigger is non-zero; a
zero trigger republishes the previous result. `csnfftfreq` and `csnrfftfreq` also
accept k-rate lengths and do not require powers of two.

- [**csnfft**](csnfft.md) - full complex FFT along one axis (i, k — real, complex input; complex output)
- [**csnrfft**](csnrfft.md) - one-sided FFT of a real array (i, k — real input; complex output)
- [**csnifft**](csnifft.md) - inverse full complex FFT (i, k — real, complex input; complex output)
- [**csnirfft**](csnirfft.md) - real inverse of a one-sided spectrum (i, k — real, complex input; real output)
- [**csnfft2**](csnfft2.md) - two-dimensional full complex FFT (i, k — real, complex input; complex output)
- [**csnrfft2**](csnrfft2.md) - two-dimensional real FFT with a one-sided last axis (i, k — real input; complex output)
- [**csnifft2**](csnifft2.md) - two-dimensional inverse complex FFT (i, k — real, complex input; complex output)
- [**csnirfft2**](csnirfft2.md) - real inverse of a two-dimensional one-sided spectrum (i, k — real, complex input; real output)
- [**csnstft**](csnstft.md) - short-time Fourier transform and coordinates (i, k — real, complex input; complex frames)
- [**csnistft**](csnistft.md) - inverse STFT and sample coordinates (i, k — complex input; real or complex output)
- [**csnfftfreq**](csnfftfreq.md) - coordinates for a full FFT spectrum (i, k — real output)
- [**csnrfftfreq**](csnrfftfreq.md) - coordinates for a one-sided real spectrum (i, k — real output)
- [**csnfftshift**](csnfftshift.md) - moves zero frequency to the centre of an axis (i, k — real, complex)
- [**csnifftshift**](csnifftshift.md) - restores native FFT ordering (i, k — real, complex)

The four trigonometric transforms below take their length from the array rather
than from an argument, so they accept any length: the symmetric extension each
one builds is always even, which is all the transform needs. Accuracy does not
depend on the length, only the time does.

- [**csndctone1d**](csndctone1d.md) - DCT-I along one axis (i, k — real input; real output)
- [**csndcttwo1d**](csndcttwo1d.md) - DCT-II along one axis (i, k — real input; real output)
- [**csndstone1d**](csndstone1d.md) - DST-I along one axis (i, k — real input; real output)
- [**csndsttwo1d**](csndsttwo1d.md) - DST-II along one axis (i, k — real input; real output)

The Hilbert forms take their length from the array as well, and additionally
need it even: the transform is global, so a padded length would not extend the
answer but change every sample of it, and an odd one is refused rather than
padded. They accept real input only, the analytic signal of a complex array
being undefined.

- [**csnhilbert1d**](csnhilbert1d.md) - analytic signal along one axis (i, k — real input; complex output)
- [**csnhilbert1dr**](csnhilbert1dr.md) - the Hilbert transform itself (i, k — real input; real output)
- [**csnhilbert2**](csnhilbert2.md) - two-dimensional analytic signal (i, k — real input; complex output)

## Cepstral and mel analysis

Band edges are placed on the HTK mel scale. The filterbank triangles are
evaluated at each bin's centre frequency instead of being built from rounded bin
edges, so a band narrower than the bin spacing keeps fractional weight from its
neighbours rather than collapsing. `nfft` is a power of two, as everywhere else.

- [**csnmfcc**](csnmfcc.md) - mel-frequency cepstral coefficients of a signal (i, k — real input; real output)
- [**csnmfbank**](csnmfbank.md) - triangular mel filterbank matrix (i — real output)
- [**csnmlogfbank**](csnmlogfbank.md) - the same matrix in logarithmic scale (i — real output)

## Audio features

Measures taken along an axis, one value or one curve per frame of
[csnframe](csnframe.md). The k-rate forms take a trigger and then the axis,
which they require.

- [**csnzcr**](csnzcr.md) - zero crossing rate, of a 1-D signal or along an axis, as librosa's (i, k — real only)
- [**csnamdf**](csnamdf.md) - average magnitude difference function D(tau) up to a lag, along an axis (i, k — real only)

## Convolution and correlation

The kernel is flipped for a convolution and read as it stands, conjugated, for
a correlation; that is the whole difference between the two. The `edges`
argument selects NumPy's three spans, `0` FULL, `1` SAME, `2` VALID, and both
it and the axis are i-rate on every overload, since they fix the shape of the
output. An empty kernel is refused.

- [**csnconvolve1d**](csnconvolve1d.md) - convolution with a 1-D kernel, flat or along one axis (i, k — real, complex)
- [**csncorrelate1d**](csncorrelate1d.md) - cross-correlation with a 1-D kernel, flat or along one axis (i, k — real, complex)
- [**csnconvolve**](csnconvolve.md) - N-D convolution with a kernel of the same rank (i, k — real, complex)
- [**csncorrelate**](csncorrelate.md) - N-D cross-correlation with a kernel of the same rank (i, k — real, complex)
- [**csnfftconvolve1d**](csnfftconvolve1d.md) - the same convolution through Fourier transforms (i, k — real, complex)
- [**csnfftcorrelate1d**](csnfftcorrelate1d.md) - the same cross-correlation through Fourier transforms (i, k — real, complex)
- [**csnfftconvolve**](csnfftconvolve.md) - N-D convolution through Fourier transforms (i, k — real, complex)
- [**csnfftcorrelate**](csnfftcorrelate.md) - N-D cross-correlation through Fourier transforms (i, k — real, complex)
- [**csndeconvolve1d**](csndeconvolve1d.md) - inverse of a FULL `csnconvolve1d`, flat or along one axis (i, k — real, complex)
- [**csndecorrelate1d**](csndecorrelate1d.md) - inverse of a FULL `csncorrelate1d`, flat or along one axis (i, k — real, complex)
- [**csndeconvolve**](csndeconvolve.md) - inverse of a FULL N-D `csnconvolve` (i, k — real, complex)
- [**csndecorrelate**](csndecorrelate.md) - inverse of a FULL N-D `csncorrelate` (i, k — real, complex)
- [**csnfftdeconvolve1d**](csnfftdeconvolve1d.md) - the same deconvolution through Fourier transforms (i, k — real, complex)
- [**csnfftdecorrelate1d**](csnfftdecorrelate1d.md) - the same decorrelation through Fourier transforms (i, k — real, complex)
- [**csnfftdeconvolve**](csnfftdeconvolve.md) - N-D deconvolution through Fourier transforms (i, k — real, complex)
- [**csnfftdecorrelate**](csnfftdecorrelate.md) - N-D decorrelation through Fourier transforms (i, k — real, complex)

The `csnfft*` forms answer what the direct ones answer, to within floating-point
rounding, by padding both operands to a power of two, multiplying in the
spectrum and transforming back. The direct forms cost one multiply-add per
output element per tap and win on short kernels; the transform costs `n log n`
whatever the kernel does and wins from roughly a dozen taps up. The transform
length is derived from the operands, never asked for.

The deconvolve and decorrelate forms undo the FULL span of the forward ones and
take no `edges` argument: the answer is `x - h + 1` on each axis, and the axis
is the third argument, after the trigger on the k-rate overloads. The direct
forms divide by a pivot tap, `h[0]` for a deconvolution and `conj(h[last])` for
a decorrelation, which must be non-zero; they are recursive filters, stable only
when the kernel is minimum phase (reversed, for a decorrelation). The `csnfft*`
forms divide spectra instead, have no such limit, and refuse a kernel whose
spectrum has a zero on the transform grid, such as `[1, 1]` at Nyquist.

## Interpolation and resampling

- [**csninterp**](csninterp.md) - maps values through a breakpoint table, five interpolation modes (i, k — real only)
- [**csnresample**](csnresample.md) - resamples an array to a new length along one axis (i, k — real only)
- [**csnlagrange**](csnlagrange.md) - coefficients of the Lagrange interpolating polynomial, highest degree first (i — real only)
- [**csnroots**](csnroots.md) - roots of a polynomial, one per slice along an axis, as a complex array (i — real, complex)

## Filter design

The transforms take and return a filter as zeros, poles and gain, as the
`scipy.signal` `*_zpk` functions do. Frequencies are in rad/s, the sampling
rate of `csnbilinearzpk` in Hz. The zeros may be empty; there must be at least
as many poles as zeros, and the results are always complex.

- [**csnlptolpzpk**](csnlptolpzpk.md) - moves the cutoff of a lowpass prototype, zeros-poles-gain (i — real, complex)
- [**csnlptohpzpk**](csnlptohpzpk.md) - lowpass prototype to highpass, zeros-poles-gain (i — real, complex)
- [**csnlptobpzpk**](csnlptobpzpk.md) - lowpass prototype to bandpass, zeros-poles-gain (i — real, complex)
- [**csnlptobszpk**](csnlptobszpk.md) - lowpass prototype to bandstop, zeros-poles-gain (i — real, complex)
- [**csnbilinearzpk**](csnbilinearzpk.md) - analog to digital by the bilinear transform, zeros-poles-gain (i — real, complex)
- [**csntftozpk**](csntftozpk.md) - transfer function coefficients to zeros, poles and gain (i — real only)
- [**csnzpktotf**](csnzpktotf.md) - zeros, poles and gain to transfer function coefficients (i — real, complex)
- [**csnlptolp**](csnlptolp.md) - moves the cutoff of a lowpass prototype, transfer-function coefficients (i — real, complex)
- [**csnlptohp**](csnlptohp.md) - lowpass prototype to highpass, transfer-function coefficients (i — real, complex)
- [**csnlptobp**](csnlptobp.md) - lowpass prototype to bandpass, transfer-function coefficients (i — real, complex)
- [**csnlptobs**](csnlptobs.md) - lowpass prototype to bandstop, transfer-function coefficients (i — real, complex)
- [**csnzpktosos**](csnzpktosos.md) - zeros, poles and gain to second-order sections (i — real, complex)
- [**csnbuttap**](csnbuttap.md) - analog Butterworth lowpass prototype, zeros-poles-gain (i — complex output)
- [**csnbutterba**](csnbutterba.md) - digital Butterworth lowpass, highpass, bandpass or bandstop, transfer-function coefficients (i — real only)
- [**csnbuttersos**](csnbuttersos.md) - digital Butterworth lowpass, highpass, bandpass or bandstop, second-order sections (i — real only)
- [**csncheby1ba**](csncheby1ba.md) - digital Chebyshev type I lowpass, highpass, bandpass or bandstop, transfer-function coefficients (i — real only)
- [**csncheby1sos**](csncheby1sos.md) - digital Chebyshev type I lowpass, highpass, bandpass or bandstop, second-order sections (i — real only)
- [**csncheby2ba**](csncheby2ba.md) - digital Chebyshev type II lowpass, highpass, bandpass or bandstop, transfer-function coefficients (i — real only)
- [**csncheby2sos**](csncheby2sos.md) - digital Chebyshev type II lowpass, highpass, bandpass or bandstop, second-order sections (i — real only)
- [**csnellipba**](csnellipba.md) - digital elliptic lowpass, highpass, bandpass or bandstop, transfer-function coefficients (i — real only)
- [**csnellipsos**](csnellipsos.md) - digital elliptic lowpass, highpass, bandpass or bandstop, second-order sections (i — real only)
- [**csnlfilter**](csnlfilter.md) - filters an array along an axis, or an audio signal, with b / a (i, k, a — real, complex)
- [**csnsosfilter**](csnsosfilter.md) - filters an array along an axis, or an audio signal, with second-order sections (i, k, a — real, complex)
- [**csnzlfilter**](csnzlfilter.md) - csnlfilter from a given state zi, returning the final state zf (i, k, a — real, complex)
- [**csnzsosfilter**](csnzsosfilter.md) - csnsosfilter from a given state zi, returning the final state zf (i, k, a — real, complex)
- [**csnrtbutter**](csnrtbutter.md) - real-time digital Butterworth lowpass, highpass, bandpass or bandstop on audio, k-rate cutoff or band (a — real only)
- [**csnrtcheby1**](csnrtcheby1.md) - real-time digital Chebyshev type I lowpass, highpass, bandpass or bandstop on audio, k-rate cutoff or band (a — real only)
- [**csnrtcheby2**](csnrtcheby2.md) - real-time digital Chebyshev type II lowpass, highpass, bandpass or bandstop on audio, k-rate cutoff or band (a — real only)
- [**csnrtellip**](csnrtellip.md) - real-time digital elliptic lowpass, highpass, bandpass or bandstop on audio, k-rate cutoff or band (a — real only)

## Windows

- [**csnhanning**](csnhanning.md) - Hann window (i, k — real only)
- [**csnhamming**](csnhamming.md) - Hamming window (i, k — real only)
- [**csnbartlett**](csnbartlett.md) - Bartlett (triangular) window (i, k — real only)
- [**csnblackman**](csnblackman.md) - Blackman window (i, k — real only)
- [**csnkaiser**](csnkaiser.md) - Kaiser window with a beta parameter (i, k — real only)

## Coordinate systems

Conversions between cartesian coordinates and the polar, cylindrical and
spherical systems, each pair named for its own so nothing depends on how many
arguments were passed. The spherical order is `(r, theta, phi)` with `theta` the
inclination from `+z`, and both directions of a pair use it, so a conversion and
its inverse return the point they started from. An optional trailing flag reads
`0` for radians, the default, and `1` for degrees, on whichever side of the
conversion carries the angles.

- [**csnpoltocar**](csnpoltocar.md) - polar to cartesian, in the plane (i, k — real only)
- [**csncartopol**](csncartopol.md) - cartesian to polar, in the plane (i, k — real only)
- [**csncyltocar**](csncyltocar.md) - cylindrical to cartesian, the height carried through (i, k — real only)
- [**csncartocyl**](csncartocyl.md) - cartesian to cylindrical (i, k — real only)
- [**csnsphtocar**](csnsphtocar.md) - spherical to cartesian (i, k — real only)
- [**csncartosph**](csncartosph.md) - cartesian to spherical (i, k — real only)
- [**csnhoatocar**](csnhoatocar.md) - ambisonics direction to cartesian, elevation from the horizon (i, k — real only)
- [**csncartohoa**](csncartohoa.md) - cartesian to ambisonics direction (i, k — real only)
- [**csnrotmat**](csnrotmat.md) - 3 x 3 rotation matrix, about a basis axis or an arbitrary direction (i, k — real only)
- [**csnrotmatypr**](csnrotmatypr.md) - one 3 x 3 matrix composing a yaw, a pitch and a roll (i, k — real only)
- [**csnnmtoacn**](csnnmtoacn.md) - ACN channel index from an order and a degree (i, k — real only)
- [**csnacntonm**](csnacntonm.md) - the order and degree an ACN index stands for (i, k — real only)
- [**csnhoaordtochnls**](csnhoaordtochnls.md) - channels in a complete 3-D set of a given order (i, k — real only)
- [**csnchnlstohoaord**](csnchnlstohoaord.md) - the order a channel count stands for, perfect squares only (i, k — real only)
- [**csnsn3dton3d**](csnsn3dton3d.md) - per-channel gains from SN3D to N3D, indexed by ACN (i — real only)
- [**csnn3dtosn3d**](csnn3dtosn3d.md) - per-channel gains from N3D to SN3D, indexed by ACN (i — real only)

## Special functions

Written from their recurrences, since math.h has none of them. Neither carries
the Condon-Shortley phase, and the harmonics are the real ones of the AmbiX
convention: ACN order, SN3D, no global `1/sqrt(4 pi)`, with the direction read
as `csnhoatocar` reads it.

- [**csnlegendre**](csnlegendre.md) - associated Legendre function P_n^m(x), scalar or elementwise over an array (i, k — real only)
- [**csnsphharm**](csnsphharm.md) - one real spherical harmonic at one direction (i, k — real only)
- [**csnsphharmacn**](csnsphharmacn.md) - every harmonic up to an order by ACN, at one direction or as a channels x directions matrix (i, k — real only)

## Room acoustics

Estimates a designer works with before there is any audio. In every one of these
the operands may be scalars or arrays: `csnt60sab` and `csnt60eyr` answer one
time per volume, while `csnrt60absp` and `csnfschrd` pair every volume with
every target when both sides are arrays, giving a `volumes x targets` matrix,
and `csnt60tofbg` / `csnfbgtot60` pair delays with target times or gains the
same way.

- [**csnt60sab**](csnt60sab.md) - Sabine reverberation time from a volume and its absorbing surfaces (i, k — real only)
- [**csnt60eyr**](csnt60eyr.md) - Eyring-Norris reverberation time, the model that still holds in an absorbent room (i, k — real only)
- [**csnrt60absp**](csnrt60absp.md) - the absorption a room needs to reach a target reverberation time (i, k — real only)
- [**csnfschrd**](csnfschrd.md) - Schroeder frequency, the crossover between the modal and diffuse regions (i, k — real only)
- [**csnfpqr**](csnfpqr.md) - resonant frequency of a rectangular room for one modal index triple (i, k — real only)
- [**csnt60tofbg**](csnt60tofbg.md) - the feedback gain a comb of a given delay needs to decay by 60 dB in a given time (i, k — real only)
- [**csnfbgtot60**](csnfbgtot60.md) - the decay time of a comb of a given delay at a given feedback gain (i, k — real only)

## Levels and time conversion

The sample rate is an argument rather than the orchestra's, and is init-time on
every overload including the k-rate ones.

- [**csndbsum**](csndbsum.md) - sums levels in dB by adding their powers, over a pair, an array, or one axis (i, k — real only)
- [**csnsamptomillis**](csnsamptomillis.md) - sample counts into milliseconds at a given rate (i, k — real only)
- [**csnsamptosec**](csnsamptosec.md) - sample counts into seconds at a given rate (i, k — real only)
- [**csnmillistosamp**](csnmillistosamp.md) - milliseconds into sample counts at a given rate (i, k — real only)
- [**csnsectosamp**](csnsectosamp.md) - seconds into sample counts at a given rate (i, k — real only)

## Audio bridge

Performance-time only, on the audio path. The frame size in `csnsnap` and
`csnstream` is independent of `ksmps`; their hop must be at least `ksmps`, since
one `CsnArr` can publish one frame per control period. The optional trailing `irt`
defaults to 1 and marks the array as a real-time path, forbidding reallocation
during performance for it and everything derived from it; 0 lifts the
restriction for the derived arrays. `csnrtlock` sets the same mark on any
array, for chains that run under a deadline without touching audio;
`csnrtunlock` clears it on a selected branch. Both have init and triggered
k-rate forms, and affect only arrays created from the source after the change.

- [**csnfromaudio**](csnfromaudio.md) - one control period of an audio signal into an array (a — real only)
- [**csntoaudio**](csntoaudio.md) - an array of ksmps elements back out as audio (a — real only)
- [**csnpack**](csnpack.md) - an array of audio signals into one channels x ksmps array (a — real only)
- [**csnunpack**](csnunpack.md) - that array back into one signal per channel (a — real only)
- [**csnsnap**](csnsnap.md) - slices a stream into overlapping frames of a chosen size (a — real only)
- [**csnstream**](csnstream.md) - overlap-adds frames back into a continuous signal (a — real only)
- [**csnrtlock**](csnrtlock.md) - marks any array as a real-time path (i, k — real, complex, string)
- [**csnrtunlock**](csnrtunlock.md) - clears the real-time mark from one array (i, k — real, complex, string)
- [**csnrtlockstart**](csnrtlockstart.md) - starts marking every array the current note creates (i, k)
- [**csnrtlockend**](csnrtlockend.md) - stops that marking; the note ending stops it too (i, k)
- [**csnrtlockall**](csnrtlockall.md) - marks every array for the whole performance; orchestra header only, and there is no way to switch it off (i)
