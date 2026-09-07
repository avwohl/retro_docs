# -*- coding: utf-8 -*-
"""Port-assignment dataset for Altair / S-100 bus systems."""

# (mfr, board, category, port, dir, function, notes, addressing, confidence, source)
# port: int, or (lo, hi) tuple, or None for "no I/O port"

S_MITS_SIO   = "MITS 88-SIO manual (Theory of Operation); Altair8800 simulator serial.cpp; SIMH"
S_MITS_4PIO  = "MITS 88-4PIO manual, pp.5/9/27 (Address Selection Chart)"
S_MITS_VI    = "MITS 88-VI(RTC) manual p.5: 'uses I/O address 254 (decimal) or 376 (octal)'"
S_SIMH_DOC   = "SIMH AltairZ80 documentation (altairz80_doc.pdf)"
S_HANSEL     = "Altair 8800 Simulator (dhansel/Altair8800) io.cpp + device sources"
S_SIMH_SRC   = "SIMH simh/AltairZ80 device sources"
S_BOTH       = "SIMH AltairZ80 + Altair 8800 Simulator (independent implementations agree)"
S_CROMIX     = "Cromemco Cromix Instruction Manual (023-4022), TU-ART switch settings"
S_IF4        = "CompuPro Interfacer 4 Technical Manual (187C, May 1983), PORT MAP section"
S_S100PORTS  = ("s100computers.com 'S100 Computers Port Assignements' (J. Monahan). Note this is a modern "
                "builder's list of ports he uses in his own systems, mixing vintage and present-day boards - "
                "it is not a manufacturer source.")
S_IMSAI      = "IMSAI CP/M System User's Guide / SIO-2 Rev 3 manual; deramp.com IMSAI notes"

MITS = [
 # ---- 88-SIO -------------------------------------------------------------
 ("MITS", "88-SIO", "Serial", 0x00, "R", "Status: bit 0 = transmitter buffer empty, bit 1 = receive data available (flags are active-low in hardware)", "The de-facto first serial port on early Altairs. 4K/8K BASIC picks SIO at 0/1 vs 2SIO at 10/11 from sense switch SW11.", "Jumper: any even octal address 000-376 (2 consecutive ports; A0 selects control vs data)", "High", S_MITS_SIO),
 ("MITS", "88-SIO", "Serial", 0x00, "W", "Control: interrupt enable / reset", "", "Jumper (see above)", "High", S_MITS_SIO),
 ("MITS", "88-SIO", "Serial", 0x01, "R", "Received data", "", "Jumper (see above)", "High", S_MITS_SIO),
 ("MITS", "88-SIO", "Serial", 0x01, "W", "Transmit data", "", "Jumper (see above)", "High", S_MITS_SIO),
 # ---- 88-LPC / line printer ---------------------------------------------
 ("MITS", "88-LPC (line printer interface)", "Printer", 0x02, "R", "Printer status (busy / ready)", "Serves the 88-LP Okidata printer and the Centronics 700/701/703. Used by Altair BASIC LINEPRINTER and by CP/M as LST:.", "Fixed by convention", "Medium-High", S_HANSEL),
 ("MITS", "88-LPC (line printer interface)", "Printer", 0x02, "W", "Printer control", "", "Fixed by convention", "Medium-High", S_HANSEL),
 ("MITS", "88-LPC (line printer interface)", "Printer", 0x03, "W", "Printer data", "", "Fixed by convention", "Medium-High", S_HANSEL),
 # ---- 88-ACR -------------------------------------------------------------
 ("MITS", "88-ACR (audio cassette)", "Cassette", 0x06, "R", "Status: transmit buffer empty / receive data available", "300 baud Kansas City standard. The ACR is an 88-SIO-type serial interface strapped to 006/007 plus a modulator/demodulator board. CSAVE/CLOAD in Extended BASIC use it.", "Jumper (SIO-style), standard 006/007 octal", "High", S_BOTH),
 ("MITS", "88-ACR (audio cassette)", "Cassette", 0x06, "W", "Control", "", "Jumper, standard 006/007 octal", "High", S_BOTH),
 ("MITS", "88-ACR (audio cassette)", "Cassette", 0x07, "R", "Data read from tape", "", "Jumper, standard 006/007 octal", "High", S_BOTH),
 ("MITS", "88-ACR (audio cassette)", "Cassette", 0x07, "W", "Data written to tape", "", "Jumper, standard 006/007 octal", "High", S_BOTH),
 # ---- 88-DCDD ------------------------------------------------------------
 ("MITS", "88-DCDD / 88-DISK", "Floppy", 0x08, "R", "Drive status flags: b0 ENWD (ready to write), b1 head-move OK, b2 head loaded, b6 track 0, b7 NRDA (new read data available). Flags are INVERTED on the bus (0 = true).", "8-inch floppy controller (Pertec FD-400 mechanism). Programmed I/O only: no interrupts, no DMA, so a transfer holds the CPU. The 88-MDS minidisk (5.25-inch) uses the same three ports.", "Fixed at 8/9/0A by MITS convention", "High", S_BOTH + "; " + S_SIMH_DOC),
 ("MITS", "88-DCDD / 88-DISK", "Floppy", 0x08, "W", "Drive select / enable: b0-b3 = drive 0-15, b7 = disable controller (deselect)", "", "Fixed", "High", S_BOTH),
 ("MITS", "88-DCDD / 88-DISK", "Floppy", 0x09, "R", "Sector position register: b0 = sector true, b1-b5 = sector number (0-31)", "", "Fixed", "High", S_BOTH),
 ("MITS", "88-DCDD / 88-DISK", "Floppy", 0x09, "W", "Drive control: b0 step in, b1 step out, b2 head load, b3 head unload, b4 interrupt enable, b5 interrupt disable, b7 write enable", "", "Fixed", "High", S_BOTH),
 ("MITS", "88-DCDD / 88-DISK", "Floppy", 0x0A, "R", "Read data", "", "Fixed", "High", S_BOTH),
 ("MITS", "88-DCDD / 88-DISK", "Floppy", 0x0A, "W", "Write data", "", "Fixed", "High", S_BOTH),
 # ---- 88-2SIO ------------------------------------------------------------
 ("MITS", "88-2SIO", "Serial", 0x10, "R", "Port 1 ACIA status: b0 receive data register full, b1 transmit data register empty, b2 DCD, b3 CTS, b7 IRQ", "THE canonical Altair console port. Built on the Motorola MC6850 ACIA. Baud rate jumper-selectable 110-9600 per port.", "Jumper; MITS standard is 10-13 hex", "High", S_SIMH_DOC + "; " + S_BOTH),
 ("MITS", "88-2SIO", "Serial", 0x10, "W", "Port 1 ACIA control: counter divide / master reset, word select, transmit control, receive interrupt enable", "", "Jumper; standard 10-13 hex", "High", S_SIMH_DOC),
 ("MITS", "88-2SIO", "Serial", 0x11, "R", "Port 1 receive data", "", "Jumper; standard 10-13 hex", "High", S_SIMH_DOC),
 ("MITS", "88-2SIO", "Serial", 0x11, "W", "Port 1 transmit data", "", "Jumper; standard 10-13 hex", "High", S_SIMH_DOC),
 ("MITS", "88-2SIO", "Serial", 0x12, "R/W", "Port 2 ACIA status (R) / control (W)", "Port 2 commonly drove the paper-tape reader/punch, and later a printer. SIMH exposes it as the PTR/PTP device.", "Jumper; standard 10-13 hex", "High", S_SIMH_DOC),
 ("MITS", "88-2SIO", "Serial", 0x13, "R/W", "Port 2 receive data (R) / transmit data (W)", "", "Jumper; standard 10-13 hex", "High", S_SIMH_DOC),
 ("MITS", "88-2SIO (second board)", "Serial", (0x14, 0x17), "R/W", "Second 88-2SIO board: port 1 at 14/15, port 2 at 16/17", "Common strapping when a second dual-serial board is fitted.", "Jumper", "Medium-High", S_HANSEL),
 # ---- 88-4PIO ------------------------------------------------------------
 ("MITS", "88-4PIO", "Parallel", (0x10, 0x1F), "R/W", "Four parallel ports, 4 addresses each. Per port n at base+4n: +0 = section A control/status, +1 = section A data or DDR (selected by control bit 2), +2 = section B control/status, +3 = section B data or DDR", "Built from MC6820 PIAs. Occupies 16 consecutive addresses. A2/A3 select the port, A0/A1 select section and channel. The manual's worked example uses 020-037 octal (0x10-0x1F), which collides with a standard 88-2SIO - choose another group in practice.", "Jumper, in 16-port groups: 000, 020, 040, 060, 100, 120 ... octal", "High", S_MITS_4PIO),
 # ---- 88-HDSK ------------------------------------------------------------
 ("MITS", "88-HDSK (Altair hard disk)", "Hard disk", (0xA0, 0xA3), "R/W", "88-4PIO port 1 - command channel. Section A carries command bytes, section B carries acknowledge/status. CA1/CB1 handshake lines are wired to the drive controller's CRDY and CMDACK.", "The Altair 10 MB hard disk has no controller card of its own on the bus: it hangs off an 88-4PIO strapped to base 0xA0 (240 octal).", "Jumper (4PIO group at 240 octal)", "Medium-High", S_HANSEL),
 ("MITS", "88-HDSK (Altair hard disk)", "Hard disk", (0xA4, 0xA7), "R/W", "88-4PIO port 2 - data channel. CA1/CB1 carry the controller's CDA (controller data available) and ADPA (accept data) handshakes.", "", "Jumper (4PIO group at 240 octal)", "Medium-High", S_HANSEL),
 # ---- 88-VI/RTC ----------------------------------------------------------
 ("MITS", "88-VI/RTC", "Interrupt / clock", 0xFE, "W", "Vectored-interrupt level enable mask (b0-b7 enable VI0-VI7). Bit 4 also clears the real-time-clock interrupt.", "Prioritises the eight VI lines on the Altair bus into RST vectors. Required by Altair Time-Sharing BASIC; little other commercial software used it.", "Fixed at 376 octal", "High", S_MITS_VI),
 # ---- front panel --------------------------------------------------------
 ("MITS", "Altair 8800 front panel", "System", 0xFF, "R", "Front-panel sense switches (the A8-A15 toggles)", "Universal Altair convention. Read by BASIC and by most boot ROMs to pick a console device or a boot option.", "Fixed", "High", S_HANSEL),
]

