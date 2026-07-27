# -*- coding: utf-8 -*-
"""
build_status.py <KW> [--dir DIR]

Render the weekly CALM status deck from .status_work/KW<NN>.json (+ optional
KW<NN>.summaries.json) onto the customer's *WeeklyStatus.pptx brand template.
One title slide, then table slides grouped per project team (teams already
alphabetical in the JSON), 7 rows per slide. Deterministic output name so a
re-run overwrites in place.
"""
import argparse
import json
import os
import re
import sys

try:
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
    from pptx.oxml.ns import qn
except ImportError:
    sys.exit("python-pptx missing -> run: python -m pip install python-pptx openpyxl")

# SYNTAX brand palette (from the template theme)
BLUE = RGBColor(0x06, 0x32, 0xA0)   # header / topic
ACCENT = RGBColor(0x38, 0x6E, 0xF7)  # meeting-sourced comment marker
GREEN = RGBColor(0x3C, 0xC8, 0x5A)   # In Bearbeitung
DGREEN = RGBColor(0x2A, 0x8A, 0x3E)  # Fertig
GREY = RGBColor(0x80, 0x80, 0x80)    # Offen
DARK = RGBColor(0x4D, 0x4D, 0x4D)    # text
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
BAND = RGBColor(0xF2, 0xF2, 0xF2)
FONT = "Aptos"

HEADERS = ["ID", "Topic", "Status", "Last update", "Last comment / change"]
COLW = [0.95, 2.65, 1.30, 1.15, 5.95]   # inches, sum 12.0
PER_PAGE = 7
TABLE_STYLE = "{5C22544A-7EE6-4342-B048-85BDC9FD1C3A}"


def status_color(s):
    sl = (s or "").lower()
    if "bearbeitung" in sl:
        return GREEN
    if any(k in sl for k in ("fertig", "abgeschlossen", "erledigt", "done", "closed")):
        return DGREEN
    return GREY


def set_run(run, size, color=DARK, bold=False, font=FONT):
    run.font.size = Pt(size)
    run.font.name = font
    run.font.bold = bold
    run.font.color.rgb = color


def pick_layout(prs, *names):
    for name in names:
        for lay in prs.slide_layouts:
            if lay.name == name:
                return lay
    return prs.slide_layouts[0]


