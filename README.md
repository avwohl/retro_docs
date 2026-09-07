# retro_docs

A collection of vintage computer manuals as PDF files and text conversions. It
covers CP/M, MP/M II, Z80, 8008, MACRO-80, PL/M-80, and Microsoft BASIC, and it
supplies reference material for the related emulator and compiler projects.

The archive holds 64 files in approximately 299 MB. Each top-level directory has
the name of the project that uses the documents in it. The documents are primary
sources. They are the manuals that the projects implement. They are not
documentation of the projects themselves.

`s100_ports` is the one exception to both rules. It is named for a subject, not a
project, and it holds a compilation rather than a scan. The section on it below
says what it is and where its facts come from.

## What is here

| Directory | Supports | Contents |
|---|---|---|
| `cpmemu` | [cpmemu](https://github.com/avwohl/cpmemu) | The Zilog Z80 manual, the CP/M 2.2 BDOS and BIOS call lists, the FCB layout, the CP/M 2.2 memory map, the 8080 instruction encoding, and a guide to a CP/M port |
| `mbasic` | [mbasic](https://github.com/avwohl/mbasic) | The Microsoft BASIC Compiler manual of 1980, the BASIC-80 reference manual, and notes on string garbage collection |
| `mbasic2025` | [mbasic2025](https://github.com/avwohl/mbasic2025) | Altair BASIC of 1975 and the Altair 8800 BASIC reference manual of July 1977 |
| `mpm2` | [mpm2](https://github.com/avwohl/mpm2) | The MP/M II System Implementor's Guide of August 1982, the user guide, the programmer's guide, and a summary |
| `s100_ports` | — | A catalogue of Altair and S-100 I/O port assignments, with the scripts that build it. See the section that follows. |
| `scelbal` | [scelbal](https://github.com/avwohl/scelbal) | The SCELBAL book, the strings supplement, update issues 1 through 6, and the Intel 8008 manual of April 1972 |
| `uada80` | [uada80](https://github.com/avwohl/uada80) | The Ada reference manuals for Ada 2012 and Ada 2022. For the CP/M 2.2 call lists, see `cpmemu`. |
| `um80_and_friends` | [um80_and_friends](https://github.com/avwohl/um80_and_friends) | The Microsoft MACRO-80 manuals: the M80 assembler, the L80 linker, the CREF and LIB utilities, and 8080 assembly language |
| `uplm80` | [uplm80](https://github.com/avwohl/uplm80) | The Intel PL/M-80 programming manuals and the CP/M source listings. See the section that follows. |
| `z80cpmw` | [z80cpmw](https://github.com/avwohl/z80cpmw) | The Cromemco Dazzler manual of 1979 |

## The `s100_ports` directory

This directory is a compilation, not a scan. It lists the I/O port assignments of
MITS Altair factory boards and of the third-party S-100 cards that Altair-era
systems used: serial terminal, printer, floppy, hard disk and support boards.

Read `Altair_S100_Port_Assignments.md`. The same data is in
`Altair_S100_Port_Assignments.xlsx` for filtering.

Both files are generated. `ports_data.py` is the source of truth, and
`build.py` rebuilds the two outputs from it. Edit the data file, never the
outputs, or the two will disagree. The directory `README.md` gives the steps.

Almost nothing on the S-100 bus had a fixed address. Boards decoded their port
range with jumpers or a DIP switch. Every entry is therefore a documented factory
default or a de-facto standard, which is the setting that software expected to
find. It is not a hard-wired fact, and a given machine may differ.

Each entry carries the source it came from and a confidence value. `High` means a
manufacturer manual, or two independent emulator implementations that agree.
`Unverified` means the board is listed but no address was confirmed. Those
entries are left blank on purpose. A plausible wrong address is worse than an
admitted gap.

## The `uplm80` directory

This directory holds 193 MB, which is most of the archive. It has three parts.

| Path | Contents |
|---|---|
| `uplm80/PLM80/` | The Intel PL/M-80 programming manual, in two scans, with text conversions |
| `uplm80/CPM_source_1.3/` | Scanned listings of the CP/M 1.3 source code, in 15 files |
| `uplm80/CPM_source_2.0/` | A scan of the CP/M 2.0 source code |

`CPM_source_1.3` has one file for each part of the system, in the order that the
original listing uses:

```
00_cover      01_license    02_boot       03_CCP        04_BDOS
05_BIOS       06_ASM        07_SYSGEN     08_ED         09_STAT
10_DDT        11_DDT_UTILS  12_PIP        13_SUBMIT     disassembly
```

These listings are the reference for the PL/M-80 compiler. The compiler rebuilds
the original CP/M utilities from their PL/M-80 source code, and these scans show
what the output must agree with.

## Text conversions

Some PDF files have a `.txt` file with the same name. The text file is a
conversion of the PDF. A text file is easy to search, and a program can read it.

The conversions are automatic. They can contain errors, and the page layout is
lost. **Always use the PDF as the authority.** Use the text file only to find a
page.

The archive has text conversions for these documents:

- The Z80 manual
- The 8080 instruction encoding
- The CP/M port guide
- The BASIC-80 reference manual
- The Microsoft BASIC Compiler manual
- The SCELBAL book and its strings supplement
- Both PL/M-80 manuals

## Documents that more than one project uses

Some documents apply to more than one project. Each such document is in the
archive one time only, in the directory of the project that uses it most. The
table shows where to find them.

| Document | Location | Also applies to |
|---|---|---|
| CP/M 2.2 BDOS calls | `cpmemu/cpm22_bdos_calls.pdf` | `uada80` |
| CP/M 2.2 BIOS calls | `cpmemu/cpm22_bios_calls.pdf` | `uada80` |
| CP/M 2.2 memory layout | `cpmemu/cpm22_memory_layout.pdf` | `uada80` |
| BASIC-80 Reference Manual v5.21, part number AA-P226A-TV, 1981 | `mbasic/basic_ref.pdf` | `cpmemu`, `mbasicc` |

The archive held five identical pairs until 2026-08-02. Each pair is now one
file. The copies were byte-identical, thus no content is lost.

One of the five pairs was an error and not a shared document:
`mbasic_string_garbage_collection_history.pdf` had a different name from
`mbasic_string_garbage_collection.pdf` but the same contents. The archive keeps
`mbasic_string_garbage_collection.pdf`. There is no separate history document.

**A note on the size of a clone:** the delete operations remove the files from
the current tree, but git keeps them in the history. Thus a fresh clone is
approximately the same size as before. Only a rewrite of the history can make a
clone smaller, and that changes every commit ID.

## Provenance

These are scans of manuals from Digital Research, Intel, Microsoft, Zilog,
Cromemco, and SCELBI. Most of the documents are more than 40 years old, and many
of the companies no longer operate.

The documents are here as reference material for the emulator and compiler
projects that this account holds. The scans came from public retro-computing
archives. This repository does not add a license to them, and it does not make a
statement about their copyright status. The copyright of each document stays with
its owner.

If you own the rights to a document here, open an issue. I will remove the
document.

## Related Projects

- [cpmemu](https://github.com/avwohl/cpmemu) - Z80/CP/M emulator for Linux and Windows, with Z80 and 8080 CPU cores. It translates the BDOS and BIOS calls of CP/M 2.2 programs to the host file system.
- [mbasic](https://github.com/avwohl/mbasic) - Python interpreter for MBASIC 5.21, the Microsoft BASIC-80 for CP/M. Two compiler backends compile the programs to CP/M .COM files or to JavaScript.
- [mbasic2025](https://github.com/avwohl/mbasic2025) - Reconstruction of the lost source code of MBASIC 5.21, the Microsoft BASIC-80 for CP/M. The MACRO-80 source code assembles to a binary that matches mbasic.com byte for byte.
- [mpm2](https://github.com/avwohl/mpm2) - Z80 emulator for MP/M II, the multi-user CP/M operating system. Users connect over SSH, and SFTP clients transfer files.
- [scelbal](https://github.com/avwohl/scelbal) - Floating-point BASIC interpreter for the 8080 processor and CP/M. A translator converts the original 8008 source code to 8080 source code.
- [uada80](https://github.com/avwohl/uada80) - Ada compiler for the Z80 processor and CP/M 2.2. It compiles a subset of Ada 2012 to CP/M .COM files.
- [um80_and_friends](https://github.com/avwohl/um80_and_friends) - Linux toolchain that is compatible with Microsoft MACRO-80. It has an assembler, a linker, a librarian, and a disassembler.
- [uplm80](https://github.com/avwohl/uplm80) - PL/M-80 compiler for the Z80 processor and CP/M. It writes Intel 8080 and Zilog Z80 assembly language.
- [z80cpmw](https://github.com/avwohl/z80cpmw) - Z80/CP/M emulator for Windows. It emulates the RomWBW HBIOS interface and boots CP/M from disk images.
