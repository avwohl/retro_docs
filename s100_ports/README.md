# S-100 / Altair port-assignment reference

A catalogue of I/O port assignments for MITS Altair factory boards and the
third-party S-100 cards you actually meet in Altair-era systems: serial
terminal, printer, floppy, hard disk and support boards.

| File | What it is |
|---|---|
| [`Altair_S100_Port_Assignments.md`](Altair_S100_Port_Assignments.md) | The reference, readable here on GitHub |
| `Altair_S100_Port_Assignments.xlsx` | The same data as a filterable workbook |
| `ports_data.py` | **The source of truth.** Every port, with its function, addressing, confidence and citation |
| `render_md.py`, `render_xlsx.py` | Renderers |
| `build.py` | Runs both |

## Regenerating

```sh
python3 -m venv venv
./venv/bin/pip install -r requirements.txt
./venv/bin/python build.py
```

Edit `ports_data.py` and rebuild. Do not hand-edit the `.md` or `.xlsx` — they
are generated, and editing one would silently desync it from the other.

## Adding a board

Append a tuple to `MITS` or `THIRD` in `ports_data.py`:

```python
(manufacturer, board, category, port, direction, function,
 notes, addressing, confidence, source)
```

`port` is an `int` for a single port, a `(lo, hi)` tuple for a range, or `None`
for a board that is listed but has no confirmed port. One row per register, and
separate rows where read and write do different things — which on this hardware
is most of the time.

## The rule this catalogue follows

Almost nothing on the S-100 bus had a fixed address; boards decoded their range
with jumpers or a DIP switch. So every entry is a *documented factory default or
de-facto standard* — the setting software expected to find — not a hard-wired
fact. The `confidence` field records how well each one is attested:

| Value | Meaning |
|---|---|
| `High` | Stated in a manufacturer manual, or agreed on by two independent emulator implementations |
| `Medium-High` | One strong source |
| `Medium` | One source, or a documented conflict between sources |
| `Unverified` | Board listed for completeness, no address confirmed — **left blank rather than guessed at** |

Keep that last row honest. A plausible-looking wrong address is worse than an
admitted gap.