def add_table_slide(prs, title_text, rows, left, top):
    slide = prs.slides.add_slide(pick_layout(prs, "Title Only", "1_Title only", "Blank"))
    try:
        if slide.shapes.title is not None:
            slide.shapes.title.text = title_text
    except Exception:
        pass

    n = len(rows) + 1
    gtbl = slide.shapes.add_table(n, len(HEADERS), Inches(left), Inches(top),
                                  Inches(sum(COLW)), Inches(0.4 * n))
    tbl = gtbl.table
    tblPr = tbl._tbl.find(qn("a:tblPr"))
    sid = tblPr.find(qn("a:tableStyleId"))
    if sid is None:
        sid = tblPr.makeelement(qn("a:tableStyleId"), {})
        tblPr.append(sid)
    sid.text = TABLE_STYLE
    tblPr.set("firstRow", "1")
    tblPr.set("bandRow", "1")
    for ci, w in enumerate(COLW):
        tbl.columns[ci].width = Inches(w)

    for ci, h in enumerate(HEADERS):
        c = tbl.cell(0, ci)
        c.fill.solid(); c.fill.fore_color.rgb = BLUE
        c.vertical_anchor = MSO_ANCHOR.MIDDLE
        c.margin_left = c.margin_right = Inches(0.06)
        c.margin_top = c.margin_bottom = Inches(0.03)
        p = c.text_frame.paragraphs[0]; p.text = h
        set_run(p.runs[0], 11, WHITE, bold=True)

    for ri, it in enumerate(rows, start=1):
        vals = [it["id"], it["topic"], it["status"], it["updated"], it["summary"]]
        is_mm = str(it.get("source", "")).startswith("Meeting")
        band = BAND if ri % 2 == 0 else WHITE
        for ci, val in enumerate(vals):
            c = tbl.cell(ri, ci)
            c.fill.solid(); c.fill.fore_color.rgb = band
            c.vertical_anchor = MSO_ANCHOR.MIDDLE
            c.margin_left = c.margin_right = Inches(0.06)
            c.margin_top = c.margin_bottom = Inches(0.03)
            tf = c.text_frame; tf.word_wrap = True
            p = tf.paragraphs[0]
            if ci == 4 and is_mm:
                # meeting-sourced comment: accent marker + note
                r1 = p.add_run(); r1.text = "» "; set_run(r1, 9.5, ACCENT, bold=True)
                r2 = p.add_run(); r2.text = val; set_run(r2, 9.5, DARK)
                r3 = p.add_run(); r3.text = f"  [{it['source']}]"; set_run(r3, 8, ACCENT, bold=True)
            else:
                p.text = val
                run = p.runs[0] if p.runs else p.add_run()
                if ci == 0:
                    set_run(run, 10, DARK, bold=True); p.alignment = PP_ALIGN.CENTER
                elif ci == 1:
                    set_run(run, 10.5, BLUE, bold=True)
                elif ci == 2:
                    set_run(run, 10.5, status_color(val), bold=True)
                elif ci == 3:
                    set_run(run, 10, DARK); p.alignment = PP_ALIGN.CENTER
                else:
                    set_run(run, 9.5, DARK)
    return slide


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("kw")
    ap.add_argument("--dir", default=".")
    args = ap.parse_args()
    directory = os.path.abspath(args.dir)
    kw = int(re.search(r"(\d{1,2})", str(args.kw)).group(1))
    kw_s = f"{kw:02d}"
    work = os.path.join(directory, ".status_work")

    with open(os.path.join(work, f"KW{kw_s}.json"), encoding="utf-8") as fh:
        data = json.load(fh)
    summaries = {}
    spath = os.path.join(work, f"KW{kw_s}.summaries.json")
    if os.path.exists(spath):
        with open(spath, encoding="utf-8") as fh:
            summaries = json.load(fh)

    prs = Presentation(os.path.join(directory, data["template"]))
    EMU_IN = 914400
    SW = prs.slide_width / EMU_IN
    LEFT = round((SW - sum(COLW)) / 2, 2)
    TOP = 1.55

    # strip template slides (drop rels so parts are not re-serialized)
    lst = prs.slides._sldIdLst
    for sldId in list(lst):
        rId = sldId.get(qn("r:id"))
        if rId:
            prs.part.drop_rel(rId)
        lst.remove(sldId)

    # fill summaries (fallback to trimmed raw)
    n_items = 0
    for team, items in data["teams"].items():
        for it in items:
            it["summary"] = (summaries.get(it["id"]) or it.get("summary")
                             or (it.get("raw") or "")[:180] or "—")
            n_items += 1

    # ---- title slide ----
    ts = prs.slides.add_slide(pick_layout(prs, "Title and subtitle", "1_Title and subtitle"))
    subtitle = None
    for ph in ts.placeholders:
        if ph.placeholder_format.idx == 0:
            ph.text = f"{data['customer']} – Interface Status"
        elif ph.placeholder_format.type is not None and "SUBTITLE" in str(ph.placeholder_format.type):
            subtitle = ph
    src_line = f"Quelle: SAP Cloud ALM „{data['source_xlsx']}“"
    if data.get("minutes_file"):
        src_line += f"  +  Meeting-Minutes „{data['minutes_file']}“"
    dateline = f"Status Meeting · KW{kw_s}" + (f" · {data['meeting_date']}" if data.get("meeting_date") else "")
    if subtitle is not None:
        subtitle.text = f"{dateline}\n{src_line}  ·  {n_items} Aufgaben / {len(data['teams'])} Teams"

    # ---- per team (alphabetical order preserved from JSON) ----
    team_pages = []
    for team, items in data["teams"].items():
        short = team.replace("[Projektteam] ", "").strip()
        pages = [items[i:i + PER_PAGE] for i in range(0, len(items), PER_PAGE)] or [[]]
        for pi, page in enumerate(pages, start=1):
            suffix = f" ({pi}/{len(pages)})" if len(pages) > 1 else ""
            add_table_slide(prs, f"{short} – Status{suffix}", page, LEFT, TOP)
        team_pages.append((short, len(items), len(pages)))

    out = os.path.join(directory, data["output"])
    prs.save(out)
    print(f"Saved: {out}  ({len(list(prs.slides))} slides, {n_items} items)")
    for short, n, p in team_pages:
        print(f"  - {short:42} {n:3} items  ->  {p} slide(s)")


if __name__ == "__main__":
    main()
