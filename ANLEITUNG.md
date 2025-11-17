# Anleitung - Home Assistant Overview Tool

## Übersicht

Dieses Tool bietet eine webbasierte Benutzeroberfläche (GUI) mit Frontend und Backend, um einen vollständigen Überblick über Ihre Home Assistant Installation zu erhalten.

## Was macht dieses Tool?

Das Tool erstellt eine vollständige Dokumentation von:
- Alle installierten Integrationen/Komponenten
- Alle Entitäten sortiert nach Domain (z.B. light, switch, sensor, etc.)
- Verfügbare Services
- System-Informationen
- Detaillierte Statistiken

## Voraussetzungen

1. **Python 3.7 oder höher** installiert
2. **Home Assistant** läuft und ist erreichbar
3. **Long-Lived Access Token** von Home Assistant

## Installation

### Schritt 1: Repository klonen oder herunterladen

```bash
git clone https://github.com/Kenearos/Homeassistant.git
cd Homeassistant
```

### Schritt 2: Abhängigkeiten installieren

```bash
pip install -r requirements.txt
```

Oder manuell:

```bash
pip install Flask requests
```

## Home Assistant Token erstellen

### Schritt-für-Schritt:

1. **Öffnen Sie Ihre Home Assistant Web-Oberfläche**
   - Im Browser: `http://homeassistant.local:8123` (oder Ihre IP-Adresse)

2. **Melden Sie sich an**
   - Mit Ihren Home Assistant Zugangsdaten

3. **Öffnen Sie Ihr Profil**
   - Klicken Sie auf das Profilsymbol (unten links in der Seitenleiste)
   - Oder navigieren Sie zu: Einstellungen → Personen → Ihr Name

4. **Erstellen Sie einen Long-Lived Access Token**
   - Scrollen Sie nach unten zum Abschnitt "Long-Lived Access Tokens"
   - Klicken Sie auf "TOKEN ERSTELLEN"
   - Geben Sie einen Namen ein (z.B. "Overview Tool")
   - Klicken Sie auf "OK"

5. **Token kopieren**
   - **WICHTIG:** Der Token wird nur EINMAL angezeigt!
   - Kopieren Sie den Token sofort
   - Speichern Sie ihn sicher (z.B. in einem Passwort-Manager)

## Verwendung

### Option 1: Web-GUI (Empfohlen) 🌐

#### Server starten:

```bash
python app.py
```

Der Server startet auf `http://localhost:5000`

#### Im Browser öffnen:

1. Öffnen Sie Ihren Browser
2. Gehen Sie zu: `http://localhost:5000`
3. Sie sehen die Web-Oberfläche mit integrierter Anleitung

#### Bericht erstellen:

1. **Home Assistant URL eingeben**
   - Beispiel: `http://homeassistant.local:8123`
   - Oder: `http://192.168.1.100:8123`

2. **Token eingeben**
   - Fügen Sie Ihren Long-Lived Access Token ein

3. **Optional: Konfiguration speichern**
   - Aktivieren Sie die Checkbox "Konfiguration speichern"
   - Beim nächsten Start werden die Daten automatisch geladen

4. **Verbindung testen**
   - Klicken Sie auf "Verbindung testen"
   - Warten Sie auf die Bestätigung

5. **Bericht generieren**
   - Klicken Sie auf "Bericht generieren"
   - Der Bericht wird erstellt und angezeigt

6. **Bericht herunterladen (optional)**
   - Klicken Sie auf "Als JSON herunterladen" oder "Als Text herunterladen"
   - Die Datei wird automatisch heruntergeladen

### Option 2: Kommandozeile (Original-Skript)

```bash
python ha-overview.py
```

Sie werden nach URL und Token gefragt. Der Bericht wird als JSON, TXT und HTML gespeichert.

## Ausgabeformate

### JSON
- Maschinenlesbar
- Enthält alle Details
- Ideal für Weiterverarbeitung

### TXT
- Menschenlesbar
- Strukturierte Textausgabe
- Ideal für Dokumentation

### HTML (nur bei Kommandozeilen-Tool)
- Webseite mit schöner Darstellung
- Alle Informationen übersichtlich
- Kann im Browser geöffnet werden

## Beispiel-Workflow

### Szenario: Erste Verwendung

1. **Installation durchführen**
   ```bash
   pip install -r requirements.txt
   ```

2. **Token in Home Assistant erstellen**
   - Profil → Long-Lived Access Tokens → TOKEN ERSTELLEN

3. **Web-GUI starten**
   ```bash
   python app.py
   ```

4. **Browser öffnen**
   - Gehe zu `http://localhost:5000`

5. **Daten eingeben**
   - URL: `http://homeassistant.local:8123`
   - Token: (Ihr Token)
   - ✓ Konfiguration speichern

6. **Verbindung testen**
   - Klick auf "Verbindung testen"
   - Warte auf grüne Bestätigung

