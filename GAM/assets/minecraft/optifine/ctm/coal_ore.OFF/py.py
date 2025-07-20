from PIL import Image
from pathlib import Path

def split_into_tiles(image_path, output_dir):
    image_path = Path(image_path)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)  # Ordner erstellen, falls nicht vorhanden

    img = Image.open(image_path)
    width, height = img.size
    tiles_x = 7
    tiles_y = 3  # 4x4 = 16 Kacheln
    tile_width = width // tiles_x
    tile_height = height // tiles_y

    i = 0
    for y in range(tiles_y):
        for x in range(tiles_x):
            box = (x * tile_width, y * tile_height, (x + 1) * tile_width, (y + 1) * tile_height)
            tile = img.crop(box)
            tile.save(output_dir / f"{i}.png")
            i += 1

# Beispiel: aktuelle Datei "bild.png", Kacheln nach "output/" schreiben
split_into_tiles("C:\\Users\\Annhilati\\AppData\\Roaming\\.minecraft\\resourcepacks\\GAM\\assets\\minecraft\\optifine\\ctm\\coal_ore\\tiles.png",
                 "C:\\Users\\Annhilati\\AppData\\Roaming\\.minecraft\\resourcepacks\\GAM\\assets\\minecraft\\optifine\\ctm\\coal_ore")
