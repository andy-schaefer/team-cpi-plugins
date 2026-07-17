---
description: 'Erstellt einen Jira-Task aus einer E-Mail (.eml) für einen direkten Kunden (= Jira Epic). Aufruf: /jira-mail-task C:\path\to\email.eml <Kunde> — z.B. /jira-mail-task C:\path\to\email.eml MCA oder /jira-mail-task C:\path\to\email.eml Fuchs. Der Kunde ist der direkte SYNTAX-Kunde (z.B. MCA, Fuchs, Syntax, Aryzta) — nicht der Endkunde des Kunden (z.B. Ostermann, Intrakon). Sucht nach Ticketnummern (MCA→MCAS-xxx, andere→PRJKTxxxxxxx/INCxxxxxxxx), CPI-Nachrichtenreferenzen, und legt den Task unter dem passenden Epic an.'
---

Du bekommst als Argument einen Dateipfad zu einer E-Mail (.eml) sowie den Namen des **direkten Kunden** (= Jira Epic): $ARGUMENTS

Das erste Token ist der Dateipfad, das zweite Token ist der **direkte Kunde** — das ist der SYNTAX-Kunde, unter dessen Jira-Epic der Task angelegt wird (z.B. `MCA`, `Fuchs`, `Syntax`, `Aryzta`).

**Wichtig:** Der Kunde ist NICHT der Endkunde des Kunden. Ostermann, Intrakon usw. sind Endkunden von MCA und tauchen nur im E-Mail-Inhalt auf — sie werden in der Beschreibung erwähnt, aber nicht für die Epic-Zuordnung verwendet.

Führe folgende Schritte aus:

## Schritt 1: E-Mail lesen und parsen

Lese die .eml-Datei und extrahiere Metadaten sowie den Klartextinhalt:

```powershell
$parts  = "$ARGUMENTS" -split ' ', 2
$file   = $parts[0].Trim()
$kunde  = if ($parts.Count -gt 1) { $parts[1].Trim() } else { "" }

$raw = Get-Content $file -Raw -Encoding UTF8

# Header extrahieren
$from    = if ($raw -match '(?m)^From:\s*(.+)$') { $matches[1].Trim() } else { "Unbekannt" }
$subject = if ($raw -match '(?m)^Subject:\s*(.+)$') { $matches[1].Trim() } else { "Kein Betreff" }
$date    = if ($raw -match '(?m)^Date:\s*(.+)$') { $matches[1].Trim() } else { "" }

# Quoted-Printable Decoder (ISO-8859-1)
function Decode-QP {
    param([string]$text)
    $text = $text -replace "=`r`n", "" -replace "=`n", ""
    $result = [System.Text.RegularExpressions.Regex]::Replace($text, '=([0-9A-Fa-f]{2})', {
        param($m)
        $byte = [Convert]::ToByte($m.Groups[1].Value, 16)
        [System.Text.Encoding]::GetEncoding("iso-8859-1").GetString([byte[]]@($byte))
    })
    return $result
}

# text/plain Block extrahieren
$plainBlock = ""
if ($raw -match '(?s)Content-Type: text/plain[^\r\n]*\r?\nContent-Transfer-Encoding: quoted-printable\r?\n\r?\n(.*?)(?=\r?\n--|\z)') {
    $plainBlock = Decode-QP $matches[1]
} elseif ($raw -match '(?s)Content-Type: text/plain[^\r\n]*\r?\n\r?\n(.*?)(?=\r?\n--|\z)') {
    $plainBlock = $matches[1]
}

Write-Host "=== HEADER ==="
Write-Host "Von:     $from"
Write-Host "Betreff: $subject"
Write-Host "Datum:   $date"
Write-Host "Kunde:   $kunde"
Write-Host ""
Write-Host "=== INHALT ==="
Write-Host $plainBlock
```

## Schritt 2: Prefix-Nummer bestimmen (abhängig vom Kunden)

Suche im **gesamten E-Mail-Text** (Header + Body) nach einer Referenznummer. Die Regel hängt vom Kunden ab:

| Kunde | Suchmuster | Beispiel-Prefix |
|---|---|---|
| `MCA` | `MCAS-\d+` | `MCAS-123` |
| alle anderen | `PRJKT\d+` oder `INC\d+` | `PRJKT0012345` / `INC0001234` |

```powershell
$prefix = ""

if ($kunde -eq "MCA") {
    if ($raw -match 'MCAS-(\d+)') {
        $prefix = "MCAS-$($matches[1])"
    } else {
        $prefix = "MCAS-xxx"
    }
} else {
    if ($raw -match '(PRJKT\d+)') {
        $prefix = $matches[1]
    } elseif ($raw -match '(INC\d+)') {
        $prefix = $matches[1]
    } else {
        $prefix = "PRJKT-xxx"
    }
}

Write-Host "Prefix: $prefix"
```

## Schritt 3: CPI-Nachricht suchen (optional)

Falls im E-Mail-Text eine CPI Nachrichten-ID (GUID-Format `[0-9a-f-]{36}`) gefunden wird, suche die Nachricht im CPI Prod-System:

```powershell
$msgId = ""
if ($raw -match '\b([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})\b') {
    $msgId = $matches[1]
}

