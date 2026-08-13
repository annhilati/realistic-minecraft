import urllib.request
import zipfile
import io
from pathlib import Path
from beet import DataPack

def get_vanilla_datapack(version: str) -> DataPack:
    """
    Lädt das Standard-Datenpaket (Vanilla) für eine bestimmte Minecraft-Version herunter
    und gibt es als beet DataPack zurück. Die heruntergeladenen Daten werden lokal 
    gecacht, um redundante Downloads zu vermeiden.
    
    Verwendet das mcmeta-Repository von Misode.
    """
    # Cache-Ordner anlegen (z.B. im Projektverzeichnis)
    cache_dir = Path(".beet_cache/vanilla_data") / version
    
    # Prüfen, ob wir die Version schon heruntergeladen haben
    if not cache_dir.exists() or not (cache_dir / "pack.mcmeta").exists():
        print(f"Lade Vanilla-Datenpaket für Version {version} herunter...")
        url = f"https://github.com/misode/mcmeta/archive/refs/tags/{version}-data.zip"
        
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as response:
                zip_data = io.BytesIO(response.read())
        except urllib.error.HTTPError as e:
            if e.code == 404:
                raise ValueError(f"Minecraft-Version '{version}' wurde bei Misode nicht gefunden (oder hat kein data-tag).")
            raise

        print("Entpacke Daten in Cache...")
        with zipfile.ZipFile(zip_data) as zf:
            # Die ZIP-Datei von GitHub hat einen Root-Ordner wie "mcmeta-1.21.1-data"
            root_dir = zf.namelist()[0].split('/')[0]
            
            cache_dir.mkdir(parents=True, exist_ok=True)
            for member in zf.infolist():
                if member.filename.startswith(root_dir + '/'):
                    relative_path = member.filename[len(root_dir)+1:]
                    if relative_path:
                        # Den internen Dateinamen für das Entpacken anpassen
                        member.filename = relative_path
                        zf.extract(member, cache_dir)
                        
        print("Download und Entpacken abgeschlossen!")
        
    return DataPack(path=str(cache_dir))
