import yaml
from beet import Context, BlockTag, Recipe, LootTable
from beetsmith import CustomItem
from beetsmith.library.contrib import shaped_recipe
import json

def implement_pickaxes(ctx: Context):
    dp = ctx.data

    with open("Caveman/pickaxes.yml", "r") as f:
        data: dict[str, dict] = yaml.safe_load(f)

    instances: dict[str, CustomItem] = {}

    for pickaxe_key, specs in data.items():
        default_speed = specs["speed"]
        tier = specs["tier"]

        instance = CustomItem(pickaxe_key, {"translate": f"item.{pickaxe_key.replace(":", ".")}"}, pickaxe_key)

        instance.components.tool = {
            "rules": [
                {
                    "blocks": f"#materials:tier/{tier}/cannot_mine",
                    "correct_for_drops": False
                },
                *[{
                    "blocks": f"#{modifier}",
                    "speed": round(default_speed / float(modifier.split("/")[-1]), 2)
                }
                for modifier in [modifier for modifier in dp[BlockTag] if modifier.startswith("materials:toughness_modifier")]],
                {
                    "blocks": "#minecraft:mineable/pickaxe",
                    "speed": default_speed,
                    "correct_for_drops": True
                },
            ]
        }

        instance.item = pickaxe_key
        instance.components.attribute_modifiers = None
        instance.removed_components = []
        instance.components.unbreakable = None
        instance.components.max_stack_size = None
        instance.components
        instance.implement(ctx.data)

        instances[pickaxe_key] = instance

        if specs.get("recipe"):
            ctx.data[pickaxe_key] = Recipe(
                {
                    **specs["recipe"],
                    "result": {
                        "count": 1,
                        "id": pickaxe_key,
                        "components": instance._components_data
                    }
                }
            )


    from pathlib import Path

    root_dir = Path("C:/Users/Annhilati/Documents/GitHub/realistic-minecraft/1.21.9 loot_table")

    for file_path in root_dir.rglob("*"):
        if file_path.is_file():
            loot_table = LootTable(json.loads(file_path.read_text(encoding="utf-8", errors="ignore")))

            def replace_pickaxe_data(obj):
                if isinstance(obj, dict):
                    new_obj = {}
                    for k, v in obj.items():
                        if isinstance(v, str) and "pickaxe" in v:
                            # Falls functions schon existieren -> anhängen
                            funcs = obj.get("functions", [])
                            funcs.append({
                                "function": "minecraft:set_components",
                                "components": instances[v]._components_data
                            })
                            new_obj[k] = v  # den Wert behalten
                            new_obj["functions"] = funcs
                        else:
                            new_obj[k] = replace_pickaxe_data(v)
                    return new_obj

                elif isinstance(obj, list):
                    return [replace_pickaxe_data(v) for v in obj]

                else:
                    return obj

            
            loot_table.data = replace_pickaxe_data(loot_table.data)

            if "pickaxe" in str(loot_table.data):
                dp["minecraft:" + str(file_path.relative_to(root_dir).with_suffix("")).replace("\\", "/")] = loot_table


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
                
                required_hardness = 0.5 * (toughness ** 2)

                value = round(required_hardness / vanilla_hardness, 2)
                # print(f"{block}, {toughness}, {vanilla_hardness}, {value}")
                dp[BlockTag].setdefault(f"materials:toughness_modifier/{value}").merge(BlockTag({"values": [block]}))