THIRD = [
 # ---- Tarbell ------------------------------------------------------------
 ("Tarbell Electronics", "1011 / 1011A FDC (single density)", "Floppy", 0xF8, "R", "WD1771 status register", "The most widely cloned S-100 floppy controller; the address most CP/M distributions assumed. Boot PROM phantoms in at 0x0000.", "DIP switch; F8 is the factory/de-facto standard", "High", S_SIMH_SRC + " (s100_tarbell.c); " + S_HANSEL),
 ("Tarbell Electronics", "1011 / 1011A FDC (single density)", "Floppy", 0xF8, "W", "WD1771 command register", "", "DIP switch", "High", S_SIMH_SRC),
 ("Tarbell Electronics", "1011 / 1011A FDC (single density)", "Floppy", 0xF9, "R/W", "Track register", "", "DIP switch", "High", S_SIMH_SRC),
 ("Tarbell Electronics", "1011 / 1011A FDC (single density)", "Floppy", 0xFA, "R/W", "Sector register", "", "DIP switch", "High", S_SIMH_SRC),
 ("Tarbell Electronics", "1011 / 1011A FDC (single density)", "Floppy", 0xFB, "R/W", "Data register", "", "DIP switch", "High", S_SIMH_SRC),
 ("Tarbell Electronics", "1011 / 1011A FDC (single density)", "Floppy", 0xFC, "R", "Wait / status: b7 = INTRQ (end of job)", "", "DIP switch", "High", S_SIMH_SRC),
 ("Tarbell Electronics", "1011 / 1011A FDC (single density)", "Floppy", 0xFC, "W", "Drive select and control (drive number, side, density)", "", "DIP switch", "High", S_SIMH_SRC),
 ("Tarbell Electronics", "2022 FDC (double density)", "Floppy", 0xFD, "R", "DMA status", "The DD controller is a superset of the 1011: same F8-FC plus FD, and an Intel 8257 DMA controller.", "DIP switch", "High", S_SIMH_SRC),
 ("Tarbell Electronics", "2022 FDC (double density)", "Floppy", 0xFD, "W", "Extended (DMA) address register", "", "DIP switch", "High", S_SIMH_SRC),
 ("Tarbell Electronics", "2022 FDC - 8257 DMA controller", "DMA", (0xE0, 0xEF), "R/W", "Intel 8257 DMA controller channel and control registers", "", "DIP switch", "Medium-High", S_SIMH_SRC),
 ("Tarbell Electronics", "1001 cassette interface", "Cassette", (0x6E, 0x6F), "R/W", "Cassette interface register block - 0x6E and 0x6F are read, 0x6F is written. The source gives the addresses only; individual register functions are not documented there.", "The board is fully DIP-switch selectable, so this is a commonly-used setting rather than a factory default. Tarbell's own manual does not name one.", "DIP switch, any address", "Medium", S_S100PORTS),
 # ---- Cromemco -----------------------------------------------------------
 ("Cromemco", "4FDC / 16FDC / 64FDC (and CCS 2422)", "Floppy", 0x03, "R", "Interrupt vector - returns the RST opcode for the highest pending interrupt (16FDC / 64FDC)", "Cromemco's standard disk controller family, based on the WD1771 (4FDC) or WD1793 (16FDC/64FDC). Boot PROM (RDOS) at 0xC000.", "Fixed by Cromemco convention", "High", S_SIMH_SRC + " (s100_64fdc.c)"),
 ("Cromemco", "4FDC / 16FDC / 64FDC (and CCS 2422)", "Floppy", 0x03, "W", "Interrupt mask", "", "Fixed", "High", S_SIMH_SRC),
 ("Cromemco", "4FDC / 16FDC / 64FDC (and CCS 2422)", "Floppy", 0x04, "R", "Status 2 - configuration DIP switches plus RTC bit", "", "Fixed", "High", S_SIMH_SRC),
 ("Cromemco", "4FDC / 16FDC / 64FDC (and CCS 2422)", "Floppy", 0x04, "W", "Auxiliary control - side select, restore, fast seek, eject, control-out", "", "Fixed", "High", S_SIMH_SRC),
 ("Cromemco", "16FDC / 64FDC", "Timer", (0x05, 0x09), "R/W", "Five programmable interval timers (timer 1-5)", "Not present on the 4FDC.", "Fixed", "High", S_SIMH_SRC),
 ("Cromemco", "4FDC / 16FDC / 64FDC (and CCS 2422)", "Floppy", 0x30, "R", "WD179x status register", "", "Fixed", "High", S_SIMH_SRC + "; " + S_HANSEL),
 ("Cromemco", "4FDC / 16FDC / 64FDC (and CCS 2422)", "Floppy", 0x30, "W", "WD179x command register", "", "Fixed", "High", S_SIMH_SRC + "; " + S_HANSEL),
 ("Cromemco", "4FDC / 16FDC / 64FDC (and CCS 2422)", "Floppy", 0x31, "R/W", "Track register", "", "Fixed", "High", S_SIMH_SRC),
 ("Cromemco", "4FDC / 16FDC / 64FDC (and CCS 2422)", "Floppy", 0x32, "R/W", "Sector register", "", "Fixed", "High", S_SIMH_SRC),
 ("Cromemco", "4FDC / 16FDC / 64FDC (and CCS 2422)", "Floppy", 0x33, "R/W", "Data register", "", "Fixed", "High", S_SIMH_SRC),
 ("Cromemco", "4FDC / 16FDC / 64FDC (and CCS 2422)", "Floppy", 0x34, "R", "Disk flags: b7 DRQ, b6 boot jumper, b5 head load / select request, b4 inhibit-init, b3 motor on, b2 motor timeout, b1 autowait timeout, b0 EOJ (INTRQ)", "", "Fixed", "High", S_SIMH_SRC),
 ("Cromemco", "4FDC / 16FDC / 64FDC (and CCS 2422)", "Floppy", 0x34, "W", "Disk control: b7 autowait enable, b6 double density, b5 motor on, b4 maxi (8-inch), b3-b0 drive select 4/3/2/1", "", "Fixed", "High", S_SIMH_SRC),
 ("Cromemco", "4FDC / 16FDC / 64FDC (and CCS 2422)", "Floppy", 0x40, "W", "Bank select - any write disables the on-board boot PROM at 0xC000", "", "Fixed", "High", S_SIMH_SRC + "; " + S_HANSEL),
 ("Cromemco", "TU-ART (console)", "Serial", (0x00, 0x03), "R/W", "base+0 = serial data; base+1 = status (R: TBE, RDA, interrupt pending, overrun, framing error) / command (W: reset, interrupt enable, high baud); base+2/+3 = interrupt mask and address, interval timers, parallel port", "Cromemco's combined serial + parallel + timer board. The console TU-ART sits at 0x00; multi-user Cromix systems add more.", "DIP switch", "Medium-High", S_SIMH_SRC + " (s100_tuart.c)"),
 ("Cromemco", "TU-ART #1 port A", "Serial", (0x20, 0x23), "R/W", "Serial port A - user 2 under Cromix", "Cromix multi-user switch settings.", "DIP switch", "High", S_CROMIX),
 ("Cromemco", "TU-ART #1 port B", "Serial", (0x50, 0x53), "R/W", "Serial port B - user 3 under Cromix", "", "DIP switch", "High", S_CROMIX),
 ("Cromemco", "TU-ART #2 port A", "Serial", (0x60, 0x63), "R/W", "Serial port A - user 4 under Cromix", "", "DIP switch", "High", S_CROMIX),
 ("Cromemco", "TU-ART #2 port B", "Serial", (0x70, 0x73), "R/W", "Serial port B - user 5 under Cromix", "", "DIP switch", "High", S_CROMIX),
 ("Cromemco", "TU-ART #3 port A", "Serial", (0x80, 0x83), "R/W", "Serial port A - user 6 under Cromix", "", "DIP switch", "High", S_CROMIX),
 ("Cromemco", "Dazzler", "Video", 0x0E, "R", "Status: b6 = end of frame, b7 = even line", "The first colour graphics card for a personal computer. Display data is DMA'd from a 512-byte or 2 KB block of main memory.", "Fixed", "High", S_SIMH_SRC + "; " + S_HANSEL),
 ("Cromemco", "Dazzler", "Video", 0x0E, "W", "Display on/off (b7) plus the video memory start page (2 KB aligned)", "", "Fixed", "High", S_SIMH_SRC),
 ("Cromemco", "Dazzler", "Video", 0x0F, "W", "Format: b6 resolution x4, b5 2 KB vs 512-byte picture, b4 colour vs B/W, b3 high intensity, b2-b0 blue/green/red", "", "Fixed", "High", S_SIMH_SRC),
 ("Cromemco", "D+7A I/O with JS-1 joystick console", "Analog I/O", (0x18, 0x1F), "R/W", "Seven A/D input and seven D/A output channels plus a parallel port. Joystick axes and buttons read at 0x18-0x1C.", "Used together with the Dazzler for games and instrumentation.", "Fixed", "Medium-High", S_SIMH_SRC + "; " + S_HANSEL),
 # ---- IMSAI --------------------------------------------------------------
 ("IMSAI", "SIO-2 channel A (TTY)", "Serial", 0x02, "R/W", "Channel A data", "Note the convention is the reverse of the Altair 88-2SIO: data on the EVEN port, status on the ODD port. Default decoded block is 00-0F; a second SIO-2 is usually strapped to 20-2F.", "Jumper block, default 00-0F", "Medium-High", S_IMSAI),
 ("IMSAI", "SIO-2 channel A (TTY)", "Serial", 0x03, "R/W", "Channel A status / control", "", "Jumper block", "Medium-High", S_IMSAI),
 ("IMSAI", "SIO-2 channel B (CRT / keyboard)", "Serial", 0x04, "R/W", "Channel B data", "This is the port IMSAI's CP/M BIOS maps the CRT to.", "Jumper block", "Medium-High", S_IMSAI),
 ("IMSAI", "SIO-2 channel B (CRT / keyboard)", "Serial", 0x05, "R/W", "Channel B status / control", "", "Jumper block", "Medium-High", S_IMSAI),
 ("IMSAI", "FIF floppy controller", "Floppy", 0xFD, "R", "Status", "Unusual design: a single port. The CPU writes a pointer to a disk descriptor block held in main memory and the controller does the rest. Collides with the Tarbell 2022's DMA port and with SIMH's simulated HDSK.", "Fixed", "High", S_SIMH_SRC + " (s100_fif.c); " + S_SIMH_DOC),
 ("IMSAI", "FIF floppy controller", "Floppy", 0xFD, "W", "Command / disk-descriptor pointer", "", "Fixed", "High", S_SIMH_SRC),
 # ---- Processor Technology ----------------------------------------------
 ("Processor Technology", "Sol-20 (built-in I/O)", "Serial", 0xF8, "R", "Serial status: b7 TBE, b6 data ready, b5 CTS, b4 overrun, b3 framing error, b2 parity error, b1 DSR, b0 carrier detect", "The Sol-20 is a Sol-PC single-board S-100 machine: its I/O is on the CPU board rather than on separate cards.", "Fixed", "High", S_SIMH_SRC + " (sol20.c)"),
 ("Processor Technology", "Sol-20 (built-in I/O)", "Serial", 0xF9, "R/W", "Serial data", "", "Fixed", "High", S_SIMH_SRC),
 ("Processor Technology", "Sol-20 (built-in I/O)", "System", 0xFA, "R", "General status: b7 tape TBE, b6 tape data ready, b4 tape overrun, b3 tape framing error, b2 parallel device ready, b1 parallel data ready, b0 keyboard data ready", "", "Fixed", "High", S_SIMH_SRC),
 ("Processor Technology", "Sol-20 (built-in I/O)", "Cassette", 0xFB, "R/W", "Tape data", "", "Fixed", "High", S_SIMH_SRC),
 ("Processor Technology", "Sol-20 (built-in I/O)", "Keyboard", 0xFC, "R", "Keyboard data", "", "Fixed", "High", S_SIMH_SRC),
 ("Processor Technology", "Sol-20 (built-in I/O)", "Parallel", 0xFD, "R/W", "Parallel port data", "", "Fixed", "High", S_SIMH_SRC),
 ("Processor Technology", "Sol-20 (built-in I/O)", "Video", 0xFE, "W", "Display control - VDM beginning-of-display / scroll register, plus tape drive 1 and 2 motor control (b7/b6)", "Confirmed by the OUT 0FEh instructions in the Sol-20 monitor ROM.", "Fixed", "Medium-High", S_SIMH_SRC),
 ("Processor Technology", "Sol-20 (built-in I/O)", "System", 0xFF, "R", "Sense switches", "", "Fixed", "Medium", S_SIMH_SRC),
 ("Processor Technology", "VDM-1", "Video", 0xC8, "W", "Display control - beginning-of-display / scroll register", "Display RAM is memory-mapped (see the Memory-Mapped sheet), not port-mapped; only the scroll register is a port. The address is jumper-selectable and SIMH's model defaults to 0xFE instead, so verify against your own board.", "Jumper", "Medium", S_HANSEL + " (vdm1.cpp registers 0xC8); SIMH s100_vdm1.c defaults to 0xFE"),
 ("Processor Technology", "3P+S", "Serial / Parallel", None, "-", "Three parallel ports and one serial port; occupies 4 consecutive addresses", "Jumper-selectable to any one of 64 port groups, so there is no single factory default. Frequently used as the console interface.", "Jumper, 64 possible groups", "Unverified", "3P+S product literature (addressing described as jumper-selectable across 64 groups)"),
 # ---- CompuPro / Godbout -------------------------------------------------
 ("CompuPro (Godbout)", "Interfacer 3 / Interfacer 4", "Serial", 0x10, "R/W", "base+0: USART data (Centronics data / DIP switch read on the IF4)", "Eight-channel serial board; the base is switch-selectable to any multiple of 8, and CompuPro's own CP/M-80 and CP/M-86 default to 10-17 hex. IF3 and IF4 are software compatible and can be intermixed.", "DIP switch, any multiple of 8; CompuPro default 0x10", "High", S_IF4),
 ("CompuPro (Godbout)", "Interfacer 3 / Interfacer 4", "Serial", 0x11, "R", "base+1: USART status", "", "DIP switch", "High", S_IF4),
 ("CompuPro (Godbout)", "Interfacer 3 / Interfacer 4", "Serial", 0x11, "W", "base+1: SYN1/SYN2/DLE register (Centronics control on the IF4)", "", "DIP switch", "High", S_IF4),
 ("CompuPro (Godbout)", "Interfacer 3 / Interfacer 4", "Serial", 0x12, "R/W", "base+2: USART mode register (parallel data register on the IF4)", "", "DIP switch", "High", S_IF4),
 ("CompuPro (Godbout)", "Interfacer 3 / Interfacer 4", "Serial", 0x13, "R/W", "base+3: USART command register (parallel status register on the IF4)", "", "DIP switch", "High", S_IF4),
 ("CompuPro (Godbout)", "Interfacer 3 / Interfacer 4", "Serial", 0x14, "R", "base+4: transmit interrupt status", "", "DIP switch", "High", S_IF4),
 ("CompuPro (Godbout)", "Interfacer 3 / Interfacer 4", "Serial", 0x14, "W", "base+4: transmit interrupt mask", "", "DIP switch", "High", S_IF4),
 ("CompuPro (Godbout)", "Interfacer 3 / Interfacer 4", "Serial", 0x15, "R", "base+5: receive interrupt status", "", "DIP switch", "High", S_IF4),
 ("CompuPro (Godbout)", "Interfacer 3 / Interfacer 4", "Serial", 0x15, "W", "base+5: receive interrupt mask", "", "DIP switch", "High", S_IF4),
 ("CompuPro (Godbout)", "Interfacer 3 / Interfacer 4", "Serial", 0x16, "-", "base+6: not used", "", "DIP switch", "High", S_IF4),
 ("CompuPro (Godbout)", "Interfacer 3 / Interfacer 4", "Serial", 0x17, "W", "base+7: user (channel) select register - picks which of the 8 channels the other 7 ports address", "", "DIP switch", "High", S_IF4),
 ("CompuPro (Godbout)", "System Support 1", "System", 0x50, "R/W", "Master 8259A interrupt controller, register 0", "A single board carrying interrupt controllers, timers, a clock/calendar, an AM9511A maths processor and a serial port. Default base 0x50.", "DIP switch, default 0x50", "High", S_SIMH_SRC + " (s100_ss1.c)"),
 ("CompuPro (Godbout)", "System Support 1", "System", 0x51, "R/W", "Master 8259A interrupt controller, register 1", "", "DIP switch", "High", S_SIMH_SRC),
 ("CompuPro (Godbout)", "System Support 1", "System", 0x52, "R/W", "Slave 8259A interrupt controller, register 0", "", "DIP switch", "High", S_SIMH_SRC),
 ("CompuPro (Godbout)", "System Support 1", "System", 0x53, "R/W", "Slave 8259A interrupt controller, register 1", "", "DIP switch", "High", S_SIMH_SRC),
 ("CompuPro (Godbout)", "System Support 1", "Timer", 0x54, "R/W", "8253 timer, counter 0", "", "DIP switch", "High", S_SIMH_SRC),
 ("CompuPro (Godbout)", "System Support 1", "Timer", 0x55, "R/W", "8253 timer, counter 1", "", "DIP switch", "High", S_SIMH_SRC),
 ("CompuPro (Godbout)", "System Support 1", "Timer", 0x56, "R/W", "8253 timer, counter 2", "", "DIP switch", "High", S_SIMH_SRC),
 ("CompuPro (Godbout)", "System Support 1", "Timer", 0x57, "W", "8253 timer, control word", "", "DIP switch", "High", S_SIMH_SRC),
 ("CompuPro (Godbout)", "System Support 1", "Math", 0x58, "R/W", "AM9511A arithmetic processor - data", "", "DIP switch", "High", S_SIMH_SRC),
 ("CompuPro (Godbout)", "System Support 1", "Math", 0x59, "R/W", "AM9511A arithmetic processor - command / status", "", "DIP switch", "High", S_SIMH_SRC),
 ("CompuPro (Godbout)", "System Support 1", "Clock", 0x5A, "W", "Real-time clock command", "", "DIP switch", "High", S_SIMH_SRC),
 ("CompuPro (Godbout)", "System Support 1", "Clock", 0x5B, "R/W", "Real-time clock data", "", "DIP switch", "High", S_SIMH_SRC),
 ("CompuPro (Godbout)", "System Support 1", "Serial", 0x5C, "R/W", "8251 USART data", "", "DIP switch", "High", S_SIMH_SRC),
 ("CompuPro (Godbout)", "System Support 1", "Serial", 0x5D, "R", "8251 USART status", "", "DIP switch", "High", S_SIMH_SRC),
 ("CompuPro (Godbout)", "System Support 1", "Serial", 0x5E, "W", "8251 USART mode", "", "DIP switch", "High", S_SIMH_SRC),
 ("CompuPro (Godbout)", "System Support 1", "Serial", 0x5F, "W", "8251 USART command", "", "DIP switch", "High", S_SIMH_SRC),
 ("CompuPro (Godbout)", "Disk 1 / Disk 1A", "Floppy", 0xC0, "R", "i8272 (NEC 765) main status register", "High-performance 8-inch / 5.25-inch floppy controller with an on-board bootstrap PROM holding 8085, 8088 and 68000 boot loaders.", "DIP switch, default 0xC0", "High", S_SIMH_SRC + " (s100_disk1a.c)"),
 ("CompuPro (Godbout)", "Disk 1 / Disk 1A", "Floppy", 0xC1, "R/W", "i8272 data register", "", "DIP switch", "High", S_SIMH_SRC),
 ("CompuPro (Godbout)", "Disk 1 / Disk 1A", "Floppy", 0xC2, "R", "Drive status register", "", "DIP switch", "High", S_SIMH_SRC),
 ("CompuPro (Godbout)", "Disk 1 / Disk 1A", "Floppy", 0xC2, "W", "DMA address register", "", "DIP switch", "High", S_SIMH_SRC),
 ("CompuPro (Godbout)", "Disk 1 / Disk 1A", "Floppy", 0xC3, "W", "Motor control register", "", "DIP switch", "High", S_SIMH_SRC),
 ("CompuPro (Godbout)", "Disk 2", "Hard disk", (0xC8, 0xC9), "R/W", "Hard disk controller command and status", "20 MB fixed-disk controller. Must be paired with the CompuPro Selector Channel for DMA.", "DIP switch, default 0xC8", "Medium-High", S_SIMH_SRC + " (s100_disk2.c)"),
 ("Viasyn / CompuPro", "Disk 3", "Hard disk", (0x90, 0x91), "R/W", "ST-506 hard disk controller command and status", "DMA controller driven by linked-list descriptors in memory.", "DIP switch, default 0x90", "Medium-High", S_SIMH_SRC + " (s100_disk3.c)"),
 ("CompuPro (Godbout)", "Selector Channel", "DMA", 0xF0, "R/W", "Selector Channel DMA controller", "Provides DMA for the Disk 2 hard disk controller.", "DIP switch, default 0xF0", "Medium-High", S_SIMH_SRC + " (s100_selchan.c)"),
 ("CompuPro (Godbout)", "M-Drive/H", "RAM disk", (0xC6, 0xC7), "R/W", "RAM-disk data (R) / DMA address (W) and control", "Solid-state disk of up to 4 MB.", "DIP switch, default 0xC6", "Medium-High", S_SIMH_SRC + " (s100_mdriveh.c)"),
 # ---- Morrow -------------------------------------------------------------
 ("Morrow Designs", "Disk Jockey 2D (models A and B)", "Floppy", None, "-", "Memory-mapped, not port-mapped - see the Memory-Mapped sheet", "The DJ/2D puts its WD1791 registers and an on-board serial port in the memory window behind its boot PROM. It uses no I/O ports at all.", "Memory address switch", "High", S_SIMH_SRC + " (s100_dj2d.c)"),
 ("Morrow Designs", "Disk Jockey HDC-DMA", "Hard disk", (0x54, 0x55), "R/W", "Hard disk controller command and status", "Command link block is fetched from RAM at 0x0050.", "DIP switch, default 0x54", "Medium-High", S_SIMH_SRC + " (s100_djhdc.c)"),
 # ---- North Star ---------------------------------------------------------
 ("North Star", "MDS-A / MDS-AD (Micro Disk System)", "Floppy", None, "-", "Memory-mapped, not port-mapped - see the Memory-Mapped sheet", "North Star deliberately put the controller in memory space. Boot by jumping to 0xE800. Single- and double-density variants use the same window.", "Memory address jumper", "High", S_SIMH_SRC + "; " + S_SIMH_DOC),
 ("North Star", "Horizon motherboard I/O", "Serial / Parallel", None, "-", "Two 8251 serial ports and two parallel ports - addresses not established in this pass", "The hardware is confirmed (2x 8251 USART, 2 parallel, headers for pin assignment and baud rate) but none of the sources checked gave the port numbers. Check your machine's own BIOS listing.", "Unknown", "Unverified", "deramp.com North Star Horizon restoration notes (describes the hardware, not the addresses)"),
 # ---- Others -------------------------------------------------------------
 ("Advanced Digital Corp.", "HDC-1001", "Hard disk", (0xE0, 0xE7), "R/W", "Standard IDE/ATA task-file registers (data, error/features, sector count, sector number, cylinder low/high, drive-head, status/command)", "Because it uses the plain ATA task file, other task-file controllers behave the same way at this base.", "DIP switch, default 0xE0", "Medium-High", S_SIMH_SRC + " (s100_hdc1001.c)"),
 ("Advanced Digital Corp.", "Super Six SBC", "System", (0x03, 0x04), "R/W", "On-board control and status", "Z80 single-board computer; boot ROM at 0xF000.", "DIP switch", "Medium", S_SIMH_SRC + " (s100_adcs6.c)"),
 ("Jade Computer Products", "Double D", "Floppy", 0x43, "R/W", "Single-port command / status interface", "The Double D carries its own Z80, memory and I/O space; the host talks to it through one port. Boot PROM at 0xF000.", "DIP switch, default 0x43", "Medium-High", S_SIMH_SRC + " (s100_jadedd.c)"),
 ("iCOM", "FD3712 / FD3812", "Floppy", 0xC0, "R/W", "Command register (W) / data in (R)", "FD3712 is single density, FD3812 adds double density. PROM at 0xF000, buffer RAM at 0xF400.", "DIP switch, default 0xC0", "Medium-High", S_SIMH_SRC + " (s100_icom.c)"),
 ("iCOM", "FD3712 / FD3812", "Floppy", 0xC1, "W", "Data out", "", "DIP switch", "Medium-High", S_SIMH_SRC),
 ("Micropolis", "FD controller (MDSK)", "Floppy", None, "-", "Memory-mapped, not port-mapped - see the Memory-Mapped sheet", "Used in Micropolis and Vector Graphic systems.", "Memory address jumper", "High", S_SIMH_SRC + " (mfdc.c)"),
 ("Vector Graphic / Micropolis", "FD-HD controller (VFDHD)", "Floppy / Hard disk", (0xC0, 0xC3), "R/W", "Combined floppy and hard disk controller registers", "", "DIP switch, default 0xC0", "Medium-High", S_SIMH_SRC + " (vfdhd.c); " + S_SIMH_DOC),
 ("Vector Graphic", "Flashwriter II", "Video", None, "-", "Memory-mapped, not port-mapped - see the Memory-Mapped sheet", "Memory-mapped video board used as the console in Vector Graphic systems.", "Memory address jumper", "High", S_SIMH_DOC),
 ("Seattle Computer Products", "SCP-300F support board", "System", (0xF0, 0xFD), "R/W", "Serial ports, timers and support functions (14 consecutive ports)", "Support board for SCP's 8086 systems; ROM at 0xFF800. Overlaps the Tarbell FDC range, so the two cannot coexist unmodified.", "DIP switch, default 0xF0", "Medium", S_SIMH_SRC + " (s100_scp300f.c)"),
 ("PMMI Communications", "MM-103 modem", "Modem", (0xC0, 0xC3), "R/W", "base+0 modem control/status, base+1 UART data, base+2 UART status, base+3 rate / dial control", "The classic S-100 originate/answer modem (MC6860). Switch-selectable; note that SIMH's model uses base 0xC0 while its own documentation text cites E0-E3, so confirm against your board.", "DIP switch", "Medium", S_SIMH_SRC + " (s100_pmmi.c)"),
 ("D.C. Hayes", "80-103A / Micromodem 100", "Modem", (0x80, 0x83), "R/W", "Modem control/status and UART registers", "", "DIP switch, default 0x80", "Medium", S_SIMH_SRC + " (s100_hayes.c)"),
 ("XComp", "Hard disk controller", "Hard disk", (0x78, 0x7F), "R/W", "Controller register block of 8 ports", "Individual register assignments not documented in the source.", "DIP switch", "Medium", S_S100PORTS),
 ("Cromemco", "Octart", "Serial", None, "-", "Eight-channel serial board - addresses not established in this pass", "Well-known board; no address confirmed from the sources checked.", "DIP switch", "Unverified", "-"),
 ("SD Systems", "VersaFloppy I / II", "Floppy", (0x50, 0x57), "R/W", "Controller register block of 8 ports (WD179x registers plus drive and density control). The source gives the block only; individual register assignments are not documented there.", "Widely used WD179x-based controller. Note this block collides with the CompuPro System Support 1 at 0x50-0x5F and with a Cromemco TU-ART at 0x50.", "DIP switch", "Medium", S_S100PORTS),
]

