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
            else:
                return jsonify({'success': False, 'error': 'Ungültiges Format'})
            
            return send_file(filename, as_attachment=True)
        else:
            return jsonify({'success': False, 'error': 'Report-Generierung fehlgeschlagen'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    # Erstelle templates-Verzeichnis falls nicht vorhanden
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static', exist_ok=True)
    
    print("\n" + "="*80)
    print("HOME ASSISTANT OVERVIEW - WEB APPLICATION")
    print("="*80)
    print("\nStarte Server auf http://localhost:5000")
    print("Drücke CTRL+C zum Beenden\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