if ($msgId) {
    $cpiUser  = "sb-7d85bba5-3dda-42dc-8193-8a1c5e1f8db4!b57419|it-rt-mca-prod!b29889"
    $cpiPass  = "2d98a9fc-b2b9-4ff8-b99b-cb08c60d33ab$wAjXJGEzYD5KY32UMi_TXFXoxJwdBi-H3XJVEXHrN0="
    $cpiBase  = "https://mca-prod.it-cpi018.cfapps.eu10-002.hana.ondemand.com"
    $base64   = [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes("${cpiUser}:${cpiPass}"))
    $headers  = @{ Authorization = "Basic $base64" }

    $url = "$cpiBase/api/v1/MessageProcessingLogs?`$filter=CorrelationId eq '$msgId'&`$format=json"
    $r   = Invoke-RestMethod -Uri $url -Headers $headers
    $r.d.results | Select-Object MessageGuid, Status, LogStart, LogEnd, IntegrationFlowName, CorrelationId | Format-Table -AutoSize
}
```

Falls keine GUID gefunden → Schritt überspringen.

## Schritt 4: Passendes Epic suchen

Suche das Epic anhand des Kundennamens (`$kunde`):

```powershell
$token  = $env:ATLASSIAN_API_TOKEN
$email  = $env:ATLASSIAN_EMAIL
$base64 = [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes("${email}:${token}"))
$headers = @{ Authorization = "Basic $base64"; "Content-Type" = "application/json" }

$body = @{
    jql        = "project = SAPIP AND issuetype = Epic AND statusCategory != Done AND summary ~ `"$kunde`" ORDER BY updated DESC"
    maxResults = 10
    fields     = @("summary","status","customfield_11649")
} | ConvertTo-Json
$r = Invoke-RestMethod -Uri "https://syntax.atlassian.net/rest/api/3/search/jql" -Headers $headers -Method Post -Body $body
$r.issues | ForEach-Object {
    [PSCustomObject]@{
        Key      = $_.key
        Customer = $_.fields.customfield_11649.value
        Status   = $_.fields.status.name
        Summary  = $_.fields.summary
    }
} | Format-Table -AutoSize
```

Falls genau ein Epic gefunden → automatisch verwenden. Falls mehrere oder keines → Nutzer fragen.

## Schritt 5: Customer-Wert ermitteln

```powershell
$token  = $env:ATLASSIAN_API_TOKEN
$email  = $env:ATLASSIAN_EMAIL
$base64 = [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes("${email}:${token}"))
$headers = @{ Authorization = "Basic $base64" }
$r = Invoke-RestMethod -Uri "https://syntax.atlassian.net/rest/api/3/issue/createmeta/SAPIP/issuetypes/13334" -Headers $headers
$field = $r.fields | Where-Object { $_.fieldId -eq "customfield_11649" }
$field.allowedValues | Where-Object { $_.value -match $kunde } | Select-Object id, value | Format-Table
```

## Schritt 6: Task-Summary und Beschreibung vorbereiten

- **Summary:** `<Prefix> - <Betreff der E-Mail>`
  - Beispiel MCA mit gefundener Nummer: `MCAS-123 - Intrakon EDI Sondereinstellungen`
  - Beispiel MCA ohne Nummer: `MCAS-xxx - Intrakon EDI Sondereinstellungen`
  - Beispiel anderer Kunde mit PRJKT: `PRJKT0012345 - Lieferavise Konfiguration`
- **Beschreibung (ADF):** Strukturiert mit:
  - **Anforderung**: Von wem, wann, Kurzinhalt der E-Mail
  - **Technische Details**: Bullet-Liste aller Konfigurationsangaben
  - **CPI-Kontext** *(nur wenn Nachrichten-Referenz gefunden)*: iFlow-Name, Status, Zeitstempel
  - **Aufgaben**: Standard-Checklist

Standard-Aufgaben:
- Anforderungen aus E-Mail analysieren und klären
- Rückfragen an Absender bei Unklarheiten
- Konfiguration im T-System umsetzen und testen
- Konfiguration im P-System umsetzen
- Abnahme mit Fachbereich durchführen
- Dokumentation aktualisieren

## Schritt 7: Task erstellen

```powershell
$token  = $env:ATLASSIAN_API_TOKEN
$email  = $env:ATLASSIAN_EMAIL
$base64 = [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes("${email}:${token}"))
$headers = @{ Authorization = "Basic $base64"; "Content-Type" = "application/json" }

# $epicKey    = gewähltes Epic (z.B. "SAPIP-18")
# $customerId = Customer-ID (z.B. "11089")
# $summary    = "$prefix - $subject"
# $description = ADF-Objekt

$body = @{
    fields = @{
        project           = @{ key = "SAPIP" }
        issuetype         = @{ id = "13334" }
        summary           = $summary
        description       = $description
        parent            = @{ key = $epicKey }
        customfield_11649 = @{ id = $customerId }
        assignee          = @{ accountId = "557058:a8b44127-1380-49e8-b019-b59f0d76eb2a" }
    }
} | ConvertTo-Json -Depth 20

$r = Invoke-RestMethod -Uri "https://syntax.atlassian.net/rest/api/3/issue" -Headers $headers -Method Post -Body $body
Write-Host "Task erstellt: $($r.key)"
Write-Host "Link: https://syntax.atlassian.net/browse/$($r.key)"
```

## Schritt 8: Ergebnis anzeigen

| Feld | Wert |
|---|---|
| Key | SAPIP-xxx |
| Summary | ... |
| Epic | ... |
| Customer | ... |
| Prefix | gefunden (`MCAS-123` / `PRJKT0012345` / `INC0001234`) oder Platzhalter |
| CPI-Referenz | gefunden / nicht gefunden |
| Link | https://syntax.atlassian.net/browse/SAPIP-xxx |
