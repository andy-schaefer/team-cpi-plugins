---
description: 'Liest eine IDoc-Struktur aus einer WE60-Exportdatei (.txt) und trägt sie als Destination-Struktur in ein Excel-Mapping-Template (.xlsx) ein. Aufruf: /syntax:idoc-map <xlsx-Pfad> <txt-Pfad>.'
argument-hint: <xlsx-Pfad> <txt-Pfad>
---

# IDoc Mapping Skill

Liest eine IDoc-Struktur aus einer WE60-Exportdatei (.txt) und trägt sie als Destination-Struktur in ein Excel-Mapping-Template (.xlsx) ein.

## Aufruf

```
/idoc-map <xlsx-Pfad> <txt-Pfad>
```

**Beispiel:**
```
/idoc-map C:\Users\itshaea\Downloads\@vc\VC_Payroll_CN_map.xlsx C:\Users\itshaea\Downloads\acc_employee_exp01.txt
```

## Was der Skill tut

1. Liest die IDoc-Strukturdatei (WE60-Format) ein
2. Parst alle Segmente und Felder (Datentyp, externe Länge, Beschreibung)
3. Öffnet die Excel-Datei per PowerShell/COM
4. Findet das Mapping-Sheet (sucht nach Sheet mit Spaltenheader "segment" und "field")
5. Hebt zusammengeführte Zellen (MergeCells) im Destination-Bereich auf
6. Trägt die IDoc-Struktur ab Zeile 7 in die Destination-Spalten ein:
   - Spalte 11: structure (IDoc-Typname)
   - Spalte 12: segment (z.B. E1BPACHE04)
   - Spalte 13: field (Feldname)
   - Spalte 14: data type (CHAR, NUMC, DATS, DEC, ...)
   - Spalte 15: data length (externe Länge)
   - Spalte 16: Mandatory (M für Pflichtfelder wie COMP_CODE, PSTNG_DATE)
   - Spalte 17: description (Feldbeschreibung)
   - Spalte 18: comment / conversion (z.B. "YYYYMMDD" für DATS-Felder)
7. Speichert die Excel-Datei

## Verhalten

- Segment-Headerzeilen (ohne Feldname) enthalten in Spalte 16 die Kardinalität (z.B. `1..1`, `0..n`)
- DATS-Felder erhalten automatisch den Kommentar `YYYYMMDD`
- DEC/QUAN-Felder erhalten einen Hinweis auf die Dezimalstellen
- Felder wie COMP_CODE, PSTNG_DATE, DOC_DATE, FISC_YEAR, GL_ACCOUNT, ITEMNO_ACC, CURRENCY, AMT_DOCCUR werden als Mandatory (`M`) markiert
- Veraltete Felder (Feldname enthält "LONG" und Beschreibung "Obsolete") erhalten den Kommentar `obsolete`

## Implementierungshinweise für Claude

Beim Ausführen dieses Skills:

1. **Argumente parsen**: Erstes Argument = xlsx-Pfad, zweites Argument = txt-Pfad.

2. **IDoc-Datei lesen und parsen**:
   - IDoc-Name steht in Zeile 2 nach "Structure of basic type "
   - Segmente werden erkannt durch Zeilen der Form `E1XXXXX : Beschreibung`
   - Felder: Feldname steht in der Zeile vor "internal data type : XXX"
   - Externe Länge: `external length : XXXXXX`
   - Kardinalität aus `min. number` und `max. number`

3. **Excel per PowerShell befüllen** (Windows COM-Objekt):
   ```powershell
   $excel = New-Object -ComObject Excel.Application
   $excel.Visible = $false
   $excel.DisplayAlerts = $false
   $wb = $excel.Workbooks.Open("<xlsx-Pfad>")
   ```

4. **Mapping-Sheet finden**: Suche Sheet, das in Zeile 6 die Spaltenheader
   "structure", "segment", "field" enthält. Falls keines gefunden, nimm das Sheet mit "<Message>" im Namen.

5. **Startzeile ermitteln**: Zeile nach dem Header-Row (typisch Zeile 7).

6. **MergeCells aufheben**: Alle zusammengeführten Zellen in Spalten 11-18
   vor dem Schreiben aufheben (`MergeArea.UnMerge()`).

7. **Daten schreiben**: Pro Segment eine Headerzeile, dann je eine Zeile pro Feld.

8. **Speichern**: `$wb.Save()` dann `$wb.Close($true)`.

9. **Abschluss**: Anzahl geschriebener Segmente und Felder ausgeben.
