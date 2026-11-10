# Model B — the agreed iFlow shape

Source: Confluence CPI "iFlow Template System — Design Discussion" (page 2249064452). The team chose
**Model B**: one iFlow per message type, instantiated from a template. Not a generic per-direction flow.

## The shape

```
Collaboration
├─ Participant  S4_Payment (EndpointSender)   ──HTTPS──▶ StartEvent of  Production Process
├─ Participant  Test_Sender (EndpointSender)  ──HTTPS──▶ StartEvent of  Test Process
├─ Integration Process  PRODUCTION
│     Start(message) → ProcessCall(Local) → End(message)
├─ Integration Process  TEST
│     Start(message) → ContentModifier[set SAP_Trace=true, SAP_Test=true] → ProcessCall(Local) → End
└─ Local Integration Process  "<the work>"   ← the ONLY place the real logic lives
      Start → ContentModifier(flags normalise + routing props) → <task steps> → End
    + Exception Subprocess (Error Start → CM sets short custom error header → Error End)
```

Why two senders + one local process: the production endpoint and the HTTPS **test** endpoint both call
the same Local Integration Process, so test and prod run identical logic. The test sender pre-sets the
control flags; production doesn't.

## The three control flags (carried as EXCHANGE PROPERTIES)

| Flag (property) | Meaning | Default |
|---|---|---|
| `SAP_Trace` | emit extra MPL log/attachments in every step/subflow | `false` (negative) |
| `SAP_Archive` | persist incoming (unmodified) + final outbound message | `false` |
| `SAP_Test` | suppress real send-out (no POST leaves CPI) | `false` |

Properties survive external calls within an iFlow but are **lost across ProcessDirect**; headers survive
ProcessDirect but may be **dropped after an external call**. Rule: **properties are the source of truth,
normalise header→property on entry** (a first Content Modifier reads header→property with a safe
default), and **map property→header right before any ProcessDirect call**. Suggested names shared by
header and property: `SAP_Trace` / `SAP_Archive` / `SAP_Test`.

## Standard routing/log properties (Best Practices §6.1)

Set early (in the first Content Modifier of the Local Integration Process):
`SAP_Sender`, `SAP_Receiver`, `SAP_MessageType` (constants/params), and `SAP_ApplicationId` (XPath on the
payload — only AFTER any decode step, so the payload is parseable).

## Error handling (§5.6 + Best Practices §1.5)

- Exception subprocess in the Local Integration Process; MPL-attachment logging is **Trace-gated**,
  default negative.
- Prefer a short **custom header** (~200 char status) over an MPL attachment.
- Make logging configurable via a `logging` parameter so it can be toggled in prod with no redeploy.

## Externalised parameters (Best Practices §1.4)

No hardcoding. URLs, credentials, stage values, user roles, XPaths → `{{Param}}` externalised in
`parameters.prop` + `.propdef`. **Defaults carry PRODUCTIVE values**; override in the TEST configuration.
