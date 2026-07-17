#!/usr/bin/env python3
"""
extract_tpz.py - parse SAP PI 7.1 ESR transport packages (.tpz) for the PI -> CPI/Seeburger migration.

FORMAT (reverse-engineered):
  .tpz  = ZIP. Members: META-INF/*, Metadata.properties (numberOfXiObjs, swcv), payload *.tpt (+ *.dlt).
  .tpt  = binary SAP DTR "versionset" (signature 00 00 00 00 dc 35 8a 91 ...). ESR objects are stored
          inside it as concatenated, UNCOMPRESSED XML documents -> split on the b'<?xml' marker.
          Each object document is <p1:xiObj xmlns:p1="urn:sap-com:xi"> ... </p1:xiObj> followed by
          binary framing bytes (cut the segment at </p1:xiObj>).
  xiObj:
    p1:idInfo > p1:key typeID="..." oid="..." > two p1:elem  = the object's NAME and NAMESPACE.
    p1:lnks   > p1:lnkRole role="..." > p1:lnk > p1:key + two p1:elem = dependency links
                (SOURCE_IFR_MESS, TARGET_IFR_MESS, UsedFuncLib, value-mapping/other refs).
    p1:content > tr:XiTrafo (mappings): tr:SourceStructure/TargetStructure + tr:blob payloads.
  typeID legend: see TYPE_LABELS below. External definitions (ifmextdef) store plain XSD in
    p1:content > extdef category="xsd" > name + xml. Mapping logic (graphical tree / generated Java)
    lives in tr:blob = '!zip!' + base64( zip( 'value' -> zip( 'metadata' -> <mappingtool> XML ) ) ).

COMMANDS:
  inventory  <tpz...>                       print object table (package, typeID, type, name, namespace)
  graph      <tpz...>                       print mapping dependency edges (role -> linked object)
  extdefs    <tpz> <outdir>                 write external-definition schemas (EDIFACT/VDA/X12) to files
  extract-mapping <tpz> <name> [outdir]     decode a mapping's tr:blob payloads via nested-unzip
  report     <outdir> <tpz...>              write the committed reference snapshot:
                                            inventory.csv/.json, mappings.md, external-definitions.md,
                                            summary.md
  lookups    <esr.tpz...>                    list CONCRETE OData lookups actually invoked by each mapping
                                            (service / resource / $filter / source fields)
  configured <outdir> <config.tpz> <esr.tpz...>
                                            parse a production Integration-Directory export: live
                                            scenarios (ICos) -> configured operation/message mappings ->
                                            the lookups actually used, + channels. Writes
                                            configured-production.md
  gen-lookups <outdir> <spec.json> <LOOKUP_TEMPLATE_dir>
                                            generate CPI lookup-iFlow artifacts (folder + importable zip)
                                            from a lookup spec by cloning the cpi-lookup-template skeleton
                                            and filling its tokens (see cmd_gen_lookups for the spec format)
"""
import sys, os, re, io, csv, json, base64, zipfile
import xml.etree.ElementTree as ET

TYPE_LABELS = {
    "XI_TRAFO":   "Message Mapping",
    "MAPPING":    "Operation Mapping",
    "FUNC_LIB":   "Function Library",
    "TRAFO_JAR":  "Imported Archive",
    "ifmtypedef": "Data Type",
    "ifmmessage": "Message Type",
    "ifmmessif":  "Service Interface",
    "ifmextdef":  "External Definition",
    "ifmfaultm":  "Fault Message Type",
    "DOCU":       "Documentation",
    "FOLDER":     "Folder",
    "namespdecl": "Namespace Declaration",
    "ifmoper":    "Service Interface (operation)",
}

# 1 MB chunk-boundary marker the DTR versionset injects into large objects: 4 NUL bytes + 4 bytes.
# 4 consecutive NULs never occur in valid XML/base64 text, so stripping these reassembles the content.
_CHUNK = re.compile(rb'\x00\x00\x00\x00.{4}', re.DOTALL)

# ---------------------------------------------------------------- low-level parsing

def read_tpt(tpz):
    """Return the .tpt payload bytes from a .tpz."""
    with zipfile.ZipFile(tpz) as z:
        name = [n for n in z.namelist() if n.endswith(".tpt")][0]
        return z.read(name)

