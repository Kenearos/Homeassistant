#!/usr/bin/env python3
"""
Sony Bravia TV Remote - Automatisches Setup
Findet deinen TV und erstellt die fertige Lovelace-Karte
"""

import requests
import json
import os

# === KONFIGURATION - NUR HIER ANPASSEN ===
HA_URL = "http://homeassistant.local:8123"
HA_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiI2YWU4NDc0YzEwNjE0YzkxOGVmZjNlODJkZWJiMjJhNCIsImlhdCI6MTc2NTYzNDU4MCwiZXhwIjoyMDgwOTk0NTgwfQ.1jHlByvkcFkMhV1LcxLxzrLcCU9ogSBUf9IQ2AbjUnk"
# =========================================

def get_entities():
    """Hole alle Entities von Home Assistant"""
    headers = {
        "Authorization": f"Bearer {HA_TOKEN}",
        "Content-Type": "application/json"
    }
    response = requests.get(f"{HA_URL}/api/states", headers=headers, timeout=30)
    response.raise_for_status()
    return response.json()

def find_sony_tv(entities):
    """Finde Sony Bravia TV Entities"""
    media_players = []
    remotes = []

    for entity in entities:
        eid = entity.get('entity_id', '').lower()
        name = entity.get('attributes', {}).get('friendly_name', '').lower()

        # Suche nach Sony/Bravia/TV
        is_sony = any(x in eid or x in name for x in ['sony', 'bravia', 'kd-55', 'kd55'])
        is_tv = 'tv' in eid or 'tv' in name or 'fernseher' in name

        if entity['entity_id'].startswith('media_player.'):
            if is_sony or is_tv:
                media_players.append({
                    'entity_id': entity['entity_id'],
                    'name': entity.get('attributes', {}).get('friendly_name', entity['entity_id']),
                    'state': entity.get('state')
                })

        if entity['entity_id'].startswith('remote.'):
            if is_sony or is_tv:
                remotes.append({
                    'entity_id': entity['entity_id'],
                    'name': entity.get('attributes', {}).get('friendly_name', entity['entity_id']),
                    'state': entity.get('state')
                })

    return media_players, remotes

