import yaml
from pathlib import Path
from beet import Context, BlockTag
from beetsmith import load_from_file

def implement_pickaxes(ctx: Context):
    pickaxes = [
        (Path("Caveman/items/iron_pickaxe.yml"), "minecraft:iron_pickaxe"),
        (Path("Caveman/items/wooden_pickaxe.yml"), "minecraft:wooden_pickaxe"),
        (Path("Caveman/items/stone_pickaxe.yml"), "minecraft:stone_pickaxe")
    ]
  
    for item in pickaxes:
        instance = load_from_file(item[0])
        instance.item = item[1]
        instance.components.attribute_modifiers = None
        instance.removed_components = []
        instance.components.unbreakable = None
        instance.components.max_stack_size = None
        instance.components
        instance.implement(ctx.data)

def build_tags(ctx: Context):
    dp = ctx.data
    
    with open("Caveman/atlas.yml", "r") as f:
        data: dict[str, dict[float, list[dict]]] = yaml.safe_load(f)

    for tier, toughnesses in data.items():
        for toughness, blocks in toughnesses.items():
            for block_entry in blocks:
                block = next(iter(block_entry))
                vanilla_hardness = next(iter(block_entry.values()))
                dp[BlockTag].setdefault(f"materials:tier/{tier}/unlocks").merge(BlockTag({"values": [block]}))
                # Missing code for hardness tags