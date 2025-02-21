---
title: "Spool"
---
# Spool
Spool is a **dynamically typed, interpreted** programming language written in [Rust](https://rust-lang.org).
It has no specific goal, other than for me to learn how interpreted languages work.

## Roadmap
- [x] Mathematical expressions
- [x] Code blocks
- [x] CLI
- [ ] Primitive types
  - [x] Strings
  - [x] Integers[<sup>1</sup>](#notes)
  - [x] Floats[<sup>1</sup>](#notes)
  - [ ] Booleans
- [x] Functions
- [ ] Bindings
  - [x] Binding definitions
  - [ ] Mutability
- [ ] File interpreter
- [ ] Standard library
- [ ] Interpreter intrinsics
- [ ] Order of operations
- [ ] Custom types (a.k.a. Structs)

## Installation
You can either download the installation script or
```sh
curl --proto "=https" -fsSL --output installer.sh "https://sunkenpotato.com/spool/installer"
chmod +x installer.sh
./installer.sh
```

<hr>

### Notes
1. Spool currently internally only uses rusts `f32` to store both integers and floats
