---
description: 'Generate a deployable SAP CPI iFlow bundle from the team''s Model-B template conventions, then upload (and optionally deploy) it to a CPI tenant. Use when asked to create/scaffold a new iFlow. Request params: (1) iFlow name as "<PackageId> - <iFlow Name>", (2) type = default|complex|lookup, (3) a free-text task description. Produces a real .iflw BPMN bundle on disk (project + MANIFEST + parameters), validates it by POST to the tenant''s IntegrationDesigntimeArtifacts, and can deploy it. Invoke e.g. /syntax:create-iflow FIN01.BankingPayments - Payment File Encryption, type=default, "decode base64 then PGP-encrypt".'
---

# Create CPI iFlow (Model B scaffold → upload → deploy)

Generates a **deployable `.iflw` bundle** following the team's agreed conventions, writes it to disk,
and validates it against a real tenant. This skill exists because the SAP `.iflw` BPMN2 dialect is
**undocumented and unforgiving** — every flow-step has an exact `activityType` + `cmdVariantUri` that
the web editor must recognise, or the artifact uploads fine but then **fails to open** ("Error while
loading the details of the integration flow"). Do **not** invent step XML. Use the proven schemas in
`reference/iflw-dialect.md` and the step library in `reference/steps/`.

> Conventions come from Confluence space **CPI**: iFlow Template System design (**Model B**, page
> 2249064452), Best Practices (1655439361), Naming Conventions (2285666311). The design decision is
> **Model B** — one iFlow per message type; per-interface logic in a **Local Integration Process** called
> by both the production sender and a separate HTTPS **test** sender; the `Trace`/`Test`/`Archive` control
> flags live as **exchange properties**. `reference/model-b.md` summarises it.

## Request parameters

| Param | Form | Notes |
|---|---|---|
| **iFlow name** | `<PackageId> - <iFlow Name>` | e.g. `FIN01.BankingPayments - Payment File Encryption`. PackageId must already exist on the tenant (or pass `--create-package`). Artifact Id is derived: `<Prefix>_<PascalCaseName>` (e.g. `FIN01_PaymentFileEncryption`). |
| **type** | `default` \| `complex` \| `lookup` | See table below. |
| **task description** | free text | What the flow does. Drives which steps go into the Local Integration Process and the `metainfo.prop` description. |

### iFlow types (map to the Confluence design)

| type | What it scaffolds | Confluence basis |
|---|---|---|
| **default** | Simple Model-B iFlow: prod HTTPS sender + test HTTPS sender → one Local Integration Process (Content Modifier for `SAP_ApplicationId`/sender/receiver/msgtype → your task steps) → exception subprocess. **This is the validated FIN01 shape.** | §3 Model B main flow |
| **complex** | Generic message-processing iFlow: dynamic mapping to a message-dependent **CDM**, **loop over configured lookups**, join in a **postmap**, send out directly or via ProcessDirect, message-type identified by root-tag value mapping, `SAP_ApplicationId` by XPath. | §3 + brief "Generic message processing iFlow" |
| **lookup** | Lookup iFlow: loop over lookup sets, execute + collect, common **key/value XML request/response envelope** (§5.4 option B), exception → datastore + rethrow to caller. | §5.4, §6 lookup template |

> Honesty about maturity: **`default` is proven** (FIN01 deployed to SW-D). **`complex` and `lookup` are
> guided builds** — assemble from the validated step library, then ALWAYS validate by upload (below) and
> fix per the tenant's response before claiming done.

## Workflow

1. **Parse the request.** Split the name on the first ` - ` into PackageId + iFlow Name. Derive artifact
   Id (`<Prefix>_<PascalCase>`, strip spaces/punctuation). Pick the type. Read the task description.
2. **Confirm the target tenant.** Default **SW-D** (the `sap-cpi-dev` MCP). Confirm with the user before
   any write. The connection table is in the `cpi` skill (`SKILL.md` system config).
3. **Scaffold the bundle on disk:**
   ```
   python "${CLAUDE_PLUGIN_ROOT}/skills/create-iflow/scripts/scaffold_iflow.py" \
     --package "<PackageId>" --name "<iFlow Name>" --type <default|complex|lookup> \
     --desc "<task description>" --out "<target dir>"
   ```
   It writes `.project`, `META-INF/MANIFEST.MF`, `metainfo.prop`, `src/main/resources/parameters.prop`
   + `.propdef`, and a starter `.iflw` from `reference/templates/<type>.iflw` with placeholders filled.
4. **Author the task-specific steps** into the Local Integration Process, using ONLY the step XML in
   `reference/steps/` (content modifier, base64, pgp, mapping, lookup loop, request-reply, process call,
   router, groovy, exception subprocess). Wire `incoming`/`outgoing` sequence flows + a diagram shape and
   edge for each step. `reference/iflw-dialect.md` is the rulebook.
5. **Validate locally:** `xmllint --noout` the `.iflw`; run `scripts/check_flow.py` (every
   incoming/outgoing resolves to a sequenceFlow; every diagram edge points to a real element).
6. **Upload to the tenant (the real validator):**
   ```
   python "${CLAUDE_PLUGIN_ROOT}/skills/create-iflow/scripts/cpi_upload_deploy.py" \
     --system SW-D --package "<PackageId>" --id "<ArtifactId>" --name "<iFlow Name>" \
     --bundle "<target dir>" [--create-package] [--deploy]
   ```
   POST (create) or PUT (update) to `IntegrationDesigntimeArtifacts`. HTTP 201/200 = SAP's parser
   accepted the BPMN. Anything else → read the error, fix the offending step, re-upload.
7. **Open in the GUI** to confirm it hydrates (no "Error while loading the details…"). If it errors, a
   step's `activityType`/`cmdVariantUri` is wrong — compare against `reference/steps/`.
8. **Deploy** (optional, `--deploy`): async; poll runtime status to `STARTED`. If it sticks in `STARTING`,
   read `ErrorInformation/$value` — see the gotchas.

## Non-negotiable gotchas (learned the hard way)

- **Never invent step schemas.** Real examples live in `reference/steps/`; the originals were mined from
  deployed flows (`SCI_TM5_SendBankPayments` = PGP, `BYD_TM5_PaymentFileReplication` = Base64, and the
  fanuc Q2C flow = content modifier / process call / exception subprocess). When you need a step not in
  the library, find a real deployed flow that has it and copy its XML — do not guess.
- **PGP Encryptor** ≠ what you'd guess. It is `activityType=PgpEncrypt`,
  `cmdVariantUri=ctype::FlowstepVariant/cname::PgpEncrypt/version::1.0.3`, with keys `PgpSignatureOption`,
  `PgpContentEncryptionAlgorithm`, `PgpEncryptionUserIDs` (a `&lt;row>&lt;cell>ID&lt;/cell>&lt;/row>`
  table), `PgpArmored`, `PgpIntegrity`, `PgpCompressionAlgorithm`, `Key_Length`. A PGP flow will **deploy
  but hang in `STARTING`** with `UNRESOLVED (objectClass=...PGPPublicKeyringAccessor)` until a **PGP public
  keyring is uploaded to the tenant** (Monitor → Manage Security → PGP Keys) and the `PgpEncryptionUserIDs`
  matches a key's user ID. That's tenant provisioning, not a flow bug.
- **Base64** step: encode = `activityType=Encoder`,`encoderType=Base64 Encode`; decode =
  `activityType=Decoder`,`encoderType=Base64 Decode`; `componentVersion=1.0.0`, no cmdVariantUri.
- **Deploy needs a role** the service key may lack: `GenerationAndBuild.generationandbuildcontent`
  (deploy returns **403** without it). Upload/save only needs `WebToolingWorkspace.Write`.
- **The MCP cannot author or upload BPMN** — it only reads/deploys. Upload is the direct REST POST in
  `cpi_upload_deploy.py` (OAuth client_credentials + `X-CSRF-Token: Fetch` then POST/PUT). The OData
  service rejects `$select` (501) and `IntegrationDesigntimeArtifacts` isn't directly queryable (501) —
  list via package.
- **Naming** (space CPI 2285666311): artifact Id and display name both start with the package prefix;
  `SAP` prefix is forbidden; pick one case convention and keep it to avoid content-modifier/groovy typos.

## Files

- `reference/model-b.md` — the Model B shape, the three control flags, where per-interface logic lives.
- `reference/iflw-dialect.md` — the `.iflw` BPMN2 structure: definitions/collaboration/process/diagram,
  how senders attach, sequence-flow + diagram-edge rules, the HTTPS sender message-flow.
- `reference/steps/` — one file per proven flow-step (copy-paste XML with `@@PLACEHOLDERS@@`).
- `reference/templates/` — full starter `.iflw` per type (`default.iflw` = FIN01, validated).
- `scripts/scaffold_iflow.py` — write the bundle (project files + starter .iflw) with placeholders filled.
- `scripts/check_flow.py` — local integrity check (flow refs, diagram edges, well-formedness).
- `scripts/cpi_upload_deploy.py` — OAuth + CSRF + POST/PUT upload, optional package create + deploy + poll.

## Related

- **`cpi`** — tenant connection table (SW-D/SYN-D/MCA-*), list/deploy/status/logs/compare.
- **`po-migration`**, **`pi-mapping`** — upstream analysis that feeds a new iFlow's mappings/lookups.
