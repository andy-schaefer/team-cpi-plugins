# Program context — SAP PO → SAP Integration Suite (CPI)

Distilled from `C:\Users\itshaea\Downloads\Migration SAP PO nach CPI - Management Summary.docx`
(Stand 10.06.2026). These are the **constraints any migration plan must respect** — read before scoping.

## The situation

- Customer runs B2B/EDI for customers & suppliers in **VDA, EDIFACT, ANSI X12** — today on **SAP PO**
  (B2B add-on).
- **Hard deadline: the SAP PO license ends March 2027, no extension.** Replacement is mandatory; ~9 months.
- A SAP Integration Suite (CPI) tenant exists but is licensed/sized **only for SAP DMC**, not B2B/EDI.
- CPI has **no OFTP2 adapter**.
- Cost: ~€650/month today → **>€8,000/month** for Standard Edition with B2B adapter (Premium is more).

**Core message:** this is a license- and budget-driven re-platform under time pressure — not a pure
technical migration.

## Technical blockers

- **OFTP2 missing natively** (critical for VDA/automotive) — only via third party (Seeburger, Advantco) or
  an external OFTP2 gateway / managed-EDI. Hard stop for VDA without an add-on/partner.
- **EDI/B2B needs the Premium Edition** — EDIFACT/X12/VDA run via Integration Advisor (MIG/MAG) + Trading
  Partner Management (TPM).
- **No lift-&-shift of mappings** — PO B2B (SAP B2B / Seeburger) mappings do not port automatically;
  Integration Advisor is a different paradigm → full rebuild of EDI mappings + partner agreements. SAP
  migration tooling covers **A2A iFlows**, not B2B content.
- **Monitoring & acknowledgements** (CONTRL/FA, AS2-MDN) are structured differently in CPI/TPM → re-design.

## Commercial / project risks

- ~12× cost jump; consumption-based billing adds variability; extending the DMC-only tenant to B2B means a
  **new entitlement** and SAP negotiation.
- Hard March-2027 cutover; every partner re-onboarded/tested/re-certified; dual-run only partly possible;
  team needs Integration-Advisor/TPM skills or a service provider.

## Options (from the summary)

1. **Hybrid with CPI Premium** — A2A→CPI; B2B/EDI on CPI Premium (IA+TPM) + third-party OFTP2. Closest to
   SAP, highest cost & build effort.
2. **Hybrid with managed B2B/EDI (recommended)** — A2A→CPI; B2B/EDI incl. VDA/OFTP2 to a managed-EDI/VAN
   provider. Predictable OPEX, far less self-build, realistic by March 2027, sidesteps the OFTP2 gap and
   the Premium cost jump.
3. **Specialised B2B platform** — B2B/EDI on a dedicated platform (e.g. Seeburger BIS), A2A→CPI.
4. **In parallel:** negotiate with SAP (Premium / CPEA credits tied to real message volume).

## What this means for our artifacts

- **Classify every scenario A2A vs B2B/EDI first.** It decides the target and the artifact set.
- **A2A → CPI now.** This is where this skill + `cpi-lookup-template` + `pi-mapping gen-lookups` apply
  directly; start here (it's also where SAP tooling helps).
- **B2B/EDI → managed-EDI / specialised platform** (target TBD). Do **not** assume a CPI rebuild is funded.
  The CPI-side lookups for EDI scenarios reuse the existing `pi-mapping` + Seeburger work.
- **Keep mapping/lookup logic target-neutral** where practical (see `artifact-conventions.md`) — the B2B
  target and even the A2A target (CPI vs **WSO2**) may still change.
- Use volume to prioritise: `parse_po_inventory.py` on `Syntax SAP PO Integrations.xlsx`.
