#!/usr/bin/env python3
"""
Home Assistant Overview - Web Application
Flask-basierte Web-Anwendung mit Frontend und Backend
"""

from flask import Flask, render_template, request, jsonify, send_file
from ha_overview import HomeAssistantOverview
import os
import json
from datetime import datetime

app = Flask(__name__)

# Konfigurationsdatei
CONFIG_FILE = 'config.json'

def load_config():
    """Lade gespeicherte Konfiguration"""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_config(url, token):
    """Speichere Konfiguration"""
    config = {'url': url, 'token': token}
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f)

@app.route('/')
def index():
    """Hauptseite mit Anleitung und Formular"""
    config = load_config()
    return render_template('index.html', 
                         saved_url=config.get('url', ''),
                         has_config=bool(config))

@app.route('/api/test-connection', methods=['POST'])
def test_connection():
    """Teste die Verbindung zu Home Assistant"""
    data = request.json
    url = data.get('url')
    token = data.get('token')
    
    if not url or not token:
        return jsonify({'success': False, 'error': 'URL und Token sind erforderlich'})
    
    try:
        ha = HomeAssistantOverview(url, token)
        success = ha.test_connection()
        
        if success:
            # Speichere Konfiguration wenn gewünscht
            if data.get('save_config'):
                save_config(url, token)
            
            return jsonify({'success': True, 'message': 'Verbindung erfolgreich!'})
        else:
            return jsonify({'success': False, 'error': 'Verbindung fehlgeschlagen'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/generate-report', methods=['POST'])
def generate_report():
    """Generiere vollständigen Bericht"""
    data = request.json
    url = data.get('url')
    token = data.get('token')
    
    if not url or not token:
        return jsonify({'success': False, 'error': 'URL und Token sind erforderlich'})
    
    try:
        ha = HomeAssistantOverview(url, token)
        report = ha.generate_report()
        
        if report:
            # Speichere Konfiguration wenn gewünscht
            if data.get('save_config'):
                save_config(url, token)
            
            return jsonify({
                'success': True,
                'report': report
            })
        else:
            return jsonify({'success': False, 'error': 'Report-Generierung fehlgeschlagen'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/download-report', methods=['POST'])
def download_report():
    """Erstelle und lade Report-Datei herunter"""
    data = request.json
    url = data.get('url')
    token = data.get('token')
    format_type = data.get('format', 'json')

    if not url or not token:
        return jsonify({'success': False, 'error': 'URL und Token sind erforderlich'})

    try:
        ha = HomeAssistantOverview(url, token)
        report = ha.generate_report()

        if report:
            # Erstelle temporäres Verzeichnis falls nicht vorhanden
            os.makedirs('downloads', exist_ok=True)

            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

            if format_type == 'json':
                filename = f'downloads/ha_overview_{timestamp}.json'
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(report, f, indent=2, ensure_ascii=False)
            elif format_type == 'txt':
                filename = f'downloads/ha_overview_{timestamp}.txt'
                # Vereinfachte Textausgabe
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write("="*80 + "\n")
                    f.write("HOME ASSISTANT - VOLLSTÄNDIGER ÜBERBLICK\n")
                    f.write("="*80 + "\n")
                    f.write(f"Generiert am: {datetime.now().strftime('%d.%m.%Y um %H:%M:%S')}\n")
                    f.write("="*80 + "\n\n")
                    f.write(f"System: {report['system_info']['version']}\n")
                    f.write(f"Entitäten: {report['statistics']['total_entities']}\n")
                    f.write(f"Komponenten: {report['statistics']['total_components']}\n")
            elif format_type == 'claude':
                filename = f'downloads/ha_overview_{timestamp}_claude.md'
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(generate_claude_format(report))
            else:
                return jsonify({'success': False, 'error': 'Ungültiges Format'})

            return send_file(filename, as_attachment=True)
        else:
            return jsonify({'success': False, 'error': 'Report-Generierung fehlgeschlagen'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


def generate_claude_format(report):
    """Generiere Claude-freundliches Markdown-Format"""
    lines = []

    # Header
    lines.append("# Home Assistant Konfiguration")
    lines.append("")
    lines.append("Dieser Export enthält alle relevanten Informationen meiner Home Assistant Installation.")
    lines.append("Bitte nutze diese Daten um mir bei Fragen, Automatisierungen oder Problemlösungen zu helfen.")
    lines.append("")

    # System Info
    sys_info = report.get('system_info', {})
    lines.append("## System Information")
    lines.append("")
    lines.append(f"- **Version:** {sys_info.get('version', 'Unbekannt')}")
    lines.append(f"- **Standort:** {sys_info.get('location_name', 'Unbekannt')}")
    lines.append(f"- **Zeitzone:** {sys_info.get('timezone', 'Unbekannt')}")
    lines.append(f"- **Einheiten:** {sys_info.get('unit_system', 'Unbekannt')}")
    lines.append("")

    # Statistiken
    stats = report.get('statistics', {})
    lines.append("## Übersicht / Statistiken")
    lines.append("")
    lines.append(f"- **Komponenten/Integrationen:** {stats.get('total_components', 0)}")
    lines.append(f"- **Entitäten gesamt:** {stats.get('total_entities', 0)}")
    lines.append(f"- **Services:** {stats.get('total_services', 0)}")
    lines.append(f"- **Domains:** {stats.get('total_domains', 0)}")
    lines.append(f"- **Events:** {stats.get('total_events', 0)}")
    lines.append("")

    # Entitäten nach Domain
    entities_by_domain = report.get('entities_by_domain', {})
    if entities_by_domain:
        lines.append("## Entitäten nach Domain")
        lines.append("")
        lines.append("| Domain | Anzahl |")
        lines.append("|--------|--------|")
        for domain, count in sorted(entities_by_domain.items(), key=lambda x: -x[1]):
            lines.append(f"| {domain} | {count} |")
        lines.append("")

    # Detaillierte Entitäten
    detailed = report.get('detailed_entities', {})
    if detailed:
        lines.append("## Alle Entitäten (Details)")
        lines.append("")
        for domain, entities in sorted(detailed.items()):
            lines.append(f"### {domain.upper()} ({len(entities)} Entitäten)")
            lines.append("")
            for entity in entities:
                entity_id = entity.get('entity_id', 'unknown')
                friendly_name = entity.get('attributes', {}).get('friendly_name', entity_id)
                state = entity.get('state', 'unknown')
                device_class = entity.get('attributes', {}).get('device_class', '')

                device_info = f" ({device_class})" if device_class else ""
                lines.append(f"- `{entity_id}`: **{friendly_name}**{device_info} = `{state}`")
            lines.append("")

    # Installierte Komponenten
    components = report.get('components', [])
    if components:
        lines.append("## Installierte Komponenten/Integrationen")
        lines.append("")
        # Gruppiere in Zeilen zu je 5
        for i in range(0, len(components), 5):
            chunk = components[i:i+5]
            lines.append("- " + ", ".join(f"`{c}`" for c in chunk))
        lines.append("")

    # Services (gruppiert)
    services = report.get('services', [])
    if services:
        lines.append("## Verfügbare Services")
        lines.append("")
        services_by_domain = {}
        for service in services:
            domain = service.get('domain', 'unknown')
            if domain not in services_by_domain:
                services_by_domain[domain] = []
            services_by_domain[domain].append(service.get('service', ''))

        for domain, service_list in sorted(services_by_domain.items()):
            lines.append(f"### {domain}")
            for svc in sorted(service_list):
                lines.append(f"- `{domain}.{svc}`")
            lines.append("")

    # Footer mit Hinweis
    lines.append("---")
    lines.append("")
    lines.append("## Hinweise für Claude")
    lines.append("")
    lines.append("Mit diesen Daten kannst du mir helfen bei:")
    lines.append("- Automatisierungen erstellen (YAML für automations.yaml)")
    lines.append("- Skripte schreiben")
    lines.append("- Dashboard/Lovelace Konfigurationen")
    lines.append("- Problemdiagnose")
    lines.append("- Entity-IDs für Szenen und Skripte finden")
    lines.append("- Service-Calls zusammenstellen")
    lines.append("")
    lines.append(f"*Exportiert am: {datetime.now().strftime('%d.%m.%Y um %H:%M:%S')}*")

    return "\n".join(lines)

if __name__ == '__main__':
    # Erstelle templates-Verzeichnis falls nicht vorhanden
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static', exist_ok=True)
    
    print("\n" + "="*80)
    print("HOME ASSISTANT OVERVIEW - WEB APPLICATION")
    print("="*80)
    print("\nStarte Server auf http://localhost:5000")
    print("Drücke CTRL+C zum Beenden\n")
    
    # Note: debug=False for security. Set to True only in trusted development environments.
    app.run(debug=False, host='0.0.0.0', port=5000)