def swcv_name(tpz):
    """Software-component name, e.g. 'SYNTAX_EDI_S4HC' (from SAP_MANIFEST scname, fallback filename)."""
    try:
        with zipfile.ZipFile(tpz) as z:
            man = z.read("META-INF/SAP_MANIFEST.MF").decode("latin-1")
        m = re.search(r'scname="([^"]+)"', man)
        if m:
            return m.group(1)
    except Exception:
        pass
    base = os.path.basename(tpz)
    m = re.match(r'XI7_1_(.+?)_\d+\.\d+_of_', base)
    return m.group(1) if m else base

def iter_xiobjs(tpt_bytes):
    """Yield each xiObj as a decoded XML string (cut at </p1:xiObj>)."""
    starts = [m.start() for m in re.finditer(rb'<\?xml', tpt_bytes)] + [len(tpt_bytes)]
    for i in range(len(starts) - 1):
        seg = tpt_bytes[starts[i]:starts[i + 1]]
        if b'<p1:xiObj' not in seg[:200]:
            continue
        seg = _CHUNK.sub(b'', seg)          # strip 1 MB chunk-boundary markers
        s = seg.decode("latin-1")
        end = s.find("</p1:xiObj>")
        yield s[:end + 11] if end >= 0 else s

_KEY = re.compile(r'<p1:key typeID="([^"]*)"(?:\s+oid="([^"]*)")?\s*>\s*'
                  r'<p1:elem>([^<]*)</p1:elem>\s*<p1:elem>([^<]*)</p1:elem>')

_OWNKEY = re.compile(r'<p1:key typeID="([^"]*)"(?:\s+oid="([^"]*)")?\s*>(.*?)</p1:key>', re.DOTALL)

def parse_obj(seg):
    """The object's own identity = first p1:key (inside p1:idInfo). Keys carry one elem (namespace
    declarations, folders) or two (name + namespace)."""
    m = _OWNKEY.search(seg)
    if not m:
        return None
    typ, oid, inner = m.groups()
    elems = re.findall(r'<p1:elem>([^<]*)</p1:elem>', inner)
    name = elems[0] if elems else ""
    ns = elems[1] if len(elems) > 1 else ""
    return {"typeID": typ, "type": TYPE_LABELS.get(typ, typ),
            "name": name, "namespace": ns, "oid": oid or ""}

def parse_links(seg):
    """Dependency links from the p1:lnks block: list of (role, typeID, name, namespace)."""
    lo = seg.find("<p1:lnks>")
    if lo < 0:
        return []
    hi = seg.find("</p1:lnks>", lo)
    block = seg[lo:hi if hi > 0 else None]
    out = []
    # split into per-role chunks; first chunk is before any lnkRole -> skip
    chunks = re.split(r'(<p1:lnkRole\b[^>]*>)', block)
    for i in range(1, len(chunks), 2):
        role = re.search(r'role="([^"]*)"', chunks[i])
        role = role.group(1) if role else "?"
        body = chunks[i + 1] if i + 1 < len(chunks) else ""
        for km in _KEY.finditer(body):
            t, _oid, nm, ns = km.groups()
            out.append((role, t, nm, ns))
    return out

# ---------------------------------------------------------------- blob decoding (mappings)

def unwrap_blob(b64):
    """'!zip!'+base64 -> recursively de-zip single-entry archives -> return {entry_name: bytes}."""
    raw = base64.b64decode(b64)
    result = {}
    def descend(data, prefix=""):
        if data[:2] == b'PK':
            try:
                z = zipfile.ZipFile(io.BytesIO(data))
            except Exception:
                result[prefix or "blob"] = data
                return
            for n in z.namelist():
                descend(z.read(n), prefix + "/" + n if prefix else n)
        else:
            result[prefix or "blob"] = data
    descend(raw)
    return result

