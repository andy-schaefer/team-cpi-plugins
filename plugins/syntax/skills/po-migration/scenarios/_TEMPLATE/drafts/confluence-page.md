# Draft Confluence page — __CUSTOMER__: __INTEGRATION__

> Draft only. Create on confirmation in space **CPI** (parent = customer/program page; analog baseline:
> "SmartPressShop AMS") via `mcp__jira__create_confluence_page`. Link the Jira task (SAPIP-25 child).

**Title:** `__CUSTOMER__: __INTEGRATION__ — PO→CPI Migration`

## Overview
- Customer / integration: __CUSTOMER__ / __INTEGRATION__
- Traffic class: A2A / B2B-EDI — Target: CPI / managed-EDI / WSO2
- Jira: SAPIP-XXX (epic SAPIP-25)
- Status: Draft / In progress / Done

## Source — SAP PO (as-is)
- Sender → Receiver, adapters, routing, mappings, lookups, acks.

## Target design (to-be)
- Connectivity & certificates
- Mapping design (source→target)
- Lookups (reused from `cpi-lookup-template`)
- Scripts
- Error handling / acknowledgements / monitoring

## Artifacts
| Type | Name | Location |
|---|---|---|
| Lookup / pre-mapper | | cpi-lookup-template/generated/__INTEGRATION__/ |
| Mapping | | |
| Script | | |

## Test & cutover
- Test cases / results
- Cutover & dual-run notes (deadline March 2027)

## Open points / risks
-
