---
description: 'Playbook + tooling for migrating SAP PO (Process Orchestration) integrations to SAP CPI / Integration Suite (and, as an alternative target, WSO2). Use when scoping or building a PO→CPI scenario: run the detailed integration intake questions, scaffold a per-scenario workspace, classify A2A vs B2B/EDI, and produce the common artifacts (lookups, mappings, scripts, a Jira task under epic SAPIP-25, Confluence docs in space CPI) by REUSING cpi-lookup-template, pi-mapping/gen-lookups, the cpi skill and the jira-* skills rather than rebuilding them. Invoke e.g. /po-migration intake, /po-migration scaffold <name>, /po-migration inventory. Respect the program constraints in reference/program-context.md (PO license ends March 2027; no native OFTP2 in CPI).'
---

# SAP PO → CPI Migration (playbook + intake)

Umbrella skill for the **SAP PO → SAP Integration Suite (CPI)** re-platforming program. It standardises
how each integration scenario is taken in, classified, designed, and turned into the common artifacts —
and it **reuses** the existing migration assets instead of duplicating them. More scenarios are uploaded
over time; each gets its own workspace under `scenarios/`.

> Not a lift-&-shift. This is license/budget-driven and time-boxed. **Read `reference/program-context.md`
> before scoping** — the PO license ends **March 2027**, CPI has **no native OFTP2**, and B2B/EDI on CPI
> needs the Premium Edition. The working assumption: **A2A → CPI**, **B2B/EDI → managed-EDI / specialised
> platform** (target may still change; keep artifacts target-neutral).

## Classify first (per scenario)

Decide the **traffic class** before anything else — it picks the target and the artifact set:

| Class | Target (working assumption) | How we build it |
|---|---|---|
| **A2A** | CPI (or WSO2) | CPI iFlow rebuild — this skill + `cpi-lookup-template` + `pi-mapping gen-lookups`. Start here. |
| **B2B / EDI** (VDA, EDIFACT, X12) | managed-EDI / specialised platform | No lift-&-shift; rebuilt in Integration Advisor (MIG/MAG) or at the provider. CPI-side lookups reuse `pi-mapping`. Watch the **OFTP2** gap. |

## Intake — the detailed questions

`reference/questionnaire.md` holds the full question set (landscape once; then per interface: inventory,
communication channels, certificates & security, dependencies & carve-out scope, plus a B2B/EDI addendum).
It is the working copy of `Downloads/SAP_PI_CarveOut_Questionnaire.xlsx`. Ask the landscape questions once;
ask the rest per scenario into `scenarios/<name>/intake.md`.

## Per-scenario workflow

1. **Scaffold** — `python scripts/scaffold_scenario.py <name> --customer <C> --integration <I>` creates
   `scenarios/<name>/` (intake.md, analysis.md, drafts/jira-task.md, drafts/confluence-page.md) from
   `scenarios/_TEMPLATE`.
2. **Intake** — fill `intake.md` from the uploaded scenario export / interface doc (`reference/questionnaire.md`).
3. **Classify & design** — in `analysis.md`: A2A vs B2B/EDI, target, source as-is, target to-be, and the
   artifacts to build/reuse.
4. **Build (reuse)** — generate lookups via `cpi-lookup-template`; build mappings/scripts; see
   `reference/artifact-conventions.md` for where each artifact lives.
5. **Jira draft → confirm → create** — fill `drafts/jira-task.md`; create under epic **SAPIP-25** only
   after the user confirms.
6. **Confluence draft → confirm → create** — fill `drafts/confluence-page.md`; create in space **CPI**
   only after the user confirms.

## Common artifacts (reuse, don't duplicate)

Full conventions + paths: `reference/artifact-conventions.md`.

| Artifact | Where / how | Reuse |
|---|---|---|
| Lookups / pre-mappers | `LOOKUP_<ENTITY>_<EXT>` / `PREMAP_<MSG>_<ENTITY>_<EXT>` | `Downloads/cpi-lookup-template/` + `pi-mapping\scripts\extract_tpz.py gen-lookups` |
| Mappings | per scenario (CPI msg map / XSLT / Groovy; EDI → Integration Advisor) | document logic target-neutral in `analysis.md` |
| Scripts | Groovy helpers | reusable examples in `Downloads/` (e.g. `getUniquePO.groovy`) |
| Jira task | project SAPIP, epic **SAPIP-25**, title `<Customer>: <Integration>`, ~2 PD | `jira-cpi-task` / `jira-mail-task` + memory `sapip-po-migration-epic` |
| Confluence | space **CPI** (analog: "SmartPressShop AMS") | `mcp__jira__create_confluence_page` |

## Tooling — `scripts/`

```
python "${CLAUDE_PLUGIN_ROOT}/skills/po-migration/scripts/scaffold_scenario.py" <name> [--customer C] [--integration I] [--force]
python "${CLAUDE_PLUGIN_ROOT}/skills/po-migration/scripts/parse_po_inventory.py" "<...\Syntax SAP PO Integrations.xlsx>" [--top N] [--csv out.csv]
```

- **scaffold_scenario.py** — new scenario workspace from `_TEMPLATE` (fills `__CUSTOMER__`/`__INTEGRATION__`).
- **parse_po_inventory.py** — normalizes the PO inventory: splits the pipe-delimited `Integration Scenario`
  into sender/receiver party·component·interface + namespace, with MessageCount, sorted by volume.

## Inventory & scoping

Run `parse_po_inventory.py` on `C:\Users\itshaea\Downloads\Syntax SAP PO Integrations.xlsx` to rank
scenarios by message volume and prioritise migration order (31 scenarios; the ServiceNow A2A traffic
dominates by volume). Use it to fill the landscape interface counts in the questionnaire.

## Jira & Confluence (draft, then create on confirmation)

- Create via the `mcp__jira__*` tools. **Always show the draft and create only after the user confirms.**
- **Jira:** project `SAPIP`, type Task, epic **SAPIP-25**; title `<Customer>: <Integration>`; English; lean
  **~2 PD per interface** (no PM%/contingency padding). The **Customer** field `customfield_11649` is
  mandatory on the create screen and **cannot be set via the MCP tool / API by name → set it in the Jira
  UI** after create; `parent` linking to the epic works via `jira_update_issue {"parent":{"key":"SAPIP-25"}}`.
  See memory `sapip-jira-ticketing`, `sapip-po-migration-epic`.
- **Confluence:** space **CPI**; one page per scenario (or per customer with children).

## Alternative target — WSO2

WSO2 is a candidate alternative target (cheaper than CPI Premium for the budget problem in
`reference/program-context.md`). Tooling is already downloaded: `Downloads/wso2mi-4.5.0.15.zip`,
`Downloads/WSO2-Integration-Studio-8.5.0-linux-gtk-x86_64.tar.gz`, and course material
(`WSO2IF.Course.Outline.pptx`, `WSO2MI46DF_PPT*`). Keep mapping/lookup/routing **logic** documented
independently of runtime in `analysis.md`; the runtime build (CPI iFlow vs WSO2 MI/synapse) is the last
step, so a scenario can be re-targeted without re-doing the analysis.

## Related skills & assets

- **`pi-mapping`** — SAP PI 7.1 ESR + Seeburger EDI knowledge & tooling (`gen-lookups`); the B2B/EDI side.
- **`cpi-lookup-template`** (`Downloads/cpi-lookup-template/`) — lookup + pre-mapper skeletons (V2 & V4/A2X).
- **`cpi`** — operate CPI tenants (list / deploy / status / logs / compare).
- **`jira-cpi-task`**, **`jira-mail-task`** — Jira task creation conventions for SAPIP.
