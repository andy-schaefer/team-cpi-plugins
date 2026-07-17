---
description: 'Interagiert mit SAP CPI / Integration Suite Systemen. Nutzen für: iFlows auflisten, deployen, Deployment-Status prüfen, Nachrichten-Logs anzeigen, Systeme vergleichen. Aufruf z.B. /cpi list, /cpi deploy <ArtifactId>, /cpi logs, /cpi status, /cpi compare <SYS1> <SYS2>.'
---

# SAP CPI Skill

## Systemkonfiguration

```powershell
# Systeme - API-URL nach Erhalt ergänzen
$CPI_SYSTEMS = @{
    DEV = @{
        TokenUrl     = "https://integrationsuite-30nqhpsj.authentication.eu30.hana.ondemand.com/oauth/token"
        ClientId     = "sb-ba67c0f9-a733-4381-a16b-18b0082965ce!b10087|it!b293"
        ClientSecret = $env:CPI_DEV_CLIENT_SECRET   # in ~/.claude/settings.json env setzen
        ApiUrl       = "https://integrationsuite-30nqhpsj.it-cpi020.cfapps.eu30.hana.ondemand.com"
    }
    PROD = @{
        TokenUrl     = "https://integrations-5jxkrzkq.authentication.eu10.hana.ondemand.com/oauth/token"
        ClientId     = "sb-91689ba5-8992-4857-af2d-46a030133c4f!b532000|it!b182722"
        ClientSecret = $env:CPI_PROD_CLIENT_SECRET  # in ~/.claude/settings.json env setzen
        ApiUrl       = "https://integrations-5jxkrzkq.it-cpi024.cfapps.eu10-002.hana.ondemand.com"
    }
    # TEST = @{ ... }
}
```

## Hilfsfunktion: OAuth Token holen

```powershell
function Get-CpiToken($system) {
    $s = $CPI_SYSTEMS[$system]
    $body = "grant_type=client_credentials&client_id=$([Uri]::EscapeDataString($s.ClientId))&client_secret=$([Uri]::EscapeDataString($s.ClientSecret))"
    $r = Invoke-RestMethod -Uri $s.TokenUrl -Method Post -Body $body -ContentType "application/x-www-form-urlencoded"
    return $r.access_token
}
```

## Befehle

Interpretiere das Argument `$ARGUMENTS` und führe den passenden Befehl aus.
Fragt der Nutzer nicht explizit nach einem System, verwende DEV als Standard.
Ist die ApiUrl noch "TODO", weise den Nutzer darauf hin dass die URL noch eingetragen werden muss.

---

### list — iFlows auflisten

```powershell
$token = Get-CpiToken "DEV"
$headers = @{ Authorization = "Bearer $token"; Accept = "application/json" }
$packages = Invoke-RestMethod -Uri "$($CPI_SYSTEMS['DEV'].ApiUrl)/api/v1/IntegrationPackages" -Headers $headers
$packages.d.results | ForEach-Object {
    $pkgId = $_.Id
    $artifacts = Invoke-RestMethod -Uri "$($CPI_SYSTEMS['DEV'].ApiUrl)/api/v1/IntegrationPackages('$pkgId')/IntegrationDesigntimeArtifacts" -Headers $headers
    $artifacts.d.results | Select-Object Id, Name, Version, @{N="PackageId";E={$pkgId}}
} | Format-Table -AutoSize
```

---

### status — Deployed Artifacts anzeigen

```powershell
$token = Get-CpiToken "DEV"
$headers = @{ Authorization = "Bearer $token"; Accept = "application/json" }
$r = Invoke-RestMethod -Uri "$($CPI_SYSTEMS['DEV'].ApiUrl)/api/v1/IntegrationRuntimeArtifacts" -Headers $headers
$r.d.results | Select-Object Id, Name, Version, Status | Format-Table -AutoSize
```

---

### deploy — iFlow deployen

