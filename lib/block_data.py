import urllib.request
import json
from pathlib import Path
from typing import Any

def get_block_metadata_all(version: str) -> list[dict[str, Any]]:
    """
    Lädt die kompletten Block-Metadaten (Härte, Werkzeuge etc.) von PrismarineJS herunter.
    Falls die exakte Version nicht existiert, wird als Fallback die neuste verfügbare Version genutzt.
    """
    cache_dir = Path(".beet_cache/block_data")
    cache_dir.mkdir(parents=True, exist_ok=True)
    
    # 1. dataPaths.json holen, um den genauen Ordner-Pfad für die Version zu finden
    paths_cache = cache_dir / "dataPaths.json"
    
    # (Wir laden die Datei nur herunter, wenn sie fehlt. Will man Updates, löscht man den Cache)
    if not paths_cache.exists():
        url = "https://raw.githubusercontent.com/PrismarineJS/minecraft-data/master/data/dataPaths.json"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            paths_cache.write_bytes(response.read())
            
    with open(paths_cache, "r", encoding="utf-8") as f:
        data_paths = json.load(f)
        
    pc_versions = data_paths.get("pc", {})
    
    # 2. Version auflösen
    resolved_folder = None
    if version in pc_versions and "blocks" in pc_versions[version]:
        resolved_folder = pc_versions[version]["blocks"]
    else:
        # Fallback auf die aktuellste verfügbare Version
        available_versions = list(pc_versions.keys())
        latest_version = available_versions[-1]
        print(f"Warnung: Block-Daten für '{version}' nicht direkt in PrismarineJS gefunden. Nutze Fallback auf '{latest_version}'.")
        resolved_folder = pc_versions[latest_version]["blocks"]
        
    # 3. blocks.json für den aufgelösten Ordner herunterladen
    # resolved_folder sieht z.B. so aus: "pc/1.20"
    blocks_filename = resolved_folder.replace("/", "_") + "_blocks.json"
    blocks_cache = cache_dir / blocks_filename
    
    if not blocks_cache.exists():
        url = f"https://raw.githubusercontent.com/PrismarineJS/minecraft-data/master/data/{resolved_folder}/blocks.json"
        print(f"Lade Block-Metadaten aus {url} herunter...")
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            blocks_cache.write_bytes(response.read())
            
    with open(blocks_cache, "r", encoding="utf-8") as f:
        return json.load(f)


def get_block_metadata(version: str, block_name: str) -> dict[str, Any] | None:
    """
    Gibt die Metadaten für einen spezifischen Block zurück (Härtegrad, Abbauwerkzeuge etc.).
    Der 'block_name' kann wahlweise mit oder ohne "minecraft:"-Präfix übergeben werden.
    """
    # Entferne evtl. vorhandenes "minecraft:" Prefix
    if block_name.startswith("minecraft:"):
        block_name = block_name[10:]
        
    blocks = get_block_metadata_all(version)
    
    # Wir durchsuchen die Liste aller Blöcke nach dem gewünschten Namen
    for block in blocks:
        if block["name"] == block_name:
            return block
            
    return None
