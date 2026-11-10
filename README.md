# SYNTAX CPI Team – Claude Code Plugins

Geteilte **Skills, Slash-Commands und MCP-Server** für das SYNTAX CPI/SAP-Integrationsteam,
verteilt als **Claude-Code-Plugin-Marketplace** über dieses Git-Repo.

- **Team (dieses Repo, GitHub-synchronisiert):** alles unter `plugins/syntax/` – wird geteilt.
- **Lokal/persönlich (nicht synchronisiert):** bleibt in `~/.claude/` (eigene Skills, Token, Env).

## Inhalt

Plugin **`syntax`** (Marketplace `syntax-team`):

| Typ | Name | Aufruf |
|---|---|---|
| Skill | cpi | `/syntax:cpi` |
| Skill | create-iflow | `/syntax:create-iflow` |
| Skill | jira-cpi-task | `/syntax:jira-cpi-task` |
| Skill | jira-mail-task | `/syntax:jira-mail-task` |
| Skill | pi-mapping | `/syntax:pi-mapping` |
| Skill | po-migration | `/syntax:po-migration` |
| Command | idoc-map | `/syntax:idoc-map` |
| MCP | jira | (Tools `mcp__jira__*`) |

> Plugin-Skills sind **immer** mit dem Plugin-Namen genamespaced (`/syntax:<name>`) – das
> verhindert Konflikte mit gleichnamigen persönlichen Skills.

## Installation (einmalig, pro Teammitglied)

```
/plugin marketplace add <github-owner>/team-cpi-plugins
/plugin install syntax@syntax-team
```

Danach `/reload-plugins` – die Skills erscheinen in `/help`.

### Voraussetzung für den jira-MCP: Env-Variablen

Der `jira`-Server liest Zugangsdaten aus der **Umgebung** (nie aus dem Repo). Jede:r trägt sie in
die **eigene** `~/.claude/settings.json` ein:

```json
{
  "env": {
    "ATLASSIAN_EMAIL": "vorname.nachname@syntax.com",
    "ATLASSIAN_API_TOKEN": "<dein-atlassian-api-token>"
  }
}
```

API-Token erstellen: https://id.atlassian.com/manage-profile/security/api-tokens
`ATLASSIAN_URL` (`https://syntax.atlassian.net`) ist im Plugin fest hinterlegt.

## Updates beziehen

```
/plugin        # -> Plugin auswählen -> Update (zieht git pull im Hintergrund)
/reload-plugins
```

## Beitragen (neue geteilte Sachen anlegen)

Im Klon dieses Repos arbeiten, dann committen + pushen. Das Team zieht per Update nach.

| Was | Wohin |
|---|---|
| Neue **Skill** | `plugins/syntax/skills/<name>/SKILL.md` (+ optional `scripts/`, `reference/`) |
| Neuer **Command** | `plugins/syntax/commands/<name>.md` |
| Neuer **MCP-Server** | Eintrag in `plugins/syntax/.mcp.json` |

**Regeln:**
- **Keine Secrets** ins Repo. Tokens/Passwörter/E-Mails immer als `${ENV_VAR}` referenzieren
  (siehe `.mcp.json`), Wert lokal in `~/.claude/settings.json`.
- Auf **gebündelte Dateien** (eigene Skripte/Referenzen) mit **`${CLAUDE_PLUGIN_ROOT}/...`**
  verweisen – nie mit absoluten `C:\Users\...`-Pfaden. `${CLAUDE_PLUGIN_ROOT}` wird in
  SKILL.md-Inhalten automatisch auf den Installationspfad aufgelöst.
- `version` in `plugins/syntax/.claude-plugin/plugin.json` bei relevanten Änderungen hochzählen.

### Lokal entwickeln & testen

```
claude --plugin-dir <pfad>\team-cpi-plugins\plugins\syntax
claude plugin validate <pfad>\team-cpi-plugins\plugins\syntax
```

Änderungen ohne Neustart übernehmen: `/reload-plugins`.

## Lokal vs. Team – Merksatz

- **Geteilt** → in dieses Repo (`plugins/syntax/...`) → commit + push.
- **Nur für dich** → direkt in `~/.claude/skills/` bzw. `~/.claude/commands/` (kurzer Name, kein
  Namespace, nicht synchronisiert).

## Struktur

```
team-cpi-plugins/
├── .claude-plugin/marketplace.json     # Marketplace-Definition
└── plugins/syntax/
    ├── .claude-plugin/plugin.json      # Plugin-Manifest
    ├── skills/<name>/SKILL.md          # Skills (+ Support-Dateien)
    ├── commands/<name>.md              # Slash-Commands
    └── .mcp.json                       # MCP-Server (Secrets via ${ENV})
```
