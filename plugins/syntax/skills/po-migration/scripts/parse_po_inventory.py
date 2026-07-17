#!/usr/bin/env python3
"""Parse "Syntax SAP PO Integrations.xlsx" into a normalized integration inventory.

Usage:
    python parse_po_inventory.py "<path to Syntax SAP PO Integrations.xlsx>" [--csv out.csv] [--top N]

The sheet has two columns: a pipe-delimited "Integration Scenario" and a "MessageCount".
Each Integration Scenario is:
    SenderParty | SenderComponent | SenderInterface | ReceiverParty | ReceiverComponent | ReceiverInterface | Namespace

This splits it into those columns, sorts by MessageCount (desc), prints a markdown table
(top N, default 30) plus totals, and optionally writes the full normalized set to CSV.
Pure stdlib (zipfile + ElementTree) — no openpyxl needed.
"""
import os
import re
import sys
import csv
import zipfile
import xml.etree.ElementTree as ET

NS = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
COLS = ["SenderParty", "SenderComponent", "SenderInterface",
        "ReceiverParty", "ReceiverComponent", "ReceiverInterface", "Namespace"]


def _shared_strings(z):
    out = []
    if "xl/sharedStrings.xml" not in z.namelist():
        return out
    root = ET.fromstring(z.read("xl/sharedStrings.xml"))
    for si in root.findall(NS + "si"):
        out.append("".join(t.text or "" for t in si.iter(NS + "t")))
    return out


def _cell_text(c, ss):
    t = c.get("t")
    is_ = c.find(NS + "is")
    if is_ is not None:
        return "".join(x.text or "" for x in is_.iter(NS + "t"))
    v = c.find(NS + "v")
    if v is None or v.text is None:
        return ""
    if t == "s":
        return ss[int(v.text)]
    return v.text


def _rows(z, ss):
    sheets = sorted(n for n in z.namelist() if re.match(r"xl/worksheets/sheet\d+\.xml", n))
    for sf in sheets:
        root = ET.fromstring(z.read(sf))
        got = False
        for row in root.iter(NS + "row"):
            cells = [_cell_text(c, ss).strip() for c in row.iter(NS + "c")]
            cells = [c for c in cells if c != ""]
            if cells:
                got = True
                yield cells
        if got:
            return  # first sheet that actually has data


def parse(path):
    z = zipfile.ZipFile(path)
    ss = _shared_strings(z)
    recs = []
    for cells in _rows(z, ss):
        scenario = cells[0]
        # skip header
        if scenario.lower().startswith("integration scenario"):
            continue
        count = 0
        if len(cells) > 1:
            m = re.search(r"\d+", cells[-1])
            count = int(m.group()) if m else 0
        parts = scenario.split("|")
        parts += [""] * (len(COLS) - len(parts))          # pad
        if len(parts) > len(COLS):                          # join overflow into Namespace
            parts = parts[:len(COLS) - 1] + ["|".join(parts[len(COLS) - 1:])]
        rec = dict(zip(COLS, [p.strip() for p in parts]))
        rec["MessageCount"] = count
        rec["Scenario"] = scenario
        recs.append(rec)
    recs.sort(key=lambda r: r["MessageCount"], reverse=True)
    return recs


def main(argv):
    if len(argv) < 2 or argv[1] in ("-h", "--help"):
        print(__doc__); return 1
    path = argv[1]
    csv_out = None
    top = 30
    i = 2
    while i < len(argv):
        if argv[i] == "--csv":
            csv_out = argv[i + 1]; i += 2
        elif argv[i] == "--top":
            top = int(argv[i + 1]); i += 2
        else:
            print(f"unknown arg: {argv[i]}"); print(__doc__); return 1
    if not os.path.isfile(path):
        print(f"file not found: {path}"); return 2

    recs = parse(path)
    total = sum(r["MessageCount"] for r in recs)
    print(f"{len(recs)} integration scenarios, {total} messages total\n")
    print("| # | Sender (party/comp/iface) | Receiver (party/comp/iface) | Msgs |")
    print("|---|---|---|---|")
    for n, r in enumerate(recs[:top], 1):
        snd = "/".join(x for x in (r["SenderParty"], r["SenderComponent"], r["SenderInterface"]) if x)
        rcv = "/".join(x for x in (r["ReceiverParty"], r["ReceiverComponent"], r["ReceiverInterface"]) if x)
        print(f"| {n} | {snd} | {rcv} | {r['MessageCount']} |")
    if len(recs) > top:
        print(f"\n...{len(recs) - top} more (use --top {len(recs)} or --csv to get all).")

    if csv_out:
        with open(csv_out, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=COLS + ["MessageCount", "Scenario"])
            w.writeheader()
            w.writerows(recs)
        print(f"\nwrote {csv_out}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
