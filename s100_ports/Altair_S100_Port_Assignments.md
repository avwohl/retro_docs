# Altair / S-100 Bus I/O Port Assignments

MITS Altair factory hardware and third-party S-100 cards — serial, printer, floppy, hard disk and support boards.

*Compiled 2026-09-07. Also available as a spreadsheet: `Altair_S100_Port_Assignments.xlsx`.*

---

## Read this first

**Almost nothing on the S-100 bus had a fixed address.** Boards decoded their port range with jumpers or a DIP
switch, so the addresses below are *documented factory defaults and de-facto standards* — the settings software
expected to find — not hard-wired facts. Any given machine may differ. Where a board's address really is fixed,
the Addressing line says so.

**MITS documented ports in octal**, and so did most Altair-era software listings. The 88-2SIO console at
`0x10`/`0x11` is "port 20 and 21" in every MITS manual. All three radixes are given on every row so you can read
a period listing without converting in your head.

**Confidence** — `High` = stated in a manufacturer manual, or agreed on by two independent emulator
implementations. `Medium-High` = one strong source. `Medium` = one source, or a documented conflict between
sources. `Unverified` = the board is listed for completeness but no address was confirmed; those rows are
deliberately left blank rather than guessed at.

**Coverage** — this covers the manufacturers whose cards you actually meet in Altair-era systems. Several hundred
S-100 boards were made in total, and a long tail of them — mostly memory, prototyping and one-off cards — is not
represented here.

## Quick reference

| Function | Altair (MITS) | Common third-party |
| --- | --- | --- |
| **Terminal serial** | `0x10`/`0x11` (88-2SIO)<br>`0x00`/`0x01` (88-SIO) | `0x10`–`0x17` CompuPro Interfacer 3/4<br>`0x02`–`0x05` IMSAI SIO-2<br>`0x20`/`0x50`/`0x60`/`0x70`/`0x80` Cromemco TU-ART |
| **Printer** | `0x02`/`0x03` (88-LPC) | on-board serial on many disk controllers |
| **Floppy** | `0x08`/`0x09`/`0x0A` (88-DCDD) | `0xF8`–`0xFC` Tarbell 1011<br>`0x30`–`0x34` Cromemco 4/16/64FDC<br>`0xC0`–`0xC3` CompuPro Disk 1A<br>`0xFD` IMSAI FIF |
| **Hard disk** | `0xA0`–`0xA7` (88-HDSK, via an 88-4PIO) | `0xC8` CompuPro Disk 2<br>`0x90` Viasyn Disk 3<br>`0x54` Morrow HDC-DMA<br>`0xE0`–`0xE7` ADC HDC-1001 |
| **Interrupts / clock** | `0xFE` (88-VI/RTC) | `0x50`–`0x5F` CompuPro System Support 1 |
| **Sense switches** | `0xFF` | `0xFF` on the Sol-20 too |

> [!IMPORTANT]
> Two collisions that will bite you. The 88-4PIO manual's own worked example is 020–037 octal = `0x10`–`0x1F`,
> sitting directly on the standard 88-2SIO console. And `0xFD` is claimed by both the IMSAI FIF and the Tarbell
> 2022. Cromemco's timers at `0x05`–`0x09` also overlap the 88-DCDD floppy controller.

---

## Contents

