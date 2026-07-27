# -*- coding: utf-8 -*-
"""
prepare_status.py <KW> [--dir DIR]

Mechanical preparation step for the weekly CALM status deck (skill: calm-status).
Reads the SAP Cloud ALM export for calendar week <KW> and the previous week's
meeting minutes, matches follow-up tasks to CALM items, groups items by project
team, and emits an intermediate JSON that the AI step summarizes and that
build_status.py renders.

No AI here - purely deterministic parsing so re-runs are stable.
"""
import argparse
import datetime as dt
import glob
import json
import os
import re
import sys

try:
    import openpyxl
except ImportError:
    sys.exit("openpyxl missing -> run: python -m pip install openpyxl python-pptx")

MONTHS = {m: i for i, m in enumerate(
    ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"], start=1)}

# Header names we consume. Columns shift between exports, so we ALWAYS map by header.
WANT = ["Titel", "ID", "Status", "Team", "Kommentare", "Historie", "Beschreibung", "Geändert am"]


def parse_kw(raw):
    m = re.search(r"(\d{1,2})", str(raw))
    if not m:
        sys.exit(f"Could not parse a calendar week from '{raw}'. Use e.g. 31 or KW31.")
    return int(m.group(1))


def fmt_date(js):
    """'Wed Jul 08 2026 14:13:50 GMT+0200 ...' -> '08.07.2026'."""
    if not js:
        return ""
    m = re.search(r"\b([A-Z][a-z]{2})\s+(\d{1,2})\s+(\d{4})", str(js))
    if not m:
        return str(js)[:12]
    mon, day, year = m.group(1), int(m.group(2)), m.group(3)
    return f"{day:02d}.{MONTHS.get(mon, 0):02d}.{year}"


def clean_topic(t):
    t = t or ""
    t = re.sub(r"Vorbereitung\s*&\s*Durchf\w*hrung\s*F2S-Workshop\s*\[[^\]]*\]\s*", "", t)
    t = re.sub(r"Vorbereitung\s*/\s*Durchf\w*hrung\s*WS-Inhalt:\s*", "", t)
    t = t.replace('"', "").strip()
    t = re.sub(r"\s{2,}", " ", t)
    if " - " in t:
        t = t.replace(" - ", " – ")
    return t.strip()


def find_one(directory, patterns, label, required=True):
    for pat in patterns:
        hits = [p for p in glob.glob(os.path.join(directory, pat))]
        # case-insensitive fallback
        if not hits:
            low = pat.lower()
            hits = [os.path.join(directory, f) for f in os.listdir(directory)
                    if glob.fnmatch.fnmatch(f.lower(), low)]
        hits = sorted(set(hits))
        if hits:
            return hits[0]
    if required:
        sys.exit(f"Required input not found ({label}). Looked for: {patterns} in {directory}")
    return None


def header_map(ws):
    hdr = {}
    for c in range(1, ws.max_column + 1):
        v = ws.cell(row=1, column=c).value
        if v is not None:
            hdr[str(v).strip()] = c
    return hdr


def cell(ws, r, idx):
    if not idx:
        return ""
    v = ws.cell(row=r, column=idx).value
    return "" if v is None else str(v).strip()


def parse_minutes(path, prev_kw):
    """Return (mm_map, mm_context, mm_unmatched).

    mm_map: calm_id -> {'text':..., 'owner':..., 'action':'Update'|'Neu', 'kw':prev_kw}
    """
    mm_map, unmatched = {}, []
    with open(path, encoding="utf-8", errors="replace") as fh:
        text = fh.read()

    # Split narrative vs. follow-ups.
    parts = re.split(r"(?im)^\s*Folgeaufgaben\s*:?\s*$", text, maxsplit=1)
    context = parts[0]
    context = re.sub(r"(?im)^\s*Besprechungsnotizen\s*:?\s*$", "", context).strip()
    follow = parts[1] if len(parts) > 1 else ""

    # Build blocks: a block is the text lines up to (and including) any '=>' lines,
    # separated by blank lines.
    blocks, cur = [], []
    for line in follow.splitlines():
        if line.strip() == "":
            if cur:
                blocks.append(cur)
                cur = []
        else:
            cur.append(line.rstrip())
    if cur:
        blocks.append(cur)

    for blk in blocks:
        body = [l for l in blk if not l.lstrip().startswith("=>")]
        refs = [l for l in blk if l.lstrip().startswith("=>")]
        text_block = " ".join(l.strip() for l in body).strip()
        if not text_block:
            continue
        owner = ""
        mo = re.search(r"\(([^()]+)\)\s*$", text_block)
        if mo:
            owner = mo.group(1).strip()
        ids, action = [], ""
        for rf in refs:
            if re.search(r"\bNeu\b", rf, re.I):
                action = "Neu"
            elif re.search(r"\bUpdate\b", rf, re.I):
                action = action or "Update"
            ids += re.findall(r"\b3-\d+\b", rf)
        if ids:
            for cid in ids:
                mm_map[cid] = {"text": text_block, "owner": owner,
                               "action": action or "Update", "kw": prev_kw}
        else:
            unmatched.append({"text": text_block, "owner": owner})
    return mm_map, context, unmatched


def iso_monday(year, week):
    try:
        return dt.date.fromisocalendar(year, week, 1).strftime("%d.%m.%Y")
    except Exception:
        return ""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("kw")
    ap.add_argument("--dir", default=".")
    ap.add_argument("--year", type=int, default=None)
    args = ap.parse_args()

    directory = os.path.abspath(args.dir)
    kw = parse_kw(args.kw)
    prev = kw - 1
    kw_s = f"{kw:02d}"

    src = find_one(directory, [f"Items*Analysis*KW{kw_s}.xlsx", f"Items*Analysis*KW{kw}.xlsx"],
                   "CALM export xlsx")
    template = find_one(directory, ["*WeeklyStatus.pptx", "*Weekly*Status*.pptx"],
                        "brand template *WeeklyStatus.pptx")
    mm_path = None
    if prev >= 1:
        mm_path = find_one(directory, [f"MeetingMinutes*KW{prev:02d}.txt", f"MeetingMinutes*KW{prev}.txt"],
                           "meeting minutes", required=False)

    customer = os.path.basename(template)
    customer = re.split(r"[_\s]*Weekly", customer, flags=re.I)[0] or "Status"
    year = args.year or dt.date.today().year
    out_name = f"{customer}_InterfaceStatus_StatusMeeting_KW{kw_s}.pptx"

    # ---- minutes ----
    mm_map, mm_context, mm_unmatched = ({}, "", [])
    if mm_path:
        mm_map, mm_context, mm_unmatched = parse_minutes(mm_path, prev)

    # ---- export ----
    wb = openpyxl.load_workbook(src, data_only=True)
    ws = wb.active
    H = header_map(ws)
    missing = [w for w in ("Titel", "ID", "Status", "Team") if w not in H]
    if missing:
        sys.exit(f"Export missing expected columns {missing}. Found headers: {list(H)[:20]} ...")

    teams = {}
    for r in range(2, ws.max_row + 1):
        title = cell(ws, r, H.get("Titel"))
        cid = cell(ws, r, H.get("ID"))
        if not title and not cid:
            continue
        team = cell(ws, r, H.get("Team")) or "(kein Team)"
        if cid in mm_map:
            source = f"Meeting KW{prev:02d}"
            raw = mm_map[cid]["text"]
        else:
            source = "CALM"
            raw = (cell(ws, r, H.get("Kommentare"))
                   or cell(ws, r, H.get("Historie"))
                   or cell(ws, r, H.get("Beschreibung")))
        teams.setdefault(team, []).append({
            "id": cid,
            "topic": clean_topic(title),
            "status": cell(ws, r, H.get("Status")),
            "updated": fmt_date(cell(ws, r, H.get("Geändert am"))),
            "source": source,
            "raw": re.sub(r"\s+", " ", raw).strip(),
            "summary": None,
        })

    ordered = {t: teams[t] for t in sorted(teams)}  # teams alphabetical

    work = os.path.join(directory, ".status_work")
    os.makedirs(work, exist_ok=True)
    data = {
        "kw": kw, "prev_kw": prev, "customer": customer,
        "meeting_date": iso_monday(year, kw),
        "source_xlsx": os.path.basename(src),
        "minutes_file": os.path.basename(mm_path) if mm_path else None,
        "template": os.path.basename(template),
        "output": out_name,
        "mm_context": mm_context,
        "mm_matched_ids": sorted(mm_map),
        "mm_unmatched": mm_unmatched,
        "teams": ordered,
    }
    out_json = os.path.join(work, f"KW{kw_s}.json")
    with open(out_json, "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2)

    n_items = sum(len(v) for v in ordered.values())
    n_mm = sum(1 for v in ordered.values() for it in v if it["source"].startswith("Meeting"))
    print(f"KW{kw_s}: {n_items} items in {len(ordered)} teams "
          f"({n_mm} comments sourced from {data['minutes_file'] or 'no minutes'}).")
    for t, v in ordered.items():
        print(f"  - {t.replace('[Projektteam] ', ''):42} {len(v):3} items")
    if mm_unmatched:
        print(f"  MM follow-ups without CALM reference (not shown in deck): {len(mm_unmatched)}")
        for u in mm_unmatched:
            print(f"     · {u['text'][:90]}")
    print(f"JSON: {out_json}")
    print(f"NEXT: summarize each item's 'raw' into 'summary' -> KW{kw_s}.summaries.json, then build_status.py")


if __name__ == "__main__":
    main()
