#!/usr/bin/env python3
"""Scaffold a new PO-migration scenario workspace from scenarios/_TEMPLATE.

Usage:
    python scaffold_scenario.py <scenario-name> [--customer C] [--integration I] [--force]

Copies scenarios/_TEMPLATE -> scenarios/<scenario-name>, replacing the tokens
__CUSTOMER__ and __INTEGRATION__ in every text file. Pure stdlib.

    <scenario-name>   folder name under scenarios/ (e.g. freudenberg-cats)
    --customer C      value for __CUSTOMER__ (default: scenario-name)
    --integration I   value for __INTEGRATION__ (default: scenario-name)
    --force           overwrite an existing scenario folder
"""
import os
import sys
import shutil

SKILL_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE = os.path.join(SKILL_ROOT, "scenarios", "_TEMPLATE")


def main(argv):
    if len(argv) < 2 or argv[1] in ("-h", "--help"):
        print(__doc__)
        return 1
    name = argv[1]
    customer = integration = None
    force = False
    i = 2
    while i < len(argv):
        a = argv[i]
        if a == "--customer":
            customer = argv[i + 1]; i += 2
        elif a == "--integration":
            integration = argv[i + 1]; i += 2
        elif a == "--force":
            force = True; i += 1
        else:
            print(f"unknown arg: {a}"); print(__doc__); return 1
    customer = customer or name
    integration = integration or name

    if not os.path.isdir(TEMPLATE):
        print(f"template not found: {TEMPLATE}"); return 2
    dest = os.path.join(SKILL_ROOT, "scenarios", name)
    if os.path.exists(dest):
        if not force:
            print(f"scenario already exists: {dest}  (use --force to overwrite)"); return 3
        shutil.rmtree(dest)

    tokens = {"__CUSTOMER__": customer, "__INTEGRATION__": integration}
    made = []
    for root, _dirs, files in os.walk(TEMPLATE):
        for fn in files:
            sp = os.path.join(root, fn)
            rel = os.path.relpath(sp, TEMPLATE)
            dp = os.path.join(dest, rel)
            os.makedirs(os.path.dirname(dp), exist_ok=True)
            text = open(sp, encoding="utf-8", newline="").read()
            for k, v in tokens.items():
                text = text.replace(k, v)
            open(dp, "w", encoding="utf-8", newline="").write(text)
            made.append(rel.replace("\\", "/"))

    print(f"scaffolded scenario '{name}'  (customer={customer}, integration={integration})")
    print(f"  -> {dest}")
    for rel in sorted(made):
        print(f"     {rel}")
    print("next: fill intake.md, then classify in analysis.md (A2A vs B2B/EDI).")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
