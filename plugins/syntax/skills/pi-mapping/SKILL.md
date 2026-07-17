---
description: 'Knowledge + tooling for migrating the SYNTAX SAP PI 7.1 ESR mappings to SAP CPI + Seeburger. Use when working with the .tpz transport packages (SYNTAX_EDI / SYNTAX_S4HC / SYNTAX_EDI_S4HC / SPS_S4HC) in the local Downloads folder: parse them, inventory ESR objects, trace mapping dependencies (source/target message, function libraries), extract EDI external-definition XSDs, or decode message-mapping logic (graphical tree + generated Java). Runs scripts/extract_tpz.py. Invoke before extracting Seeburger mappings or generating CPI lookup iFlows.'
---

# PI Mapping Knowledge (PI 7.1 → CPI + Seeburger)

This skill holds the knowledge and tooling about the SAP PI 7.1 ESR mappings that are being migrated
to **SAP CPI + Seeburger**. It lets you read what the mappings are, how they depend on each other,
and (with a decode step) what they actually do — the foundation for the later migration steps.

## Migration model

- **Seeburger** performs the **EDIFACT / VDA / ANSI X12** conversion (EDI standard ↔ XML).
- **SAP CPI** performs the **lookup** (reuse the skeleton at `C:\Users\itshaea\Downloads\cpi-lookup-template\`)
  and the **final processing**.
- These four PI transport packages are the source of truth for the mappings being split between them.

## Source packages (`C:\Users\itshaea\Downloads\`)

| `.tpz` | objects | role |
|---|---|---|
| `XI7_1_SYNTAX_EDI_1.0_of_syntax.com.tpz` | 381 | EDI standards side (EDIFACT/VDA/ANSI X12 structures + mappings) → **Seeburger-relevant** |
| `XI7_1_SYNTAX_S4HC_1.0_of_syntax.com.tpz` | 167 | S/4HANA Cloud side (CDM / S4HC message types + mappings) |
| `XI7_1_SYNTAX_EDI_S4HC_1.0_of_syntax.com.tpz` | 59 | **bridge**: CDM ↔ S4HC mappings (e.g. `MM_CO_EDI_INVOICE_REQUEST_OUT_cdm__2__INVOICE`) |
| `XI7_1_SPS_S4HC_1.0_of_syntax.com.tpz` | 240 | self-billing / SPS ↔ S4HC |

847 ESR objects total. A committed snapshot is in `reference/` (see below).

## Tooling — `scripts/extract_tpz.py` (pure-stdlib Python 3)

Run with Python (the source `.tpz` live in `C:\Users\itshaea\Downloads`):

```
SK="${CLAUDE_PLUGIN_ROOT}/skills/pi-mapping/scripts/extract_tpz.py"
python "$SK" inventory  <tpz...>                  # object table: package, typeID, type, name, namespace
python "$SK" graph      <tpz...>                  # mapping deps: source/target message, function libs
python "$SK" extdefs    <tpz> <outdir>            # write external-definition schemas (XSD/WSDL) to files
python "$SK" extract-mapping <tpz> <name> [outdir]  # decode a mapping: graphical-tree .xml + generated .java
python "$SK" report     <outdir> <tpz...>         # (re)generate the reference/ snapshot
python "$SK" lookups    <esr.tpz...>              # CONCRETE OData lookups per mapping: service/resource/$filter
python "$SK" configured <outdir> <config.tpz> <esr.tpz...>  # production scope: ICos -> configured mappings ->
                                                  #   the lookups actually used; writes configured-production.md
python "$SK" gen-lookups <outdir> <spec.json> <LOOKUP_TEMPLATE_dir>  # generate CPI lookup iFlows from a spec
```

**Lookup detection is by the function GUID wired into the mapping's graphical tree (a tf `brick`), NOT
the `UsedFuncLib` link** — the link over-counts (libraries are declared on a mapping but frequently not
called). Lookups are OData calls (`lookupWithURLParameter`/`lookupRequest` = GET, `postWithUrlParameter`/
`excuteBatchRequest` = POST/$batch) defined in the `*Lookup` function libraries; each call's
`odata_service` / resource (`A_…('%s')`) / `$filter` constants live in the brick bindings.

Regenerate the full snapshot:
```
python "$SK" report "${CLAUDE_PLUGIN_ROOT}/skills/pi-mapping/reference" \
  C:\Users\itshaea\Downloads\XI7_1_SYNTAX_S4HC_1.0_of_syntax.com.tpz \
  C:\Users\itshaea\Downloads\XI7_1_SYNTAX_EDI_1.0_of_syntax.com.tpz \
  C:\Users\itshaea\Downloads\XI7_1_SYNTAX_EDI_S4HC_1.0_of_syntax.com.tpz \
  C:\Users\itshaea\Downloads\XI7_1_SPS_S4HC_1.0_of_syntax.com.tpz
```

## Committed snapshot — `reference/`

- `inventory.csv` / `inventory.json` — every object: `package, typeID, type, name, namespace, oid`.
- `summary.md` — per-package counts by type + package roles.
- `mappings.md` — the **225 message mappings**: `source message → target message` + used function libraries.
- `external-definitions.md` — the `ifmextdef` schemas; the `SYNTAX_EDI` rows are the **Seeburger** EDI structures.
- `configured-production.md` — **the production scope** (from `XI7_1_SmartPressShop.tpz`): the 5 live
  Integrated Configurations, the 32 configured message mappings, and the **12 that actually invoke OData
  lookups** with concrete service / resource / `$filter` / source fields. This is the authoritative
  "only configured mappings are relevant" filter — start here for migration work.

For most "what exists / what depends on what" questions, read `reference/` directly — no need to re-parse.
Re-run `report` only after the `.tpz` files change.

## `.tpz` / `.tpt` format (so you can parse on demand)

- `.tpz` = ZIP. Members: `META-INF/*`, `Metadata.properties` (`numberOfXiObjs`, `swcv`), payload `*.tpt`
  (+ delta `*.dlt`). `META-INF/SAP_MANIFEST.MF` has `scname=` (the SWCV / package name).
- `.tpt` = binary SAP **DTR "versionset"** (signature `00 00 00 00 dc 35 8a 91 …`, **not** zip/gzip).
  ESR objects are stored inside it as concatenated, uncompressed XML documents — **split on the
  `<?xml` marker**; each object is `<p1:xiObj xmlns:p1="urn:sap-com:xi"> … </p1:xiObj>` followed by
  binary framing (cut the segment at `</p1:xiObj>`).
- **1 MB chunk markers:** the versionset injects an **8-byte marker** (`00 00 00 00` + 4 bytes) at
  ~1 MB file boundaries — even *inside* a large object's text. Strip every `\x00\x00\x00\x00` + 4 bytes
  before decoding (4 NULs never occur in valid XML/base64). The parser does this automatically; it is
  why large external-definition schemas and large mapping blobs come out clean.
- **`xiObj` anatomy:**
  - `p1:idInfo > p1:key typeID="…" oid="…"` + `p1:elem`×(1–2) = the object's **NAME** (+ **NAMESPACE**).
  - `p1:lnks > p1:lnkRole role="…" > p1:lnk > p1:key + p1:elem×2` = **dependency links**. Key roles:
    `SOURCE_IFR_MESS` (source message), `TARGET_IFR_MESS` (target message), `UsedFuncLib` (function
    library); operation mappings use `REQUEST_TRAFO` (→ message mapping), `INBOUND_IF`/`OUTBOUND_IF`.
  - mappings: `p1:content > tr:XiTrafo` with `tr:SourceStructure`, `tr:TargetStructure`, and `tr:blob`s.
- **`typeID` legend:** `XI_TRAFO`=Message Mapping · `MAPPING`=Operation Mapping · `FUNC_LIB`=Function
  Library (Java UDFs) · `TRAFO_JAR`=Imported Archive · `ifmtypedef`=Data Type · `ifmmessage`=Message
  Type · `ifmmessif`=Service Interface · `ifmextdef`=External Definition · `ifmfaultm`=Fault Message ·
  `namespdecl`=Namespace · `FOLDER`/`DOCU`.
- **Deep mapping content:** a mapping's `tr:blob` = `!zip!` + base64( ZIP(`value`) → ZIP(`metadata`) → payload).
  Payloads: the graphical mapping tree (`<mappingtool>` XML, ~125 KB) and the **generated Java source**
  (`package com.sap.xi.tf; …`, which imports `com.sap.aii.mapping.lookup.*` and `ValueMapping*` — i.e.
  lookups/value-mappings are embedded in the mappings). `extract-mapping` decodes these.

## Generating CPI lookup iFlows (`gen-lookups`)

Turns the extracted lookups into importable CPI iFlows by cloning the **`cpi-lookup-template`** LOOKUP
engine (`C:\Users\itshaea\Downloads\cpi-lookup-template\skeleton\LOOKUP_TEMPLATE`) and filling its tokens.

```
python "$SK" gen-lookups <outdir> specs/<scenario>.lookups.json \
  C:\Users\itshaea\Downloads\cpi-lookup-template\skeleton\LOOKUP_TEMPLATE
```

- **Specs** live in `specs/*.lookups.json` — one lookup definition per iFlow: `name, service, entity,
  filter_keys, select, filter, response_fields, result, edmx`. The command builds the `$select`+`$filter`,
  the content-modifier tables and the `<lookupResult>` body; writes a folder + importable `dist/<name>.zip`.
- **Reformulation:** PI key+nav reads `A_X('K')/to_Y` become the template's entity-set + `$filter`
  (`entity=A_Y`, `filter="<keyfield> eq '${header.<key>}'"`). This judgment (entity, `$select`,
  naming) lives in the spec; the command is purely mechanical.
- **edmx:** shared service metadata is staged in `edmx/` (e.g. `API_BUSINESS_PARTNER.edmx`); specs
  reference it by relative path, or `"zip:<artifact.zip>!<inner/path>.edmx"`.
- **Worked example:** `specs/delfor-out.lookups.json` → `LOOKUP_BP_ADDRESS` + `LOOKUP_BP_IDENTIFICATION`
  (output committed under `cpi-lookup-template/generated/DELFOR-out/`).
- **Deploy-time:** set `s4hc-instance` / `s4hc-credentials` (externalized params) to the real S/4HANA
  host + credential alias on import.

## Proposed Seeburger ↔ CPI split (refine per scenario)

- **→ Seeburger:** mappings that touch the EDI standard structures (EDIFACT/VDA/ANSI X12) + the
  `SYNTAX_EDI` external definitions. These are the EDI↔XML conversion mappings.
- **→ CPI:** the CDM ↔ S4HC bridge mappings (`SYNTAX_EDI_S4HC`, `SPS_S4HC`, `SYNTAX_S4HC`), the
  value-mapping / lookup logic (functions in `SyntaxEDI_Lookup`, `SyntaxS4HC_Lookup`, `ValueMapping*`),
  and final processing. Lookups are realized with `C:\Users\itshaea\Downloads\cpi-lookup-template\`.

Use `graph` / `mappings.md` to see which side a given mapping belongs to (EDI-facing source/target ⇒ Seeburger).

## How to use this skill

- **Inventory / dependency questions** → read `reference/inventory.*`, `mappings.md`, `summary.md`,
  `external-definitions.md`.
- **A specific mapping's logic** → `extract-mapping <tpz> <MM_name> <outdir>`, then read the `.xml`
  (graphical tree) and `.java` (generated source).
- **EDI schemas for Seeburger** → `extdefs <tpz> <outdir>` (use the `SYNTAX_EDI` package).
- **Fresh export** → re-run `report`.

## Next steps (later)

1. ✅ Concrete lookups extracted for the production scope — see `reference/configured-production.md`
   (OData service / resource / `$filter` / source fields per configured mapping).
2. **Generate CPI lookup iFlows** via `gen-lookups` + a `specs/<scenario>.lookups.json` (see above).
   ✅ DELFOR-out (`specs/delfor-out.lookups.json` → `generated/DELFOR-out/`: LOOKUP_BP_ADDRESS, LOOKUP_BP_IDENTIFICATION).
   ✅ DESADV CustomerSalesArea/PartnerFunction (`specs/desadv-custsales-partnerfunc.lookups.json` →
   `generated/DESADV/`: LOOKUP_CUSTSALES_PARTNERFUNC [one iFlow, PartnerFunction passed as a filter key =
   SH/CR; Supplier returned not server-filtered], LOOKUP_CUSTOMER_SALESAREA).
   NEXT: remaining DESADV lookups (BP address/identification, Equipment via API_EQUIPMENT, Batch via
   API_BATCH_SRV), INVOICE batch chars, inbound delivery (API_INBOUND_DELIVERY_SRV) — stage new edmx in `edmx/`.
3. **Extract Seeburger mappings** from the EDI-side mappings + external definitions (the EDIFACT/VDA/X12
   conversion that Seeburger takes over).
4. **Field-level transform extraction** for the configured CDM↔S4HC mappings (decode `<mappingtool>` tree)
   to rebuild the non-lookup mapping logic in CPI.
