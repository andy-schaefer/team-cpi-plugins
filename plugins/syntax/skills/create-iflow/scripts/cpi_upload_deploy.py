#!/usr/bin/env python3
"""Upload (and optionally deploy) a CPI iFlow bundle to an Integration Suite tenant.

The sap-cpi-dev MCP can read/deploy but CANNOT upload BPMN, so this does the direct REST dance:
OAuth client_credentials -> X-CSRF-Token: Fetch -> POST (create) / PUT (update)
IntegrationDesigntimeArtifacts with the base64'd bundle zip -> optional deploy + status poll.

System connection (TokenUrl/ClientId/ApiUrl) comes from the `cpi` skill's table; the client SECRET
comes from env (never the repo): CPI_<SYS>_CLIENT_SECRET, with a non-hyphenated fallback
CPI_<SYSNOHYPHEN>_CLIENT_SECRET because ${VAR} expansion can't resolve a hyphen (e.g. SW-D ->
CPI_SWD_CLIENT_SECRET). Run with `python -I` when reading untrusted dirs.

Usage:
  python cpi_upload_deploy.py --system SW-D --package FIN01.BankingPayments \
      --id FIN01_PaymentFileEncryption --name "FIN01 - Payment File Encryption" \
      --bundle /path/to/FIN01_PaymentFileEncryption [--create-package] [--deploy]
"""
import argparse, base64, io, json, os, sys, time, urllib.parse, urllib.request, zipfile

# TokenUrl / ClientId / ApiUrl per system — keep in sync with the `cpi` skill SKILL.md.
SYSTEMS = {
    "SW-D": {
        "token": "https://sw-ci-d-3jiely4m.authentication.eu10.hana.ondemand.com/oauth/token",
        "client_id": "sb-36bb2928-6a9c-482e-b588-ee8574205e2e!b778833|it!b641068",
        "api": "https://sw-ci-d-3jiely4m.it-cpi049.cfapps.eu10-003.hana.ondemand.com/api/v1",
    },
    "SYN-D": {
        "token": "https://syntax-integration-suite-7i3vjnji.authentication.eu20.hana.ondemand.com/oauth/token",
        "client_id": "sb-dcd33f83-dfd7-4571-a01d-11a93fd9ae46!b161150|it!b150645",
        "api": "https://syntax-integration-suite-7i3vjnji.it-cpi050.cfapps.eu20-002.hana.ondemand.com/api/v1",
    },
    "MCA-D": {
        "token": "https://integrationsuite-30nqhpsj.authentication.eu30.hana.ondemand.com/oauth/token",
        "client_id": "sb-ba67c0f9-a733-4381-a16b-18b0082965ce!b10087|it!b293",
        "api": "https://integrationsuite-30nqhpsj.it-cpi020.cfapps.eu30.hana.ondemand.com/api/v1",
    },
    "MCA-P": {
        "token": "https://integrations-5jxkrzkq.authentication.eu10.hana.ondemand.com/oauth/token",
        "client_id": "sb-91689ba5-8992-4857-af2d-46a030133c4f!b532000|it!b182722",
        "api": "https://integrations-5jxkrzkq.it-cpi024.cfapps.eu10-002.hana.ondemand.com/api/v1",
    },
}


def secret_for(system):
    for key in (f"CPI_{system}_CLIENT_SECRET", f"CPI_{system.replace('-', '')}_CLIENT_SECRET"):
        v = os.environ.get(key)
        if v:
            return v
    sys.exit(f"ERROR: no client secret in env (tried CPI_{system}_CLIENT_SECRET and the hyphen-free "
             f"alias). Set it in ~/.claude/settings.json env.")


