import yaml
from pathlib import Path
from beet import Context, TagFile, Plugin, NamespaceFileScope
from beetsmith.toolchain.file import load_from_file, CustomItem
from typing import ClassVar

def main(ctx: Context):
    items = [
        (Path("src/data/minecraft/beetsmith/iron_pickaxe.yml"), "minecraft:iron_pickaxe")
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
    with open("atlas.yml", "r") as f:
        data: dict[str, dict[float, list[dict]]] = yaml.safe_load(f)

    print(data)
    dp = ctx.data

    for tier, vanilla_hardnesses in data.items():
        for vanilla_hardness, blocks in vanilla_hardnesses.items():
            for block_entry in blocks:
                block = next(iter(block_entry))
                hardness = next(iter(block_entry))

                dp[Tag].setdefault(f"materials:tier/{tier}/unlocks").merge(Tag({"values": [block]}))