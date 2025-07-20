import re
import warnings
from PIL import Image
from beet import Context
from beet.contrib.optifine import OptifineTexture

def main(ctx: Context):
    ctm_textures = {
        resource_location: file
        for resource_location, file in ctx.assets[OptifineTexture].items()
        if resource_location.startswith("minecraft:ctm") and re.search(r'\b\d+-\d+\b', resource_location) is not None
    }
    
    for resource_location, file in ctm_textures.items():
        print(f"Slicing {resource_location}")
        try:
            tiles = slice_image_by_tiles(file.image)
            
            for n, tile in enumerate(tiles):
                new_name = re.sub(r'\b\d+-\d+\b', str(n), resource_location)
                ctx.assets[new_name] = OptifineTexture(tile)
        
        except Exception as e:
            warnings.warn(f"Couldn't slice {resource_location}: {e}")

ratios = {
    7/3: (7, 3),
    3.0: (12, 4),
    4.0: (4, 1),
    5.0: (5, 1),
    7.0: (7, 1),
}

def slice_image_by_tiles(image: Image.Image):
    w, h = image.size

    if ratios.get(w / h) is None:
        raise Exception("File has a ratio unknown for CTM")
    
    tiles_x, tiles_y = ratios[w / h]
    
    w_tile = w // tiles_x
    h_tile = h // tiles_y

    tiles: list[Image.Image] = []

    for j in range(tiles_y):
        for i in range(tiles_x):
            left = i * w_tile
            upper = j * h_tile
            right = left + w_tile
            lower = upper + h_tile
            tile = image.crop((left, upper, right, lower))
            tiles.append(tile)

    return tiles