import yaml
from pathlib import Path
from beet import Context, TagFile, Plugin, NamespaceFileScope
from beetsmith.toolchain.file import load_from_file
from typing import ClassVar

def main(ctx: Context):
    items = [
        (Path("src/items/iron_pickaxe.yml"), "minecraft:iron_pickaxe")
    ]
  
    for item in items:
        instance = load_from_file(item[0])
        instance.item = item[1]
        instance.implement(ctx.data)

class Tag(TagFile):
    scope: ClassVar[NamespaceFileScope] = ("tags",)

def tag_building_requirements(ctx: Context) -> Plugin:
    print("extended")
    ctx.data.extend_namespace.append(Tag)

def build_tags(ctx: Context):
    dp = ctx.data
    
    with open("src/atlas.yml", "r") as f:
        data: dict[str, dict[float, list[dict]]] = yaml.safe_load(f)
    for tier, hardnesses in data.items():
        for hardness, blocks in hardnesses.items():
            for block_entry in blocks:
                block = next(iter(block_entry))
                vanilla_hardness = next(iter(block_entry.values()))
                dp[Tag].setdefault(f"materials:tier/{tier}/unlocks").merge(Tag({"values": [block]}))
                # Missing code for hardness tags