def extract_mapping(tpz, name, outdir):
    seg = None
    for s in iter_xiobjs(read_tpt(tpz)):
        o = parse_obj(s)
        if o and o["name"] == name:
            seg = s
            break
    if seg is None:
        sys.exit(f"mapping not found: {name}")
    os.makedirs(outdir, exist_ok=True)
    # each tr:blob, with the element that owns it (SourceCode / MetaData(graphical tree) / ByteCodeJar)
    written = []
    for owner, b64 in re.findall(r'<tr:(\w+)[^>]*>\s*<tr:blob[^>]*>!zip!([A-Za-z0-9+/=]+)', seg):
        for entry, data in unwrap_blob(b64).items():
            head = data[:300]
            printable = sum(1 for c in head if 9 <= c < 127) >= 0.9 * max(1, len(head))
            if head[:5] == b'<?xml':
                ext = ".xml"
            elif head[:2] == b'PK':
                ext = ".jar"
            elif printable and (b'class ' in head or b'import ' in head or b'package ' in head):
                ext = ".java"
            elif printable:
                ext = ".txt"
            else:
                ext = ".bin"
            fn = os.path.join(outdir, f"{name}.{owner}.{entry.replace('/', '_')}{ext}")
            with open(fn, "wb") as f:
                f.write(data)
            written.append((fn, len(data)))
    # also a direct tr:blob not wrapped in a known owner element
    for b64 in re.findall(r'<tr:blob[^>]*>!zip!([A-Za-z0-9+/=]+)', seg):
        pass
    for fn, n in written:
        print(f"  wrote {fn} ({n} bytes)")
    if not written:
        print("  (no tr:blob payloads found)")

# ---------------------------------------------------------------- external definitions

def iter_extdefs(seg):
    """Yield (category, filename, schema_text) for each <extdef> in an ifmextdef object."""
    for m in re.finditer(r'<extdef\s+category="([^"]*)"[^>]*>(.*?)</extdef>', seg, re.DOTALL):
        cat, body = m.group(1), m.group(2)
        nm = re.search(r'<name>([^<]*)</name>', body)
        xml = re.search(r'<xml>(.*)</xml>', body, re.DOTALL)
        if nm and xml:
            yield cat, nm.group(1), xml.group(1)

def cmd_extdefs(tpz, outdir):
    os.makedirs(outdir, exist_ok=True)
    n = 0
    for seg in iter_xiobjs(read_tpt(tpz)):
        o = parse_obj(seg)
        if not o or o["typeID"] != "ifmextdef":
            continue
        for cat, fname, schema in iter_extdefs(seg):
            safe = re.sub(r'[^\w.\-]', "_", fname) or f"{o['name']}.{cat}"
            path, k = os.path.join(outdir, safe), 1
            while os.path.exists(path):       # avoid clobbering same-named defs from different objects
                root, ext = os.path.splitext(safe)
                path = os.path.join(outdir, f"{root}_{k}{ext}")
                k += 1
            with open(path, "w", encoding="utf-8") as f:
                f.write(schema)
            n += 1
            print(f"  {o['name']} -> {os.path.basename(path)} ({len(schema)} chars, {cat})")
    print(f"{n} external definition file(s) written to {outdir}")

# ---------------------------------------------------------------- collection

def collect(tpzs):
    """Return list of (package, obj, links) across the given .tpz files."""
    rows = []
    for tpz in tpzs:
        pkg = swcv_name(tpz)
        for seg in iter_xiobjs(read_tpt(tpz)):
            o = parse_obj(seg)
            if not o:
                continue
            links = parse_links(seg) if o["typeID"] in ("XI_TRAFO", "MAPPING") else []
            rows.append((pkg, o, links))
    return rows

# ---------------------------------------------------------------- commands

def cmd_inventory(tpzs):
    rows = collect(tpzs)
    print(f"{'PACKAGE':22} {'TYPE':22} NAME")
    for pkg, o, _ in sorted(rows, key=lambda r: (r[0], r[1]["type"], r[1]["name"])):
        print(f"{pkg:22} {o['type']:22} {o['name']}")
    print(f"\n{len(rows)} objects")

def cmd_graph(tpzs):
    for pkg, o, links in collect(tpzs):
        if not links:
            continue
        print(f"\n[{pkg}] {o['type']}: {o['name']}")
        for role, t, nm, ns in links:
            print(f"    {role:18} -> {TYPE_LABELS.get(t, t)}: {nm}")