def generate_lovelace_card(media_player_id, remote_id):
    """Generiere die Lovelace Karte"""

    card = f'''type: vertical-stack
cards:
  - type: entities
    title: "Sony Bravia TV"
    entities:
      - entity: {media_player_id}
        name: "TV Status"
    state_color: true

  - type: grid
    columns: 3
    square: false
    cards:
      - type: button
        name: "Power"
        icon: mdi:power
        tap_action:
          action: call-service
          service: media_player.toggle
          target:
            entity_id: {media_player_id}
        icon_height: 40px

      - type: button
        name: "Home"
        icon: mdi:home
        tap_action:
          action: call-service
          service: remote.send_command
          data:
            command: HOME
          target:
            entity_id: {remote_id}
        icon_height: 40px

      - type: button
        name: "Input"
        icon: mdi:import
        tap_action:
          action: call-service
          service: remote.send_command
          data:
            command: INPUT
          target:
            entity_id: {remote_id}
        icon_height: 40px

      - type: button
        name: ""
        tap_action:
          action: none

      - type: button
        icon: mdi:chevron-up
        tap_action:
          action: call-service
          service: remote.send_command
          data:
            command: UP
          target:
            entity_id: {remote_id}
        icon_height: 50px

      - type: button
        name: ""
        tap_action:
          action: none

      - type: button
        icon: mdi:chevron-left
        tap_action:
          action: call-service
          service: remote.send_command
          data:
            command: LEFT
          target:
            entity_id: {remote_id}
        icon_height: 50px

      - type: button
        name: "OK"
        icon: mdi:checkbox-blank-circle
        tap_action:
          action: call-service
          service: remote.send_command
          data:
            command: CONFIRM
          target:
            entity_id: {remote_id}
        icon_height: 50px

      - type: button
        icon: mdi:chevron-right
        tap_action:
          action: call-service
          service: remote.send_command
          data:
            command: RIGHT
          target:
            entity_id: {remote_id}
        icon_height: 50px

      - type: button
        name: ""
        tap_action:
          action: none

      - type: button
        icon: mdi:chevron-down
        tap_action:
          action: call-service
          service: remote.send_command
          data:
            command: DOWN
          target:
            entity_id: {remote_id}
        icon_height: 50px

      - type: button
        name: ""
        tap_action:
          action: none

      - type: button
        name: "Zurueck"
        icon: mdi:arrow-left
        tap_action:
          action: call-service
          service: remote.send_command
          data:
            command: RETURN
          target:
            entity_id: {remote_id}
        icon_height: 40px

      - type: button
        name: "Menu"
        icon: mdi:menu
        tap_action:
          action: call-service
          service: remote.send_command
          data:
            command: OPTIONS
          target:
            entity_id: {remote_id}
        icon_height: 40px

      - type: button
        name: "Guide"
        icon: mdi:television-guide
        tap_action:
          action: call-service
          service: remote.send_command
          data:
            command: GUIDE
          target:
            entity_id: {remote_id}
        icon_height: 40px

  - type: grid
    columns: 4
    square: false
    cards:
      - type: button
        name: "Vol+"
        icon: mdi:volume-plus
        tap_action:
          action: call-service
          service: media_player.volume_up
          target:
            entity_id: {media_player_id}
        icon_height: 40px

      - type: button
        name: "Vol-"
        icon: mdi:volume-minus
        tap_action:
          action: call-service
          service: media_player.volume_down
          target:
            entity_id: {media_player_id}
        icon_height: 40px

      - type: button
        name: "CH+"
        icon: mdi:chevron-up-box
        tap_action:
          action: call-service
          service: remote.send_command
          data:
            command: CHANNEL_UP
          target:
            entity_id: {remote_id}
        icon_height: 40px

      - type: button
        name: "CH-"
        icon: mdi:chevron-down-box
        tap_action:
          action: call-service
          service: remote.send_command
          data:
            command: CHANNEL_DOWN
          target:
            entity_id: {remote_id}
        icon_height: 40px

      - type: button
        name: "Mute"
        icon: mdi:volume-mute
        tap_action:
          action: call-service
          service: media_player.volume_mute
          data:
            is_volume_muted: true
          target:
            entity_id: {media_player_id}
        icon_height: 40px

  - type: grid
    columns: 5
    square: false
    cards:
      - type: button
        icon: mdi:rewind
        tap_action:
          action: call-service
          service: remote.send_command
          data:
            command: REWIND
          target:
            entity_id: {remote_id}
        icon_height: 35px

      - type: button
        icon: mdi:play
        tap_action:
          action: call-service
          service: media_player.media_play
          target:
            entity_id: {media_player_id}
        icon_height: 35px

      - type: button
        icon: mdi:pause
        tap_action:
          action: call-service
          service: media_player.media_pause
          target:
            entity_id: {media_player_id}
        icon_height: 35px

      - type: button
        icon: mdi:stop
        tap_action:
          action: call-service
          service: media_player.media_stop
          target:
            entity_id: {media_player_id}
        icon_height: 35px

      - type: button
        icon: mdi:fast-forward
        tap_action:
          action: call-service
          service: remote.send_command
          data:
            command: FORWARD
          target:
            entity_id: {remote_id}
        icon_height: 35px

  - type: grid
    columns: 4
    square: false
    cards:
      - type: button
        name: "Netflix"
        icon: mdi:netflix
        tap_action:
          action: call-service
          service: remote.send_command
          data:
            command: NETFLIX
          target:
            entity_id: {remote_id}
        icon_height: 35px

      - type: button
        name: "YouTube"
        icon: mdi:youtube
        tap_action:
          action: call-service
          service: media_player.select_source
          data:
            source: "YouTube"
          target:
            entity_id: {media_player_id}
        icon_height: 35px

      - type: button
        name: "Prime"
        icon: mdi:amazon
        tap_action:
          action: call-service
          service: media_player.select_source
          data:
            source: "Prime Video"
          target:
            entity_id: {media_player_id}
        icon_height: 35px

      - type: button
        name: "Disney+"
        icon: mdi:movie-open
        tap_action:
          action: call-service
          service: media_player.select_source
          data:
            source: "Disney+"
          target:
            entity_id: {media_player_id}
        icon_height: 35px

  - type: grid
    columns: 3
    square: true
    cards:
      - type: button
        name: "1"
        tap_action:
          action: call-service
          service: remote.send_command
          data:
            command: NUM_1
          target:
            entity_id: {remote_id}
      - type: button
        name: "2"
        tap_action:
          action: call-service
          service: remote.send_command
          data:
            command: NUM_2
          target:
            entity_id: {remote_id}
      - type: button
        name: "3"
        tap_action:
          action: call-service
          service: remote.send_command
          data:
            command: NUM_3
          target:
            entity_id: {remote_id}
      - type: button
        name: "4"
        tap_action:
          action: call-service
          service: remote.send_command
          data:
            command: NUM_4
          target:
            entity_id: {remote_id}
      - type: button
        name: "5"
        tap_action:
          action: call-service
          service: remote.send_command
          data:
            command: NUM_5
          target:
            entity_id: {remote_id}
      - type: button
        name: "6"
        tap_action:
          action: call-service
          service: remote.send_command
          data:
            command: NUM_6
          target:
            entity_id: {remote_id}
      - type: button
        name: "7"
        tap_action:
          action: call-service
          service: remote.send_command
          data:
            command: NUM_7
          target:
            entity_id: {remote_id}
      - type: button
        name: "8"
        tap_action:
          action: call-service
          service: remote.send_command
          data:
            command: NUM_8
          target:
            entity_id: {remote_id}
      - type: button
        name: "9"
        tap_action:
          action: call-service
          service: remote.send_command
          data:
            command: NUM_9
          target:
            entity_id: {remote_id}
      - type: button
        name: ""
        tap_action:
          action: none
      - type: button
        name: "0"
        tap_action:
          action: call-service
          service: remote.send_command
          data:
            command: NUM_0
          target:
            entity_id: {remote_id}
      - type: button
        name: ""
        tap_action:
          action: none
'''
    return card

