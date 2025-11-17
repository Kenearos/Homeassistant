#!/usr/bin/env python3
"""
Home Assistant Complete Overview Tool
Erstellt eine vollständige Dokumentation aller Integrationen, Entitäten und Dienste
"""

import requests
import json
from datetime import datetime
from collections import defaultdict

class HomeAssistantOverview:
    def __init__(self, url, token):
        """
        Initialize Home Assistant connection
        
        Args:
            url: Home Assistant URL (z.B. http://homeassistant.local:8123)
            token: Long-Lived Access Token
        """
        self.url = url.rstrip('/')
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
    def test_connection(self):
        """Teste die Verbindung zu Home Assistant"""
        try:
            response = requests.get(f"{self.url}/api/", headers=self.headers, timeout=10)
            if response.status_code == 200:
                print("✓ Verbindung erfolgreich!")
                return True
            else:
                print(f"✗ Fehler: Status Code {response.status_code}")
                return False
        except Exception as e:
            print(f"✗ Verbindungsfehler: {e}")
            return False
    
    def get_config(self):
        """Hole die Konfiguration"""
        response = requests.get(f"{self.url}/api/config", headers=self.headers)
        return response.json()
    
    def get_components(self):
        """Hole alle installierten Komponenten/Integrationen"""
        response = requests.get(f"{self.url}/api/config/core", headers=self.headers)
        data = response.json()
        return data.get('components', [])
    
    def get_states(self):
        """Hole alle Entitäten mit ihren Zuständen"""
        response = requests.get(f"{self.url}/api/states", headers=self.headers)
        return response.json()
    
    def get_services(self):
        """Hole alle verfügbaren Services"""
        response = requests.get(f"{self.url}/api/services", headers=self.headers)
        return response.json()
    
    def get_events(self):
        """Hole alle verfügbaren Events"""
        response = requests.get(f"{self.url}/api/events", headers=self.headers)
        return response.json()
    
    def analyze_entities(self, states):
        """Analysiere Entitäten nach Domains"""
        by_domain = defaultdict(list)
        for entity in states:
            domain = entity['entity_id'].split('.')[0]
            by_domain[domain].append(entity)
        return dict(by_domain)
    
    def generate_report(self):
        """Erstelle einen vollständigen Bericht"""
        print("\n" + "="*80)
        print("HOME ASSISTANT - VOLLSTÄNDIGER ÜBERBLICK")
        print("="*80)
        print(f"Generiert am: {datetime.now().strftime('%d.%m.%Y um %H:%M:%S')}")
        print("="*80 + "\n")
        
        # Test connection
        if not self.test_connection():
            return None
        
        print("\n📊 Sammle Daten...\n")
        
        # Sammle alle Daten
        config = self.get_config()
        components = self.get_components()
        states = self.get_states()
        services = self.get_services()
        events = self.get_events()
        entities_by_domain = self.analyze_entities(states)
        
        # Erstelle Report-Struktur
        report = {
            "timestamp": datetime.now().isoformat(),
            "system_info": {
                "version": config.get('version'),
                "location_name": config.get('location_name'),
                "timezone": config.get('time_zone'),
                "unit_system": config.get('unit_system'),
                "latitude": config.get('latitude'),
                "longitude": config.get('longitude')
            },
            "statistics": {
                "total_components": len(components),
                "total_entities": len(states),
                "total_services": sum(len(domain['services']) for domain in services),
                "total_domains": len(entities_by_domain),
                "total_events": len(events)
            },
            "components": sorted(components),
            "entities_by_domain": {
                domain: len(entities) for domain, entities in sorted(entities_by_domain.items())
            },
            "detailed_entities": entities_by_domain,
            "services": services,
            "events": events,
            "all_states": states
        }
        
        return report
    
    def print_summary(self, report):
        """Drucke eine Zusammenfassung auf die Konsole"""
        if not report:
            return
        
        print("\n" + "="*80)
        print("SYSTEM INFORMATIONEN")
        print("="*80)
        info = report['system_info']
        print(f"Version:        {info['version']}")
        print(f"Standort:       {info['location_name']}")
        print(f"Zeitzone:       {info['timezone']}")
        print(f"Einheitensystem: {info['unit_system']}")
        
        print("\n" + "="*80)
        print("STATISTIKEN")
        print("="*80)
        stats = report['statistics']
        print(f"Komponenten:    {stats['total_components']}")
        print(f"Entitäten:      {stats['total_entities']}")
        print(f"Services:       {stats['total_services']}")
        print(f"Domains:        {stats['total_domains']}")
        print(f"Events:         {stats['total_events']}")
        
        print("\n" + "="*80)
        print("ENTITÄTEN NACH DOMAIN")
        print("="*80)
        for domain, count in sorted(report['entities_by_domain'].items(), key=lambda x: x[1], reverse=True):
            print(f"{domain:.<30} {count:>4}")
        
        print("\n" + "="*80)
        print("TOP 20 KOMPONENTEN")
        print("="*80)
        for i, component in enumerate(report['components'][:20], 1):
            print(f"{i:2}. {component}")
        if len(report['components']) > 20:
            print(f"... und {len(report['components']) - 20} weitere")
        
    def save_report(self, report, format='json'):
        """Speichere den Report in verschiedenen Formaten"""
        if not report:
            return None
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        if format == 'json':
            filename = f"/mnt/user-data/outputs/ha_overview_{timestamp}.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            return filename
        
        elif format == 'txt':
            filename = f"/mnt/user-data/outputs/ha_overview_{timestamp}.txt"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("="*80 + "\n")
                f.write("HOME ASSISTANT - VOLLSTÄNDIGER ÜBERBLICK\n")
                f.write("="*80 + "\n")
                f.write(f"Generiert am: {datetime.now().strftime('%d.%m.%Y um %H:%M:%S')}\n")
                f.write("="*80 + "\n\n")
                
                # System Info
                f.write("SYSTEM INFORMATIONEN\n")
                f.write("-"*80 + "\n")
                info = report['system_info']
                for key, value in info.items():
                    f.write(f"{key:20}: {value}\n")
                
                # Statistiken
                f.write("\n" + "="*80 + "\n")
                f.write("STATISTIKEN\n")
                f.write("-"*80 + "\n")
                stats = report['statistics']
                for key, value in stats.items():
                    f.write(f"{key:20}: {value}\n")
                
                # Komponenten
                f.write("\n" + "="*80 + "\n")
                f.write(f"ALLE KOMPONENTEN ({len(report['components'])})\n")
                f.write("-"*80 + "\n")
                for component in sorted(report['components']):
                    f.write(f"  • {component}\n")
                
                # Entitäten nach Domain
                f.write("\n" + "="*80 + "\n")
                f.write("ENTITÄTEN NACH DOMAIN\n")
                f.write("-"*80 + "\n")
                for domain, count in sorted(report['entities_by_domain'].items(), key=lambda x: x[1], reverse=True):
                    f.write(f"{domain:.<30} {count:>4}\n")
                
                # Detaillierte Entitäten
                f.write("\n" + "="*80 + "\n")
                f.write("ALLE ENTITÄTEN (DETAILLIERT)\n")
                f.write("-"*80 + "\n")
                for domain, entities in sorted(report['detailed_entities'].items()):
                    f.write(f"\n### {domain.upper()} ({len(entities)} Entitäten) ###\n")
                    for entity in entities:
                        f.write(f"\n  Entity ID: {entity['entity_id']}\n")
                        f.write(f"  Name:      {entity['attributes'].get('friendly_name', 'N/A')}\n")
                        f.write(f"  Zustand:   {entity['state']}\n")
                        if entity['attributes'].get('device_class'):
                            f.write(f"  Klasse:    {entity['attributes']['device_class']}\n")
                        f.write(f"  Letzte Änderung: {entity['last_changed']}\n")
                
                # Services
                f.write("\n" + "="*80 + "\n")
                f.write("VERFÜGBARE SERVICES\n")
                f.write("-"*80 + "\n")
                for domain_services in report['services']:
                    domain = domain_services['domain']
                    f.write(f"\n### {domain.upper()} ###\n")
                    for service_name, service_data in domain_services['services'].items():
                        f.write(f"  • {domain}.{service_name}\n")
                        if service_data.get('description'):
                            f.write(f"    {service_data['description']}\n")
                
                # Events
                f.write("\n" + "="*80 + "\n")
                f.write("VERFÜGBARE EVENTS\n")
                f.write("-"*80 + "\n")
                for event in report['events']:
                    f.write(f"  • {event['event']}\n")
            
            return filename
        
        elif format == 'html':
            filename = f"/mnt/user-data/outputs/ha_overview_{timestamp}.html"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("""<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Home Assistant Überblick</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        h1, h2, h3 {
            color: #03a9f4;
        }
        .header {
            background: linear-gradient(135deg, #03a9f4 0%, #0288d1 100%);
            color: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 20px;
        }
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-bottom: 20px;
        }
        .stat-card {
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            text-align: center;
        }
        .stat-card h3 {
            margin: 0 0 10px 0;
            font-size: 14px;
            color: #666;
        }
        .stat-card .number {
            font-size: 32px;
            font-weight: bold;
            color: #03a9f4;
        }
        .section {
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }
        .entity-list {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 10px;
        }
        .entity-card {
            border: 1px solid #e0e0e0;
            padding: 15px;
            border-radius: 5px;
            background: #fafafa;
        }
        .entity-card .id {
            font-weight: bold;
            color: #0288d1;
            margin-bottom: 5px;
        }
        .entity-card .state {
            color: #4caf50;
            font-weight: bold;
        }
        table {
            width: 100%;
            border-collapse: collapse;
        }
        th, td {
            padding: 10px;
            text-align: left;
            border-bottom: 1px solid #e0e0e0;
        }
        th {
            background-color: #03a9f4;
            color: white;
        }
        .component-tag {
            display: inline-block;
            background: #e3f2fd;
            color: #0288d1;
            padding: 5px 10px;
            margin: 5px;
            border-radius: 15px;
            font-size: 12px;
        }
    </style>
</head>
<body>
""")
                
                f.write(f"""
    <div class="header">
        <h1>🏠 Home Assistant Überblick</h1>
        <p>Generiert am: {datetime.now().strftime('%d.%m.%Y um %H:%M:%S')}</p>
        <p>Version: {report['system_info']['version']} | Standort: {report['system_info']['location_name']}</p>
    </div>
    
    <div class="stats-grid">
        <div class="stat-card">
            <h3>Komponenten</h3>
            <div class="number">{report['statistics']['total_components']}</div>
        </div>
        <div class="stat-card">
            <h3>Entitäten</h3>
            <div class="number">{report['statistics']['total_entities']}</div>
        </div>
        <div class="stat-card">
            <h3>Services</h3>
            <div class="number">{report['statistics']['total_services']}</div>
        </div>
        <div class="stat-card">
            <h3>Domains</h3>
            <div class="number">{report['statistics']['total_domains']}</div>
        </div>
        <div class="stat-card">
            <h3>Events</h3>
            <div class="number">{report['statistics']['total_events']}</div>
        </div>
    </div>
    
    <div class="section">
        <h2>📦 Installierte Komponenten</h2>
""")
                
                for component in sorted(report['components']):
                    f.write(f'        <span class="component-tag">{component}</span>\n')
                
                f.write("""
    </div>
    
    <div class="section">
        <h2>📊 Entitäten nach Domain</h2>
        <table>
            <thead>
                <tr>
                    <th>Domain</th>
                    <th>Anzahl</th>
                </tr>
            </thead>
            <tbody>
""")
                
                for domain, count in sorted(report['entities_by_domain'].items(), key=lambda x: x[1], reverse=True):
                    f.write(f"""
                <tr>
                    <td><strong>{domain}</strong></td>
                    <td>{count}</td>
                </tr>
""")
                
                f.write("""
            </tbody>
        </table>
    </div>
    
    <div class="section">
        <h2>🔧 Alle Entitäten</h2>
""")
                
                for domain, entities in sorted(report['detailed_entities'].items()):
                    f.write(f"""
        <h3>{domain.upper()} ({len(entities)} Entitäten)</h3>
        <div class="entity-list">
""")
                    for entity in entities:
                        name = entity['attributes'].get('friendly_name', entity['entity_id'])
                        f.write(f"""
            <div class="entity-card">
                <div class="id">{entity['entity_id']}</div>
                <div>{name}</div>
                <div class="state">Zustand: {entity['state']}</div>
            </div>
""")
                    f.write("        </div>\n")
                
                f.write("""
    </div>
</body>
</html>
""")
            
            return filename


def main():
    """Hauptfunktion"""
    print("\n" + "="*80)
    print("HOME ASSISTANT OVERVIEW TOOL")
    print("="*80 + "\n")
    
    # Eingaben
    url = input("Home Assistant URL (z.B. http://homeassistant.local:8123): ").strip()
    token = input("Long-Lived Access Token: ").strip()
    
    # Erstelle Overview-Objekt
    ha = HomeAssistantOverview(url, token)
    
    # Generiere Report
    report = ha.generate_report()
    
    if report:
        # Zeige Zusammenfassung
        ha.print_summary(report)
        
        # Speichere in allen Formaten
        print("\n" + "="*80)
        print("SPEICHERE BERICHTE...")
        print("="*80)
        
        json_file = ha.save_report(report, 'json')
        txt_file = ha.save_report(report, 'txt')
        html_file = ha.save_report(report, 'html')
        
        print(f"\n✓ JSON-Bericht:  {json_file}")
        print(f"✓ Text-Bericht:  {txt_file}")
        print(f"✓ HTML-Bericht:  {html_file}")
        
        print("\n" + "="*80)
        print("FERTIG!")
        print("="*80 + "\n")


if __name__ == "__main__":
    main()
