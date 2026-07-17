---
description: Erstellt einen neuen Jira-Task für CPI iFlow Entwicklung aus einem Interface-Dokument (.docx). Aufrufen mit dem Dateipfad als Argument, z.B. /jira-cpi-task C:\path\to\interface.docx. Verwenden wenn der Nutzer einen Jira-Task für ein Interface anlegen möchte.
---

Du bekommst einen Dateipfad zu einem Word-Dokument (.docx) als Argument: $ARGUMENTS

Führe folgende Schritte aus:

## Schritt 1: Dokument lesen

Lese den Text aus der .docx-Datei mit PowerShell:

```powershell
Add-Type -AssemblyName System.IO.Compression.FileSystem
$zip = [System.IO.Compression.ZipFile]::OpenRead("$ARGUMENTS")
$entry = $zip.GetEntry("word/document.xml")
$reader = New-Object System.IO.StreamReader($entry.Open())
$xml = $reader.ReadToEnd()
$reader.Close(); $zip.Dispose()
$doc = [xml]$xml
$nm = New-Object System.Xml.XmlNamespaceManager($doc.NameTable)
$nm.AddNamespace("w","http://schemas.openxmlformats.org/wordprocessingml/2006/main")
$paras = $doc.SelectNodes("//w:p", $nm)
foreach ($p in $paras) {
    $line = ($p.SelectNodes(".//w:t", $nm) | ForEach-Object { $_.InnerText }) -join ""
    if ($line.Trim()) { Write-Host $line }
}
```

Extrahiere aus dem Inhalt:
- Interface-Name
- Technische Details (Transaktionen, URLs, Systeme)
- Ansprechpartner (Business Contact)
- Sonstige relevante Informationen

## Schritt 2: Epic auswählen

Frage den Nutzer: "Unter welchem Epic soll der Task angelegt werden?" und zeige verfügbare Epics an:

```powershell
$token = $env:ATLASSIAN_API_TOKEN
$email = $env:ATLASSIAN_EMAIL
$base64 = [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes("${email}:${token}"))
$headers = @{ Authorization = "Basic $base64"; "Content-Type" = "application/json" }
$body = @{
    jql = 'project = SAPIP AND issuetype = Epic AND statusCategory != Done ORDER BY updated DESC'
    maxResults = 30
    fields = @("summary","status","customfield_11649")
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

Falls der Nutzer einen Suchbegriff nennt, filtere die Epics entsprechend (z.B. `summary ~ "Neptune"`).

## Schritt 3: Customer-Wert ermitteln

Hole die erlaubten Customer-Werte und wähle den passenden zum Epic:

```powershell
$token = $env:ATLASSIAN_API_TOKEN
$email = $env:ATLASSIAN_EMAIL
$base64 = [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes("${email}:${token}"))
$headers = @{ Authorization = "Basic $base64" }
$r = Invoke-RestMethod -Uri "https://syntax.atlassian.net/rest/api/3/issue/createmeta/SAPIP/issuetypes/13334" -Headers $headers
$nm2 = New-Object System.Xml.XmlNamespaceManager
$field = $r.fields | Where-Object { $_.fieldId -eq "customfield_11649" }
$field.allowedValues | Select-Object id, value | Format-Table
```

Wähle den Customer-Wert, der zum ausgewählten Epic passt (Name-Matching). Falls unklar, frage den Nutzer.

## Schritt 4: Task-Summary und Beschreibung vorbereiten

Erstelle:
- **Summary:** `<Interface-Name> - CPI iFlow Entwicklung`
- **Beschreibung:** Strukturiert mit Abschnitten: Interface-Details, Technische Details (Bullet-Liste), Aufgaben (Bullet-Liste mit Standard-Schritten für CPI iFlow Entwicklung)

Standard-Aufgaben für jeden CPI iFlow Task:
- Anforderungen und Dokumentation analysieren
- CPI iFlow entwickeln
- Unit Test durchführen
- Integration Test mit Zielsystem durchführen
- Dokumentation aktualisieren

## Schritt 5: Task erstellen

```powershell
$token = $env:ATLASSIAN_API_TOKEN
$email = $env:ATLASSIAN_EMAIL
$base64 = [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes("${email}:${token}"))
$headers = @{ Authorization = "Basic $base64"; "Content-Type" = "application/json" }

# ADF-Beschreibung und Body hier aufbauen (siehe vorheriges Beispiel)
# parent.key = gewähltes Epic
# customfield_11649 = @{ id = "<customer-id>" }
# assignee = @{ accountId = "557058:a8b44127-1380-49e8-b019-b59f0d76eb2a" }

$r = Invoke-RestMethod -Uri "https://syntax.atlassian.net/rest/api/3/issue" -Headers $headers -Method Post -Body $body
Write-Host "Task erstellt: $($r.key)"
Write-Host "Link: https://syntax.atlassian.net/browse/$($r.key)"
```

## Schritt 6: Ergebnis anzeigen

Zeige den erstellten Task mit allen Details an (Key, Summary, Epic, Customer, Assignee, Link).
