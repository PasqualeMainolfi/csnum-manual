# Requirements

- **Csound 7** (API 7.0). The plugin is not built for Csound 6: the opcodes rely
  on Csound 7 user-defined types for `CsnArr` and complex arguments.
- `[]` on `CsnArr` (`v[i][j]`, `v[start:end]`) needs Csound 7.0, which lets a
  plugin type provide it (csound PR #3363). On an earlier 7.0.0 beta,
  `csnget`, `csnset` and `csngetslice` do the same work.
- A C11 compiler and CMake ≥ 3.16.
