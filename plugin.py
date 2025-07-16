from pathlib import Path
from beet import Context
from beetsmith.toolchain.file import load_from_file, CustomItem

def main(ctx: Context):
    load_from_file(Path("src/data/minecraft/beetsmith/iron_pickaxe.yml")).implement(ctx.data)
    # CustomItem().encha