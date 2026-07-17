# Integration intake questionnaire (SAP PO → CPI)

The detailed questions to ask per landscape and per integration scenario. Transcribed and expanded from
`C:\Users\itshaea\Downloads\SAP_PI_CarveOut_Questionnaire.xlsx` (sheets: Landscape_Questions,
Interface_Inventory, Communication_Channels, Certificates_and_Security, Dependencies_and_CarveOut_Scope),
plus a B2B/EDI addendum — the part that actually drives risk on this program (see `program-context.md`).

Ask the **landscape** questions once for the system; ask **sections 2–6** per integration scenario (each
new scenario gets its own `scenarios/<name>/intake.md`, scaffolded from `_TEMPLATE`).

## 1. Landscape (once per system)

- SAP PI/PO version and support package?
- Single stack or dual stack?
- Existing environments (DEV / QA / PROD) and their hostnames?
- Is ChaRM or other transport governance used?
- Total number of active interfaces?
- Number of interfaces relevant for the carve-out / migration?
- Target platform per traffic class: A2A → CPI; B2B/EDI → managed-EDI vs CPI Premium vs alternative (WSO2)?
- Hard dates / license end (PO license ends **March 2027** — see `program-context.md`)?

## 2. Interface inventory (per interface)

| Field | Ask |
|---|---|
| Interface_Name | logical name / scenario id |
| Sender_System | sending business system / party-component |
| Receiver_System | receiving business system / party-component |
| Protocol | HTTP(S)/SOAP/REST/IDoc/RFC/File/SFTP/JDBC/JMS/Mail/AS2/OFTP2 … |
| Adapter_Type | PO adapter (SOAP, REST, RFC, IDoc_AAE, File, SFTP, Mail, JDBC, B2B/Seeburger …) |
| Direction | Inbound / Outbound |
| Business_Owner | business contact |
| Technical_Owner | technical contact |
| Criticality | High / Medium / Low |
| Avg_Daily_Volume | messages/day (use `parse_po_inventory.py` for actuals) |
| Notes | quirks, SLAs, batch windows |

## 3. Communication channels (per channel)

- Channel_Name, Adapter_Type, Sender or Receiver?
- Authentication_Method (Basic / OAuth / client-cert / none)?
- Encryption (TLS, message-level, PGP)?
- Endpoint_or_Path (URL / directory / queue)?
- Certificates_Used (which, see section 4)?
- Proxy / Cloud Connector / on-prem reachability?

## 4. Certificates & security (per certificate)

- Certificate_Name, Used_For_Interface, Expiry_Date, System, Notes.
- Keystore location, renewal owner, who must re-issue for the new platform?

## 5. Dependencies & carve-out scope (per interface)

- Belongs_To: Remain_with_Source / Move_to_NewCo / Shared?
- Dependent_Systems (upstream/downstream that must move together)?
- Temporary_Transition_Interface needed (Yes/No) — bridge during dual-run?
- Notes (sequencing, data dependencies).

## 6. B2B/EDI addendum (ask when the scenario is B2B/EDI)

- EDI standard(s): VDA / EDIFACT / ANSI X12 — message types and versions?
- Transport: **OFTP2** / AS2 / SFTP / X.400 / VAN? (CPI has **no native OFTP2** — see `program-context.md`.)
- Trading partners: count, identifiers (GLN/DUNS/ILN), partner agreements?
- Acknowledgements: CONTRL / Functional Acknowledgement / AS2-MDN — required, and how monitored?
- Mapping complexity: 1:1 vs enriched (lookups), code lists, custom value mappings?
- Existing Seeburger / SAP B2B content to be re-built (no lift-&-shift — Integration Advisor MIG/MAG)?
- Re-certification needed with the partner after cutover?

## How to use

1. Scaffold a scenario: `python scripts/scaffold_scenario.py <name> --customer <C> --integration <I>`.
2. Fill `scenarios/<name>/intake.md` (sections 2–6) from the uploaded scenario export / interface doc.
3. Classify A2A vs B2B/EDI in `analysis.md` — that decides the target and the artifact set.
