# Analysis & design — __CUSTOMER__: __INTEGRATION__

## Classification (do this first)

- **Traffic class:** A2A  /  B2B-EDI   ← decides target + artifact set (see `../../reference/program-context.md`)
- **Target platform:** CPI  /  managed-EDI  /  WSO2  /  TBD
- **Rationale:**

> A2A → CPI rebuild (this skill + `cpi-lookup-template`). B2B/EDI → managed-EDI / specialised platform;
> CPI-side enrichment reuses `pi-mapping`. Watch the OFTP2 gap and the no-lift-&-shift rule for EDI mappings.

## Source (SAP PO) — as-is

- Sender → Receiver, adapters, routing, mapping(s) used:
- Value mappings / lookups / code lists:
- Error handling, acknowledgements, monitoring:

## Target design — to-be

- Adapters / connectivity (Cloud Connector, certs, auth):
- Mapping design (source→target; keep logic **target-neutral** where practical):
- Lookups needed (entity / key / service) → reuse `cpi-lookup-template` (`LOOKUP_<ENTITY>_<EXT>`):
- Scripts (Groovy / helpers):
- Routing / error handling / acks / monitoring:

## Artifacts (index — reuse, don't duplicate)

| Type | Name | Location / status |
|---|---|---|
| Lookup iFlow(s) | LOOKUP_… | `cpi-lookup-template/generated/__INTEGRATION__/` |
| Pre-mapper | PREMAP_… | `cpi-lookup-template/generated/__INTEGRATION__/` |
| Mapping(s) | | |
| Script(s) | | |
| Jira task | | `drafts/jira-task.md` → SAPIP-25 |
| Confluence page | | `drafts/confluence-page.md` → space CPI |

## Risks / open questions

- (OFTP2? Premium licensing? partner re-cert? dual-run window? March-2027 deadline impact?)

## Effort

~2 PD all-in (adjust: less for 1:1, more for complex/EDI). See `../../reference/artifact-conventions.md`.