def cmd_report(outdir, tpzs):
    os.makedirs(outdir, exist_ok=True)
    rows = collect(tpzs)

    # inventory.csv / .json
    recs = [dict(package=p, **o) for p, o, _ in rows]
    with open(os.path.join(outdir, "inventory.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["package", "typeID", "type", "name", "namespace", "oid"])
        w.writeheader()
        w.writerows(recs)
    with open(os.path.join(outdir, "inventory.json"), "w", encoding="utf-8") as f:
        json.dump(recs, f, indent=1, ensure_ascii=False)

    # summary.md
    from collections import Counter, defaultdict
    by_pkg = defaultdict(Counter)
    for p, o, _ in rows:
        by_pkg[p][o["type"]] += 1
    roles = {
        "SYNTAX_EDI": "EDI standards side (EDIFACT/VDA/ANSI X12) -> Seeburger-relevant",
        "SYNTAX_S4HC": "S/4HANA Cloud side (CDM/S4HC message types + mappings)",
        "SYNTAX_EDI_S4HC": "Bridge: CDM <-> S4HC mappings",
        "SPS_S4HC": "Self-billing / SPS <-> S4HC",
    }
    with open(os.path.join(outdir, "summary.md"), "w", encoding="utf-8") as f:
        f.write("# ESR object inventory - summary\n\n")
        f.write(f"Total objects: **{len(rows)}** across {len(by_pkg)} packages. ")
        f.write("Generated by `scripts/extract_tpz.py report`.\n\n")
        for p in sorted(by_pkg):
            f.write(f"## {p}\n\n_{roles.get(p, '')}_\n\n")
            f.write(f"Objects: {sum(by_pkg[p].values())}\n\n")
            f.write("| Type | Count |\n|---|---|\n")
            for t, c in by_pkg[p].most_common():
                f.write(f"| {t} | {c} |\n")
            f.write("\n")

    # mappings.md (message mappings + their source/target/funclibs)
    with open(os.path.join(outdir, "mappings.md"), "w", encoding="utf-8") as f:
        f.write("# Message mappings (XI_TRAFO) - dependency graph\n\n")
        f.write("source message -> [mapping] -> target message, plus used function libraries. ")
        f.write("Field-level logic is in the `tr:blob` payloads (decode with `extract-mapping`).\n")
        for p, o, links in sorted(rows, key=lambda r: (r[0], r[1]["name"])):
            if o["typeID"] != "XI_TRAFO":
                continue
            byrole = {}
            for role, t, nm, ns in links:
                byrole.setdefault(role, []).append(nm)
            src = ", ".join(byrole.get("SOURCE_IFR_MESS", [])) or "-"
            tgt = ", ".join(byrole.get("TARGET_IFR_MESS", [])) or "-"
            fl = ", ".join(byrole.get("UsedFuncLib", []))
            f.write(f"\n### `{o['name']}`\n")
            f.write(f"- package: {p}  |  namespace: `{o['namespace']}`\n")
            f.write(f"- source: `{src}`  ->  target: `{tgt}`\n")
            if fl:
                f.write(f"- function libraries: {fl}\n")
            other = {r: v for r, v in byrole.items()
                     if r not in ("SOURCE_IFR_MESS", "TARGET_IFR_MESS", "UsedFuncLib")}
            for r, v in other.items():
                f.write(f"- {r}: {', '.join(v)}\n")

    # external-definitions.md (EDI structures = Seeburger-relevant)
    with open(os.path.join(outdir, "external-definitions.md"), "w", encoding="utf-8") as f:
        f.write("# External definitions (`ifmextdef`)\n\n")
        f.write("Imported schemas (XSD/WSDL). Two flavours: **EDI message structures** "
                "(EDIFACT/VDA/ANSI X12, in `SYNTAX_EDI`) are the **Seeburger-relevant** ones; the rest "
                "are S4HC / SPS service-API structures (CPI side). "
                "Extract the schema files with `extract_tpz.py extdefs <tpz> <outdir>`.\n\n")
        f.write("| Package | Name | Namespace |\n|---|---|---|\n")
        for p, o, _ in sorted(rows, key=lambda r: (r[0], r[1]["name"])):
            if o["typeID"] == "ifmextdef":
                f.write(f"| {p} | {o['name']} | `{o['namespace']}` |\n")

    print(f"Wrote inventory.csv, inventory.json, summary.md, mappings.md, external-definitions.md "
          f"to {outdir}  ({len(rows)} objects)")

# ---------------------------------------------------------------- lookups (concrete)

_DATAFN = re.compile(r'<name>(lookupWithURLParameter|lookupRequest|lookupRequest2|'
                     r'postWithUrlParameter|excuteBatchRequest)</name>\s*<key>([^<]+)</key>')

def lookup_function_keys(tpzs):
    """{function-key GUID: (library, function)} for the lookup data-functions across the libraries."""
    k2f = {}
    for tpz in tpzs:
        for seg in iter_xiobjs(read_tpt(tpz)):
            o = parse_obj(seg)
            if not o or o["typeID"] != "FUNC_LIB" or "lookup" not in o["name"].lower():
                continue
            for _bt, b64 in re.findall(r'<(\w+):blob[^>]*>!zip!([A-Za-z0-9+/=]+)', seg):
                for d in unwrap_blob(b64).values():
                    if d[:5] == b'<?xml' and b'functionstorage' in d[:200]:
                        for fn, ky in _DATAFN.findall(d.decode('utf-8', 'replace')):
                            k2f[ky] = (o["name"], fn)
    return k2f

def _mapping_tree_bytes(seg):
    for _bt, b64 in re.findall(r'<(\w+):blob[^>]*>!zip!([A-Za-z0-9+/=]+)', seg):
        for d in unwrap_blob(b64).values():
            if d[:5] == b'<?xml' and b'mappingtool' in d[:300]:
                return d
    return b""

def _classify(consts):
    """Sort a lookup brick's constant inputs into OData service / resource / $filter / other."""
    service = resource = filt = None
    other = []
    for v in consts:
        v = v.strip()
        if not v:
            continue
        if v.startswith('API_') or 'odata/sap/' in v or v.endswith('_SRV'):
            service = service or v
        elif ' eq ' in v or (' and ' in v and "'" in v):
            filt = filt or v
        elif v.startswith('A_') or "('%s')" in v or '/to_' in v:
            resource = resource or v
        else:
            other.append(v)
    return service, resource, filt, other

def _walk_args(el, keyset, consts, srcs):
    """Collect constant values + source paths feeding a lookup brick, NOT descending into nested
    lookup bricks (those are reported as their own lookup)."""
    for child in el:
        if child.tag == 'brick' and child.get('type') == 'Func' and child.get('fname') in keyset:
            continue
        if child.tag == 'brick' and child.get('type') == 'Src' and child.get('path'):
            srcs.append(child.get('path'))
        if child.tag == 'value' and (child.text or '').strip():
            consts.append(child.text.strip())
        _walk_args(child, keyset, consts, srcs)

def extract_lookups(seg, k2f):
    """List the concrete lookups a mapping invokes: [{lib, fn, service, resource, filter, other, sources}]."""
    raw = _mapping_tree_bytes(seg)
    if not raw:
        return []
    try:
        root = ET.fromstring(raw)
    except ET.ParseError:
        return []
    keyset = set(k2f)
    out = []
    for br in root.iter('brick'):
        if br.get('type') == 'Func' and br.get('fname') in keyset:
            lib, fn = k2f[br.get('fname')]
            consts, srcs = [], []
            _walk_args(br, keyset, consts, srcs)
            service, resource, filt, other = _classify(consts)
            out.append(dict(lib=lib, fn=fn, service=service, resource=resource,
                            filter=filt, other=other, sources=srcs))
    return out

def cmd_lookups(tpzs):
    k2f = lookup_function_keys(tpzs)
    total = 0
    for tpz in tpzs:
        for seg in iter_xiobjs(read_tpt(tpz)):
            o = parse_obj(seg)
            if not o or o["typeID"] != "XI_TRAFO":
                continue
            lks = extract_lookups(seg, k2f)
            if not lks:
                continue
            total += 1
            print(f"\n{o['name']}  ({len(lks)} lookup call(s))")
            for k in lks:
                print(f"   {k['lib']}.{k['fn']}: service={k['service']} resource={k['resource']} "
                      f"filter={k['filter']!r}")
                if k['sources']:
                    print(f"      keys <- {', '.join(k['sources'][:4])}")
    print(f"\n{total} mappings invoke at least one lookup.")

# ---------------------------------------------------------------- configuration (Integration Directory)

def _channel_info(seg):
    """Best-effort (adapter, endpoint) for a Channel object."""
    adapters = [a for a in ('OFTP', 'File', 'EDISeparator', 'SOAP', 'REST', 'OData', 'JDBC', 'JMS',
                            'Mail', 'RFC', 'HTTP') if a.lower() in seg.lower()]
    url = re.search(r'(https?://(?!sap\.com/xi/)[^\s<"]+|/sap/opu/odata/[^\s<"]+)', seg)
    host = re.search(r'<Name>[^<]*(?:[Hh]ost|[Ss]erver)[^<]*</Name>\s*<Namespace[^>]*/>\s*<Value>([^<]+)</Value>', seg)
    return (adapters[0] if adapters else '?'), (url.group(1) if url else (host.group(1) if host else ''))

def cmd_configured(outdir, config_tpz, esr_tpzs):
    os.makedirs(outdir, exist_ok=True)
    k2f = lookup_function_keys(esr_tpzs)

    # index ESR: operation-mapping -> message mappings, and message-mapping -> concrete lookups
    om_mm, mm_lookups = {}, {}
    for tpz in esr_tpzs:
        for seg in iter_xiobjs(read_tpt(tpz)):
            o = parse_obj(seg)
            if not o:
                continue
            if o["typeID"] == "MAPPING":
                om_mm.setdefault(o["name"], []).extend(
                    nm for r, t, nm, ns in parse_links(seg) if t == "XI_TRAFO")
            elif o["typeID"] == "XI_TRAFO" and o["name"] not in mm_lookups:
                mm_lookups[o["name"]] = extract_lookups(seg, k2f)

    # config: ICos + channels
    icos, channels = [], []
    for seg in iter_xiobjs(read_tpt(config_tpz)):
        o = parse_obj(seg)
        if not o:
            continue
        if o["typeID"] == "AllInOne":
            links = parse_links(seg)
            snd = next((nm for r, t, nm, ns in links if r == "senderOperation"), None)
            oms = []
            for r, t, nm, ns in links:
                if t == "MAPPING" and nm not in oms:
                    oms.append(nm)
            icos.append((o["namespace"], snd, oms))
        elif o["typeID"] == "Channel":
            ad, ep = _channel_info(seg)
            channels.append((o["namespace"], o["name"], ad, ep))

    conf_mms = []
    for _ns, _snd, oms in icos:
        for om in oms:
            for mm in om_mm.get(om, []):
                if mm not in conf_mms:
                    conf_mms.append(mm)
    relevant = [m for m in conf_mms if mm_lookups.get(m)]

    out = os.path.join(outdir, "configured-production.md")
    with open(out, "w", encoding="utf-8") as f:
        f.write(f"# Configured production scope — {os.path.basename(config_tpz)}\n\n")
        f.write("Generated by `extract_tpz.py configured`. Only mappings wired into an Integrated "
                "Configuration (ICo) below are live; everything else in the ESR is unused/legacy.\n\n")
        f.write(f"- Integrated Configurations (scenarios): **{len(icos)}**\n")
        f.write(f"- Configured operation mappings → message mappings: **{len(conf_mms)}**\n")
        f.write(f"- Of those, mappings that actually invoke an OData lookup: **{len(relevant)}**\n\n")

        f.write("## Live scenarios\n")
        for ns, snd, oms in icos:
            f.write(f"\n**ICo `{ns}`** — sender op `{snd or '?'}`\n")
            for om in oms:
                f.write(f"  - {om}\n")

        f.write("\n## Concrete lookups (configured mappings only)\n")
        f.write("\nEach lookup → OData **service** / **resource** (entity, `%s` = key from source) / "
                "**$filter**, with the source fields supplying the keys. These become CPI lookup iFlows.\n")
        for mm in relevant:
            f.write(f"\n### `{mm}`\n")
            for k in mm_lookups[mm]:
                f.write(f"- **{k['service'] or '?'}** · `{k['resource'] or '?'}`"
                        f"{' · filter `'+k['filter']+'`' if k['filter'] else ''}\n")
                if k['other']:
                    f.write(f"    - params: {', '.join(k['other'][:6])}\n")
                if k['sources']:
                    f.write(f"    - keys ← {', '.join(k['sources'][:5])}\n")

        f.write("\n## Channels (Integration Directory)\n\n| Party/Service | Channel | Adapter | Endpoint |\n|---|---|---|---|\n")
        for ns, nm, ad, ep in channels:
            f.write(f"| {ns} | {nm} | {ad} | {ep} |\n")

        f.write("\n## Notes\n")
        f.write("- Lookup detection is by the function GUID actually wired into the mapping's graphical "
                "tree (a tf `brick`), not the `UsedFuncLib` link — the latter over-counts (libraries are "
                "declared but often not called).\n")
        f.write("- `%s` placeholders in a resource/filter are filled at runtime from the listed source "
                "fields.\n- The OData host comes from the channel; the lookup base path is `/sap/opu/odata/sap/<service>`.\n")

    print(f"Wrote {out}")
    print(f"  scenarios={len(icos)}  configured mappings={len(conf_mms)}  with-lookups={len(relevant)}")
    for mm in relevant:
        svcs = sorted({k['service'] for k in mm_lookups[mm] if k['service']})
        print(f"   - {mm}: {len(mm_lookups[mm])} lookup(s) -> {', '.join(svcs)}")

# ---------------------------------------------------------------- generate CPI lookup iFlows

def _cell(i, v):
    return f"&lt;cell id='{i}'&gt;{v}&lt;/cell&gt;"

def _row(xpath, name):
    v = xpath.replace("'", "&amp;apos;")
    return ("&lt;row&gt;" + _cell('Action', 'Create') + _cell('Type', 'xpath') + _cell('Value', v) +
            _cell('Default', '') + _cell('Name', name) + _cell('Datatype', 'java.lang.String') + "&lt;/row&gt;")

def _req_header_table(filter_keys):
    rows = [_row(f"//filter[key='{k}']/value", k) for k in filter_keys]
    rows.append(_row("/lookupParameter/lookups/lookup", "LookupName"))
    return "".join(rows)

def _resp_header_table(fields):
    return "".join(_row(f"//{f}", f) for f in fields)

def _result_body(pairs):
    out = ["&lt;lookupResult&gt;", "\t&lt;results&gt;",
           "\t\t&lt;lookupName&gt;${header.LookupName}&lt;/lookupName&gt;"]
    for key, expr in pairs:
        out.append(f"\t\t&lt;result&gt;&lt;key&gt;{key}&lt;/key&gt;&lt;value&gt;{expr}&lt;/value&gt;&lt;/result&gt;")
    out += ["\t&lt;/results&gt;", "&lt;/lookupResult&gt;"]
    return "\n".join(out)

def _load_edmx(val, specdir):
    """edmx spec value: 'zip:<zip>!<inner>' or a file path (absolute or relative to the spec file)."""
    if not val:
        return None
    if val.startswith("zip:"):
        zp, inner = val[4:].split("!", 1)
        zp = zp if os.path.isabs(zp) else os.path.join(specdir, zp)
        with zipfile.ZipFile(zp) as z:
            return z.read(inner)
    p = val if os.path.isabs(val) else os.path.join(specdir, val)
    with open(p, "rb") as f:
        return f.read()

def _zip_dir(srcdir, zippath):
    with zipfile.ZipFile(zippath, "w", zipfile.ZIP_DEFLATED) as z:
        for root, _dirs, files in os.walk(srcdir):
            for fn in files:
                full = os.path.join(root, fn)
                z.write(full, os.path.relpath(full, srcdir).replace("\\", "/"))

def cmd_gen_lookups(outdir, spec_path, template_dir):
    """Generate CPI lookup-iFlow artifacts (folder + importable zip) from a lookup spec by cloning a
    cpi-lookup-template skeleton and filling its tokens. Spec JSON:
      { "lookups": [ {
          "name","description","service","entity",
          "service_path": "<OData address segment after the base; defaults to 'service'>",
          "filter_keys": [<incoming <filter> keys -> headers used in $filter>],
          "select": [<OData $select fields>], "filter": "<$filter expr, may use ${header.<key>}>",
          "response_fields": [<OData response fields to extract into headers>],
          "result": [["<resultKey>","<valueExpr e.g. ${header.X}>"], ...],
          "edmx": "zip:<zip>!<inner>" | "<path>",  "version": "1.0.0" } ] }
    The $select+$filter, the content-modifier tables and the <lookupResult> body are built from the spec.
    Pick the template by OData version: LOOKUP_TEMPLATE (OData V2, base /sap/opu/odata/sap/<service>) or
    LOOKUP_TEMPLATE_V4 (OData V4 / A2X, base /sap/opu/odata4/sap/<service_path>). 'service' names the edmx
    file (no slashes); for A2X V4 set 'service_path' to the full path segment, e.g.
    'api_handlingunit/srvd_a2x/sap/handlingunit/0001' (fills __ODATA_SERVICE_PATH__ in the V4 template).
    """
    spec = json.load(open(spec_path, encoding="utf-8"))
    specdir = os.path.dirname(os.path.abspath(spec_path))
    os.makedirs(outdir, exist_ok=True)
    distdir = os.path.join(outdir, "dist")
    os.makedirs(distdir, exist_ok=True)
    for lk in spec["lookups"]:
        query = "$select=" + ",".join(lk["select"]) + "&amp;$filter=" + lk["filter"]
        tok = {
            "__LOOKUP_NAME__": lk["name"], "__DESCRIPTION__": lk.get("description", ""),
            "__ODATA_SERVICE__": lk["service"], "__ENTITY_SET__": lk["entity"],
            "__ODATA_SERVICE_PATH__": lk.get("service_path", lk["service"]),
            "__QUERY_OPTIONS__": query, "__EDMX_PATH__": "edmx/" + lk["service"] + ".edmx",
            "__REQUEST_PARAM_HEADERS__": _req_header_table(lk.get("filter_keys", [])),
            "__REQUEST_PARAM_PROPERTIES__": "",
            "__RESPONSE_FIELD_HEADERS__": _resp_header_table(lk.get("response_fields", [])),
            "__RESULT_BODY__": _result_body(lk["result"]),
        }
        version = lk.get("version", "1.0.0")
        dest = os.path.join(outdir, lk["name"])
        for root, _dirs, files in os.walk(template_dir):
            for fn in files:
                if fn == "__PUT_service_edmx_HERE.md":
                    continue
                sp = os.path.join(root, fn)
                rel = os.path.relpath(sp, template_dir).replace("__LOOKUP_NAME__.iflw", lk["name"] + ".iflw")
                dp = os.path.join(dest, rel)
                os.makedirs(os.path.dirname(dp), exist_ok=True)
                t = open(sp, encoding="utf-8", newline="").read()
                for k, v in tok.items():
                    t = t.replace(k, v)
                t = re.sub(r'Bundle-Version: [0-9.]+', 'Bundle-Version: ' + version, t)
                open(dp, "w", encoding="utf-8", newline="").write(t)
        edmx = _load_edmx(lk.get("edmx"), specdir)
        edmx_dir = os.path.join(dest, "src", "main", "resources", "edmx")
        os.makedirs(edmx_dir, exist_ok=True)
        if edmx is not None:
            open(os.path.join(edmx_dir, lk["service"] + ".edmx"), "wb").write(edmx)
        else:
            open(os.path.join(edmx_dir, f"__PUT_{lk['service']}_edmx_HERE.md"), "w",
                 encoding="utf-8").write(f"Drop {lk['service']}.edmx here (edmxFilePath already points to it).")
        _zip_dir(dest, os.path.join(distdir, lk["name"] + ".zip"))
        print(f"  {lk['name']}: {lk['service']}/{lk['entity']}  ->  dist/{lk['name']}.zip"
              f"{'' if edmx is not None else '  (edmx MISSING - add it)'}")
    print(f"{len(spec['lookups'])} lookup iFlow(s) -> {outdir}")

# ---------------------------------------------------------------- main

def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 1
    cmd = argv[1]
    if cmd == "inventory":
        cmd_inventory(argv[2:])
    elif cmd == "graph":
        cmd_graph(argv[2:])
    elif cmd == "extdefs":
        cmd_extdefs(argv[2], argv[3])
    elif cmd == "extract-mapping":
        extract_mapping(argv[2], argv[3], argv[4] if len(argv) > 4 else ".")
    elif cmd == "report":
        cmd_report(argv[2], argv[3:])
    elif cmd == "lookups":
        cmd_lookups(argv[2:])
    elif cmd == "configured":
        cmd_configured(argv[2], argv[3], argv[4:])
    elif cmd == "gen-lookups":
        cmd_gen_lookups(argv[2], argv[3], argv[4])
    else:
        print(__doc__)
        return 1
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))
