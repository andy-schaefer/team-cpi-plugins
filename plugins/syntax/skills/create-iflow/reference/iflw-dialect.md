# The `.iflw` BPMN2 dialect — structural rules

An `.iflw` is SAP's flavour of BPMN2. It uploads as part of a bundle zip but the **web editor** is the
strict validator: a structurally-complete file with a wrong step identifier uploads fine (HTTP 201) then
**fails to open**. Get the skeleton below right and use ONLY `reference/steps/` for step bodies.

## Top-level skeleton

```xml
<?xml version="1.0" encoding="UTF-8"?>
<bpmn2:definitions xmlns:bpmn2="http://www.omg.org/spec/BPMN/20100524/MODEL"
    xmlns:bpmndi="http://www.omg.org/spec/BPMN/20100524/DI"
    xmlns:dc="http://www.omg.org/spec/DD/20100524/DC"
    xmlns:di="http://www.omg.org/spec/DD/20100524/DI"
    xmlns:ifl="http:///com.sap.ifl.model/Ifl.xsd"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" id="Definitions_1">
  <bpmn2:collaboration id="Collaboration_1" name="Default Collaboration"> ... </bpmn2:collaboration>
  <bpmn2:process id="Process_Prod"  name="Production Process"> ... </bpmn2:process>
  <bpmn2:process id="Process_Test"  name="Test Process"> ... </bpmn2:process>
  <bpmn2:process id="Process_Local" name="<the work>"> ... </bpmn2:process>
  <bpmndi:BPMNDiagram id="BPMNDiagram_1" name="Default Collaboration Diagram">
    <bpmndi:BPMNPlane bpmnElement="Collaboration_1" id="BPMNPlane_1"> ...shapes + edges... </bpmndi:BPMNPlane>
  </bpmndi:BPMNDiagram>
</bpmn2:definitions>
```

Everything is expressed as `<ifl:property><key>..</key><value>..</value></ifl:property>` inside each
element's `<bpmn2:extensionElements>`.

## Collaboration

- One `IFlowConfiguration` property block (`cmdVariantUri=ctype::IFlowVariant/cname::IFlowConfiguration/version::1.2.4`).
- One `<bpmn2:participant ifl:type="EndpointSender">` **per sender** (prod + test).
- One `<bpmn2:participant ifl:type="IntegrationProcess" processRef="Process_X">` **per process**
  (prod, test, local). The Local Integration Process is referenced by ProcessCall steps, not by a sender.
- One `<bpmn2:messageFlow>` per sender → that process's StartEvent. HTTPS sender body is in
  `steps/sender-https.xml`.
- Receivers (if any) are `ifl:type="EndpointRecevier"` participants (note SAP's spelling **Recevier**)
  with a messageFlow from the calling ServiceTask.

## Process blocks

- **Main integration process** (prod/test): `cmdVariantUri=ctype::FlowElementVariant/cname::IntegrationProcess/version::1.2.1`,
  `transactionalHandling=Not Required`. Start/End are **message** events
  (`MessageStartEvent/version::1.0` + `<bpmn2:messageEventDefinition/>`; `MessageEndEvent/version::1.1`).
- **Local Integration Process**: `cname::LocalIntegrationProcess/version::1.1.3`, `processType=directCall`,
  `transactionalHandling=From Calling Process`. Start/End are **plain** events (`cname::StartEvent` /
  `cname::EndEvent`, `activityType=StartEvent`/`EndEvent`, NO messageEventDefinition).
- Steps are `<bpmn2:callActivity>` (most flow steps) or `<bpmn2:serviceTask>` (adapter calls / ExternalCall).

## Sequence flows — the #1 source of breakage

Every step has `<bpmn2:incoming>FlowId</bpmn2:incoming>` and `<bpmn2:outgoing>FlowId</bpmn2:outgoing>`,
and each FlowId must have exactly one `<bpmn2:sequenceFlow id="FlowId" sourceRef=".." targetRef=".."/>`
in the same process. Start has only outgoing; End only incoming. One outgoing per start (no duplicates).
Run `scripts/check_flow.py` — it catches dangling refs, orphan flows, and edges to missing elements.

## Diagram

Every element needs a `<bpmndi:BPMNShape bpmnElement="X" id="BPMNShape_X"><dc:Bounds .../></bpmndi:BPMNShape>`
and every sequenceFlow/messageFlow a `<bpmndi:BPMNEdge bpmnElement="Flow" id="BPMNEdge_Flow"
sourceElement="BPMNShape_src" targetElement="BPMNShape_tgt"><di:waypoint .../><di:waypoint .../></bpmndi:BPMNEdge>`.
Lay processes out on separate Y bands (prod ~y=40, test ~y=280, local ~y=540); events 32×32, call
activities 100×60, participants 100×140, subprocess ~360×120. Exact coordinates don't matter; presence does.

## Golden rule

If a step isn't in `reference/steps/`, don't hand-write it from memory. Find a **real deployed flow**
that uses it and copy the `callActivity`/`serviceTask` verbatim, then parameterise. The editor accepts
only the exact `activityType` + `cmdVariantUri` SAP ships.