**[MITS Altair boards](#mits-altair-boards)**

- *MITS* — [88-SIO](#88-sio--mits), [88-LPC (line printer interface)](#88-lpc-line-printer-interface--mits), [88-ACR (audio cassette)](#88-acr-audio-cassette--mits), [88-DCDD / 88-DISK](#88-dcdd--88-disk--mits), [88-2SIO](#88-2sio--mits), [88-2SIO (second board)](#88-2sio-second-board--mits), [88-4PIO](#88-4pio--mits), [88-HDSK (Altair hard disk)](#88-hdsk-altair-hard-disk--mits), [88-VI/RTC](#88-virtc--mits), [Altair 8800 front panel](#altair-8800-front-panel--mits)

**[Third-party cards](#third-party-cards)**

- *Tarbell Electronics* — [1011 / 1011A FDC (single density)](#1011--1011a-fdc-single-density--tarbell-electronics), [2022 FDC (double density)](#2022-fdc-double-density--tarbell-electronics), [2022 FDC - 8257 DMA controller](#2022-fdc---8257-dma-controller--tarbell-electronics), [1001 cassette interface](#1001-cassette-interface--tarbell-electronics)
- *Cromemco* — [4FDC / 16FDC / 64FDC (and CCS 2422)](#4fdc--16fdc--64fdc-and-ccs-2422--cromemco), [16FDC / 64FDC](#16fdc--64fdc--cromemco), [TU-ART (console)](#tu-art-console--cromemco), [TU-ART #1 port A](#tu-art-1-port-a--cromemco), [TU-ART #1 port B](#tu-art-1-port-b--cromemco), [TU-ART #2 port A](#tu-art-2-port-a--cromemco), [TU-ART #2 port B](#tu-art-2-port-b--cromemco), [TU-ART #3 port A](#tu-art-3-port-a--cromemco), [Dazzler](#dazzler--cromemco), [D+7A I/O with JS-1 joystick console](#d7a-io-with-js-1-joystick-console--cromemco), [Octart](#octart--cromemco)
- *IMSAI* — [SIO-2 channel A (TTY)](#sio-2-channel-a-tty--imsai), [SIO-2 channel B (CRT / keyboard)](#sio-2-channel-b-crt--keyboard--imsai), [FIF floppy controller](#fif-floppy-controller--imsai)
- *Processor Technology* — [Sol-20 (built-in I/O)](#sol-20-built-in-io--processor-technology), [VDM-1](#vdm-1--processor-technology), [3P+S](#3ps--processor-technology)
- *CompuPro (Godbout)* — [Interfacer 3 / Interfacer 4](#interfacer-3--interfacer-4--compupro-godbout), [System Support 1](#system-support-1--compupro-godbout), [Disk 1 / Disk 1A](#disk-1--disk-1a--compupro-godbout), [Disk 2](#disk-2--compupro-godbout), [Selector Channel](#selector-channel--compupro-godbout), [M-Drive/H](#m-driveh--compupro-godbout)
- *Viasyn / CompuPro* — [Disk 3](#disk-3--viasyn--compupro)
- *Morrow Designs* — [Disk Jockey 2D (models A and B)](#disk-jockey-2d-models-a-and-b--morrow-designs), [Disk Jockey HDC-DMA](#disk-jockey-hdc-dma--morrow-designs)
- *North Star* — [MDS-A / MDS-AD (Micro Disk System)](#mds-a--mds-ad-micro-disk-system--north-star), [Horizon motherboard I/O](#horizon-motherboard-io--north-star)
- *Advanced Digital Corp.* — [HDC-1001](#hdc-1001--advanced-digital-corp), [Super Six SBC](#super-six-sbc--advanced-digital-corp)
- *Jade Computer Products* — [Double D](#double-d--jade-computer-products)
- *iCOM* — [FD3712 / FD3812](#fd3712--fd3812--icom)
- *Micropolis* — [FD controller (MDSK)](#fd-controller-mdsk--micropolis)
- *Vector Graphic / Micropolis* — [FD-HD controller (VFDHD)](#fd-hd-controller-vfdhd--vector-graphic--micropolis)
- *Vector Graphic* — [Flashwriter II](#flashwriter-ii--vector-graphic)
- *Seattle Computer Products* — [SCP-300F support board](#scp-300f-support-board--seattle-computer-products)
- *PMMI Communications* — [MM-103 modem](#mm-103-modem--pmmi-communications)
- *D.C. Hayes* — [80-103A / Micromodem 100](#80-103a--micromodem-100--dc-hayes)
- *XComp* — [Hard disk controller](#hard-disk-controller--xcomp)
- *SD Systems* — [VersaFloppy I / II](#versafloppy-i--ii--sd-systems)

**[Port map, `0x00`–`0xFF`](#port-map-0x000xff)** · **[Memory-mapped controllers](#memory-mapped-controllers)** · **[Sources](#sources)**

---

## MITS Altair boards

### 88-SIO — MITS

*Serial* &nbsp;·&nbsp; **Addressing:** Jumper: any even octal address 000-376 (2 consecutive ports; A0 selects control vs data) &nbsp;·&nbsp; **Confidence:** High

> The de-facto first serial port on early Altairs. 4K/8K BASIC picks SIO at 0/1 vs 2SIO at 10/11 from sense switch SW11.

| Port (hex) | Dec | Octal | R/W | Function |
| --- | --- | --- | --- | --- |
| `0x00` | 0 | 000 | R | Status: bit 0 = transmitter buffer empty, bit 1 = receive data available (flags are active-low in hardware) |
| `0x00` | 0 | 000 | W | Control: interrupt enable / reset |
| `0x01` | 1 | 001 | R | Received data |
| `0x01` | 1 | 001 | W | Transmit data |

<sub>Source: MITS 88-SIO manual (Theory of Operation); Altair8800 simulator serial.cpp; SIMH</sub>

### 88-LPC (line printer interface) — MITS

*Printer* &nbsp;·&nbsp; **Addressing:** Fixed by convention &nbsp;·&nbsp; **Confidence:** Medium-High

> Serves the 88-LP Okidata printer and the Centronics 700/701/703. Used by Altair BASIC LINEPRINTER and by CP/M as LST:.

| Port (hex) | Dec | Octal | R/W | Function |
| --- | --- | --- | --- | --- |
| `0x02` | 2 | 002 | R | Printer status (busy / ready) |
| `0x02` | 2 | 002 | W | Printer control |
| `0x03` | 3 | 003 | W | Printer data |

<sub>Source: Altair 8800 Simulator (dhansel/Altair8800) io.cpp + device sources</sub>

### 88-ACR (audio cassette) — MITS

*Cassette* &nbsp;·&nbsp; **Addressing:** Jumper (SIO-style), standard 006/007 octal &nbsp;·&nbsp; **Confidence:** High

> 300 baud Kansas City standard. The ACR is an 88-SIO-type serial interface strapped to 006/007 plus a modulator/demodulator board. CSAVE/CLOAD in Extended BASIC use it.

| Port (hex) | Dec | Octal | R/W | Function |
| --- | --- | --- | --- | --- |
| `0x06` | 6 | 006 | R | Status: transmit buffer empty / receive data available |
| `0x06` | 6 | 006 | W | Control |
| `0x07` | 7 | 007 | R | Data read from tape |
| `0x07` | 7 | 007 | W | Data written to tape |

<sub>Source: SIMH AltairZ80 + Altair 8800 Simulator (independent implementations agree)</sub>

### 88-DCDD / 88-DISK — MITS

*Floppy* &nbsp;·&nbsp; **Addressing:** Fixed at 8/9/0A by MITS convention &nbsp;·&nbsp; **Confidence:** High

> 8-inch floppy controller (Pertec FD-400 mechanism). Programmed I/O only: no interrupts, no DMA, so a transfer holds the CPU. The 88-MDS minidisk (5.25-inch) uses the same three ports.

| Port (hex) | Dec | Octal | R/W | Function |
| --- | --- | --- | --- | --- |
| `0x08` | 8 | 010 | R | Drive status flags: b0 ENWD (ready to write), b1 head-move OK, b2 head loaded, b6 track 0, b7 NRDA (new read data available). Flags are INVERTED on the bus (0 = true). |
| `0x08` | 8 | 010 | W | Drive select / enable: b0-b3 = drive 0-15, b7 = disable controller (deselect) |
| `0x09` | 9 | 011 | R | Sector position register: b0 = sector true, b1-b5 = sector number (0-31) |
| `0x09` | 9 | 011 | W | Drive control: b0 step in, b1 step out, b2 head load, b3 head unload, b4 interrupt enable, b5 interrupt disable, b7 write enable |
| `0x0A` | 10 | 012 | R | Read data |
| `0x0A` | 10 | 012 | W | Write data |

<sub>Source: SIMH AltairZ80 + Altair 8800 Simulator (independent implementations agree); SIMH AltairZ80 documentation (altairz80_doc.pdf)</sub>

### 88-2SIO — MITS

*Serial* &nbsp;·&nbsp; **Addressing:** Jumper; MITS standard is 10-13 hex &nbsp;·&nbsp; **Confidence:** High

> THE canonical Altair console port. Built on the Motorola MC6850 ACIA. Baud rate jumper-selectable 110-9600 per port.
>
> Port 2 commonly drove the paper-tape reader/punch, and later a printer. SIMH exposes it as the PTR/PTP device.

| Port (hex) | Dec | Octal | R/W | Function |
| --- | --- | --- | --- | --- |
| `0x10` | 16 | 020 | R | Port 1 ACIA status: b0 receive data register full, b1 transmit data register empty, b2 DCD, b3 CTS, b7 IRQ |
| `0x10` | 16 | 020 | W | Port 1 ACIA control: counter divide / master reset, word select, transmit control, receive interrupt enable |
| `0x11` | 17 | 021 | R | Port 1 receive data |
| `0x11` | 17 | 021 | W | Port 1 transmit data |
| `0x12` | 18 | 022 | R/W | Port 2 ACIA status (R) / control (W) |
| `0x13` | 19 | 023 | R/W | Port 2 receive data (R) / transmit data (W) |

<sub>Source: SIMH AltairZ80 documentation (altairz80_doc.pdf); SIMH AltairZ80 + Altair 8800 Simulator (independent implementations agree)</sub>

### 88-2SIO (second board) — MITS

*Serial* &nbsp;·&nbsp; **Addressing:** Jumper &nbsp;·&nbsp; **Confidence:** Medium-High

> Common strapping when a second dual-serial board is fitted.

| Port (hex) | Dec | Octal | R/W | Function |
| --- | --- | --- | --- | --- |
| `0x14`–`0x17` | 20–23 | 024–027 | R/W | Second 88-2SIO board: port 1 at 14/15, port 2 at 16/17 |

<sub>Source: Altair 8800 Simulator (dhansel/Altair8800) io.cpp + device sources</sub>

### 88-4PIO — MITS

*Parallel* &nbsp;·&nbsp; **Addressing:** Jumper, in 16-port groups: 000, 020, 040, 060, 100, 120 ... octal &nbsp;·&nbsp; **Confidence:** High

> Built from MC6820 PIAs. Occupies 16 consecutive addresses. A2/A3 select the port, A0/A1 select section and channel. The manual's worked example uses 020-037 octal (0x10-0x1F), which collides with a standard 88-2SIO - choose another group in practice.

| Port (hex) | Dec | Octal | R/W | Function |
| --- | --- | --- | --- | --- |
| `0x10`–`0x1F` | 16–31 | 020–037 | R/W | Four parallel ports, 4 addresses each. Per port n at base+4n: +0 = section A control/status, +1 = section A data or DDR (selected by control bit 2), +2 = section B control/status, +3 = section B data or DDR |

<sub>Source: MITS 88-4PIO manual, pp.5/9/27 (Address Selection Chart)</sub>

### 88-HDSK (Altair hard disk) — MITS

*Hard disk* &nbsp;·&nbsp; **Addressing:** Jumper (4PIO group at 240 octal) &nbsp;·&nbsp; **Confidence:** Medium-High

> The Altair 10 MB hard disk has no controller card of its own on the bus: it hangs off an 88-4PIO strapped to base 0xA0 (240 octal).

| Port (hex) | Dec | Octal | R/W | Function |
| --- | --- | --- | --- | --- |
| `0xA0`–`0xA3` | 160–163 | 240–243 | R/W | 88-4PIO port 1 - command channel. Section A carries command bytes, section B carries acknowledge/status. CA1/CB1 handshake lines are wired to the drive controller's CRDY and CMDACK. |
| `0xA4`–`0xA7` | 164–167 | 244–247 | R/W | 88-4PIO port 2 - data channel. CA1/CB1 carry the controller's CDA (controller data available) and ADPA (accept data) handshakes. |

<sub>Source: Altair 8800 Simulator (dhansel/Altair8800) io.cpp + device sources</sub>

### 88-VI/RTC — MITS

*Interrupt / clock* &nbsp;·&nbsp; **Addressing:** Fixed at 376 octal &nbsp;·&nbsp; **Confidence:** High

> Prioritises the eight VI lines on the Altair bus into RST vectors. Required by Altair Time-Sharing BASIC; little other commercial software used it.

| Port (hex) | Dec | Octal | R/W | Function |
| --- | --- | --- | --- | --- |
| `0xFE` | 254 | 376 | W | Vectored-interrupt level enable mask (b0-b7 enable VI0-VI7). Bit 4 also clears the real-time-clock interrupt. |

<sub>Source: MITS 88-VI(RTC) manual p.5: 'uses I/O address 254 (decimal) or 376 (octal)'</sub>

### Altair 8800 front panel — MITS

*System* &nbsp;·&nbsp; **Addressing:** Fixed &nbsp;·&nbsp; **Confidence:** High

> Universal Altair convention. Read by BASIC and by most boot ROMs to pick a console device or a boot option.

| Port (hex) | Dec | Octal | R/W | Function |
| --- | --- | --- | --- | --- |
| `0xFF` | 255 | 377 | R | Front-panel sense switches (the A8-A15 toggles) |

<sub>Source: Altair 8800 Simulator (dhansel/Altair8800) io.cpp + device sources</sub>

---

## Third-party cards

### 1011 / 1011A FDC (single density) — Tarbell Electronics

*Floppy* &nbsp;·&nbsp; **Addressing:** DIP switch; F8 is the factory/de-facto standard &nbsp;·&nbsp; **Confidence:** High

> The most widely cloned S-100 floppy controller; the address most CP/M distributions assumed. Boot PROM phantoms in at 0x0000.

| Port (hex) | Dec | Octal | R/W | Function |
| --- | --- | --- | --- | --- |
| `0xF8` | 248 | 370 | R | WD1771 status register |
| `0xF8` | 248 | 370 | W | WD1771 command register |
| `0xF9` | 249 | 371 | R/W | Track register |
| `0xFA` | 250 | 372 | R/W | Sector register |
| `0xFB` | 251 | 373 | R/W | Data register |
| `0xFC` | 252 | 374 | R | Wait / status: b7 = INTRQ (end of job) |
| `0xFC` | 252 | 374 | W | Drive select and control (drive number, side, density) |

<sub>Source: SIMH simh/AltairZ80 device sources (s100_tarbell.c); Altair 8800 Simulator (dhansel/Altair8800) io.cpp + device sources</sub>

### 2022 FDC (double density) — Tarbell Electronics

*Floppy* &nbsp;·&nbsp; **Addressing:** DIP switch &nbsp;·&nbsp; **Confidence:** High

> The DD controller is a superset of the 1011: same F8-FC plus FD, and an Intel 8257 DMA controller.

| Port (hex) | Dec | Octal | R/W | Function |
| --- | --- | --- | --- | --- |
| `0xFD` | 253 | 375 | R | DMA status |
| `0xFD` | 253 | 375 | W | Extended (DMA) address register |

<sub>Source: SIMH simh/AltairZ80 device sources</sub>

### 2022 FDC - 8257 DMA controller — Tarbell Electronics

*DMA* &nbsp;·&nbsp; **Addressing:** DIP switch &nbsp;·&nbsp; **Confidence:** Medium-High

| Port (hex) | Dec | Octal | R/W | Function |
| --- | --- | --- | --- | --- |
| `0xE0`–`0xEF` | 224–239 | 340–357 | R/W | Intel 8257 DMA controller channel and control registers |

<sub>Source: SIMH simh/AltairZ80 device sources</sub>

### 1001 cassette interface — Tarbell Electronics

*Cassette* &nbsp;·&nbsp; **Addressing:** DIP switch, any address &nbsp;·&nbsp; **Confidence:** Medium

> The board is fully DIP-switch selectable, so this is a commonly-used setting rather than a factory default. Tarbell's own manual does not name one.

| Port (hex) | Dec | Octal | R/W | Function |
| --- | --- | --- | --- | --- |
| `0x6E`–`0x6F` | 110–111 | 156–157 | R/W | Cassette interface register block - 0x6E and 0x6F are read, 0x6F is written. The source gives the addresses only; individual register functions are not documented there. |

<sub>Source: s100computers.com 'S100 Computers Port Assignements' (J. Monahan). Note this is a modern builder's list of ports he uses in his own systems, mixing vintage and present-day boards - it is not a manufacturer source.</sub>

### 4FDC / 16FDC / 64FDC (and CCS 2422) — Cromemco

*Floppy* &nbsp;·&nbsp; **Addressing:** Fixed by Cromemco convention &nbsp;·&nbsp; **Confidence:** High

> Cromemco's standard disk controller family, based on the WD1771 (4FDC) or WD1793 (16FDC/64FDC). Boot PROM (RDOS) at 0xC000.

| Port (hex) | Dec | Octal | R/W | Function |
| --- | --- | --- | --- | --- |
| `0x03` | 3 | 003 | R | Interrupt vector - returns the RST opcode for the highest pending interrupt (16FDC / 64FDC) |
| `0x03` | 3 | 003 | W | Interrupt mask |
| `0x04` | 4 | 004 | R | Status 2 - configuration DIP switches plus RTC bit |
| `0x04` | 4 | 004 | W | Auxiliary control - side select, restore, fast seek, eject, control-out |
| `0x30` | 48 | 060 | R | WD179x status register |
| `0x30` | 48 | 060 | W | WD179x command register |
| `0x31` | 49 | 061 | R/W | Track register |
| `0x32` | 50 | 062 | R/W | Sector register |
| `0x33` | 51 | 063 | R/W | Data register |
| `0x34` | 52 | 064 | R | Disk flags: b7 DRQ, b6 boot jumper, b5 head load / select request, b4 inhibit-init, b3 motor on, b2 motor timeout, b1 autowait timeout, b0 EOJ (INTRQ) |
| `0x34` | 52 | 064 | W | Disk control: b7 autowait enable, b6 double density, b5 motor on, b4 maxi (8-inch), b3-b0 drive select 4/3/2/1 |
| `0x40` | 64 | 100 | W | Bank select - any write disables the on-board boot PROM at 0xC000 |

<sub>Source: SIMH simh/AltairZ80 device sources (s100_64fdc.c)</sub>

### 16FDC / 64FDC — Cromemco

*Timer* &nbsp;·&nbsp; **Addressing:** Fixed &nbsp;·&nbsp; **Confidence:** High

> Not present on the 4FDC.

| Port (hex) | Dec | Octal | R/W | Function |
| --- | --- | --- | --- | --- |
| `0x05`–`0x09` | 5–9 | 005–011 | R/W | Five programmable interval timers (timer 1-5) |

<sub>Source: SIMH simh/AltairZ80 device sources</sub>

### TU-ART (console) — Cromemco

*Serial* &nbsp;·&nbsp; **Addressing:** DIP switch &nbsp;·&nbsp; **Confidence:** Medium-High

> Cromemco's combined serial + parallel + timer board. The console TU-ART sits at 0x00; multi-user Cromix systems add more.

| Port (hex) | Dec | Octal | R/W | Function |
| --- | --- | --- | --- | --- |
| `0x00`–`0x03` | 0–3 | 000–003 | R/W | base+0 = serial data; base+1 = status (R: TBE, RDA, interrupt pending, overrun, framing error) / command (W: reset, interrupt enable, high baud); base+2/+3 = interrupt mask and address, interval timers, parallel port |

<sub>Source: SIMH simh/AltairZ80 device sources (s100_tuart.c)</sub>

### TU-ART #1 port A — Cromemco

*Serial* &nbsp;·&nbsp; **Addressing:** DIP switch &nbsp;·&nbsp; **Confidence:** High

> Cromix multi-user switch settings.

| Port (hex) | Dec | Octal | R/W | Function |
| --- | --- | --- | --- | --- |
| `0x20`–`0x23` | 32–35 | 040–043 | R/W | Serial port A - user 2 under Cromix |

<sub>Source: Cromemco Cromix Instruction Manual (023-4022), TU-ART switch settings</sub>

### TU-ART #1 port B — Cromemco

*Serial* &nbsp;·&nbsp; **Addressing:** DIP switch &nbsp;·&nbsp; **Confidence:** High

| Port (hex) | Dec | Octal | R/W | Function |
| --- | --- | --- | --- | --- |
| `0x50`–`0x53` | 80–83 | 120–123 | R/W | Serial port B - user 3 under Cromix |

<sub>Source: Cromemco Cromix Instruction Manual (023-4022), TU-ART switch settings</sub>

### TU-ART #2 port A — Cromemco

*Serial* &nbsp;·&nbsp; **Addressing:** DIP switch &nbsp;·&nbsp; **Confidence:** High

| Port (hex) | Dec | Octal | R/W | Function |
| --- | --- | --- | --- | --- |
| `0x60`–`0x63` | 96–99 | 140–143 | R/W | Serial port A - user 4 under Cromix |

<sub>Source: Cromemco Cromix Instruction Manual (023-4022), TU-ART switch settings</sub>

### TU-ART #2 port B — Cromemco

*Serial* &nbsp;·&nbsp; **Addressing:** DIP switch &nbsp;·&nbsp; **Confidence:** High

| Port (hex) | Dec | Octal | R/W | Function |
| --- | --- | --- | --- | --- |
| `0x70`–`0x73` | 112–115 | 160–163 | R/W | Serial port B - user 5 under Cromix |

<sub>Source: Cromemco Cromix Instruction Manual (023-4022), TU-ART switch settings</sub>

### TU-ART #3 port A — Cromemco

*Serial* &nbsp;·&nbsp; **Addressing:** DIP switch &nbsp;·&nbsp; **Confidence:** High

| Port (hex) | Dec | Octal | R/W | Function |
| --- | --- | --- | --- | --- |
| `0x80`–`0x83` | 128–131 | 200–203 | R/W | Serial port A - user 6 under Cromix |

<sub>Source: Cromemco Cromix Instruction Manual (023-4022), TU-ART switch settings</sub>

### Dazzler — Cromemco

*Video* &nbsp;·&nbsp; **Addressing:** Fixed &nbsp;·&nbsp; **Confidence:** High

> The first colour graphics card for a personal computer. Display data is DMA'd from a 512-byte or 2 KB block of main memory.

| Port (hex) | Dec | Octal | R/W | Function |
| --- | --- | --- | --- | --- |
| `0x0E` | 14 | 016 | R | Status: b6 = end of frame, b7 = even line |
| `0x0E` | 14 | 016 | W | Display on/off (b7) plus the video memory start page (2 KB aligned) |
| `0x0F` | 15 | 017 | W | Format: b6 resolution x4, b5 2 KB vs 512-byte picture, b4 colour vs B/W, b3 high intensity, b2-b0 blue/green/red |

<sub>Source: SIMH simh/AltairZ80 device sources; Altair 8800 Simulator (dhansel/Altair8800) io.cpp + device sources</sub>

### D+7A I/O with JS-1 joystick console — Cromemco

*Analog I/O* &nbsp;·&nbsp; **Addressing:** Fixed &nbsp;·&nbsp; **Confidence:** Medium-High

> Used together with the Dazzler for games and instrumentation.

| Port (hex) | Dec | Octal | R/W | Function |
| --- | --- | --- | --- | --- |
| `0x18`–`0x1F` | 24–31 | 030–037 | R/W | Seven A/D input and seven D/A output channels plus a parallel port. Joystick axes and buttons read at 0x18-0x1C. |

<sub>Source: SIMH simh/AltairZ80 device sources; Altair 8800 Simulator (dhansel/Altair8800) io.cpp + device sources</sub>

### SIO-2 channel A (TTY) — IMSAI

*Serial* &nbsp;·&nbsp; **Addressing:** Jumper block, default 00-0F &nbsp;·&nbsp; **Confidence:** Medium-High

> Note the convention is the reverse of the Altair 88-2SIO: data on the EVEN port, status on the ODD port. Default decoded block is 00-0F; a second SIO-2 is usually strapped to 20-2F.

| Port (hex) | Dec | Octal | R/W | Function |
| --- | --- | --- | --- | --- |
| `0x02` | 2 | 002 | R/W | Channel A data |
| `0x03` | 3 | 003 | R/W | Channel A status / control |

<sub>Source: IMSAI CP/M System User's Guide / SIO-2 Rev 3 manual; deramp.com IMSAI notes</sub>

### SIO-2 channel B (CRT / keyboard) — IMSAI

*Serial* &nbsp;·&nbsp; **Addressing:** Jumper block &nbsp;·&nbsp; **Confidence:** Medium-High

> This is the port IMSAI's CP/M BIOS maps the CRT to.

| Port (hex) | Dec | Octal | R/W | Function |
| --- | --- | --- | --- | --- |
| `0x04` | 4 | 004 | R/W | Channel B data |
| `0x05` | 5 | 005 | R/W | Channel B status / control |

<sub>Source: IMSAI CP/M System User's Guide / SIO-2 Rev 3 manual; deramp.com IMSAI notes</sub>

### FIF floppy controller — IMSAI

*Floppy* &nbsp;·&nbsp; **Addressing:** Fixed &nbsp;·&nbsp; **Confidence:** High

> Unusual design: a single port. The CPU writes a pointer to a disk descriptor block held in main memory and the controller does the rest. Collides with the Tarbell 2022's DMA port and with SIMH's simulated HDSK.

| Port (hex) | Dec | Octal | R/W | Function |
| --- | --- | --- | --- | --- |
| `0xFD` | 253 | 375 | R | Status |
| `0xFD` | 253 | 375 | W | Command / disk-descriptor pointer |

<sub>Source: SIMH simh/AltairZ80 device sources (s100_fif.c); SIMH AltairZ80 documentation (altairz80_doc.pdf)</sub>

### Sol-20 (built-in I/O) — Processor Technology

*Serial* &nbsp;·&nbsp; **Addressing:** Fixed &nbsp;·&nbsp; **Confidence:** High

> The Sol-20 is a Sol-PC single-board S-100 machine: its I/O is on the CPU board rather than on separate cards.
>
> Confirmed by the OUT 0FEh instructions in the Sol-20 monitor ROM.

| Port (hex) | Dec | Octal | R/W | Function |
| --- | --- | --- | --- | --- |
| `0xF8` | 248 | 370 | R | Serial status: b7 TBE, b6 data ready, b5 CTS, b4 overrun, b3 framing error, b2 parity error, b1 DSR, b0 carrier detect |
| `0xF9` | 249 | 371 | R/W | Serial data |
| `0xFA` | 250 | 372 | R | General status: b7 tape TBE, b6 tape data ready, b4 tape overrun, b3 tape framing error, b2 parallel device ready, b1 parallel data ready, b0 keyboard data ready |
| `0xFB` | 251 | 373 | R/W | Tape data |
| `0xFC` | 252 | 374 | R | Keyboard data |
| `0xFD` | 253 | 375 | R/W | Parallel port data |
| `0xFE` | 254 | 376 | W | Display control - VDM beginning-of-display / scroll register, plus tape drive 1 and 2 motor control (b7/b6) |
| `0xFF` | 255 | 377 | R | Sense switches |

<sub>Source: SIMH simh/AltairZ80 device sources (sol20.c)</sub>

### VDM-1 — Processor Technology

*Video* &nbsp;·&nbsp; **Addressing:** Jumper &nbsp;·&nbsp; **Confidence:** Medium

> Display RAM is memory-mapped (see [Memory-mapped controllers](#memory-mapped-controllers)), not port-mapped; only the scroll register is a port. The address is jumper-selectable and SIMH's model defaults to 0xFE instead, so verify against your own board.

| Port (hex) | Dec | Octal | R/W | Function |
| --- | --- | --- | --- | --- |
| `0xC8` | 200 | 310 | W | Display control - beginning-of-display / scroll register |

<sub>Source: Altair 8800 Simulator (dhansel/Altair8800) io.cpp + device sources (vdm1.cpp registers 0xC8); SIMH s100_vdm1.c defaults to 0xFE</sub>

### 3P+S — Processor Technology

*Serial / Parallel* &nbsp;·&nbsp; **Addressing:** Jumper, 64 possible groups &nbsp;·&nbsp; **Confidence:** Unverified

> Jumper-selectable to any one of 64 port groups, so there is no single factory default. Frequently used as the console interface.

| Port (hex) | Dec | Octal | R/W | Function |
| --- | --- | --- | --- | --- |
| — | — | — | - | Three parallel ports and one serial port; occupies 4 consecutive addresses |

<sub>Source: 3P+S product literature (addressing described as jumper-selectable across 64 groups)</sub>

### Interfacer 3 / Interfacer 4 — CompuPro (Godbout)

*Serial* &nbsp;·&nbsp; **Addressing:** DIP switch, any multiple of 8; CompuPro default 0x10 &nbsp;·&nbsp; **Confidence:** High

> Eight-channel serial board; the base is switch-selectable to any multiple of 8, and CompuPro's own CP/M-80 and CP/M-86 default to 10-17 hex. IF3 and IF4 are software compatible and can be intermixed.

| Port (hex) | Dec | Octal | R/W | Function |
| --- | --- | --- | --- | --- |
| `0x10` | 16 | 020 | R/W | base+0: USART data (Centronics data / DIP switch read on the IF4) |
| `0x11` | 17 | 021 | R | base+1: USART status |
| `0x11` | 17 | 021 | W | base+1: SYN1/SYN2/DLE register (Centronics control on the IF4) |
| `0x12` | 18 | 022 | R/W | base+2: USART mode register (parallel data register on the IF4) |
| `0x13` | 19 | 023 | R/W | base+3: USART command register (parallel status register on the IF4) |
| `0x14` | 20 | 024 | R | base+4: transmit interrupt status |
| `0x14` | 20 | 024 | W | base+4: transmit interrupt mask |
| `0x15` | 21 | 025 | R | base+5: receive interrupt status |
| `0x15` | 21 | 025 | W | base+5: receive interrupt mask |
| `0x16` | 22 | 026 | - | base+6: not used |
| `0x17` | 23 | 027 | W | base+7: user (channel) select register - picks which of the 8 channels the other 7 ports address |

<sub>Source: CompuPro Interfacer 4 Technical Manual (187C, May 1983), PORT MAP section</sub>

### System Support 1 — CompuPro (Godbout)

*System* &nbsp;·&nbsp; **Addressing:** DIP switch, default 0x50 &nbsp;·&nbsp; **Confidence:** High

> A single board carrying interrupt controllers, timers, a clock/calendar, an AM9511A maths processor and a serial port. Default base 0x50.

| Port (hex) | Dec | Octal | R/W | Function |
| --- | --- | --- | --- | --- |
| `0x50` | 80 | 120 | R/W | Master 8259A interrupt controller, register 0 |
| `0x51` | 81 | 121 | R/W | Master 8259A interrupt controller, register 1 |
| `0x52` | 82 | 122 | R/W | Slave 8259A interrupt controller, register 0 |
| `0x53` | 83 | 123 | R/W | Slave 8259A interrupt controller, register 1 |
| `0x54` | 84 | 124 | R/W | 8253 timer, counter 0 |
| `0x55` | 85 | 125 | R/W | 8253 timer, counter 1 |
| `0x56` | 86 | 126 | R/W | 8253 timer, counter 2 |
| `0x57` | 87 | 127 | W | 8253 timer, control word |
| `0x58` | 88 | 130 | R/W | AM9511A arithmetic processor - data |
| `0x59` | 89 | 131 | R/W | AM9511A arithmetic processor - command / status |
| `0x5A` | 90 | 132 | W | Real-time clock command |
| `0x5B` | 91 | 133 | R/W | Real-time clock data |
| `0x5C` | 92 | 134 | R/W | 8251 USART data |
| `0x5D` | 93 | 135 | R | 8251 USART status |
| `0x5E` | 94 | 136 | W | 8251 USART mode |
| `0x5F` | 95 | 137 | W | 8251 USART command |

<sub>Source: SIMH simh/AltairZ80 device sources (s100_ss1.c)</sub>

### Disk 1 / Disk 1A — CompuPro (Godbout)

*Floppy* &nbsp;·&nbsp; **Addressing:** DIP switch, default 0xC0 &nbsp;·&nbsp; **Confidence:** High

> High-performance 8-inch / 5.25-inch floppy controller with an on-board bootstrap PROM holding 8085, 8088 and 68000 boot loaders.

| Port (hex) | Dec | Octal | R/W | Function |
| --- | --- | --- | --- | --- |
| `0xC0` | 192 | 300 | R | i8272 (NEC 765) main status register |
| `0xC1` | 193 | 301 | R/W | i8272 data register |
| `0xC2` | 194 | 302 | R | Drive status register |
| `0xC2` | 194 | 302 | W | DMA address register |
| `0xC3` | 195 | 303 | W | Motor control register |

<sub>Source: SIMH simh/AltairZ80 device sources (s100_disk1a.c)</sub>

### Disk 2 — CompuPro (Godbout)

*Hard disk* &nbsp;·&nbsp; **Addressing:** DIP switch, default 0xC8 &nbsp;·&nbsp; **Confidence:** Medium-High

> 20 MB fixed-disk controller. Must be paired with the CompuPro Selector Channel for DMA.

| Port (hex) | Dec | Octal | R/W | Function |
| --- | --- | --- | --- | --- |
| `0xC8`–`0xC9` | 200–201 | 310–311 | R/W | Hard disk controller command and status |

<sub>Source: SIMH simh/AltairZ80 device sources (s100_disk2.c)</sub>

### Disk 3 — Viasyn / CompuPro

*Hard disk* &nbsp;·&nbsp; **Addressing:** DIP switch, default 0x90 &nbsp;·&nbsp; **Confidence:** Medium-High

> DMA controller driven by linked-list descriptors in memory.

| Port (hex) | Dec | Octal | R/W | Function |
| --- | --- | --- | --- | --- |
| `0x90`–`0x91` | 144–145 | 220–221 | R/W | ST-506 hard disk controller command and status |

<sub>Source: SIMH simh/AltairZ80 device sources (s100_disk3.c)</sub>

### Selector Channel — CompuPro (Godbout)

*DMA* &nbsp;·&nbsp; **Addressing:** DIP switch, default 0xF0 &nbsp;·&nbsp; **Confidence:** Medium-High

> Provides DMA for the Disk 2 hard disk controller.

| Port (hex) | Dec | Octal | R/W | Function |
| --- | --- | --- | --- | --- |
| `0xF0` | 240 | 360 | R/W | Selector Channel DMA controller |

<sub>Source: SIMH simh/AltairZ80 device sources (s100_selchan.c)</sub>

### M-Drive/H — CompuPro (Godbout)

*RAM disk* &nbsp;·&nbsp; **Addressing:** DIP switch, default 0xC6 &nbsp;·&nbsp; **Confidence:** Medium-High

> Solid-state disk of up to 4 MB.

| Port (hex) | Dec | Octal | R/W | Function |
| --- | --- | --- | --- | --- |
| `0xC6`–`0xC7` | 198–199 | 306–307 | R/W | RAM-disk data (R) / DMA address (W) and control |

<sub>Source: SIMH simh/AltairZ80 device sources (s100_mdriveh.c)</sub>

### Disk Jockey 2D (models A and B) — Morrow Designs

*Floppy* &nbsp;·&nbsp; **Addressing:** Memory address switch &nbsp;·&nbsp; **Confidence:** High

> The DJ/2D puts its WD1791 registers and an on-board serial port in the memory window behind its boot PROM. It uses no I/O ports at all.

| Port (hex) | Dec | Octal | R/W | Function |
| --- | --- | --- | --- | --- |
| — | — | — | - | Memory-mapped, not port-mapped - see [Memory-mapped controllers](#memory-mapped-controllers) |

<sub>Source: SIMH simh/AltairZ80 device sources (s100_dj2d.c)</sub>

### Disk Jockey HDC-DMA — Morrow Designs

*Hard disk* &nbsp;·&nbsp; **Addressing:** DIP switch, default 0x54 &nbsp;·&nbsp; **Confidence:** Medium-High

> Command link block is fetched from RAM at 0x0050.

| Port (hex) | Dec | Octal | R/W | Function |
| --- | --- | --- | --- | --- |
| `0x54`–`0x55` | 84–85 | 124–125 | R/W | Hard disk controller command and status |

<sub>Source: SIMH simh/AltairZ80 device sources (s100_djhdc.c)</sub>

### MDS-A / MDS-AD (Micro Disk System) — North Star

*Floppy* &nbsp;·&nbsp; **Addressing:** Memory address jumper &nbsp;·&nbsp; **Confidence:** High

> North Star deliberately put the controller in memory space. Boot by jumping to 0xE800. Single- and double-density variants use the same window.

| Port (hex) | Dec | Octal | R/W | Function |
| --- | --- | --- | --- | --- |
| — | — | — | - | Memory-mapped, not port-mapped - see [Memory-mapped controllers](#memory-mapped-controllers) |

<sub>Source: SIMH simh/AltairZ80 device sources; SIMH AltairZ80 documentation (altairz80_doc.pdf)</sub>

### Horizon motherboard I/O — North Star

*Serial / Parallel* &nbsp;·&nbsp; **Addressing:** Unknown &nbsp;·&nbsp; **Confidence:** Unverified

> The hardware is confirmed (2x 8251 USART, 2 parallel, headers for pin assignment and baud rate) but none of the sources checked gave the port numbers. Check your machine's own BIOS listing.

| Port (hex) | Dec | Octal | R/W | Function |
| --- | --- | --- | --- | --- |
| — | — | — | - | Two 8251 serial ports and two parallel ports - addresses not established in this pass |

<sub>Source: deramp.com North Star Horizon restoration notes (describes the hardware, not the addresses)</sub>

### HDC-1001 — Advanced Digital Corp.

*Hard disk* &nbsp;·&nbsp; **Addressing:** DIP switch, default 0xE0 &nbsp;·&nbsp; **Confidence:** Medium-High

> Because it uses the plain ATA task file, other task-file controllers behave the same way at this base.

| Port (hex) | Dec | Octal | R/W | Function |
| --- | --- | --- | --- | --- |
| `0xE0`–`0xE7` | 224–231 | 340–347 | R/W | Standard IDE/ATA task-file registers (data, error/features, sector count, sector number, cylinder low/high, drive-head, status/command) |

<sub>Source: SIMH simh/AltairZ80 device sources (s100_hdc1001.c)</sub>

### Super Six SBC — Advanced Digital Corp.

*System* &nbsp;·&nbsp; **Addressing:** DIP switch &nbsp;·&nbsp; **Confidence:** Medium

> Z80 single-board computer; boot ROM at 0xF000.

| Port (hex) | Dec | Octal | R/W | Function |
| --- | --- | --- | --- | --- |
| `0x03`–`0x04` | 3–4 | 003–004 | R/W | On-board control and status |

<sub>Source: SIMH simh/AltairZ80 device sources (s100_adcs6.c)</sub>

### Double D — Jade Computer Products

*Floppy* &nbsp;·&nbsp; **Addressing:** DIP switch, default 0x43 &nbsp;·&nbsp; **Confidence:** Medium-High

> The Double D carries its own Z80, memory and I/O space; the host talks to it through one port. Boot PROM at 0xF000.

| Port (hex) | Dec | Octal | R/W | Function |
| --- | --- | --- | --- | --- |
| `0x43` | 67 | 103 | R/W | Single-port command / status interface |

<sub>Source: SIMH simh/AltairZ80 device sources (s100_jadedd.c)</sub>

### FD3712 / FD3812 — iCOM

*Floppy* &nbsp;·&nbsp; **Addressing:** DIP switch, default 0xC0 &nbsp;·&nbsp; **Confidence:** Medium-High

> FD3712 is single density, FD3812 adds double density. PROM at 0xF000, buffer RAM at 0xF400.

| Port (hex) | Dec | Octal | R/W | Function |
| --- | --- | --- | --- | --- |
| `0xC0` | 192 | 300 | R/W | Command register (W) / data in (R) |
| `0xC1` | 193 | 301 | W | Data out |

<sub>Source: SIMH simh/AltairZ80 device sources (s100_icom.c)</sub>

### FD controller (MDSK) — Micropolis

*Floppy* &nbsp;·&nbsp; **Addressing:** Memory address jumper &nbsp;·&nbsp; **Confidence:** High

> Used in Micropolis and Vector Graphic systems.

| Port (hex) | Dec | Octal | R/W | Function |
| --- | --- | --- | --- | --- |
| — | — | — | - | Memory-mapped, not port-mapped - see [Memory-mapped controllers](#memory-mapped-controllers) |

<sub>Source: SIMH simh/AltairZ80 device sources (mfdc.c)</sub>

### FD-HD controller (VFDHD) — Vector Graphic / Micropolis

*Floppy / Hard disk* &nbsp;·&nbsp; **Addressing:** DIP switch, default 0xC0 &nbsp;·&nbsp; **Confidence:** Medium-High

| Port (hex) | Dec | Octal | R/W | Function |
| --- | --- | --- | --- | --- |
| `0xC0`–`0xC3` | 192–195 | 300–303 | R/W | Combined floppy and hard disk controller registers |

<sub>Source: SIMH simh/AltairZ80 device sources (vfdhd.c); SIMH AltairZ80 documentation (altairz80_doc.pdf)</sub>

### Flashwriter II — Vector Graphic

*Video* &nbsp;·&nbsp; **Addressing:** Memory address jumper &nbsp;·&nbsp; **Confidence:** High

> Memory-mapped video board used as the console in Vector Graphic systems.

| Port (hex) | Dec | Octal | R/W | Function |
| --- | --- | --- | --- | --- |
| — | — | — | - | Memory-mapped, not port-mapped - see [Memory-mapped controllers](#memory-mapped-controllers) |

<sub>Source: SIMH AltairZ80 documentation (altairz80_doc.pdf)</sub>

### SCP-300F support board — Seattle Computer Products

*System* &nbsp;·&nbsp; **Addressing:** DIP switch, default 0xF0 &nbsp;·&nbsp; **Confidence:** Medium

> Support board for SCP's 8086 systems; ROM at 0xFF800. Overlaps the Tarbell FDC range, so the two cannot coexist unmodified.

| Port (hex) | Dec | Octal | R/W | Function |
| --- | --- | --- | --- | --- |
| `0xF0`–`0xFD` | 240–253 | 360–375 | R/W | Serial ports, timers and support functions (14 consecutive ports) |

<sub>Source: SIMH simh/AltairZ80 device sources (s100_scp300f.c)</sub>

### MM-103 modem — PMMI Communications

*Modem* &nbsp;·&nbsp; **Addressing:** DIP switch &nbsp;·&nbsp; **Confidence:** Medium

> The classic S-100 originate/answer modem (MC6860). Switch-selectable; note that SIMH's model uses base 0xC0 while its own documentation text cites E0-E3, so confirm against your board.

| Port (hex) | Dec | Octal | R/W | Function |
| --- | --- | --- | --- | --- |
| `0xC0`–`0xC3` | 192–195 | 300–303 | R/W | base+0 modem control/status, base+1 UART data, base+2 UART status, base+3 rate / dial control |

<sub>Source: SIMH simh/AltairZ80 device sources (s100_pmmi.c)</sub>

### 80-103A / Micromodem 100 — D.C. Hayes

*Modem* &nbsp;·&nbsp; **Addressing:** DIP switch, default 0x80 &nbsp;·&nbsp; **Confidence:** Medium

| Port (hex) | Dec | Octal | R/W | Function |
| --- | --- | --- | --- | --- |
| `0x80`–`0x83` | 128–131 | 200–203 | R/W | Modem control/status and UART registers |

<sub>Source: SIMH simh/AltairZ80 device sources (s100_hayes.c)</sub>

### Hard disk controller — XComp

*Hard disk* &nbsp;·&nbsp; **Addressing:** DIP switch &nbsp;·&nbsp; **Confidence:** Medium

> Individual register assignments not documented in the source.

| Port (hex) | Dec | Octal | R/W | Function |
| --- | --- | --- | --- | --- |
| `0x78`–`0x7F` | 120–127 | 170–177 | R/W | Controller register block of 8 ports |

<sub>Source: s100computers.com 'S100 Computers Port Assignements' (J. Monahan). Note this is a modern builder's list of ports he uses in his own systems, mixing vintage and present-day boards - it is not a manufacturer source.</sub>

### Octart — Cromemco

*Serial* &nbsp;·&nbsp; **Addressing:** DIP switch &nbsp;·&nbsp; **Confidence:** Unverified

> Well-known board; no address confirmed from the sources checked.

| Port (hex) | Dec | Octal | R/W | Function |
| --- | --- | --- | --- | --- |
| — | — | — | - | Eight-channel serial board - addresses not established in this pass |

<sub>Source: -</sub>

### VersaFloppy I / II — SD Systems

*Floppy* &nbsp;·&nbsp; **Addressing:** DIP switch &nbsp;·&nbsp; **Confidence:** Medium

> Widely used WD179x-based controller. Note this block collides with the CompuPro System Support 1 at 0x50-0x5F and with a Cromemco TU-ART at 0x50.

| Port (hex) | Dec | Octal | R/W | Function |
| --- | --- | --- | --- | --- |
| `0x50`–`0x57` | 80–87 | 120–127 | R/W | Controller register block of 8 ports (WD179x registers plus drive and density control). The source gives the block only; individual register assignments are not documented there. |

<sub>Source: s100computers.com 'S100 Computers Port Assignements' (J. Monahan). Note this is a modern builder's list of ports he uses in his own systems, mixing vintage and present-day boards - it is not a manufacturer source.</sub>

---

## Port map, `0x00`–`0xFF`

128 of the 256 ports are claimed by at least one board in this document; **60 are claimed by more than one**.

### Contested ports

| Port | Dec | Octal | Claimed by |
| --- | --- | --- | --- |
| `0x00` | 0 | 000 | Cromemco TU-ART (console) · MITS 88-SIO |
| `0x01` | 1 | 001 | Cromemco TU-ART (console) · MITS 88-SIO |
| `0x02` | 2 | 002 | Cromemco TU-ART (console) · IMSAI SIO-2 channel A (TTY) · MITS 88-LPC (line printer interface) |
| `0x03` | 3 | 003 | Advanced Digital Corp. Super Six SBC · Cromemco 4FDC / 16FDC / 64FDC (and CCS 2422) · Cromemco TU-ART (console) · IMSAI SIO-2 channel A (TTY) · MITS 88-LPC (line printer interface) |
| `0x04` | 4 | 004 | Advanced Digital Corp. Super Six SBC · Cromemco 4FDC / 16FDC / 64FDC (and CCS 2422) · IMSAI SIO-2 channel B (CRT / keyboard) |
| `0x05` | 5 | 005 | Cromemco 16FDC / 64FDC · IMSAI SIO-2 channel B (CRT / keyboard) |
| `0x06` | 6 | 006 | Cromemco 16FDC / 64FDC · MITS 88-ACR (audio cassette) |
| `0x07` | 7 | 007 | Cromemco 16FDC / 64FDC · MITS 88-ACR (audio cassette) |
| `0x08` | 8 | 010 | Cromemco 16FDC / 64FDC · MITS 88-DCDD / 88-DISK |
| `0x09` | 9 | 011 | Cromemco 16FDC / 64FDC · MITS 88-DCDD / 88-DISK |
| `0x10` | 16 | 020 | CompuPro (Godbout) Interfacer 3 / Interfacer 4 · MITS 88-2SIO · MITS 88-4PIO |
| `0x11` | 17 | 021 | CompuPro (Godbout) Interfacer 3 / Interfacer 4 · MITS 88-2SIO · MITS 88-4PIO |
| `0x12` | 18 | 022 | CompuPro (Godbout) Interfacer 3 / Interfacer 4 · MITS 88-2SIO · MITS 88-4PIO |
| `0x13` | 19 | 023 | CompuPro (Godbout) Interfacer 3 / Interfacer 4 · MITS 88-2SIO · MITS 88-4PIO |
| `0x14` | 20 | 024 | CompuPro (Godbout) Interfacer 3 / Interfacer 4 · MITS 88-2SIO (second board) · MITS 88-4PIO |
| `0x15` | 21 | 025 | CompuPro (Godbout) Interfacer 3 / Interfacer 4 · MITS 88-2SIO (second board) · MITS 88-4PIO |
| `0x16` | 22 | 026 | CompuPro (Godbout) Interfacer 3 / Interfacer 4 · MITS 88-2SIO (second board) · MITS 88-4PIO |
| `0x17` | 23 | 027 | CompuPro (Godbout) Interfacer 3 / Interfacer 4 · MITS 88-2SIO (second board) · MITS 88-4PIO |
| `0x18` | 24 | 030 | Cromemco D+7A I/O with JS-1 joystick console · MITS 88-4PIO |
| `0x19` | 25 | 031 | Cromemco D+7A I/O with JS-1 joystick console · MITS 88-4PIO |
| `0x1A` | 26 | 032 | Cromemco D+7A I/O with JS-1 joystick console · MITS 88-4PIO |
| `0x1B` | 27 | 033 | Cromemco D+7A I/O with JS-1 joystick console · MITS 88-4PIO |
| `0x1C` | 28 | 034 | Cromemco D+7A I/O with JS-1 joystick console · MITS 88-4PIO |
| `0x1D` | 29 | 035 | Cromemco D+7A I/O with JS-1 joystick console · MITS 88-4PIO |
| `0x1E` | 30 | 036 | Cromemco D+7A I/O with JS-1 joystick console · MITS 88-4PIO |
| `0x1F` | 31 | 037 | Cromemco D+7A I/O with JS-1 joystick console · MITS 88-4PIO |
| `0x50` | 80 | 120 | CompuPro (Godbout) System Support 1 · Cromemco TU-ART #1 port B · SD Systems VersaFloppy I / II |
| `0x51` | 81 | 121 | CompuPro (Godbout) System Support 1 · Cromemco TU-ART #1 port B · SD Systems VersaFloppy I / II |
| `0x52` | 82 | 122 | CompuPro (Godbout) System Support 1 · Cromemco TU-ART #1 port B · SD Systems VersaFloppy I / II |
| `0x53` | 83 | 123 | CompuPro (Godbout) System Support 1 · Cromemco TU-ART #1 port B · SD Systems VersaFloppy I / II |
| `0x54` | 84 | 124 | CompuPro (Godbout) System Support 1 · Morrow Designs Disk Jockey HDC-DMA · SD Systems VersaFloppy I / II |
| `0x55` | 85 | 125 | CompuPro (Godbout) System Support 1 · Morrow Designs Disk Jockey HDC-DMA · SD Systems VersaFloppy I / II |
| `0x56` | 86 | 126 | CompuPro (Godbout) System Support 1 · SD Systems VersaFloppy I / II |
| `0x57` | 87 | 127 | CompuPro (Godbout) System Support 1 · SD Systems VersaFloppy I / II |
| `0x80` | 128 | 200 | Cromemco TU-ART #3 port A · D.C. Hayes 80-103A / Micromodem 100 |
| `0x81` | 129 | 201 | Cromemco TU-ART #3 port A · D.C. Hayes 80-103A / Micromodem 100 |
| `0x82` | 130 | 202 | Cromemco TU-ART #3 port A · D.C. Hayes 80-103A / Micromodem 100 |
| `0x83` | 131 | 203 | Cromemco TU-ART #3 port A · D.C. Hayes 80-103A / Micromodem 100 |
| `0xC0` | 192 | 300 | CompuPro (Godbout) Disk 1 / Disk 1A · PMMI Communications MM-103 modem · Vector Graphic / Micropolis FD-HD controller (VFDHD) · iCOM FD3712 / FD3812 |
| `0xC1` | 193 | 301 | CompuPro (Godbout) Disk 1 / Disk 1A · PMMI Communications MM-103 modem · Vector Graphic / Micropolis FD-HD controller (VFDHD) · iCOM FD3712 / FD3812 |
| `0xC2` | 194 | 302 | CompuPro (Godbout) Disk 1 / Disk 1A · PMMI Communications MM-103 modem · Vector Graphic / Micropolis FD-HD controller (VFDHD) |
| `0xC3` | 195 | 303 | CompuPro (Godbout) Disk 1 / Disk 1A · PMMI Communications MM-103 modem · Vector Graphic / Micropolis FD-HD controller (VFDHD) |
| `0xC8` | 200 | 310 | CompuPro (Godbout) Disk 2 · Processor Technology VDM-1 |
| `0xE0` | 224 | 340 | Advanced Digital Corp. HDC-1001 · Tarbell Electronics 2022 FDC - 8257 DMA controller |
| `0xE1` | 225 | 341 | Advanced Digital Corp. HDC-1001 · Tarbell Electronics 2022 FDC - 8257 DMA controller |
| `0xE2` | 226 | 342 | Advanced Digital Corp. HDC-1001 · Tarbell Electronics 2022 FDC - 8257 DMA controller |
| `0xE3` | 227 | 343 | Advanced Digital Corp. HDC-1001 · Tarbell Electronics 2022 FDC - 8257 DMA controller |
| `0xE4` | 228 | 344 | Advanced Digital Corp. HDC-1001 · Tarbell Electronics 2022 FDC - 8257 DMA controller |
| `0xE5` | 229 | 345 | Advanced Digital Corp. HDC-1001 · Tarbell Electronics 2022 FDC - 8257 DMA controller |
| `0xE6` | 230 | 346 | Advanced Digital Corp. HDC-1001 · Tarbell Electronics 2022 FDC - 8257 DMA controller |
| `0xE7` | 231 | 347 | Advanced Digital Corp. HDC-1001 · Tarbell Electronics 2022 FDC - 8257 DMA controller |
| `0xF0` | 240 | 360 | CompuPro (Godbout) Selector Channel · Seattle Computer Products SCP-300F support board |
| `0xF8` | 248 | 370 | Processor Technology Sol-20 (built-in I/O) · Seattle Computer Products SCP-300F support board · Tarbell Electronics 1011 / 1011A FDC (single density) |
| `0xF9` | 249 | 371 | Processor Technology Sol-20 (built-in I/O) · Seattle Computer Products SCP-300F support board · Tarbell Electronics 1011 / 1011A FDC (single density) |
| `0xFA` | 250 | 372 | Processor Technology Sol-20 (built-in I/O) · Seattle Computer Products SCP-300F support board · Tarbell Electronics 1011 / 1011A FDC (single density) |
| `0xFB` | 251 | 373 | Processor Technology Sol-20 (built-in I/O) · Seattle Computer Products SCP-300F support board · Tarbell Electronics 1011 / 1011A FDC (single density) |
| `0xFC` | 252 | 374 | Processor Technology Sol-20 (built-in I/O) · Seattle Computer Products SCP-300F support board · Tarbell Electronics 1011 / 1011A FDC (single density) |
| `0xFD` | 253 | 375 | IMSAI FIF floppy controller · Processor Technology Sol-20 (built-in I/O) · Seattle Computer Products SCP-300F support board · Tarbell Electronics 2022 FDC (double density) |
| `0xFE` | 254 | 376 | MITS 88-VI/RTC · Processor Technology Sol-20 (built-in I/O) |
| `0xFF` | 255 | 377 | MITS Altair 8800 front panel · Processor Technology Sol-20 (built-in I/O) |

### Full map

<details>
<summary>All 256 ports — click to expand</summary>

| Port | Dec | Octal | Claimed by | Category |
| --- | --- | --- | --- | --- |
| `0x00` | 0 | 000 | **⚠ Cromemco TU-ART (console) · MITS 88-SIO** | Serial |
| `0x01` | 1 | 001 | **⚠ Cromemco TU-ART (console) · MITS 88-SIO** | Serial |
| `0x02` | 2 | 002 | **⚠ Cromemco TU-ART (console) · IMSAI SIO-2 channel A (TTY) · MITS 88-LPC (line printer interface)** | Printer, Serial |
| `0x03` | 3 | 003 | **⚠ Advanced Digital Corp. Super Six SBC · Cromemco 4FDC / 16FDC / 64FDC (and CCS 2422) · Cromemco TU-ART (console) · IMSAI SIO-2 channel A (TTY) · MITS 88-LPC (line printer interface)** | Floppy, Printer, Serial, System |
| `0x04` | 4 | 004 | **⚠ Advanced Digital Corp. Super Six SBC · Cromemco 4FDC / 16FDC / 64FDC (and CCS 2422) · IMSAI SIO-2 channel B (CRT / keyboard)** | Floppy, Serial, System |
| `0x05` | 5 | 005 | **⚠ Cromemco 16FDC / 64FDC · IMSAI SIO-2 channel B (CRT / keyboard)** | Serial, Timer |
| `0x06` | 6 | 006 | **⚠ Cromemco 16FDC / 64FDC · MITS 88-ACR (audio cassette)** | Cassette, Timer |
| `0x07` | 7 | 007 | **⚠ Cromemco 16FDC / 64FDC · MITS 88-ACR (audio cassette)** | Cassette, Timer |
| `0x08` | 8 | 010 | **⚠ Cromemco 16FDC / 64FDC · MITS 88-DCDD / 88-DISK** | Floppy, Timer |
| `0x09` | 9 | 011 | **⚠ Cromemco 16FDC / 64FDC · MITS 88-DCDD / 88-DISK** | Floppy, Timer |
| `0x0A` | 10 | 012 | MITS 88-DCDD / 88-DISK | Floppy |
| `0x0B` | 11 | 013 | — |  |
| `0x0C` | 12 | 014 | — |  |
| `0x0D` | 13 | 015 | — |  |
| `0x0E` | 14 | 016 | Cromemco Dazzler | Video |
| `0x0F` | 15 | 017 | Cromemco Dazzler | Video |
| `0x10` | 16 | 020 | **⚠ CompuPro (Godbout) Interfacer 3 / Interfacer 4 · MITS 88-2SIO · MITS 88-4PIO** | Parallel, Serial |
| `0x11` | 17 | 021 | **⚠ CompuPro (Godbout) Interfacer 3 / Interfacer 4 · MITS 88-2SIO · MITS 88-4PIO** | Parallel, Serial |
| `0x12` | 18 | 022 | **⚠ CompuPro (Godbout) Interfacer 3 / Interfacer 4 · MITS 88-2SIO · MITS 88-4PIO** | Parallel, Serial |
| `0x13` | 19 | 023 | **⚠ CompuPro (Godbout) Interfacer 3 / Interfacer 4 · MITS 88-2SIO · MITS 88-4PIO** | Parallel, Serial |
| `0x14` | 20 | 024 | **⚠ CompuPro (Godbout) Interfacer 3 / Interfacer 4 · MITS 88-2SIO (second board) · MITS 88-4PIO** | Parallel, Serial |
| `0x15` | 21 | 025 | **⚠ CompuPro (Godbout) Interfacer 3 / Interfacer 4 · MITS 88-2SIO (second board) · MITS 88-4PIO** | Parallel, Serial |
| `0x16` | 22 | 026 | **⚠ CompuPro (Godbout) Interfacer 3 / Interfacer 4 · MITS 88-2SIO (second board) · MITS 88-4PIO** | Parallel, Serial |
| `0x17` | 23 | 027 | **⚠ CompuPro (Godbout) Interfacer 3 / Interfacer 4 · MITS 88-2SIO (second board) · MITS 88-4PIO** | Parallel, Serial |
| `0x18` | 24 | 030 | **⚠ Cromemco D+7A I/O with JS-1 joystick console · MITS 88-4PIO** | Analog I/O, Parallel |
| `0x19` | 25 | 031 | **⚠ Cromemco D+7A I/O with JS-1 joystick console · MITS 88-4PIO** | Analog I/O, Parallel |
| `0x1A` | 26 | 032 | **⚠ Cromemco D+7A I/O with JS-1 joystick console · MITS 88-4PIO** | Analog I/O, Parallel |
| `0x1B` | 27 | 033 | **⚠ Cromemco D+7A I/O with JS-1 joystick console · MITS 88-4PIO** | Analog I/O, Parallel |
| `0x1C` | 28 | 034 | **⚠ Cromemco D+7A I/O with JS-1 joystick console · MITS 88-4PIO** | Analog I/O, Parallel |
| `0x1D` | 29 | 035 | **⚠ Cromemco D+7A I/O with JS-1 joystick console · MITS 88-4PIO** | Analog I/O, Parallel |
| `0x1E` | 30 | 036 | **⚠ Cromemco D+7A I/O with JS-1 joystick console · MITS 88-4PIO** | Analog I/O, Parallel |
| `0x1F` | 31 | 037 | **⚠ Cromemco D+7A I/O with JS-1 joystick console · MITS 88-4PIO** | Analog I/O, Parallel |
| `0x20` | 32 | 040 | Cromemco TU-ART #1 port A | Serial |
| `0x21` | 33 | 041 | Cromemco TU-ART #1 port A | Serial |
| `0x22` | 34 | 042 | Cromemco TU-ART #1 port A | Serial |
| `0x23` | 35 | 043 | Cromemco TU-ART #1 port A | Serial |
| `0x24` | 36 | 044 | — |  |
| `0x25` | 37 | 045 | — |  |
| `0x26` | 38 | 046 | — |  |
| `0x27` | 39 | 047 | — |  |
| `0x28` | 40 | 050 | — |  |
| `0x29` | 41 | 051 | — |  |
| `0x2A` | 42 | 052 | — |  |
| `0x2B` | 43 | 053 | — |  |
| `0x2C` | 44 | 054 | — |  |
| `0x2D` | 45 | 055 | — |  |
| `0x2E` | 46 | 056 | — |  |
| `0x2F` | 47 | 057 | — |  |
| `0x30` | 48 | 060 | Cromemco 4FDC / 16FDC / 64FDC (and CCS 2422) | Floppy |
| `0x31` | 49 | 061 | Cromemco 4FDC / 16FDC / 64FDC (and CCS 2422) | Floppy |
| `0x32` | 50 | 062 | Cromemco 4FDC / 16FDC / 64FDC (and CCS 2422) | Floppy |
| `0x33` | 51 | 063 | Cromemco 4FDC / 16FDC / 64FDC (and CCS 2422) | Floppy |
| `0x34` | 52 | 064 | Cromemco 4FDC / 16FDC / 64FDC (and CCS 2422) | Floppy |
| `0x35` | 53 | 065 | — |  |
| `0x36` | 54 | 066 | — |  |
| `0x37` | 55 | 067 | — |  |
| `0x38` | 56 | 070 | — |  |
| `0x39` | 57 | 071 | — |  |
| `0x3A` | 58 | 072 | — |  |
| `0x3B` | 59 | 073 | — |  |
| `0x3C` | 60 | 074 | — |  |
| `0x3D` | 61 | 075 | — |  |
| `0x3E` | 62 | 076 | — |  |
| `0x3F` | 63 | 077 | — |  |
| `0x40` | 64 | 100 | Cromemco 4FDC / 16FDC / 64FDC (and CCS 2422) | Floppy |
| `0x41` | 65 | 101 | — |  |
| `0x42` | 66 | 102 | — |  |
| `0x43` | 67 | 103 | Jade Computer Products Double D | Floppy |
| `0x44` | 68 | 104 | — |  |
| `0x45` | 69 | 105 | — |  |
| `0x46` | 70 | 106 | — |  |
| `0x47` | 71 | 107 | — |  |
| `0x48` | 72 | 110 | — |  |
| `0x49` | 73 | 111 | — |  |
| `0x4A` | 74 | 112 | — |  |
| `0x4B` | 75 | 113 | — |  |
| `0x4C` | 76 | 114 | — |  |
| `0x4D` | 77 | 115 | — |  |
| `0x4E` | 78 | 116 | — |  |
| `0x4F` | 79 | 117 | — |  |
| `0x50` | 80 | 120 | **⚠ CompuPro (Godbout) System Support 1 · Cromemco TU-ART #1 port B · SD Systems VersaFloppy I / II** | Floppy, Serial, System |
| `0x51` | 81 | 121 | **⚠ CompuPro (Godbout) System Support 1 · Cromemco TU-ART #1 port B · SD Systems VersaFloppy I / II** | Floppy, Serial, System |
| `0x52` | 82 | 122 | **⚠ CompuPro (Godbout) System Support 1 · Cromemco TU-ART #1 port B · SD Systems VersaFloppy I / II** | Floppy, Serial, System |
| `0x53` | 83 | 123 | **⚠ CompuPro (Godbout) System Support 1 · Cromemco TU-ART #1 port B · SD Systems VersaFloppy I / II** | Floppy, Serial, System |
| `0x54` | 84 | 124 | **⚠ CompuPro (Godbout) System Support 1 · Morrow Designs Disk Jockey HDC-DMA · SD Systems VersaFloppy I / II** | Floppy, Hard disk, Timer |
| `0x55` | 85 | 125 | **⚠ CompuPro (Godbout) System Support 1 · Morrow Designs Disk Jockey HDC-DMA · SD Systems VersaFloppy I / II** | Floppy, Hard disk, Timer |
| `0x56` | 86 | 126 | **⚠ CompuPro (Godbout) System Support 1 · SD Systems VersaFloppy I / II** | Floppy, Timer |
| `0x57` | 87 | 127 | **⚠ CompuPro (Godbout) System Support 1 · SD Systems VersaFloppy I / II** | Floppy, Timer |
| `0x58` | 88 | 130 | CompuPro (Godbout) System Support 1 | Math |
| `0x59` | 89 | 131 | CompuPro (Godbout) System Support 1 | Math |
| `0x5A` | 90 | 132 | CompuPro (Godbout) System Support 1 | Clock |
| `0x5B` | 91 | 133 | CompuPro (Godbout) System Support 1 | Clock |
| `0x5C` | 92 | 134 | CompuPro (Godbout) System Support 1 | Serial |
| `0x5D` | 93 | 135 | CompuPro (Godbout) System Support 1 | Serial |
| `0x5E` | 94 | 136 | CompuPro (Godbout) System Support 1 | Serial |
| `0x5F` | 95 | 137 | CompuPro (Godbout) System Support 1 | Serial |
| `0x60` | 96 | 140 | Cromemco TU-ART #2 port A | Serial |
| `0x61` | 97 | 141 | Cromemco TU-ART #2 port A | Serial |
| `0x62` | 98 | 142 | Cromemco TU-ART #2 port A | Serial |
| `0x63` | 99 | 143 | Cromemco TU-ART #2 port A | Serial |
| `0x64` | 100 | 144 | — |  |
| `0x65` | 101 | 145 | — |  |
| `0x66` | 102 | 146 | — |  |
| `0x67` | 103 | 147 | — |  |
| `0x68` | 104 | 150 | — |  |
| `0x69` | 105 | 151 | — |  |
| `0x6A` | 106 | 152 | — |  |
| `0x6B` | 107 | 153 | — |  |
| `0x6C` | 108 | 154 | — |  |
| `0x6D` | 109 | 155 | — |  |
| `0x6E` | 110 | 156 | Tarbell Electronics 1001 cassette interface | Cassette |
| `0x6F` | 111 | 157 | Tarbell Electronics 1001 cassette interface | Cassette |
| `0x70` | 112 | 160 | Cromemco TU-ART #2 port B | Serial |
| `0x71` | 113 | 161 | Cromemco TU-ART #2 port B | Serial |
| `0x72` | 114 | 162 | Cromemco TU-ART #2 port B | Serial |
| `0x73` | 115 | 163 | Cromemco TU-ART #2 port B | Serial |
| `0x74` | 116 | 164 | — |  |
| `0x75` | 117 | 165 | — |  |
| `0x76` | 118 | 166 | — |  |
| `0x77` | 119 | 167 | — |  |
| `0x78` | 120 | 170 | XComp Hard disk controller | Hard disk |
| `0x79` | 121 | 171 | XComp Hard disk controller | Hard disk |
| `0x7A` | 122 | 172 | XComp Hard disk controller | Hard disk |
| `0x7B` | 123 | 173 | XComp Hard disk controller | Hard disk |
| `0x7C` | 124 | 174 | XComp Hard disk controller | Hard disk |
| `0x7D` | 125 | 175 | XComp Hard disk controller | Hard disk |
| `0x7E` | 126 | 176 | XComp Hard disk controller | Hard disk |
| `0x7F` | 127 | 177 | XComp Hard disk controller | Hard disk |
| `0x80` | 128 | 200 | **⚠ Cromemco TU-ART #3 port A · D.C. Hayes 80-103A / Micromodem 100** | Modem, Serial |
| `0x81` | 129 | 201 | **⚠ Cromemco TU-ART #3 port A · D.C. Hayes 80-103A / Micromodem 100** | Modem, Serial |
| `0x82` | 130 | 202 | **⚠ Cromemco TU-ART #3 port A · D.C. Hayes 80-103A / Micromodem 100** | Modem, Serial |
| `0x83` | 131 | 203 | **⚠ Cromemco TU-ART #3 port A · D.C. Hayes 80-103A / Micromodem 100** | Modem, Serial |
| `0x84` | 132 | 204 | — |  |
| `0x85` | 133 | 205 | — |  |
| `0x86` | 134 | 206 | — |  |
| `0x87` | 135 | 207 | — |  |
| `0x88` | 136 | 210 | — |  |
| `0x89` | 137 | 211 | — |  |
| `0x8A` | 138 | 212 | — |  |
| `0x8B` | 139 | 213 | — |  |
| `0x8C` | 140 | 214 | — |  |
| `0x8D` | 141 | 215 | — |  |
| `0x8E` | 142 | 216 | — |  |
| `0x8F` | 143 | 217 | — |  |
| `0x90` | 144 | 220 | Viasyn / CompuPro Disk 3 | Hard disk |
| `0x91` | 145 | 221 | Viasyn / CompuPro Disk 3 | Hard disk |
| `0x92` | 146 | 222 | — |  |
| `0x93` | 147 | 223 | — |  |
| `0x94` | 148 | 224 | — |  |
| `0x95` | 149 | 225 | — |  |
| `0x96` | 150 | 226 | — |  |
| `0x97` | 151 | 227 | — |  |
| `0x98` | 152 | 230 | — |  |
| `0x99` | 153 | 231 | — |  |
| `0x9A` | 154 | 232 | — |  |
| `0x9B` | 155 | 233 | — |  |
| `0x9C` | 156 | 234 | — |  |
| `0x9D` | 157 | 235 | — |  |
| `0x9E` | 158 | 236 | — |  |
| `0x9F` | 159 | 237 | — |  |
| `0xA0` | 160 | 240 | MITS 88-HDSK (Altair hard disk) | Hard disk |
| `0xA1` | 161 | 241 | MITS 88-HDSK (Altair hard disk) | Hard disk |
| `0xA2` | 162 | 242 | MITS 88-HDSK (Altair hard disk) | Hard disk |
| `0xA3` | 163 | 243 | MITS 88-HDSK (Altair hard disk) | Hard disk |
| `0xA4` | 164 | 244 | MITS 88-HDSK (Altair hard disk) | Hard disk |
| `0xA5` | 165 | 245 | MITS 88-HDSK (Altair hard disk) | Hard disk |
| `0xA6` | 166 | 246 | MITS 88-HDSK (Altair hard disk) | Hard disk |
| `0xA7` | 167 | 247 | MITS 88-HDSK (Altair hard disk) | Hard disk |
| `0xA8` | 168 | 250 | — |  |
| `0xA9` | 169 | 251 | — |  |
| `0xAA` | 170 | 252 | — |  |
| `0xAB` | 171 | 253 | — |  |
| `0xAC` | 172 | 254 | — |  |
| `0xAD` | 173 | 255 | — |  |
| `0xAE` | 174 | 256 | — |  |
| `0xAF` | 175 | 257 | — |  |
| `0xB0` | 176 | 260 | — |  |
| `0xB1` | 177 | 261 | — |  |
| `0xB2` | 178 | 262 | — |  |
| `0xB3` | 179 | 263 | — |  |
| `0xB4` | 180 | 264 | — |  |
| `0xB5` | 181 | 265 | — |  |
| `0xB6` | 182 | 266 | — |  |
| `0xB7` | 183 | 267 | — |  |
| `0xB8` | 184 | 270 | — |  |
| `0xB9` | 185 | 271 | — |  |
| `0xBA` | 186 | 272 | — |  |
| `0xBB` | 187 | 273 | — |  |
| `0xBC` | 188 | 274 | — |  |
| `0xBD` | 189 | 275 | — |  |
| `0xBE` | 190 | 276 | — |  |
| `0xBF` | 191 | 277 | — |  |
| `0xC0` | 192 | 300 | **⚠ CompuPro (Godbout) Disk 1 / Disk 1A · PMMI Communications MM-103 modem · Vector Graphic / Micropolis FD-HD controller (VFDHD) · iCOM FD3712 / FD3812** | Floppy, Floppy / Hard disk, Modem |
| `0xC1` | 193 | 301 | **⚠ CompuPro (Godbout) Disk 1 / Disk 1A · PMMI Communications MM-103 modem · Vector Graphic / Micropolis FD-HD controller (VFDHD) · iCOM FD3712 / FD3812** | Floppy, Floppy / Hard disk, Modem |
| `0xC2` | 194 | 302 | **⚠ CompuPro (Godbout) Disk 1 / Disk 1A · PMMI Communications MM-103 modem · Vector Graphic / Micropolis FD-HD controller (VFDHD)** | Floppy, Floppy / Hard disk, Modem |
| `0xC3` | 195 | 303 | **⚠ CompuPro (Godbout) Disk 1 / Disk 1A · PMMI Communications MM-103 modem · Vector Graphic / Micropolis FD-HD controller (VFDHD)** | Floppy, Floppy / Hard disk, Modem |
| `0xC4` | 196 | 304 | — |  |
| `0xC5` | 197 | 305 | — |  |
| `0xC6` | 198 | 306 | CompuPro (Godbout) M-Drive/H | RAM disk |
| `0xC7` | 199 | 307 | CompuPro (Godbout) M-Drive/H | RAM disk |
| `0xC8` | 200 | 310 | **⚠ CompuPro (Godbout) Disk 2 · Processor Technology VDM-1** | Hard disk, Video |
| `0xC9` | 201 | 311 | CompuPro (Godbout) Disk 2 | Hard disk |
| `0xCA` | 202 | 312 | — |  |
| `0xCB` | 203 | 313 | — |  |
| `0xCC` | 204 | 314 | — |  |
| `0xCD` | 205 | 315 | — |  |
| `0xCE` | 206 | 316 | — |  |
| `0xCF` | 207 | 317 | — |  |
| `0xD0` | 208 | 320 | — |  |
| `0xD1` | 209 | 321 | — |  |
| `0xD2` | 210 | 322 | — |  |
| `0xD3` | 211 | 323 | — |  |
| `0xD4` | 212 | 324 | — |  |
| `0xD5` | 213 | 325 | — |  |
| `0xD6` | 214 | 326 | — |  |
| `0xD7` | 215 | 327 | — |  |
| `0xD8` | 216 | 330 | — |  |
| `0xD9` | 217 | 331 | — |  |
| `0xDA` | 218 | 332 | — |  |
| `0xDB` | 219 | 333 | — |  |
| `0xDC` | 220 | 334 | — |  |
| `0xDD` | 221 | 335 | — |  |
| `0xDE` | 222 | 336 | — |  |
| `0xDF` | 223 | 337 | — |  |
| `0xE0` | 224 | 340 | **⚠ Advanced Digital Corp. HDC-1001 · Tarbell Electronics 2022 FDC - 8257 DMA controller** | DMA, Hard disk |
| `0xE1` | 225 | 341 | **⚠ Advanced Digital Corp. HDC-1001 · Tarbell Electronics 2022 FDC - 8257 DMA controller** | DMA, Hard disk |
| `0xE2` | 226 | 342 | **⚠ Advanced Digital Corp. HDC-1001 · Tarbell Electronics 2022 FDC - 8257 DMA controller** | DMA, Hard disk |
| `0xE3` | 227 | 343 | **⚠ Advanced Digital Corp. HDC-1001 · Tarbell Electronics 2022 FDC - 8257 DMA controller** | DMA, Hard disk |
| `0xE4` | 228 | 344 | **⚠ Advanced Digital Corp. HDC-1001 · Tarbell Electronics 2022 FDC - 8257 DMA controller** | DMA, Hard disk |
| `0xE5` | 229 | 345 | **⚠ Advanced Digital Corp. HDC-1001 · Tarbell Electronics 2022 FDC - 8257 DMA controller** | DMA, Hard disk |
| `0xE6` | 230 | 346 | **⚠ Advanced Digital Corp. HDC-1001 · Tarbell Electronics 2022 FDC - 8257 DMA controller** | DMA, Hard disk |
| `0xE7` | 231 | 347 | **⚠ Advanced Digital Corp. HDC-1001 · Tarbell Electronics 2022 FDC - 8257 DMA controller** | DMA, Hard disk |
| `0xE8` | 232 | 350 | Tarbell Electronics 2022 FDC - 8257 DMA controller | DMA |
| `0xE9` | 233 | 351 | Tarbell Electronics 2022 FDC - 8257 DMA controller | DMA |
| `0xEA` | 234 | 352 | Tarbell Electronics 2022 FDC - 8257 DMA controller | DMA |
| `0xEB` | 235 | 353 | Tarbell Electronics 2022 FDC - 8257 DMA controller | DMA |
| `0xEC` | 236 | 354 | Tarbell Electronics 2022 FDC - 8257 DMA controller | DMA |
| `0xED` | 237 | 355 | Tarbell Electronics 2022 FDC - 8257 DMA controller | DMA |
| `0xEE` | 238 | 356 | Tarbell Electronics 2022 FDC - 8257 DMA controller | DMA |
| `0xEF` | 239 | 357 | Tarbell Electronics 2022 FDC - 8257 DMA controller | DMA |
| `0xF0` | 240 | 360 | **⚠ CompuPro (Godbout) Selector Channel · Seattle Computer Products SCP-300F support board** | DMA, System |
| `0xF1` | 241 | 361 | Seattle Computer Products SCP-300F support board | System |
| `0xF2` | 242 | 362 | Seattle Computer Products SCP-300F support board | System |
| `0xF3` | 243 | 363 | Seattle Computer Products SCP-300F support board | System |
| `0xF4` | 244 | 364 | Seattle Computer Products SCP-300F support board | System |
| `0xF5` | 245 | 365 | Seattle Computer Products SCP-300F support board | System |
| `0xF6` | 246 | 366 | Seattle Computer Products SCP-300F support board | System |
| `0xF7` | 247 | 367 | Seattle Computer Products SCP-300F support board | System |
| `0xF8` | 248 | 370 | **⚠ Processor Technology Sol-20 (built-in I/O) · Seattle Computer Products SCP-300F support board · Tarbell Electronics 1011 / 1011A FDC (single density)** | Floppy, Serial, System |
| `0xF9` | 249 | 371 | **⚠ Processor Technology Sol-20 (built-in I/O) · Seattle Computer Products SCP-300F support board · Tarbell Electronics 1011 / 1011A FDC (single density)** | Floppy, Serial, System |
| `0xFA` | 250 | 372 | **⚠ Processor Technology Sol-20 (built-in I/O) · Seattle Computer Products SCP-300F support board · Tarbell Electronics 1011 / 1011A FDC (single density)** | Floppy, System |
| `0xFB` | 251 | 373 | **⚠ Processor Technology Sol-20 (built-in I/O) · Seattle Computer Products SCP-300F support board · Tarbell Electronics 1011 / 1011A FDC (single density)** | Cassette, Floppy, System |
| `0xFC` | 252 | 374 | **⚠ Processor Technology Sol-20 (built-in I/O) · Seattle Computer Products SCP-300F support board · Tarbell Electronics 1011 / 1011A FDC (single density)** | Floppy, Keyboard, System |
| `0xFD` | 253 | 375 | **⚠ IMSAI FIF floppy controller · Processor Technology Sol-20 (built-in I/O) · Seattle Computer Products SCP-300F support board · Tarbell Electronics 2022 FDC (double density)** | Floppy, Parallel, System |
| `0xFE` | 254 | 376 | **⚠ MITS 88-VI/RTC · Processor Technology Sol-20 (built-in I/O)** | Interrupt / clock, Video |
| `0xFF` | 255 | 377 | **⚠ MITS Altair 8800 front panel · Processor Technology Sol-20 (built-in I/O)** | System |

</details>

---

## Memory-mapped controllers

Several important disk and video controllers use **no I/O ports at all** — they decode a window in memory space
instead. Looking for them in a port map will find nothing.

| Manufacturer | Board | Type | Memory range | Function |
| --- | --- | --- | --- | --- |
| North Star | MDS-A / MDS-AD Micro Disk System | Floppy controller | `0xE800-0xEBFF` | Boot PROM and controller registers in a 1 KB window |
| Morrow Designs | Disk Jockey 2D | Floppy controller | `0xE000-0xE3FF` | Boot PROM at 0xE000; registers at 0xE3F8-0xE3FF |
| Micropolis | FD controller (MDSK) | Floppy controller | `0xF800-0xFBFF` | Boot PROM and controller registers in a 1 KB window |
| Processor Technology | VDM-1 | Video | `0xCC00-0xCFFF` | 1 KB dual-ported display RAM (64 x 16 characters) |
| Vector Graphic | Flashwriter II | Video | `0xF000-0xF7FF` | Memory-mapped display RAM |
| Cromemco | 4FDC / 16FDC / 64FDC boot PROM | Floppy controller | `0xC000-0xDFFF` | 8 KB RDOS boot PROM |
| Tarbell Electronics | 1011 / 2022 boot PROM | Floppy controller | `0x0000-0x001F` | Bootstrap PROM, phantomed over low memory |
| CompuPro (Godbout) | Disk 1 / Disk 1A boot PROM | Floppy controller | `512 bytes, switch-selectable` | Bootstrap PROM with 8085, 8088 and 68000 loaders |
| iCOM | FD3712 / FD3812 | Floppy controller | `0xF000-0xF7FF` | PROM at 0xF000, sector buffer RAM at 0xF400 |
| Jade Computer Products | Double D | Floppy controller | `0xF000-0xF3FF` | Boot PROM |
| Seattle Computer Products | SCP-300F | Support board | `0xFF800` | ROM |
| MITS | 88-DCDD boot loader | Floppy controller | `0xFF00-0xFFFF` | Disk boot ROM location (loaded, not resident on the controller) |

- **North Star MDS-A / MDS-AD Micro Disk System** — Board decodes 0xE800-0xEFFF in the Horizon. Boot by jumping to 0xE800. Uses no I/O ports.
- **Morrow Designs Disk Jockey 2D** — Registers: E3F8 UART data; E3F9 UART status (R) / 2D control (W); E3FA 2D status (R) / 2D function (W); E3FC WD1791 status (R) / command (W); E3FD track; E3FE sector; E3FF data. The board also carries a serial port.
- **Micropolis FD controller (MDSK)** — Used in Micropolis and Vector Graphic systems.
- **Processor Technology VDM-1** — Jumper-selectable. The scroll/control register is an I/O port (see [Third-party cards](#third-party-cards)).
- **Vector Graphic Flashwriter II** — Console video in Vector Graphic systems.
- **Cromemco 4FDC / 16FDC / 64FDC boot PROM** — Disabled by a write to I/O port 0x40.
- **Tarbell Electronics 1011 / 2022 boot PROM** — Switched out once the boot loader has run.
- **Jade Computer Products Double D** — The controller's own Z80 has a private memory space behind this.
- **Seattle Computer Products SCP-300F** — 20-bit address (8086 system).
- **MITS 88-DCDD boot loader** — The 88-DCDD has no boot PROM: the bootstrap is toggled in or loaded to 0xFF00.

---

## Sources

| Source | What it establishes |
| --- | --- |
| [MITS 88-4PIO manual](http://dunfield.classiccmp.org/s100c/mits/88_4pio.pdf) | Board occupies 16 consecutive addresses; jumper groups at 000/020/040/060/100/120… octal; per-PIA register layout; worked example at 020–037 octal |
| [MITS 88-VI/RTC manual](http://dunfield.classiccmp.org/s100c/mits/88_virtc.pdf) | “The 88-VI (RTC) uses I/O address 254 (decimal) or 376 (octal)” |
| [MITS 88-SIO manual](http://dunfield.classiccmp.org/s100c/mits/88sio_2.pdf) | Two device addresses, jumper-selectable to any even octal address 000–376; A0 selects control vs data |
| [MITS 88-ACR manual](http://dunfield.classiccmp.org/s100c/mits/88_acr.pdf) | Cassette interface addressing and octal selection charts |
| [SIMH AltairZ80 documentation](http://bitsavers.trailing-edge.com/simh.trailing-edge.com_201206/pdf/altairz80_doc.pdf) | 88-2SIO at 10–13 hex as the MITS standard; 88-DISK at 8/9/0A; North Star and Micropolis memory windows |
| [SIMH AltairZ80 device sources](https://github.com/simh/simh/tree/master/AltairZ80) | Register-level maps for Tarbell, Cromemco 4/16/64FDC, CompuPro, Morrow, iCOM, Jade, PMMI, Hayes, Sol-20, TU-ART, Dazzler |
| [Altair 8800 Simulator (D. Hansel)](https://github.com/dhansel/Altair8800) | Independent confirmation of the MITS port map; 88-HDSK via a 4PIO at 0xA0–0xA7; Tarbell F8–FD; Cromemco 30–34 |
| [Altair 8800 Simulator manual](https://retrocmp.de/hardware/altair-8800/altair-8800-sim-manual.pdf) | 88-SIO at 0/1, 88-ACR at 6/7, 88-2SIO at 10/11 and 12/13; printer control port 02h |
| [Cromemco Cromix Instruction Manual (023-4022)](https://archive.org/details/023-4022-cromemco-cromix-manuals) | TU-ART switch settings and the multi-user port map: #1 A=20h B=50h, #2 A=60h B=70h, #3 A=80h |
| [CompuPro Interfacer 4 Technical Manual (187C)](https://archive.org/details/bitsavers_compupro18calManualMay83_3167199) | Eight-port block on any multiple of 8; CompuPro default 10–17h; relative port 0–7 function table |
| [IMSAI CP/M System User’s Guide and SIO-2 manual](http://www.bitsavers.org/pdf/imsai/IMSAI_SIO2-2_B_Manual.pdf) | SIO-2 default block 00–0F; IMSAI software uses 02/03 (TTY) and 04/05 (CRT); second board at 20–2F |
| [s100computers.com](http://www.s100computers.com/) | Board histories and addressing notes for MITS, Tarbell, Cromemco, CompuPro and Processor Technology cards |
| [deramp.com archive](https://deramp.com/) | North Star Horizon restoration notes (MDS controller occupies E800–EFFF); MITS and IMSAI documentation mirror |

