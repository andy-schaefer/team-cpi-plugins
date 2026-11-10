#!/usr/bin/env python3
"""Scaffold a CPI iFlow bundle on disk (Model B) ready for step authoring + upload.

Writes the project skeleton and a starter .iflw copied from reference/templates/<type>.iflw with the
package/name/id/description placeholders filled. It does NOT invent task-specific steps — after this,
author those into the Local Integration Process using reference/steps/ and the type guidance in SKILL.md,
then run check_flow.py and cpi_upload_deploy.py.

Usage:
  python scaffold_iflow.py --package FIN01.BankingPayments --name "Payment File Encryption" \
      --type default --desc "decode base64 then PGP-encrypt" --out /path/to/output_parent
Produces <out>/<ArtifactId>/ with .project, META-INF/MANIFEST.MF, metainfo.prop,
src/main/resources/{parameters.prop,parameters.propdef,scenarioflows/integrationflow/<Name>.iflw}.
"""
import argparse, os, re, shutil

HERE = os.path.dirname(os.path.abspath(__file__))
TEMPLATES = os.path.join(os.path.dirname(HERE), "reference", "templates")

MANIFEST = """Manifest-Version: 1.0
Bundle-ManifestVersion: 2
Bundle-Name: {name}
Bundle-SymbolicName: {art_id}; singleton:=true
Bundle-Version: 1.0.0
SAP-BundleType: IntegrationFlow
SAP-NodeType: IFLMAP
SAP-RuntimeProfile: iflmap
Import-Package: com.sap.esb.application.services.cxf.interceptor,com.sap.esb.security,com.sap.it.op.agent.api,com.sap.it.op.agent.collector.camel,com.sap.it.op.agent.collector.cxf,com.sap.it.op.agent.mpl,org.apache.camel;version="2.8",org.apache.camel.builder;version="2.8",org.apache.camel.model;version="2.8",org.slf4j;version="1.6",org.osgi.framework;version="1.6.0"
Origin-Bundle-Name: {name}
Origin-Bundle-SymbolicName: {art_id}
"""

PROJECT = """<?xml version="1.0" encoding="UTF-8"?><projectDescription>
   <name>{art_id}</name>
   <comment/>
   <projects/>
   <buildSpec><buildCommand><name>org.eclipse.jdt.core.javabuilder</name><arguments/></buildCommand></buildSpec>
   <natures>
      <nature>org.eclipse.jdt.core.javanature</nature>
      <nature>com.sap.ide.ifl.project.support.project.nature</nature>
      <nature>com.sap.ide.ifl.bsn</nature>
   </natures>
</projectDescription>
"""

# minimal Model-B parameter set (senders prod+test). Add task params as needed.
PARAMS_PROP = """#Externalized configuration parameters. Defaults carry PRODUCTIVE values; override in TEST config.
SAP_Sender={sender}
SAP_Receiver=Receiver
SAP_MessageType={msgtype}
SAP_ApplicationId_XPath=//*[local-name()='MsgId']
Sender_Address=/{prefix}/{slug}
Sender_Authorization=RoleBased
Sender_UserRole=ESBMessaging.send
Sender_CSRF\\ Protected=1
Sender_Test_Address=/{prefix}/{slug}/test
Sender_Test_Authorization=RoleBased
Sender_Test_UserRole=ESBMessaging.send
Sender_Test_CSRF\\ Protected=1
logging=N
"""


def pascal(s):
    return "".join(w[:1].upper() + w[1:] for w in re.split(r"[^A-Za-z0-9]+", s) if w)


def propdef(names):
    items = "".join(
        f'<parameter><key/><name>{n}</name><type>xsd:string</type>'
        f'<isRequired>false</isRequired><constraint/><description/><additionalMetadata/></parameter>'
        for n in names)
    return ('<?xml version="1.0" encoding="UTF-8" standalone="no"?>'
            f'<parameters>{items}<param_references/></parameters>\n')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--package", required=True, help="PackageId, e.g. FIN01.BankingPayments")
    ap.add_argument("--name", required=True, help="iFlow name, e.g. Payment File Encryption")
    ap.add_argument("--type", default="default", choices=["default", "complex", "lookup"])
    ap.add_argument("--desc", default="")
    ap.add_argument("--out", required=True, help="parent dir; bundle written to <out>/<ArtifactId>")
    a = ap.parse_args()

    prefix = a.package.split(".")[0]
    art_id = f"{prefix}_{pascal(a.name)}"
    slug = pascal(a.name)
    root = os.path.join(a.out, art_id)
    res = os.path.join(root, "src", "main", "resources")
    iflowdir = os.path.join(res, "scenarioflows", "integrationflow")
    os.makedirs(os.path.join(root, "META-INF"), exist_ok=True)
    os.makedirs(iflowdir, exist_ok=True)

    open(os.path.join(root, ".project"), "w").write(PROJECT.format(art_id=art_id))
    open(os.path.join(root, "META-INF", "MANIFEST.MF"), "w").write(MANIFEST.format(name=f"{prefix} - {a.name}", art_id=art_id))
    open(os.path.join(root, "metainfo.prop"), "w").write(
        f"#Store metainfo properties\ndescription={a.desc}\nsource=\ntarget=\n")
    open(os.path.join(res, "parameters.prop"), "w").write(
        PARAMS_PROP.format(prefix=prefix, slug=slug, sender=prefix, msgtype=pascal(a.name)))
    names = ["SAP_Sender", "SAP_Receiver", "SAP_MessageType", "SAP_ApplicationId_XPath",
             "Sender_Address", "Sender_Authorization", "Sender_UserRole", "Sender_CSRF Protected",
             "Sender_Test_Address", "Sender_Test_Authorization", "Sender_Test_UserRole",
             "Sender_Test_CSRF Protected", "logging"]
    open(os.path.join(res, "parameters.propdef"), "w").write(propdef(names))

    tmpl = os.path.join(TEMPLATES, f"{a.type}.iflw")
    dst = os.path.join(iflowdir, f"{prefix} - {a.name}.iflw")
    if os.path.exists(tmpl):
        shutil.copyfile(tmpl, dst)
        note = f"copied template {a.type}.iflw (edit its Local Integration Process for your task)"
    else:
        shutil.copyfile(os.path.join(TEMPLATES, "default.iflw"), dst)
        note = f"NO {a.type}.iflw template yet -> used default.iflw; build {a.type} shape per SKILL.md"

    print(f"scaffolded: {root}")
    print(f"  artifact Id : {art_id}")
    print(f"  iflow file  : {dst}")
    print(f"  {note}")
    print("next: author task steps (reference/steps/), then check_flow.py, then cpi_upload_deploy.py")


if __name__ == "__main__":
    main()