7. **Bericht erstellen**
   - Klick auf "Bericht generieren"
   - Warte bis Statistiken angezeigt werden

8. **Download (optional)**
   - Klick auf "Als JSON herunterladen"

### Szenario: Regelmäßige Nutzung

Wenn Sie die Konfiguration gespeichert haben:

1. **Server starten**
   ```bash
   python app.py
   ```

2. **Browser öffnen**
   - Gehe zu `http://localhost:5000`
   - URL ist bereits ausgefüllt!

3. **Token eingeben**
   - Fügen Sie nur noch Ihren Token ein

4. **Bericht generieren**
   - Direkt auf "Bericht generieren" klicken

## Fehlerbehebung

### Problem: "Verbindung fehlgeschlagen"

**Mögliche Ursachen:**
1. Home Assistant läuft nicht
2. Falsche URL
3. Ungültiger Token
4. Firewall blockiert die Verbindung

**Lösungen:**
- Überprüfen Sie, ob Home Assistant erreichbar ist
- Testen Sie die URL im Browser
- Erstellen Sie einen neuen Token
- Überprüfen Sie Firewall-Einstellungen

### Problem: "ModuleNotFoundError: No module named 'flask'"

**Lösung:**
```bash
pip install Flask
```

### Problem: "Port bereits in Verwendung"

**Lösung:**
Ändern Sie den Port in `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5001)  # Statt 5000
```

### Problem: Token wird nicht akzeptiert

**Lösung:**
1. Erstellen Sie einen neuen Token in Home Assistant
2. Kopieren Sie den gesamten Token (ohne Leerzeichen)
3. Probieren Sie es erneut

## Sicherheitshinweise

⚠️ **WICHTIG:**

1. **Token niemals teilen**
   - Der Token gibt vollen Zugriff auf Home Assistant
   - Behandeln Sie ihn wie ein Passwort

2. **Token sicher speichern**
   - Verwenden Sie einen Passwort-Manager
   - Speichern Sie ihn nicht in öffentlichen Repositories

3. **HTTPS verwenden (in Produktion)**
   - Für lokale Tests ist HTTP OK
   - Bei Remote-Zugriff: Verwenden Sie HTTPS

4. **Regelmäßig Token erneuern**
   - Alte Token deaktivieren
   - Neue Token erstellen

## Erweiterte Optionen

### Remote-Zugriff aktivieren

Standardmäßig läuft der Server nur lokal. Für Zugriff aus dem Netzwerk:

```python
# In app.py:
app.run(debug=False, host='0.0.0.0', port=5000)
```

**Achtung:** Nur in vertrauenswürdigen Netzwerken!

### Automatischer Start beim Systemstart

Erstellen Sie einen Systemd-Service (Linux):

```bash
sudo nano /etc/systemd/system/ha-overview.service
```

Inhalt:
```ini
[Unit]
Description=Home Assistant Overview Web GUI
After=network.target

[Service]
Type=simple
User=IhrBenutzer
WorkingDirectory=/pfad/zum/Homeassistant
ExecStart=/usr/bin/python3 /pfad/zum/Homeassistant/app.py
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

Aktivieren:
```bash
sudo systemctl enable ha-overview.service
sudo systemctl start ha-overview.service
```

## FAQ

### F: Kann ich das Tool auf einem anderen Computer nutzen?

**A:** Ja! Sie können den Server auf einem Computer starten und von einem anderen im selben Netzwerk darauf zugreifen. Verwenden Sie die IP-Adresse des Servers.

### F: Werden meine Daten gespeichert?

**A:** Nur wenn Sie "Konfiguration speichern" aktivieren. Dann werden URL und Token in `config.json` gespeichert. Berichte werden nur temporär erstellt.

### F: Kann ich mehrere Home Assistant Instanzen verwalten?

**A:** Ja, indem Sie für jede Instanz andere URL und Token eingeben. Die Konfiguration speichert nur eine Instanz, aber Sie können manuell wechseln.

### F: Funktioniert das mit Home Assistant OS?

**A:** Ja! Das Tool läuft unabhängig von Home Assistant und benötigt nur Netzwerkzugriff zur API.

### F: Wie oft sollte ich den Bericht aktualisieren?

**A:** Nach Bedarf. Bei Änderungen an Ihrer Installation (neue Geräte, Integrationen) generieren Sie einen neuen Bericht.

## Support

Bei Problemen:
1. Überprüfen Sie die Fehlerbehebung oben
2. Erstellen Sie ein Issue auf GitHub
3. Geben Sie Details an:
   - Fehlermeldung
   - Python-Version
   - Home Assistant Version
   - Betriebssystem

## Lizenz

MIT License - Frei verwendbar

## Danksagungen

- Home Assistant Community
- Flask Framework
- Alle Mitwirkenden

---

**Version:** 1.0  
**Letzte Aktualisierung:** November 2024  
**Autor:** Kenearos
