# AGENTS.md

## Projektueberblick

Dieses Repository ist eine kleine Python-App fuer einen "Bauteil Scanner". Die App sucht elektronische Bauteile anhand
einer MPN in einer lokalen SQLite-Datenbank.

- Einstiegspunkt: `main.py`
- UI: `ui_main.py`
- Datenbankzugriff: `database.py`
- Datenmodell: `component.py`
- Octopart/Nexar-API-Client: `nexar_api.py`
- Octopart/Nexar-Suchskript: `octopart_search.py`
- Lokale Datenbank: `data/bauteile.sqlite`
- Datenbankinitialisierung: `database_init.py`
- Manuelles Smoke-Test-Skript: `database_test.py`

Die UI verwendet das Pythonista-spezifische Modul `ui`. Normale CPython-Umgebungen koennen die App daher nicht
vollstaendig ausfuehren, solange keine passende Kompatibilitaetsschicht vorhanden ist.

## Entwicklungsumgebung

- Sprache: Python
- Persistenz: SQLite ueber die Standardbibliothek `sqlite3`
- Externe Bauteildaten: Octopart-Daten ueber die Nexar GraphQL API
- Externe Projektkonfigurationen wie `pyproject.toml`, `requirements.txt` oder ein Testframework sind aktuell nicht
  vorhanden.
- `.idea/` ist im Repository vorhanden, aber `.gitignore` schliesst `.idea` fuer neue Aenderungen aus.

## Wichtige Befehle

Syntaxpruefung fuer alle Python-Dateien:

```bash
python3 -m py_compile main.py ui_main.py database.py component.py camera.py database_init.py database_test.py nexar_api.py octopart_search.py
```

Datenbank initialisieren und Beispieldaten schreiben:

```bash
python3 database_init.py
```

Manueller Datenbank-Smoke-Test:

```bash
python3 database_test.py
```

Hinweis: `database_test.py` erwartet vorhandene Daten in `data/bauteile.sqlite` und ist kein isolierter Unit-Test.

Octopart/Nexar-Suche per MPN:

```bash
NEXAR_CLIENT_ID=... NEXAR_CLIENT_SECRET=... python3 octopart_search.py IRLZ44N
```

Hinweis: Die Zugangsdaten kommen aus einer Nexar-Anwendung mit Supply-Zugriff. Secrets nie in Git speichern.

App starten:

```bash
python3 main.py
```

Hinweis: Das funktioniert nur in einer Umgebung, die das Pythonista-Modul `ui` bereitstellt.

## Architekturhinweise

- `Database.__init__()` verbindet sich relativ zum aktuellen Arbeitsverzeichnis mit `data/bauteile.sqlite`. Befehle
  sollten deshalb aus dem Repository-Root ausgefuehrt werden.
- `Database.create()` legt die Tabelle `components` an, wenn sie fehlt.
- `Database.add()` schreibt oder ersetzt Komponenten anhand des Primaerschluessels `mpn`.
- `Database.find()` sucht per `LIKE` nach Teilstrings der MPN und gibt die erste gefundene Komponente zurueck.
- `Component` ist ein einfaches Datenobjekt ohne Validierung.
- `NexarApi.search_mpn()` ruft `supSearchMpn` ueber `https://api.nexar.com/graphql` auf.
- `NexarApi` holt OAuth2-Tokens ueber `https://identity.nexar.com/connect/token` und cached sie bis kurz vor Ablauf.

## Bekannte Einschraenkungen

- `camera.py` referenziert `Camera` und `scan`, definiert oder importiert sie aber nicht. Diese Datei ist aktuell kein
  lauffaehiges Modul.
- `ui_main.py` setzt voraus, dass `ui` verfuegbar ist. Beim Arbeiten ausserhalb von Pythonista nur Syntax pruefen, nicht
  importbasiert testen.
- Die SQLite-Datei ist eine produktive Projektdatenquelle. Keine destruktiven Migrationen oder Testlaeufe ausfuehren,
  die Daten loeschen, ohne vorherige Zustimmung.
- Es gibt noch keine automatisierten Tests und keine isolierte Testdatenbank.
- `database_init.py` schreibt Beispieldaten in die lokale SQLite-Datei.
- `octopart_search.py` benoetigt Netzwerkzugriff und gueltige `NEXAR_CLIENT_ID` / `NEXAR_CLIENT_SECRET`.

## Coding-Richtlinien

- Aenderungen klein und fokussiert halten.
- Bestehenden Stil beibehalten: einfache Top-Level-Module, klare Klassen, keine unnoetigen Abstraktionen.
- Datenbankpfade und SQL-Zugriffe vorsichtig aendern, weil die App aktuell stark auf `data/bauteile.sqlite` gekoppelt
  ist.
- Bei neuer Datenbanklogik zuerst eine isolierte Teststrategie einfuehren, statt `database_test.py` weiter als echten
  Test auszubauen.
- Keine generierten IDE-Dateien oder lokalen virtuellen Umgebungen einchecken.

## Vor Abschluss einer Aenderung

Mindestens ausfuehren:

```bash
python3 -m py_compile main.py ui_main.py database.py component.py camera.py database_init.py database_test.py nexar_api.py octopart_search.py
```

Wenn Datenbankverhalten betroffen ist, zusaetzlich einen gezielten Smoke-Test ausfuehren und klar dokumentieren, ob
`data/bauteile.sqlite` veraendert wurde.