Artifact-ID aus dem Argument lesen. Falls nicht angegeben, zuerst `list` ausführen und den Nutzer fragen.

```powershell
$artifactId = "<aus Argument>"
$version    = "<aus list ermitteln oder 'active'>"
$token = Get-CpiToken "DEV"
$headers = @{ Authorization = "Bearer $token"; Accept = "application/json" }
$url = "$($CPI_SYSTEMS['DEV'].ApiUrl)/api/v1/DeployIntegrationDesigntimeArtifact?Id='$artifactId'&Version='$version'"
$r = Invoke-RestMethod -Uri $url -Method Post -Headers $headers
Write-Host "Deploy gestartet: $($r.d.TaskId)"
```

Danach Status prüfen:
```powershell
$r2 = Invoke-RestMethod -Uri "$($CPI_SYSTEMS['DEV'].ApiUrl)/api/v1/IntegrationRuntimeArtifacts('$artifactId')" -Headers $headers
Write-Host "Status: $($r2.d.Status)"
```

---

### logs — Nachrichten-Logs anzeigen

```powershell
$token = Get-CpiToken "DEV"
$headers = @{ Authorization = "Bearer $token"; Accept = "application/json" }
$filter = "`$top=20&`$orderby=LogStart desc"
$r = Invoke-RestMethod -Uri "$($CPI_SYSTEMS['DEV'].ApiUrl)/api/v1/MessageProcessingLogs?$filter" -Headers $headers
$r.d.results | ForEach-Object {
    [PSCustomObject]@{
        Zeit      = $_.LogStart
        Status    = $_.Status
        iFlow     = $_.IntegrationFlowName
        MessageId = $_.MessageGuid
    }
} | Format-Table -AutoSize
```

---

### logs <iFlowName> — Logs für einen bestimmten iFlow

Filter: `$filter=IntegrationFlowName eq '<name>'`

---

### compare — Zwei Systeme vergleichen und HTML-Report generieren

Systeme aus dem Argument lesen (z.B. `compare PROD DEV`, `compare PROD TEST`). Fehlen Angaben, Standard: PROD vs. DEV.
Ist eines der Systeme nicht konfiguriert, Nutzer darauf hinweisen.

