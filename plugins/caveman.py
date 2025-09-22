import yaml
from beet import Context, BlockTag, Recipe, LootTable, Plugin, ItemModifier, Advancement, Function
from beet.core.utils import JsonDict
from beetsmith import CustomItem
import json
from pathlib import Path
from typing import cast


def beet_default(ctx: Context):
    config: dict = ctx.meta.get("caveman", cast(JsonDict, {}))

    dir = Path.cwd()

    ctx.require(build_tags(
        block_atlas=dir / config.get("block_atlas")
    ))
    ctx.require(implement_pickaxes(
        pickaxe_atlas=dir / config.get("pickaxe_atlas"),
        default_loot_tables=dir / config.get("default_loot_tables")
    ))


def implement_pickaxes(pickaxe_atlas: Path, default_loot_tables: Path) -> Plugin:

    def plugin(ctx: Context):
        dp = ctx.data

        with open(pickaxe_atlas, "r") as f:
            data: dict[str, dict] = yaml.safe_load(f)

        # ╭────────────────────────────────────────────────────────────────────────────────╮
        # │                            Component Configuration                             │ 
        # ╰────────────────────────────────────────────────────────────────────────────────╯

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

        # ╭────────────────────────────────────────────────────────────────────────────────╮
        # │                              Recipe Implementation                             │ 
        # ╰────────────────────────────────────────────────────────────────────────────────╯
            
            # Yes this has to be inside the for loop
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

        # ╭────────────────────────────────────────────────────────────────────────────────╮
        # │                          Item Modifier Implementation                          │ 
        # ╰────────────────────────────────────────────────────────────────────────────────╯

            # Yes this has to be inside the for loop
            ctx.data[pickaxe_key] = ItemModifier(
                {
                    "function": "minecraft:set_components",
                    "components": instance._components_data
                }
            )

        # ╭────────────────────────────────────────────────────────────────────────────────╮
        # │                    Loot Table Reparsing and Implementation                     │ 
        # ╰────────────────────────────────────────────────────────────────────────────────╯

        print("Loot reparsing started")
        root_dir = default_loot_tables

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
        print("Loot reparsing finished")

        # ╭────────────────────────────────────────────────────────────────────────────────╮
        # │                 Pickaxe Detecting Advancement Implementation                   │ 
        # ╰────────────────────────────────────────────────────────────────────────────────╯

        dp["caveman:pickaxes"] = Advancement(
            {
                "criteria": {
                    instance.id.split(":")[1]: {
                        "conditions": {
                            "items": [
                                {
                                    "items": instance.id
                                }
                            ]
                        },
                        "trigger": "minecraft:inventory_changed"
                    }
                    for instance in instances.values()
                },
                "requirements": [
                    [
                        instance.id.split(":")[1] for instance in instances.values()
                    ]
                ]
            }
        )
        dp["caveman:pickaxes"] = Function([

        ])

    return plugin


def build_tags(block_atlas: Path) -> Plugin:
        
    def plugin(ctx: Context):
        dp = ctx.data
        
        with open(block_atlas, "r") as f:
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

    return plugin