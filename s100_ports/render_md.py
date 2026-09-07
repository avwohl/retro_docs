# -*- coding: utf-8 -*-
"""Render the port dataset as GitHub-flavoured Markdown.

Run `python build.py` to regenerate both deliverables from ports_data.py.
"""
import pathlib, datetime, collections
OUT_DIR = pathlib.Path(__file__).resolve().parent

from ports_data import MITS, THIRD, MEMMAP

def esc(s):
    if s is None:
        return ""
    return str(s).replace("|", "\\|").replace("\n", "<br>")

def octal(n): return format(n, "03o")

def pfmt(port):
    if port is None:
        return ("—", "—", "—")
    if isinstance(port, tuple):
        lo, hi = port
        return ("`0x%02X`–`0x%02X`" % (lo, hi), "%d–%d" % (lo, hi), "%s–%s" % (octal(lo), octal(hi)))
    return ("`0x%02X`" % port, str(port), octal(port))

def anchor(s):
    out = []
    for ch in s.lower():
        if ch.isalnum(): out.append(ch)
        elif ch in " -_": out.append("-")
    return "".join(out)

L = []
w = L.append

w("# Altair / S-100 Bus I/O Port Assignments")
w("")
w("MITS Altair factory hardware and third-party S-100 cards — serial, printer, floppy, hard disk and support boards.")
w("")
w("*Compiled %s. Also available as a spreadsheet: `Altair_S100_Port_Assignments.xlsx`.*" % datetime.date.today().isoformat())
w("")
w("---")
w("")
w("## Read this first")
w("")
w("**Almost nothing on the S-100 bus had a fixed address.** Boards decoded their port range with jumpers or a DIP")
w("switch, so the addresses below are *documented factory defaults and de-facto standards* — the settings software")
w("expected to find — not hard-wired facts. Any given machine may differ. Where a board's address really is fixed,")
w("the Addressing line says so.")
w("")
w("**MITS documented ports in octal**, and so did most Altair-era software listings. The 88-2SIO console at")
w("`0x10`/`0x11` is \"port 20 and 21\" in every MITS manual. All three radixes are given on every row so you can read")
w("a period listing without converting in your head.")
w("")
w("**Confidence** — `High` = stated in a manufacturer manual, or agreed on by two independent emulator")
w("implementations. `Medium-High` = one strong source. `Medium` = one source, or a documented conflict between")
w("sources. `Unverified` = the board is listed for completeness but no address was confirmed; those rows are")
w("deliberately left blank rather than guessed at.")
w("")
w("**Coverage** — this covers the manufacturers whose cards you actually meet in Altair-era systems. Several hundred")
w("S-100 boards were made in total, and a long tail of them — mostly memory, prototyping and one-off cards — is not")
w("represented here.")
w("")

# ---------------------------------------------------------- quick ref ------
w("## Quick reference")
w("")
w("| Function | Altair (MITS) | Common third-party |")
w("| --- | --- | --- |")
w("| **Terminal serial** | `0x10`/`0x11` (88-2SIO)<br>`0x00`/`0x01` (88-SIO) | `0x10`–`0x17` CompuPro Interfacer 3/4<br>`0x02`–`0x05` IMSAI SIO-2<br>`0x20`/`0x50`/`0x60`/`0x70`/`0x80` Cromemco TU-ART |")
w("| **Printer** | `0x02`/`0x03` (88-LPC) | on-board serial on many disk controllers |")
w("| **Floppy** | `0x08`/`0x09`/`0x0A` (88-DCDD) | `0xF8`–`0xFC` Tarbell 1011<br>`0x30`–`0x34` Cromemco 4/16/64FDC<br>`0xC0`–`0xC3` CompuPro Disk 1A<br>`0xFD` IMSAI FIF |")
w("| **Hard disk** | `0xA0`–`0xA7` (88-HDSK, via an 88-4PIO) | `0xC8` CompuPro Disk 2<br>`0x90` Viasyn Disk 3<br>`0x54` Morrow HDC-DMA<br>`0xE0`–`0xE7` ADC HDC-1001 |")
w("| **Interrupts / clock** | `0xFE` (88-VI/RTC) | `0x50`–`0x5F` CompuPro System Support 1 |")
w("| **Sense switches** | `0xFF` | `0xFF` on the Sol-20 too |")
w("")
w("> [!IMPORTANT]")
w("> Two collisions that will bite you. The 88-4PIO manual's own worked example is 020–037 octal = `0x10`–`0x1F`,")
w("> sitting directly on the standard 88-2SIO console. And `0xFD` is claimed by both the IMSAI FIF and the Tarbell")
w("> 2022. Cromemco's timers at `0x05`–`0x09` also overlap the 88-DCDD floppy controller.")
w("")
TOC_AT = len(L)

