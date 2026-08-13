import sys
from pathlib import Path

# Sicherstellen, dass das Root-Verzeichnis (realistic-minecraft) im Pfad ist, 
# damit der 'lib' Ordner gefunden wird, egal von wo man das Script startet.
sys.path.insert(0, str(Path(__file__).parent.parent))

import requests
import beet

from lib.components import ItemComponents, REMOVED
from lib.vanilla_data import get_vanilla_datapack
from lib.block_data import get_block_metadata_all

from Picks.configuration import PickConfig


def create_datapack(config: PickConfig, version: tuple[int, ...]) -> beet.DataPack:    
    
    dp = beet.DataPack()
    
    VANILLA_DP = get_vanilla_datapack(".".join(map(str, version)))
    VANILLA_BLOCKS = get_block_metadata_all("26.1") # no newer Versions as of August 2026
    
    for tool_category, toughnesses in config.tools.items():
        for toughness, block_specs in toughnesses.items():
            for block_spec in block_specs:
                
                hardness_spec: None | float = None
                if isinstance(block_spec, dict):
                    hardness_spec = next(iter(block_spec.values()))
                    block_spec = next(iter(block_spec))

                blocks: dict[str, float] = []
                
                if block_spec.startswith("#"):
                    tagname = block_spec[1:]
                    if not (tag := VANILLA_DP.block_tags.get(tagname)):
                        raise ValueError(f"Block tag '{tagname}' not presented in Misode vanilla datapack. Please specify the blocks manually")
                    
                    # Resolve Block Tag
                    for block_in_tag in tag.data.get("values", []):
                        if hardness_spec:
                            blocks[block_in_tag] = hardness_spec
                        else:
                            if not (blockdata := next([b for b in VANILLA_BLOCKS if b["name"] == block_in_tag.split(".")[-1]])):
                                raise ValueError(f"Block '{block_spec}' not presented in PrismarineJS block data. Please specify manually")
                            blocks[block_in_tag] = blockdata["hardness"]
                else:
                    if hardness_spec:
                        blocks[block_spec] = hardness_spec
                    else:
                        if not (blockdata := next([b for b in VANILLA_BLOCKS if b["name"] == block_spec.split(".")[-1]])):
                            raise ValueError(f"Block '{block_spec}' not presented in PrismarineJS block data. Please specify manually")
                        blocks[block_spec] = blockdata["hardness"]
                    
                for block, hardness in blocks.items():
                    
                

                    dp[beet.BlockTag].setdefault(
                        key=f"picks:toughness_modifier/{value}").merge(beet.BlockTag({"values": [block_spec]})
                    )
        
        
if __name__ == "__main__":
    create_datapack(PickConfig(), (26, 2))