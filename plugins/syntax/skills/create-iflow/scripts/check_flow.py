#!/usr/bin/env python3
"""Local integrity check for a hand-authored .iflw before uploading.

Catches the breakage that uploads fine but fails in the editor / at deploy:
  - XML not well-formed
  - an <incoming>/<outgoing> that has no matching <sequenceFlow id=...>
  - a <sequenceFlow> that nothing references
  - a diagram <BPMNEdge bpmnElement=X> whose X is neither a sequenceFlow nor a messageFlow
It does NOT know SAP's valid activityType/cmdVariantUri set — only the tenant can confirm those, so
always upload after this passes. Usage: python check_flow.py "<file.iflw>"
"""
import re, sys, xml.dom.minidom as dom


def main(path):
    x = open(path, encoding="utf-8").read()
    try:
        dom.parseString(x)
    except Exception as e:
        print(f"FAIL: not well-formed XML: {e}"); return 1

    flow_defs = set(re.findall(r'<bpmn2:sequenceFlow id="([^"]+)"', x))
    flow_refs = set(re.findall(r'<bpmn2:(?:incoming|outgoing)>([^<]+)<', x))
    msg_defs = set(re.findall(r'<bpmn2:messageFlow id="([^"]+)"', x))
    edges = set(re.findall(r'<bpmndi:BPMNEdge bpmnElement="([^"]+)"', x))

    problems = []
    dangling = flow_refs - flow_defs
    orphan = flow_defs - flow_refs
    bad_edges = edges - flow_defs - msg_defs
    if dangling:
        problems.append(f"incoming/outgoing with no sequenceFlow def: {sorted(dangling)}")
    if orphan:
        problems.append(f"sequenceFlow defined but never referenced: {sorted(orphan)}")
    if bad_edges:
        problems.append(f"diagram edges referencing missing elements: {sorted(bad_edges)}")

    # every callActivity/serviceTask should carry an activityType (editor needs it)
    for m in re.finditer(r'<bpmn2:(callActivity|serviceTask) id="([^"]+)"(.*?)</bpmn2:\1>', x, re.S):
        if "activityType" not in m.group(3):
            problems.append(f"{m.group(1)} {m.group(2)} has no activityType property")

    if problems:
        print("FAIL:")
        for p in problems:
            print("  -", p)
        return 1
    print(f"OK: {len(flow_defs)} sequence flows, {len(msg_defs)} message flows, {len(edges)} edges — all resolve.")
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("usage: python check_flow.py <file.iflw>")
    sys.exit(main(sys.argv[1]))