```powershell
# Systeme aus Argument bestimmen
$sysA = "PROD"   # erstes System aus Argument
$sysB = "DEV"    # zweites System aus Argument

function Get-AllArtifacts($system) {
    $token   = Get-CpiToken $system
    $headers = @{ Authorization = "Bearer $token"; Accept = "application/json" }
    $apiUrl  = $CPI_SYSTEMS[$system].ApiUrl
    $packages = Invoke-RestMethod -Uri "$apiUrl/api/v1/IntegrationPackages" -Headers $headers -ErrorAction Stop
    $result   = @()
    foreach ($pkg in $packages.d.results) {
        $arts = Invoke-RestMethod -Uri "$apiUrl/api/v1/IntegrationPackages('$($pkg.Id)')/IntegrationDesigntimeArtifacts" -Headers $headers -ErrorAction SilentlyContinue
        foreach ($a in $arts.d.results) {
            $result += [PSCustomObject]@{
                PackageId   = $pkg.Id
                PackageName = $pkg.Name
                ArtifactId  = $a.Id
                Name        = $a.Name
                Version     = $a.Version
            }
        }
    }
    return $result
}

function Get-RuntimeStatus($system) {
    $token   = Get-CpiToken $system
    $headers = @{ Authorization = "Bearer $token"; Accept = "application/json" }
    $apiUrl  = $CPI_SYSTEMS[$system].ApiUrl
    $r = Invoke-RestMethod -Uri "$apiUrl/api/v1/IntegrationRuntimeArtifacts" -Headers $headers -ErrorAction Stop
    $map = @{}
    foreach ($item in $r.d.results) { $map[$item.Id] = $item.Status }
    return $map
}

Write-Host "Hole Daten von $sysA ..." -ForegroundColor Cyan
$aArtifacts = Get-AllArtifacts $sysA
$aRuntime   = Get-RuntimeStatus $sysA

Write-Host "Hole Daten von $sysB ..." -ForegroundColor Cyan
$bArtifacts = Get-AllArtifacts $sysB
$bRuntime   = Get-RuntimeStatus $sysB

$aMap = @{}; foreach ($x in $aArtifacts) { $aMap[$x.ArtifactId] = $x }
$bMap = @{}; foreach ($x in $bArtifacts) { $bMap[$x.ArtifactId] = $x }
$allIds = ($aMap.Keys + $bMap.Keys) | Sort-Object -Unique

$rows = @()
foreach ($id in $allIds) {
    $a = $aMap[$id]; $b = $bMap[$id]
    $aVer = if ($a) { $a.Version } else { "-" }
    $bVer = if ($b) { $b.Version } else { "-" }
    $aSt  = if ($aRuntime[$id]) { $aRuntime[$id] } else { "-" }
    $bSt  = if ($bRuntime[$id]) { $bRuntime[$id] } else { "-" }
    $pkg  = if ($a) { $a.PackageName } elseif ($b) { $b.PackageName } else { "?" }
    $diff = if (-not $a)          { "NUR IN $sysB" }
            elseif (-not $b)      { "NUR IN $sysA" }
            elseif ($aVer -ne $bVer) { "VERSION UNTERSCHIED" }
            else                  { "IDENTISCH" }
    $rows += [PSCustomObject]@{
        Package       = $pkg
        ArtifactId    = $id
        "${sysA}_Version" = $aVer
        "${sysB}_Version" = $bVer
        "${sysA}_Status"  = $aSt
        "${sysB}_Status"  = $bSt
        Differenz     = $diff
    }
}

# Statistik ausgeben
$total       = $rows.Count
$identical   = ($rows | Where-Object { $_.Differenz -eq "IDENTISCH" }).Count
$versionDiff = ($rows | Where-Object { $_.Differenz -eq "VERSION UNTERSCHIED" }).Count
$onlyA       = ($rows | Where-Object { $_.Differenz -eq "NUR IN $sysA" }).Count
$onlyB       = ($rows | Where-Object { $_.Differenz -eq "NUR IN $sysB" }).Count

Write-Host "`n========== ZUSAMMENFASSUNG ==========" -ForegroundColor Yellow
Write-Host "Gesamt          : $total"
Write-Host "Identisch       : $identical"
Write-Host "Version-Diff    : $versionDiff" -ForegroundColor $(if($versionDiff -gt 0){"Red"}else{"Green"})
Write-Host "Nur in $sysA    : $onlyA"
Write-Host "Nur in $sysB    : $onlyB"

# HTML-Report generieren
$date = (Get-Date).ToString("dd.MM.yyyy HH:mm")

$tableRows = ($rows | Sort-Object Package, ArtifactId | ForEach-Object {
    $diff = $_.Differenz
    $cls  = switch ($diff) {
        "VERSION UNTERSCHIED" { "diff-version" }
        "NUR IN $sysA"        { "diff-aonly"   }
        "NUR IN $sysB"        { "diff-bonly"   }
        default               { "diff-ok"      }
    }
    $badge = switch ($diff) {
        "VERSION UNTERSCHIED" { '<span class="badge badge-warn">VERSION</span>'   }
        "NUR IN $sysA"        { "<span class='badge badge-info'>NUR $sysA</span>" }
        "NUR IN $sysB"        { "<span class='badge badge-info'>NUR $sysB</span>" }
        default               { '<span class="badge badge-ok">OK</span>'          }
    }
    $aVerVal = $_."${sysA}_Version"; $bVerVal = $_."${sysB}_Version"
    $aStVal  = $_."${sysA}_Status";  $bStVal  = $_."${sysB}_Status"
    $fmtSt = { param($v)
        if ($v -eq "STARTED") { "<span class='st st-ok'>STARTED</span>" }
        elseif ($v -eq "-" -or $v -eq "") { "<span class='st st-na'>-</span>" }
        else { "<span class='st st-err'>$v</span>" }
    }
    "    <tr class='$cls'>
      <td>$($_.Package)</td>
      <td class='mono'>$($_.ArtifactId)</td>
      <td class='center mono'>$aVerVal</td>
      <td class='center mono'>$bVerVal</td>
      <td class='center'>$(& $fmtSt $aStVal)</td>
      <td class='center'>$(& $fmtSt $bStVal)</td>
      <td class='center'>$badge</td>
    </tr>"
}) -join "`n"

