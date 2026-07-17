# Artifact conventions — what to build, where it lives, what to reuse

The point of this skill is to produce the **common artifacts** for each scenario by **reusing** existing
assets, not re-creating them. Per artifact type: where it lives, the naming convention, and what to reuse.

## Lookups (OData enrichment) — REUSE

- **Home:** `C:\Users\itshaea\Downloads\cpi-lookup-template\` (tokenized skeletons: `LOOKUP_TEMPLATE` =
  OData V2, `LOOKUP_TEMPLATE_V4` = OData V4 / A2X, `PREMAP_TEMPLATE` = source pre-mapper).
- **Generate with:** `pi-mapping\scripts\extract_tpz.py gen-lookups <outdir> <spec.json> <skeleton/LOOKUP_TEMPLATE[_V4]>`.
- **Spec:** `pi-mapping\specs\*.lookups.json` (entity set, `$select`/`$filter`, response fields, edmx; for
  A2X V4 add `service_path`). Stage the service `.edmx` in `pi-mapping\edmx\`.
- **Naming:** `LOOKUP_<ENTITY>_<EXT>`, `PREMAP_<MESSAGE>_<ENTITY>_<EXT>`.
- Generated iFlows + zips land under `cpi-lookup-template\generated\<SCENARIO>\` (+ `dist/`).

## Mappings — BUILD per scenario

- **A2A (→ CPI):** CPI message mappings / XSLT / Groovy. Keep the transformation logic documented in the
  scenario's `analysis.md` so it can target CPI **or WSO2** (see WSO2 section in `SKILL.md`).
- **B2B/EDI:** no lift-&-shift — rebuilt in **Integration Advisor (MIG/MAG)** or at the managed-EDI provider
  (see `program-context.md`). For the CPI-side enrichment of EDI scenarios, reuse `pi-mapping` knowledge.
- **Naming:** mirror the interface/scenario name; note source→target in `analysis.md`.

## Scripts (Groovy / helper) — BUILD, keep reusable

- CPI Groovy scripts for header/property handling, batching, ack handling, etc. Keep them parameterised and
  store reusable ones so later scenarios can share them. Existing examples are in `C:\Users\itshaea\Downloads\`
  (e.g. `addBatchCounter.groovy`, `getUniquePO.groovy`).

## Jira task — REUSE conventions (epic SAPIP-25)

- **Project** `SAPIP`; PO-migration **epic SAPIP-25**; issue type **Task**.
- **Title:** `<Customer>: <Integration>` (e.g. `Freudenberg: CATS`). English.
- **Estimate:** lean, ~**2 PD per interface** all-in (less for 1:1, more for complex/EDI). Do **not** pad
  with PM% + contingency.
- **Customer field** `customfield_11649` is mandatory on the create screen and **cannot be set via the MCP
  tool / API by name** → set it in the Jira UI after create. `parent` linking to the epic **does** work via
  `mcp__jira__jira_update_issue` (`{"parent":{"key":"SAPIP-25"}}`).
- See `jira-cpi-task` / `jira-mail-task` skills and memory `sapip-po-migration-epic`, `sapip-jira-ticketing`.
- Draft lives in `scenarios/<name>/drafts/jira-task.md`; create on confirmation.

## Confluence doc — space CPI

- **Space:** `CPI` (analog baseline page: "SmartPressShop AMS"). One page per scenario (or per customer with
  child pages).
- Content: overview, source PO interface, target design, mappings/lookups/scripts built, partner/EDI notes,
  test & cutover notes. Draft lives in `scenarios/<name>/drafts/confluence-page.md`; create on confirmation
  via `mcp__jira__create_confluence_page` (parent = the customer/program page).

## Target-neutrality

Where practical, document the **logic** (mapping rules, lookup keys, routing) independently of the runtime so
an artifact can be realised on **CPI or WSO2**. The runtime-specific build (iFlow vs WSO2 synapse/MI) is the
last step. See the WSO2 section in `SKILL.md`.
