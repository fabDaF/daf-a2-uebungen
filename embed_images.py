#!/usr/bin/env python3
"""
embed_images.py
---------------
Lädt alle Pexels-Bilder aus einer DaF-HTML-Datei herunter
und bettet sie als Base64-Data-URLs direkt in die Datei ein.
Danach ist die HTML-Datei vollständig offline-fähig.

Verwendung:
  python embed_images.py DE_A2_1012X-meine-freunde.html

Die Originaldatei wird als *.backup.html gesichert.
"""

import sys
import re
import base64
import urllib.request
import os

def embed_images(filepath):
    if not os.path.isfile(filepath):
        print(f"Datei nicht gefunden: {filepath}")
        sys.exit(1)

    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    # Backup erstellen
    backup = filepath.replace('.html', '.backup.html')
    with open(backup, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"Backup gespeichert: {backup}")

    # Alle Pexels-Bild-URLs finden (Auflösung wird so verwendet wie in der HTML angegeben)
    pattern = r'(https://images\.pexels\.com/photos/[^\s"\']+)'
    urls = list(dict.fromkeys(re.findall(pattern, html)))  # unique, reihenfolge erhalten
    print(f"{len(urls)} Bild-URL(s) gefunden.\n")

    headers = {
        'User-Agent': 'Mozilla/5.0 (compatible; DaF-Embed/1.0)'
    }

    for url in urls:
        print(f"  Lade: {url}")
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = resp.read()
                content_type = resp.headers.get('Content-Type', 'image/jpeg').split(';')[0].strip()
            b64 = base64.b64encode(data).decode('ascii')
            data_url = f"data:{content_type};base64,{b64}"
            html = html.replace(url, data_url)
            kb = len(data) // 1024
            print(f"    ✓ {kb} KB eingebettet ({content_type})")
        except Exception as e:
            print(f"    ✗ Fehler: {e}")

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)

    size_kb = os.path.getsize(filepath) // 1024
    print(f"\nFertig! Datei gespeichert: {filepath} ({size_kb} KB)")
    print(f"Alle Bilder sind jetzt offline eingebettet.")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Verwendung: python embed_images.py <datei1.html> [datei2.html ...]")
        sys.exit(1)
    for filepath in sys.argv[1:]:
        print(f"\n{'='*60}")
        print(f"Verarbeite: {filepath}")
        print('='*60)
        embed_images(filepath)