MEMMAP = [
 # (mfr, board, category, range, function, notes, source)
 ("North Star", "MDS-A / MDS-AD Micro Disk System", "Floppy controller", "0xE800-0xEBFF", "Boot PROM and controller registers in a 1 KB window", "Board decodes 0xE800-0xEFFF in the Horizon. Boot by jumping to 0xE800. Uses no I/O ports.", S_SIMH_SRC + "; deramp.com Horizon restoration notes"),
 ("Morrow Designs", "Disk Jockey 2D", "Floppy controller", "0xE000-0xE3FF", "Boot PROM at 0xE000; registers at 0xE3F8-0xE3FF", "Registers: E3F8 UART data; E3F9 UART status (R) / 2D control (W); E3FA 2D status (R) / 2D function (W); E3FC WD1791 status (R) / command (W); E3FD track; E3FE sector; E3FF data. The board also carries a serial port.", S_SIMH_SRC + " (s100_dj2d.c)"),
 ("Micropolis", "FD controller (MDSK)", "Floppy controller", "0xF800-0xFBFF", "Boot PROM and controller registers in a 1 KB window", "Used in Micropolis and Vector Graphic systems.", S_SIMH_SRC + " (mfdc.c); " + S_SIMH_DOC),
 ("Processor Technology", "VDM-1", "Video", "0xCC00-0xCFFF", "1 KB dual-ported display RAM (64 x 16 characters)", "Jumper-selectable. The scroll/control register is an I/O port (see the Third-Party sheet).", S_SIMH_SRC + "; " + S_HANSEL),
 ("Vector Graphic", "Flashwriter II", "Video", "0xF000-0xF7FF", "Memory-mapped display RAM", "Console video in Vector Graphic systems.", S_SIMH_DOC),
 ("Cromemco", "4FDC / 16FDC / 64FDC boot PROM", "Floppy controller", "0xC000-0xDFFF", "8 KB RDOS boot PROM", "Disabled by a write to I/O port 0x40.", S_SIMH_SRC),
 ("Tarbell Electronics", "1011 / 2022 boot PROM", "Floppy controller", "0x0000-0x001F", "Bootstrap PROM, phantomed over low memory", "Switched out once the boot loader has run.", S_SIMH_SRC),
 ("CompuPro (Godbout)", "Disk 1 / Disk 1A boot PROM", "Floppy controller", "512 bytes, switch-selectable", "Bootstrap PROM with 8085, 8088 and 68000 loaders", "", S_SIMH_SRC),
 ("iCOM", "FD3712 / FD3812", "Floppy controller", "0xF000-0xF7FF", "PROM at 0xF000, sector buffer RAM at 0xF400", "", S_SIMH_SRC),
 ("Jade Computer Products", "Double D", "Floppy controller", "0xF000-0xF3FF", "Boot PROM", "The controller's own Z80 has a private memory space behind this.", S_SIMH_SRC),
 ("Seattle Computer Products", "SCP-300F", "Support board", "0xFF800", "ROM", "20-bit address (8086 system).", S_SIMH_SRC),
 ("MITS", "88-DCDD boot loader", "Floppy controller", "0xFF00-0xFFFF", "Disk boot ROM location (loaded, not resident on the controller)", "The 88-DCDD has no boot PROM: the bootstrap is toggled in or loaded to 0xFF00.", S_HANSEL),
]


