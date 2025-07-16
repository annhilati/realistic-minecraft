from pathlib import Path
from beet import Context
from beetsmith.toolchain.file import load_from_file, CustomItem

def main(ctx: Context):
    items = [
        (Path("src/data/minecraft/beetsmith/iron_pickaxe.yml"), "minecraft:iron_pickaxe")
    ]
    
    
    for item in items:
        instance = load_from_file(item[0])
        instance.item = item[1]
        instance.implement(ctx.data)