# ------------------------------------------------------- board sections ----
SECTIONS = collections.OrderedDict()

def emit_boards(rows, heading):
    w("---")
    w("")
    w("## " + heading)
    w("")
    SECTIONS[heading] = []
    groups = collections.OrderedDict()
    for r in rows:
        groups.setdefault((r[0], r[1]), []).append(r)
    for (mfr, board), grp in groups.items():
        cat  = grp[0][2]
        addr = grp[0][7]
        conf = grp[0][8]
        src  = grp[0][9]
        title = "%s — %s" % (board, mfr)
        SECTIONS[heading].append((mfr, title, anchor(title)))
        w("### " + esc(title))
        w("")
        w("*%s* &nbsp;·&nbsp; **Addressing:** %s &nbsp;·&nbsp; **Confidence:** %s" % (esc(cat), esc(addr), conf))
        w("")
        notes = []
        for n in (r[6] for r in grp):
            if n and n not in notes:
                notes.append(n)
        if notes:
            for n in notes:
                w("> " + esc(n))
                w(">")
            L.pop()
            w("")
        w("| Port (hex) | Dec | Octal | R/W | Function |")
        w("| --- | --- | --- | --- | --- |")
        for (_, _, _, port, dirn, func, _n, _a, _c, _s) in grp:
            h, d, o = pfmt(port)
            w("| %s | %s | %s | %s | %s |" % (h, d, o, esc(dirn), esc(func)))
        w("")
        w("<sub>Source: %s</sub>" % esc(src))
        w("")

emit_boards(MITS, "MITS Altair boards")
emit_boards(THIRD, "Third-party cards")

# ---------------------------------------------------------- port map -------
claims = {}
for src_rows in (MITS, THIRD):
    for (mfr, board, cat, port, dirn, func, notes, addressing, conf, s) in src_rows:
        if port is None:
            continue
        ports = range(port[0], port[1] + 1) if isinstance(port, tuple) else [port]
        for p in ports:
            label = "%s %s" % (mfr, board)
            claims.setdefault(p, [])
            if label not in [c[0] for c in claims[p]]:
                claims[p].append((label, cat))

w("---")
w("")
w("## Port map, `0x00`–`0xFF`")
w("")
claimed = len(claims)
conflicts = sorted(p for p, v in claims.items() if len({n for n, _ in v}) > 1)
w("%d of the 256 ports are claimed by at least one board in this document; **%d are claimed by more than one**." % (claimed, len(conflicts)))
w("")
w("### Contested ports")
w("")
w("| Port | Dec | Octal | Claimed by |")
w("| --- | --- | --- | --- |")
for p in conflicts:
    names = sorted({n for n, _ in claims[p]})
    w("| `0x%02X` | %d | %s | %s |" % (p, p, octal(p), esc(" · ".join(names))))
w("")
w("### Full map")
w("")
w("<details>")
w("<summary>All 256 ports — click to expand</summary>")
w("")
w("| Port | Dec | Octal | Claimed by | Category |")
w("| --- | --- | --- | --- | --- |")
for p in range(256):
    entries = claims.get(p, [])
    names = sorted({n for n, _ in entries})
    cats  = sorted({c for _, c in entries})
    label = esc(" · ".join(names)) if names else "—"
    if len(names) > 1:
        label = "**⚠ " + label + "**"
    w("| `0x%02X` | %d | %s | %s | %s |" % (p, p, octal(p), label, esc(", ".join(cats))))
w("")
w("</details>")
w("")

# ------------------------------------------------------ memory mapped ------
w("---")
w("")
w("## Memory-mapped controllers")
w("")
w("Several important disk and video controllers use **no I/O ports at all** — they decode a window in memory space")
w("instead. Looking for them in a port map will find nothing.")
w("")
w("| Manufacturer | Board | Type | Memory range | Function |")
w("| --- | --- | --- | --- | --- |")
for (mfr, board, cat, rng, func, notes, src) in MEMMAP:
    w("| %s | %s | %s | `%s` | %s |" % (esc(mfr), esc(board), esc(cat), esc(rng), esc(func)))
w("")
for (mfr, board, cat, rng, func, notes, src) in MEMMAP:
    if notes:
        w("- **%s %s** — %s" % (esc(mfr), esc(board), esc(notes)))
w("")

