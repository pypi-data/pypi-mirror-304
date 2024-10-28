[English](README.md) | [Italiano](README.it.md) | [Français](README.fr.md) | [Deutsch](README.de.md) | [Español](README.es.md)

# Lisa - Code-Analysator für LLMs

Lisa (inspiriert von Lisa Simpson) ist ein Tool, das entwickelt wurde, um die Analyse von Quellcode durch Large Language Models (LLMs) zu vereinfachen. Intelligent und analytisch wie die Figur, nach der sie benannt ist, hilft Lisa dabei, Code mit Logik und Methode zu studieren und zu interpretieren.

## Beschreibung

Lisa ist ein essentielles Werkzeug für alle, die ihren Code analysieren oder Open-Source-Projekte mithilfe von Large Language Models studieren möchten. Ihr Hauptziel ist es, eine einzelne Textdatei zu generieren, die alle Referenzen und die Struktur des ursprünglichen Codes beibehält und ihn so für ein LLM leicht interpretierbar macht.

Dieser Ansatz löst eines der häufigsten Probleme bei der Code-Analyse mit LLMs: die Fragmentierung von Dateien und den Verlust von Referenzen zwischen verschiedenen Projektkomponenten.

## Konfiguration

Das Projekt verwendet eine `combine_config.yaml` Konfigurationsdatei, mit der Sie anpassen können, welche Dateien in die Analyse einbezogen oder ausgeschlossen werden sollen. Die Standardkonfiguration ist:

```yaml
# Einschlussmuster (Erweiterungen oder Verzeichnisse zum Einschließen)
includes:
  - "*.py"  
  # Sie können weitere Erweiterungen oder Verzeichnisse hinzufügen

# Ausschlussmuster (Verzeichnisse oder Dateien zum Ausschließen)
excludes:
  - ".git"
  - "__pycache__"
  - "*.egg-info"
  - "venv*"
  - ".vscode"
  - "agents*"
  - "log"
```

### Einschluss-/Ausschlussmuster
- Muster in `includes` bestimmen, welche Dateien verarbeitet werden (z.B. "*.py" schließt alle Python-Dateien ein)
- Muster in `excludes` geben an, welche Dateien oder Verzeichnisse ignoriert werden sollen
- Sie können das *-Zeichen als Platzhalter verwenden
- Muster werden sowohl auf Dateinamen als auch auf Verzeichnispfade angewendet
- **Wichtig**: Ausschlussregeln haben immer Vorrang vor Einschlussregeln

### Regelpriorität
Wenn es "Konflikte" zwischen Einschluss- und Ausschlussregeln gibt, haben die Ausschlussregeln immer Vorrang. Hier einige Beispiele:

```
Beispiel 1:
/project_root
    /src_code
        /utils
            /logs
                file1.py
                file2.py
            helpers.py
```
Wenn wir diese Regeln haben:
- includes: ["*.py"]
- excludes: ["*logs"]

In diesem Fall werden `file1.py` und `file2.py` NICHT eingeschlossen, obwohl sie die .py-Erweiterung haben, da sie sich in einem Verzeichnis befinden, das dem Ausschlussmuster "*logs" entspricht. Die Datei `helpers.py` wird eingeschlossen.

```
Beispiel 2:
/project_root
    /includes_dir
        /excluded_subdir
            important.py
```
Wenn wir diese Regeln haben:
- includes: ["includes_dir"]
- excludes: ["*excluded*"]

In diesem Fall wird `important.py` NICHT eingeschlossen, da sie sich in einem Verzeichnis befindet, das einem Ausschlussmuster entspricht, auch wenn ihr übergeordnetes Verzeichnis einem Einschlussmuster entspricht.

## Verwendung

Das Skript wird von der Kommandozeile aus mit folgendem Befehl ausgeführt:

```bash
cmb [optionen]
```

> **Hinweis**: Der führende Unterstrich im Dateinamen ist absichtlich und ermöglicht die automatische Vervollständigung (TAB) in der Shell.

### Standardstruktur und -name
Um zu verstehen, welcher Dateiname standardmäßig verwendet wird, betrachten wir diese Struktur:

```
/home/user/projekte
    /mein_test_projekt     <- Dies ist das Wurzelverzeichnis
        /scripts
            _combine_code.py
            combine_config.yaml
        /src
            main.py
        /tests
            test_main.py
```

In diesem Fall wird der Standardname "MEIN_TEST_PROJEKT" sein (der Name des Wurzelverzeichnisses in Großbuchstaben).

### Verfügbare Parameter:

