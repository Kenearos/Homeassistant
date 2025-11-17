# Home Assistant Overview Tool

Ein webbasiertes Tool mit Frontend und Backend zur Erstellung einer vollständigen Übersicht über Ihre Home Assistant Installation.

## 🌟 Features

- 🌐 **Web-GUI** - Moderne, benutzerfreundliche Weboberfläche
- 📖 **Integrierte Anleitung** - Schritt-für-Schritt Anweisungen direkt im Frontend
- 🔄 **Echtzeit-Verbindungstest** - Testen Sie Ihre Verbindung vor der Berichtserstellung
- 💾 **Konfigurationsspeicherung** - Speichern Sie URL und Token für spätere Verwendung
- 📊 **Detaillierte Statistiken** - Komponenten, Entitäten, Services, Domains
- 📥 **Export-Funktionen** - Download als JSON oder TXT
- 🎨 **Responsive Design** - Funktioniert auf Desktop und Mobile

## 🚀 Schnellstart

### 1. Installation

```bash
git clone https://github.com/Kenearos/Homeassistant.git
cd Homeassistant
pip install -r requirements.txt
```

### 2. Server starten

```bash
python app.py
```

### 3. Browser öffnen

Öffnen Sie `http://localhost:5000` in Ihrem Browser.

## 📚 Dokumentation

Für eine ausführliche Anleitung auf Deutsch, siehe [ANLEITUNG.md](ANLEITUNG.md).

Die Anleitung enthält:
- Schritt-für-Schritt Installation
- Home Assistant Token erstellen
- Verwendung der Web-GUI
- Kommandozeilen-Tool
- Fehlerbehebung
- Sicherheitshinweise
- FAQ

## 🔑 Home Assistant Token erstellen

1. Öffnen Sie Home Assistant
2. Klicken Sie auf Ihr Profil (unten links)
3. Scrollen Sie zu "Long-Lived Access Tokens"
4. Klicken Sie auf "TOKEN ERSTELLEN"
5. Geben Sie einen Namen ein
6. Kopieren Sie den Token (wird nur einmal angezeigt!)

## 💻 Verwendung

### Web-GUI (Empfohlen)

1. Server starten: `python app.py`
2. Browser öffnen: `http://localhost:5000`
3. URL und Token eingeben
4. "Bericht generieren" klicken
5. Optional: Bericht herunterladen

### Kommandozeile

```bash
python ha-overview.py
```

Sie werden interaktiv nach URL und Token gefragt.

## 📋 Anforderungen

- Python 3.7+
- Flask
- requests
- Zugriff auf Home Assistant API
- Long-Lived Access Token

## 🛠️ Technische Details

### Architektur

- **Backend:** Flask (Python)
- **Frontend:** HTML/CSS/JavaScript
- **API-Kommunikation:** REST API mit Home Assistant
- **Datenspeicherung:** JSON (optional)

### Verzeichnisstruktur

```
Homeassistant/
├── app.py              # Flask Backend-Server
├── ha-overview.py      # Original Kommandozeilen-Tool
├── ha_overview.py      # Modul-Version
├── templates/
│   └── index.html      # Frontend Web-GUI
├── requirements.txt    # Python-Abhängigkeiten
├── ANLEITUNG.md        # Ausführliche deutsche Anleitung
└── README.md           # Diese Datei
```

## 🔒 Sicherheit

- ⚠️ Token niemals teilen oder in öffentlichen Repositories speichern
- 🔐 Verwenden Sie HTTPS für Remote-Zugriff
- 🔄 Erneuern Sie Token regelmäßig
- 🏠 Verwenden Sie das Tool nur in vertrauenswürdigen Netzwerken

## 🤝 Mitwirken

Beiträge sind willkommen! Bitte erstellen Sie ein Issue oder Pull Request.

## 📄 Lizenz

MIT License

## 👤 Autor

Kenearos

---

**Für die vollständige Anleitung auf Deutsch, siehe [ANLEITUNG.md](ANLEITUNG.md)**