# ----------------------------------------------------------- sources -------
w("---")
w("")
w("## Sources")
w("")
w("| Source | What it establishes |")
w("| --- | --- |")
SOURCES = [
 ("MITS 88-4PIO manual", "Board occupies 16 consecutive addresses; jumper groups at 000/020/040/060/100/120… octal; per-PIA register layout; worked example at 020–037 octal", "http://dunfield.classiccmp.org/s100c/mits/88_4pio.pdf"),
 ("MITS 88-VI/RTC manual", "“The 88-VI (RTC) uses I/O address 254 (decimal) or 376 (octal)”", "http://dunfield.classiccmp.org/s100c/mits/88_virtc.pdf"),
 ("MITS 88-SIO manual", "Two device addresses, jumper-selectable to any even octal address 000–376; A0 selects control vs data", "http://dunfield.classiccmp.org/s100c/mits/88sio_2.pdf"),
 ("MITS 88-ACR manual", "Cassette interface addressing and octal selection charts", "http://dunfield.classiccmp.org/s100c/mits/88_acr.pdf"),
 ("SIMH AltairZ80 documentation", "88-2SIO at 10–13 hex as the MITS standard; 88-DISK at 8/9/0A; North Star and Micropolis memory windows", "http://bitsavers.trailing-edge.com/simh.trailing-edge.com_201206/pdf/altairz80_doc.pdf"),
 ("SIMH AltairZ80 device sources", "Register-level maps for Tarbell, Cromemco 4/16/64FDC, CompuPro, Morrow, iCOM, Jade, PMMI, Hayes, Sol-20, TU-ART, Dazzler", "https://github.com/simh/simh/tree/master/AltairZ80"),
 ("Altair 8800 Simulator (D. Hansel)", "Independent confirmation of the MITS port map; 88-HDSK via a 4PIO at 0xA0–0xA7; Tarbell F8–FD; Cromemco 30–34", "https://github.com/dhansel/Altair8800"),
 ("Altair 8800 Simulator manual", "88-SIO at 0/1, 88-ACR at 6/7, 88-2SIO at 10/11 and 12/13; printer control port 02h", "https://retrocmp.de/hardware/altair-8800/altair-8800-sim-manual.pdf"),
 ("Cromemco Cromix Instruction Manual (023-4022)", "TU-ART switch settings and the multi-user port map: #1 A=20h B=50h, #2 A=60h B=70h, #3 A=80h", "https://archive.org/details/023-4022-cromemco-cromix-manuals"),
 ("CompuPro Interfacer 4 Technical Manual (187C)", "Eight-port block on any multiple of 8; CompuPro default 10–17h; relative port 0–7 function table", "https://archive.org/details/bitsavers_compupro18calManualMay83_3167199"),
 ("IMSAI CP/M System User’s Guide and SIO-2 manual", "SIO-2 default block 00–0F; IMSAI software uses 02/03 (TTY) and 04/05 (CRT); second board at 20–2F", "http://www.bitsavers.org/pdf/imsai/IMSAI_SIO2-2_B_Manual.pdf"),
 ("s100computers.com", "Board histories and addressing notes for MITS, Tarbell, Cromemco, CompuPro and Processor Technology cards", "http://www.s100computers.com/"),
 ("deramp.com archive", "North Star Horizon restoration notes (MDS controller occupies E800–EFFF); MITS and IMSAI documentation mirror", "https://deramp.com/"),
]
for (name, what, url) in SOURCES:
    w("| [%s](%s) | %s |" % (esc(name), url, esc(what)))
w("")

# ---------------------------------------------------------------- TOC ------
toc = ["---", "", "## Contents", ""]
for heading, entries in SECTIONS.items():
    toc.append("**[%s](#%s)**" % (heading, anchor(heading)))
    toc.append("")
    by_mfr = collections.OrderedDict()
    for mfr, title, anc in entries:
        by_mfr.setdefault(mfr, []).append((title, anc))
    for mfr, items in by_mfr.items():
        links = ", ".join("[%s](#%s)" % (t.split(" — ")[0], a) for t, a in items)
        toc.append("- *%s* — %s" % (mfr, links))
    toc.append("")
toc += ["**[Port map, `0x00`–`0xFF`](#port-map-0x000xff)** · "
        "**[Memory-mapped controllers](#memory-mapped-controllers)** · "
        "**[Sources](#sources)**", ""]
L[TOC_AT:TOC_AT] = toc

text = "\n".join(L) + "\n"
# this file is Markdown, not the workbook - fix cross-references to sheets
text = (text.replace("see the Memory-Mapped sheet", "see [Memory-mapped controllers](#memory-mapped-controllers)")
            .replace("see the Third-Party sheet", "see [Third-party cards](#third-party-cards)"))
assert "sheet" not in text.replace("spreadsheet", ""), "stray sheet reference"

out = str(OUT_DIR / "Altair_S100_Port_Assignments.md")
open(out, "w").write(text)
print("wrote", out)
print("lines:", len(L))