- `--clean`: Entfernt zuvor generierte Textdateien
- `--output NAME`: Gibt das Präfix für den Ausgabedateinamen an
  ```bash
  # Beispiel mit Standardnamen (aus der obigen Struktur)
  python \scripts\_combine_code.py
  # Ausgabe: MEIN_TEST_PROJEKT_20240327_1423.txt

  # Beispiel mit benutzerdefiniertem Namen
  python \scripts\_combine_code.py --output PROJEKT_ANALYSE
  # Ausgabe: PROJEKT_ANALYSE_20240327_1423.txt
  ```

### Ausgabe

Das Skript generiert eine Textdatei mit dem Format:
`NAME_JJJJMMTT_HHMM.txt`

wobei:
- `NAME` ist das mit --output angegebene oder das Standard-Präfix
- `JJJJMMTT_HHMM` ist der Generierungszeitstempel

## Verwendung mit GitHub-Projekten

Um Lisa mit einem GitHub-Projekt zu verwenden, folgen Sie diesen Schritten:

1. **Umgebungsvorbereitung**:
   ```bash
   # Erstellen Sie ein Verzeichnis für Ihre Projekte und wechseln Sie hinein
   mkdir ~/projekte
   cd ~/projekte
   ```

2. **Klonen Sie das zu analysierende Projekt**:
   ```bash
   # Beispiel mit einem hypothetischen "moon_project"
   git clone moon_project.git
   ```

3. **Integrieren Sie Lisa in das Projekt**:
   ```bash
   # Klonen Sie das Lisa-Repository
   git clone https://github.com/ihrname/lisa.git

   # Kopieren Sie den scripts-Ordner von Lisa in moon_project
   cp -r lisa/scripts moon_project/
   cp lisa/scripts/combine_config.yaml moon_project/scripts/
   ```

4. **Führen Sie die Analyse aus**:
   ```bash
   cd moon_project
   python scripts/_combine_code.py
   ```

### Best Practices für die Analyse
- Stellen Sie vor dem Ausführen von Lisa sicher, dass Sie sich im Wurzelverzeichnis des zu analysierenden Projekts befinden
- Überprüfen und passen Sie die `combine_config.yaml` Datei entsprechend den spezifischen Anforderungen des Projekts an
- Verwenden Sie die Option `--clean`, um das Verzeichnis ordentlich zu halten, wenn Sie mehrere Versionen generieren

## Zusätzliche Hinweise

- Lisa behält die hierarchische Struktur der Dateien im generierten Dokument bei
- Jede Datei wird durch Trennzeichen klar abgegrenzt, die ihren relativen Pfad anzeigen
- Der Code wird unter Beibehaltung der Verzeichnistiefenordnung organisiert
- Generierte Dateien können einfach mit LLMs zur Analyse geteilt werden

## Beitragen

Wenn Sie zum Projekt beitragen möchten, können Sie:
- Issues öffnen, um Bugs zu melden oder Verbesserungen vorzuschlagen
- Pull Requests mit neuen Funktionen einreichen
- Die Dokumentation verbessern
- Ihre Anwendungsfälle und Vorschläge teilen

## Lizenz

MIT-Lizenz

Copyright (c) 2024

Hiermit wird unentgeltlich jeder Person, die eine Kopie der Software und der zugehörigen
Dokumentationen (die "Software") erhält, die Erlaubnis erteilt, sie uneingeschränkt zu
nutzen, inklusive und ohne Ausnahme dem Recht, sie zu verwenden, zu kopieren, zu
ändern, zusammenzuführen, zu veröffentlichen, zu verbreiten, zu unterlizenzieren
und/oder zu verkaufen, und Personen, denen diese Software überlassen wird, diese
Rechte zu verschaffen, unter den folgenden Bedingungen:

Der obige Urheberrechtsvermerk und dieser Erlaubnisvermerk sind in allen Kopien oder
Teilkopien der Software beizulegen.

DIE SOFTWARE WIRD OHNE JEDE AUSDRÜCKLICHE ODER IMPLIZIERTE GARANTIE BEREITGESTELLT,
EINSCHLIESSLICH DER GARANTIE ZUR BENUTZUNG FÜR DEN VORGESEHENEN ODER EINEM
BESTIMMTEN ZWECK SOWIE JEGLICHER RECHTSVERLETZUNG, JEDOCH NICHT DARAUF BESCHRÄNKT.
IN KEINEM FALL SIND DIE AUTOREN ODER COPYRIGHTINHABER FÜR JEGLICHEN SCHADEN ODER
SONSTIGE ANSPRÜCHE HAFTBAR ZU MACHEN, OB INFOLGE DER ERFÜLLUNG EINES VERTRAGES,
EINES DELIKTES ODER ANDERS IM ZUSAMMENHANG MIT DER SOFTWARE ODER SONSTIGER
VERWENDUNG DER SOFTWARE ENTSTANDEN.