def main():
    print("=" * 60)
    print("SONY BRAVIA TV - AUTOMATISCHES LOVELACE SETUP")
    print("=" * 60)
    print()

    print("Verbinde mit Home Assistant...")
    try:
        entities = get_entities()
        print(f"Gefunden: {len(entities)} Entities")
    except Exception as e:
        print(f"FEHLER: {e}")
        print()
        print("Moegliche Loesungen:")
        print("1. Pruefe ob Home Assistant laeuft")
        print("2. Pruefe die URL und den Token")
        return

    print()
    print("Suche nach Sony TV...")
    media_players, remotes = find_sony_tv(entities)

    if not media_players:
        print("WARNUNG: Kein Sony TV Media Player gefunden!")
        print()
        print("Alle gefundenen Media Player:")
        for e in entities:
            if e['entity_id'].startswith('media_player.'):
                name = e.get('attributes', {}).get('friendly_name', '')
                print(f"  - {e['entity_id']} ({name})")
        print()
        media_player_id = input("Gib die media_player Entity-ID ein: ").strip()
    else:
        print(f"Gefunden: {len(media_players)} Media Player")
        for i, mp in enumerate(media_players):
            print(f"  [{i+1}] {mp['entity_id']} - {mp['name']} ({mp['state']})")

        if len(media_players) == 1:
            media_player_id = media_players[0]['entity_id']
        else:
            choice = input("Waehle [1-{}]: ".format(len(media_players))).strip()
            media_player_id = media_players[int(choice)-1]['entity_id']

    if not remotes:
        print("WARNUNG: Keine Sony TV Remote gefunden!")
        print()
        print("Alle gefundenen Remotes:")
        for e in entities:
            if e['entity_id'].startswith('remote.'):
                name = e.get('attributes', {}).get('friendly_name', '')
                print(f"  - {e['entity_id']} ({name})")
        print()
        remote_id = input("Gib die remote Entity-ID ein: ").strip()
    else:
        print(f"Gefunden: {len(remotes)} Remotes")
        for i, r in enumerate(remotes):
            print(f"  [{i+1}] {r['entity_id']} - {r['name']} ({r['state']})")

        if len(remotes) == 1:
            remote_id = remotes[0]['entity_id']
        else:
            choice = input("Waehle [1-{}]: ".format(len(remotes))).strip()
            remote_id = remotes[int(choice)-1]['entity_id']

    print()
    print(f"Verwende: {media_player_id}")
    print(f"Verwende: {remote_id}")
    print()

    # Generiere Karte
    card_yaml = generate_lovelace_card(media_player_id, remote_id)

    # Speichere Datei
    output_file = "sony_tv_remote_FERTIG.yaml"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(card_yaml)

    print("=" * 60)
    print("FERTIG!")
    print("=" * 60)
    print()
    print(f"Datei erstellt: {output_file}")
    print()
    print("So fuegst du die Karte hinzu:")
    print("1. Oeffne Home Assistant Dashboard")
    print("2. Klicke oben rechts auf die 3 Punkte -> 'Dashboard bearbeiten'")
    print("3. Klicke auf '+ KARTE HINZUFUEGEN'")
    print("4. Scrolle nach unten und waehle 'Manuell'")
    print(f"5. Kopiere den Inhalt von '{output_file}' und fuege ihn ein")
    print("6. Klicke 'SPEICHERN'")
    print()
    print("Oder kopiere diesen YAML-Code direkt:")
    print("-" * 60)
    print(card_yaml[:500] + "...")
    print("-" * 60)
    print(f"(Vollstaendiger Code in: {output_file})")

if __name__ == "__main__":
    main()
