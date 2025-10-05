import re
import warnings
from beet import Context
from plugins.optifine_extended import ConnectedTexture

ctm_file_regex = r'\b\d+-\d+'

def plugin(ctx: Context):
    print("CTM slicing started")
    textures_to_slice = {
        resource_location: file
        for resource_location, file in ctx.assets[ConnectedTexture].items()
        if re.search(ctm_file_regex, resource_location) is not None
    }
    
    for resource_location, file in textures_to_slice.items():
        try:
            tiles = file.sliced_tiles
            
            if len(tiles) != 1:
                for n, tile in enumerate(tiles):
                    new_name = re.sub(ctm_file_regex, str(n), resource_location)
                    ctx.assets[new_name] = ConnectedTexture(tile)
            else:
                ctx.assets[resource_location] = file
        
        except Exception as e:
            warnings.warn(f"Couldn't slice {resource_location}: {e}")
            
    print("CTM slicing finished")

def beet_default(ctx: Context):
    ctx.require(plugin)