# ===========================================================================
# RC2014 / RCBus - a DIFFERENT BUS from S-100, kept deliberately separate.
#
# RC2014 is a modern homebrew Z80 backplane (2014 onward). It shares the Z80
# and the 8-bit port space with the S-100 machines above and nothing else: no
# board, no address convention and no manufacturer carries across. It is here
# because the same question - "what is already using this port?" - has the same
# answer shape, not because the two are compatible.
#
# Two people have compiled this independently, and both are reproduced rather
# than merged, because they disagree in places. Where they differ the Notes
# column says so. Neither is a manufacturer source; both are careful community
# compilations of jumper-selectable defaults.
#
# (list, origin, module, author, category, ports, R/W, alternatives, notes)
# ===========================================================================

RC2014 = [
 # --- Steve Cousins' RC2014 module spreadsheet -----------------------------
 # Addresses recovered from the sheet's cell fill colours: green = primary
 # read, red = primary write, grey / pink = alternative.
 ('Cousins', 'Official', "RC2014 Mini's Serial", 'Spencer Owen', 'Serial', '0x80-0x83', 'R/W', '0x84-0xBF', ''),
 ('Cousins', 'Official', 'Serial I/O (68B50 UART)', 'Spencer Owen', 'Serial', '0x80-0x83', 'R/W', '0x84-0xBF', ''),
 ('Cousins', 'Official', 'Dual Serial (SIO/2 UART)', 'Spencer Owen', 'Serial', '0x80-0x83', 'R/W', '0x84-0x87', ''),
 ('Cousins', 'Official', 'Digital I/O v1', 'Spencer Owen', 'Parallel', '0x00-0x03', 'R/W', '0x04-0x7F', ''),
 ('Cousins', 'Official', 'Digital I/O v2', 'Spencer Owen', 'Parallel', '0x00-0x03', 'R/W', '', ''),
 ('Cousins', 'Official', 'Digital Input', 'Spencer Owen', 'Parallel', '0x00-0x03', 'R', '0x04-0x7F', ''),
 ('Cousins', 'Official', 'Digital Output', 'Spencer Owen', 'Parallel', '0x00-0x03', 'W', '0x04-0x7F', ''),
 ('Cousins', 'Official', 'Joystick', 'Spencer Owen', 'Parallel', '0x00-0x03', 'R', '0x04-0x7F', ''),
 ('Cousins', 'Official', 'Compact Flash', 'Spencer Owen', 'Storage', '0x10-0x17', 'R/W', '0x90-0x97', ''),
 ('Cousins', 'Official', 'IDE (82C55 PIO)', 'Ed Brindley & Spencer', 'Storage', '0x20-0x23', 'R/W', '0x10-0x13, 0x30-0x33, 0x40-0x43, 0x50-0x53, 0x60-0x63, 0x70-0x73, 0x80-0x83, 0x90-0x93, 0xA0-0xA3, 0xB0-0xB3, 0xC0-0xC3, 0xD0-0xD3, 0xE0-0xE3, 0xF0-0xF3', ''),
 ('Cousins', 'Official', 'Pageable ROM', 'Spencer Owen', 'Memory / paging', '0x30-0x3F', 'W', '0xB0-0xBF', ''),
 ('Cousins', 'Third-party', 'Serial I/O (16550 UART)', 'Ben Chong', 'Serial', '0x80-0x87', 'R/W', '0x88-0xFF', ''),
 ('Cousins', 'Third-party', 'Digital I/O / LCD (8255)', 'Thomas Riesen', 'Parallel', '0x00-0x03', 'R/W', '0x04-0xFF', ''),
 ('Cousins', 'Third-party', 'Sound Card (AY/YM)', 'Ed Brindley', 'Sound', '0xD8-0xDB', 'R', '0xD4-0xD7', ''),
 ('Cousins', 'Third-party', 'Sound Card (AY/YM)', 'Ed Brindley', 'Sound', '0xD0-0xD3, 0xD8-0xDB', 'W', '0xD4-0xD7', ''),
 ('Cousins', 'Third-party', 'Floppy Disk Controller', 'Dr Scott M Baker', 'Floppy', '0xE0-0xEB, 0xF0-0xF3, 0xF8-0xFF', 'R/W', '', ''),
 ('Cousins', 'Third-party', 'VFD/LCD controller', 'Dr Scott M Baker', 'Display', '0xE0-0xE3', 'R/W', '0xE4-0xEF', ''),
 ('Cousins', 'Third-party', 'Compact Flash', 'Dr Scott M Baker', 'Storage', '0xE0-0xE7', 'R/W', '0xE8-0xEF', ''),
 ('Cousins', 'Third-party', 'Z80 CTC', 'Dr Scott M Baker', 'Timer', '0xF0-0xF3', 'R/W', '0xF4-0xFF', ''),
 ('Cousins', 'Third-party', 'Z80 SIO', 'Dr Scott M Baker', 'Serial', '0xE0-0xE3', 'R/W', '0xE4-0xE7', ''),
 ('Cousins', 'Third-party', 'Speech Synth. (SP0245A)', 'Dr Scott M Baker', 'Sound', '0x70-0x73', 'R/W', '0x74-0x7F', ''),
 ('Cousins', 'Third-party', 'Dual DAC (AD7524)', 'Dr Scott M Baker', 'Sound', '0xE0-0xE3', 'W', '0xE8-0xEB, 0xF0-0xF3, 0xF8-0xFB', ''),
 ('Cousins', 'Third-party', 'Front Panel (TIL311)', 'Dr Scott M Baker', 'System', '0xE4-0xE7', 'R', '0xEC-0xEF, 0xF4-0xF7, 0xFC-0xFF', ''),
 ('Cousins', 'Third-party', 'Front Panel (TIL311)', 'Dr Scott M Baker', 'System', '0xE0-0xE3', 'W', '0xE8-0xEB, 0xF0-0xF3, 0xF8-0xFB', ''),
 ('Cousins', 'Third-party', 'RTClock (BEQ4845)', 'Dr Scott M Baker', 'Clock', '0xC0-0xCF', 'R', '0xD0-0xDF', ''),
 ('Cousins', 'Third-party', 'RTClock (BEQ4845)', 'Dr Scott M Baker', 'Clock', '0xC0-0xCF, 0xE0-0xE3', 'W', '0xD0-0xDF, 0xE4-0xFF', ''),
 ('Cousins', 'Third-party', 'LUT (Multiply) Module', 'Phillip Stevens', 'Math', '0x40-0x43', 'R/W', '', ''),
 ('Cousins', 'Third-party', 'Am9511 APU Module', 'Phillip Stevens', 'Math', '0x40-0x43', 'R/W', '0x20-0x23, 0x60-0x63, 0x80-0x83, 0xA0-0xA3, 0xC0-0xC3, 0xE0-0xE3', ''),

 # --- Alan Cox's "Ports" file, reproduced as written ------------------------
 ("Cox", "Official", "Digital I/O", "", "Parallel", "0x00-0x03", "R/W", "", "Agrees with Cousins."),
 ("Cox", "Third-party", "VFD (Scott Baker)", "", "Display", "0x00-0x01", "R/W", "", "Cousins puts this board at 0xE0-0xE3. The two lists disagree - verify against your own board."),
 ("Cox", "Official", "CF Adapter", "", "Storage", "0x10-0x17", "R/W", "0x90-0x97 (ghost)", "Agrees with Cousins."),
 ("Cox", "Third-party", "Speech Synthesizer (Scott Baker)", "", "Sound", "0x20", "R/W", "", "Cousins puts this board at 0x70-0x73. The two lists disagree."),
 ("Cox", "Official", "Pageable ROM", "", "Memory / paging", "0x38", "W", "", "Falls inside the 0x30-0x3F block Cousins gives."),
 ("Cox", "Third-party", "SC108 banking / paging", "", "Memory / paging", "0x38", "W", "", "Shares 0x38 with the pageable ROM."),
 ("Cox", "Third-party", "Marco's Propeller Graphics Card", "", "Video", "0x40-0x43", "R/W", "", "Collides with the LUT and Am9511 APU modules, which Cousins also puts at 0x40-0x43."),
 ("Cox", "Third-party", "Floppy Controller (Scott Baker)", "", "Floppy", "0x48-0x58", "R/W", "", "Cousins puts this board at 0xE0-0xEB, 0xF0-0xF3 and 0xF8-0xFF. A large disagreement - verify."),
 ("Cox", "Third-party", "SC103 Z80 PIO", "", "Parallel", "0x68-0x6B", "R/W", "", ""),
 ("Cox", "Official", "512K ROM/RAM paging registers", "", "Memory / paging", "0x70-0x7F", "W", "", "The forum thread corrected an earlier 0x70/0x74 reading to 0x78-0x7C; Cox records the wider 0x70-0x7F decode."),
 ("Cox", "Official", "ACIA (partial decode)", "", "Serial", "0x80-0xBF", "R/W", "", "Partial decode - the 68B50 board answers across the whole range. Consistent with Cousins' 0x80-0x83 primary plus alternates up to 0xBF."),
 ("Cox", "Official", "SIO", "", "Serial", "0x80-0x83", "R/W", "", "Agrees with Cousins."),
 ("Cox", "Third-party", "SC104 SIO", "", "Serial", "0x80-0x83", "R/W", "", ""),
 ("Cox", "Third-party", "SC104 SIO, second card", "", "Serial", "0x84-0x87", "R/W", "", ""),
 ("Cox", "Third-party", "SIO (Scott Baker)", "", "Serial", "0x80-0x83", "R/W", "", "Cox notes this board may order its ports differently from the standard RC2014 SIO."),
 ("Cox", "Third-party", "SC102 CTC, first card", "", "Timer", "0x88-0x8B", "R/W", "", ""),
 ("Cox", "Third-party", "SC102 CTC, second card", "", "Timer", "0x8C-0x8F", "R/W", "", ""),
 ("Cox", "Third-party", "CTC (Scott Baker)", "", "Timer", "0x90-0x93", "R/W", "", "Cousins puts this board at 0xF0-0xF3."),
 ("Cox", "Third-party", "Z280RC boot mode switch", "", "System", "0xA0", "R", "", ""),
 ("Cox", "Third-party", "Z280RC RTC", "", "Clock", "0xA2", "R/W", "", ""),
 ("Cox", "Third-party", "Real Time Clock (Scott Baker)", "", "Clock", "0xC0", "R/W", "", "Falls inside the 0xC0-0xCF block Cousins gives."),
 ("Cox", "Third-party", "16550A (Ancient Computing)", "", "Serial", "0xC0", "R/W", "", "Shares 0xC0 with two clock boards."),
 ("Cox", "Third-party", "DS1302 RTC (Ed Brindley)", "", "Clock", "0xC0", "R/W", "", "Shares 0xC0."),
 ("Cox", "Third-party", "Z280RC IDE", "", "Storage", "0xC0-0xCF", "R/W", "", ""),
 ("Cox", "Third-party", "YM-AY sound (Ed Brindley)", "", "Sound", "0xD0-0xD3", "W", "", "Agrees with Cousins."),
 ("Cox", "Third-party", "CF Adapter (Scott Baker)", "", "Storage", "0xE0-0xE7", "R/W", "", "Agrees with Cousins."),
 ("Cox", "Third-party", "PPIDE (Ed Brindley)", "", "Storage", "0xE0-0xE7", "R/W", "", ""),
 ("Cox", "Third-party", "DAC (Scott Baker)", "", "Sound", "", "-", "", "Cox found no documented default. Cousins gives 0xE0-0xE3 for writes."),
]