$html = @"
<!DOCTYPE html><html lang="de"><head><meta charset="UTF-8">
<title>SAP CPI – $sysA vs $sysB</title>
<style>
* { box-sizing:border-box; margin:0; padding:0; }
body { font-family:'Segoe UI',Arial,sans-serif; font-size:11px; color:#1a1a2e; background:#f5f7fa; }
.cover { background:linear-gradient(135deg,#003087 0%,#0050c8 60%,#0070d2 100%); color:#fff; padding:48px 56px; }
.cover h1 { font-size:28px; margin-bottom:6px; }
.cover .sub { font-size:14px; opacity:.85; margin-bottom:32px; }
.cover .meta { display:flex; gap:40px; }
.cover .meta-item label { font-size:10px; opacity:.7; text-transform:uppercase; letter-spacing:.8px; }
.cover .meta-item value { font-size:16px; font-weight:600; display:block; }
.kpi-strip { display:flex; gap:16px; padding:28px 56px 0; flex-wrap:wrap; }
.kpi { background:#fff; border-radius:10px; padding:18px 24px; flex:1; min-width:120px; box-shadow:0 2px 8px rgba(0,0,0,.07); border-top:4px solid #ccc; }
.kpi.blue{border-color:#0050c8}.kpi.green{border-color:#0caa5a}.kpi.orange{border-color:#f58220}.kpi.red{border-color:#d73027}
.kpi .num { font-size:32px; font-weight:700; line-height:1; }
.kpi .lbl { font-size:10px; color:#666; margin-top:4px; text-transform:uppercase; letter-spacing:.7px; }
.section { padding:28px 56px; }
.section h2 { font-size:14px; font-weight:700; text-transform:uppercase; letter-spacing:.8px; color:#003087; border-bottom:2px solid #003087; padding-bottom:6px; margin-bottom:16px; }
table { width:100%; border-collapse:collapse; background:#fff; border-radius:10px; overflow:hidden; box-shadow:0 2px 8px rgba(0,0,0,.07); }
thead th { background:#003087; color:#fff; padding:10px 12px; text-align:left; font-size:10px; text-transform:uppercase; letter-spacing:.7px; white-space:nowrap; }
tbody tr { border-bottom:1px solid #f0f0f0; }
tbody tr:hover { background:#f0f5ff; }
tbody td { padding:8px 12px; vertical-align:middle; }
.diff-version td:first-child{border-left:4px solid #f58220}
.diff-aonly td:first-child{border-left:4px solid #0050c8}
.diff-bonly td:first-child{border-left:4px solid #9c27b0}
.diff-ok td:first-child{border-left:4px solid #0caa5a}
.mono{font-family:monospace;font-size:10px}.center{text-align:center}
.badge{display:inline-block;padding:2px 8px;border-radius:20px;font-size:9px;font-weight:700;letter-spacing:.5px;text-transform:uppercase}
.badge-ok{background:#d4f5e0;color:#0a7a3e}.badge-warn{background:#fde8cc;color:#a85800}.badge-info{background:#dce8ff;color:#003087}
.st{display:inline-block;padding:2px 8px;border-radius:4px;font-size:9px;font-weight:600}
.st-ok{background:#d4f5e0;color:#0a7a3e}.st-err{background:#fde0dd;color:#c0392b}.st-na{color:#aaa}
.legend{display:flex;gap:24px;flex-wrap:wrap;margin-top:16px}
.legend-item{display:flex;align-items:center;gap:8px;font-size:11px}
.legend-dot{width:12px;height:12px;border-radius:50%;flex-shrink:0}
footer{text-align:center;padding:24px 56px;color:#888;font-size:10px;border-top:1px solid #e0e0e0;margin-top:20px}
@media print{body,.cover,.kpi,thead{-webkit-print-color-adjust:exact;print-color-adjust:exact}}
</style></head><body>
<div class="cover">
  <h1>SAP CPI – Systemvergleich</h1>
  <div class="sub">Integration Suite &middot; $sysA vs. $sysB &middot; Detaillierter Differenzbericht</div>
  <div class="meta">
    <div class="meta-item"><label>Erstellt am</label><value>$date</value></div>
    <div class="meta-item"><label>Systeme</label><value>$sysA / $sysB</value></div>
    <div class="meta-item"><label>Artifacts gesamt</label><value>$total</value></div>
  </div>
</div>
<div class="kpi-strip">
  <div class="kpi blue"><div class="num">$total</div><div class="lbl">Artifacts gesamt</div></div>
  <div class="kpi green"><div class="num">$identical</div><div class="lbl">Identisch</div></div>
  <div class="kpi orange"><div class="num">$versionDiff</div><div class="lbl">Versions-Unterschied</div></div>
  <div class="kpi blue"><div class="num">$onlyA</div><div class="lbl">Nur in $sysA</div></div>
  <div class="kpi red"><div class="num">$onlyB</div><div class="lbl">Nur in $sysB</div></div>
</div>
<div class="section">
  <div class="legend">
    <div class="legend-item"><div class="legend-dot" style="background:#0caa5a"></div>Identisch – gleiche Version in beiden Systemen</div>
    <div class="legend-item"><div class="legend-dot" style="background:#f58220"></div>Versions-Unterschied – Systeme laufen verschiedene Versionen</div>
    <div class="legend-item"><div class="legend-dot" style="background:#0050c8"></div>Nur in $sysA</div>
    <div class="legend-item"><div class="legend-dot" style="background:#9c27b0"></div>Nur in $sysB</div>
  </div>
</div>
<div class="section">
  <h2>Artifact-Vergleich im Detail</h2>
  <table>
    <thead><tr>
      <th>Package</th><th>Artifact-ID</th>
      <th class="center">$sysA Version</th><th class="center">$sysB Version</th>
      <th class="center">$sysA Status</th><th class="center">$sysB Status</th>
      <th class="center">Differenz</th>
    </tr></thead>
    <tbody>
$tableRows
    </tbody>
  </table>
</div>
<footer>SAP CPI Vergleichsreport &middot; $date &middot; $sysA vs. $sysB</footer>
</body></html>
"@

# Speicherpfad ermitteln (OneDrive-Desktop oder TEMP)
$desktopPath = "$env:USERPROFILE\OneDrive - SYNTAX SYSTEMS LTD\Desktop"
$savePath    = if (Test-Path $desktopPath) { $desktopPath } else { $env:TEMP }
$htmlFile    = "$savePath\CPI_${sysA}_vs_${sysB}_$(Get-Date -Format 'yyyyMMdd_HHmm').html"
$html | Out-File -FilePath $htmlFile -Encoding UTF8
Write-Host "Report gespeichert: $htmlFile" -ForegroundColor Green
Write-Host "PDF: Im Browser Strg+P → Als PDF speichern" -ForegroundColor Cyan
Start-Process $htmlFile
```

---

## System wechseln

Enthält das Argument "TEST" oder "PROD", ersetze "DEV" in allen Aufrufen durch das genannte System.
Beispiel: `/cpi list TEST` → listet iFlows im TEST-System.
