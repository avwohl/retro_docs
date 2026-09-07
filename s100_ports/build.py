#!/usr/bin/env python3
"""Regenerate both port-assignment deliverables from ports_data.py.

    python3 -m venv venv && ./venv/bin/pip install -r requirements.txt
    ./venv/bin/python build.py

Writes Altair_S100_Port_Assignments.md and .xlsx next to this script.
Edit ports_data.py only - never the generated files, or the two will drift.
"""
import runpy, pathlib

HERE = pathlib.Path(__file__).resolve().parent

for mod in ("render_md.py", "render_xlsx.py"):
    print("--- %s" % mod)
    runpy.run_path(str(HERE / mod), run_name="__main__")