def token(sys_cfg, secret):
    body = urllib.parse.urlencode({
        "grant_type": "client_credentials",
        "client_id": sys_cfg["client_id"],
        "client_secret": secret,
    }).encode()
    req = urllib.request.Request(sys_cfg["token"], data=body,
                                 headers={"Content-Type": "application/x-www-form-urlencoded"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)["access_token"]


def zip_bundle(bundle_dir):
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
        for root, _, files in os.walk(bundle_dir):
            for f in files:
                full = os.path.join(root, f)
                z.write(full, os.path.relpath(full, bundle_dir))
    return base64.b64encode(buf.getvalue()).decode()


def api(method, url, tok, csrf=None, data=None):
    headers = {"Authorization": f"Bearer {tok}", "Accept": "application/json"}
    if csrf:
        headers["X-CSRF-Token"] = csrf
    if data is not None:
        headers["Content-Type"] = "application/json"
        data = json.dumps(data).encode()
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            return r.status, r.read().decode(errors="replace"), dict(r.headers)
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode(errors="replace"), dict(e.headers)


def fetch_csrf(api_base, tok):
    req = urllib.request.Request(api_base + "/", headers={
        "Authorization": f"Bearer {tok}", "X-CSRF-Token": "Fetch"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.headers.get("x-csrf-token") or r.headers.get("X-CSRF-Token")


def exists(api_base, tok, art_id):
    st, _, _ = api("GET", f"{api_base}/IntegrationDesigntimeArtifacts(Id='{art_id}',Version='1.0.0')", tok)
    return st == 200


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--system", default="SW-D", choices=list(SYSTEMS))
    ap.add_argument("--package", required=True)
    ap.add_argument("--id", required=True)
    ap.add_argument("--name", required=True)
    ap.add_argument("--bundle", required=True, help="bundle dir (contents zipped at root)")
    ap.add_argument("--version", default="1.0.0")
    ap.add_argument("--create-package", action="store_true")
    ap.add_argument("--deploy", action="store_true")
    a = ap.parse_args()

    cfg = SYSTEMS[a.system]
    tok = token(cfg, secret_for(a.system))
    csrf = fetch_csrf(cfg["api"], tok)
    print(f"[auth] token ok; csrf ok; system={a.system}")

    if a.create_package:
        st, body, _ = api("POST", f"{cfg['api']}/IntegrationPackages", tok, csrf,
                          {"Id": a.package, "Name": a.package})
        print(f"[package] create {a.package}: HTTP {st}")

    payload = {"Name": a.name, "Id": a.id, "PackageId": a.package, "ArtifactContent": zip_bundle(a.bundle)}
    if exists(cfg["api"], tok, a.id):
        st, body, _ = api("PUT",
                          f"{cfg['api']}/IntegrationDesigntimeArtifacts(Id='{a.id}',Version='{a.version}')",
                          tok, csrf, payload)
        print(f"[upload] PUT update: HTTP {st}")
    else:
        st, body, _ = api("POST", f"{cfg['api']}/IntegrationDesigntimeArtifacts", tok, csrf, payload)
        print(f"[upload] POST create: HTTP {st}")
    if st not in (200, 201):
        print(body[:800]); sys.exit(f"UPLOAD FAILED (HTTP {st}). Fix the offending step and retry.")
    print("[upload] OK — SAP parser accepted the bundle. Open in GUI to confirm it hydrates.")

    if a.deploy:
        dep_url = (f"{cfg['api']}/DeployIntegrationDesigntimeArtifact"
                   f"?Id='{a.id}'&Version='{a.version}'")
        st, body, _ = api("POST", dep_url, tok, csrf)
        print(f"[deploy] HTTP {st} {body[:120]}")
        if st == 403:
            sys.exit("DEPLOY 403: service key lacks GenerationAndBuild.generationandbuildcontent role.")
        if st not in (200, 202):
            sys.exit(f"DEPLOY FAILED HTTP {st}")
        for i in range(30):
            time.sleep(10)
            st, body, _ = api("GET", f"{cfg['api']}/IntegrationRuntimeArtifacts('{a.id}')", tok)
            status = (json.loads(body).get("d", {}).get("Status") if st == 200 else "?")
            print(f"[deploy] poll {i+1}: {status}")
            if status in ("STARTED", "ERROR"):
                if status == "ERROR":
                    _, err, _ = api("GET",
                        f"{cfg['api']}/IntegrationRuntimeArtifacts('{a.id}')/ErrorInformation/$value", tok)
                    print("ERROR:", err[:600])
                    print("NB: 'UNRESOLVED (...PGPPublicKeyringAccessor)' = upload a PGP public keyring "
                          "to the tenant and match PgpEncryptionUserIDs.")
                break


if __name__ == "__main__":
    main()
