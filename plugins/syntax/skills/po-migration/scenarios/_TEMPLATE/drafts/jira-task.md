# Draft Jira task — __CUSTOMER__: __INTEGRATION__

> Draft only. Create on confirmation. Project **SAPIP**, type **Task**, epic **SAPIP-25**.
> Conventions: `../../../reference/artifact-conventions.md` + memory `sapip-po-migration-epic`,
> `sapip-jira-ticketing`. After create: set **Customer** field (`customfield_11649`) in the Jira UI — the
> MCP tool can't set it; link the epic via `jira_update_issue {"parent":{"key":"SAPIP-25"}}` (that works).

- **Project:** SAPIP
- **Issue type:** Task
- **Epic / parent:** SAPIP-25
- **Summary:** `__CUSTOMER__: __INTEGRATION__`
- **Customer (customfield_11649):** __CUSTOMER__  *(set in UI after create)*
- **Estimate:** ~2 PD all-in *(adjust for complexity)*

## Description (Markdown → ADF)

### Ausgangslage / Source (SAP PO)
- Interface: __INTEGRATION__
- Sender → Receiver:
- Adapter / protocol:

### Ziel / Target (CPI / …)
- Target platform + design summary:
- Mappings / lookups / scripts to build (reuse `cpi-lookup-template`):

### Aufgaben
- [ ] Anforderung & PO-Bestand analysieren (intake.md)
- [ ] Zieldesign festlegen (A2A→CPI / B2B→managed/alt) — analysis.md
- [ ] Mapping(s) umsetzen
- [ ] Lookups generieren (cpi-lookup-template / gen-lookups)
- [ ] Connectivity & Zertifikate einrichten
- [ ] Unit- & Integrationstest
- [ ] Dokumentation (Confluence, Space CPI)
- [ ] Cutover / Dual-Run-Plan (Stichtag März 2027)
