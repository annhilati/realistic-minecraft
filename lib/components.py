# https://minecraft.wiki/w/Data_component_format#List_of_components
# https://misode.github.io/changelog?tags=component

from dataclasses import dataclass, field, fields
from beetsmith.core.resourcelocations import ensureComponent
from typing import TypeAlias

class RemovedComponentState:
    "The Instance of this class is used to denote the state of removement to an item component.<br>Every instanciation of this class will result in identical objects."
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __str__(self) -> str:
        return "REMOVED"

REMOVED = RemovedComponentState()
"""Constant denoting that an item's component is removed.<br>
Similar to `None`, `REMOVED` can be checked on instance with `is`:
```
if component is REMOVED:
    ...
```
"""

ValidValueInComponent: TypeAlias = str | int | float | list["ValidValueInComponent"] | dict[str, "ValidValueInComponent"]
ValidComponentValue:   TypeAlias = ValidValueInComponent | RemovedComponentState | None

@dataclass
class ItemComponents():
    """Class representing a Minecraft item's components.

    You really shouldn't use the constructor of this class.<br>
    Use `.fromDict()`, `.fromVanillaItem()` or `.empty()` instead.

    Only some vanilla components are accessible through attributes. Item setting and getting can be used instead.

    To remove a component, set it's value to `REMOVED`. It can be imported from this same module.

    Supports
    ---------
    - `... = ·[...]`
    - `·[...] = ...`
    - `str(·)`
    """
    attack_animation:            dict                     | RemovedComponentState | None = None
    attack_range:                float                    | RemovedComponentState | None = None
    attribute_modifiers:         list[dict]               | RemovedComponentState | None = None
    banner_patterns:             list[dict]               | RemovedComponentState | None = None
    base_color:                  str                      | RemovedComponentState | None = None
    bees:                        list[dict]               | RemovedComponentState | None = None
    block_entity_data:           dict                     | RemovedComponentState | None = None
    block_state:                 dict                     | RemovedComponentState | None = None
    block_transformer:           dict                     | RemovedComponentState | None = None
    blocks_attacks:              dict                     | RemovedComponentState | None = None
    break_sound:                 str                      | RemovedComponentState | None = None
    brewing_fuel:                dict                     | RemovedComponentState | None = None
    bucket_entity_data:          dict                     | RemovedComponentState | None = None
    bundle_contents:             list | dict              | RemovedComponentState | None = None
    can_break:                   dict                     | RemovedComponentState | None = None
    can_place_on:                dict                     | RemovedComponentState | None = None
    charged_projectiles:         list[dict]               | RemovedComponentState | None = None
    compostable:                 dict                     | RemovedComponentState | None = None
    consumable:                  dict                     | RemovedComponentState | None = None
    container:                   list[dict]               | RemovedComponentState | None = None
    container_loot:              dict                     | RemovedComponentState | None = None
    cooking_fuel:                dict                     | RemovedComponentState | None = None
    custom_data:                 dict                     | RemovedComponentState | None = None
    custom_model_data:           dict | int | list | str  | RemovedComponentState | None = None
    custom_name:                 str | dict | list        | RemovedComponentState | None = None
    damage:                      int                      | RemovedComponentState | None = None
    damage_resistant:            dict                     | RemovedComponentState | None = None
    damage_type:                 str                      | RemovedComponentState | None = None
    death_protection:            dict                     | RemovedComponentState | None = None
    debug_stick_state:           dict                     | RemovedComponentState | None = None
    dye:                         dict                     | RemovedComponentState | None = None
    dyed_color:                  int | list | dict        | RemovedComponentState | None = None
    enchantable:                 dict                     | RemovedComponentState | None = None
    enchantment_glint_override:  bool                     | RemovedComponentState | None = None
    enchantments:                dict                     | RemovedComponentState | None = None
    entity_data:                 dict                     | RemovedComponentState | None = None
    equippable:                  dict                     | RemovedComponentState | None = None
    firework_explosion:          dict                     | RemovedComponentState | None = None
    fireworks:                   dict                     | RemovedComponentState | None = None
    food:                        dict                     | RemovedComponentState | None = None
    glider:                      dict                     | RemovedComponentState | None = None
    instrument:                  str | dict               | RemovedComponentState | None = None
    intangible_projectile:       dict                     | RemovedComponentState | None = None
    interact_animation:          dict                     | RemovedComponentState | None = None
    item_model:                  str                      | RemovedComponentState | None = None
    item_name:                   str | dict | list        | RemovedComponentState | None = None
    jukebox_playable:            str | dict               | RemovedComponentState | None = None
    kinetic_weapon:              dict                     | RemovedComponentState | None = None
    lock:                        str                      | RemovedComponentState | None = None
    lodestone_tracker:           dict                     | RemovedComponentState | None = None
    lore:                        str | dict | list        | RemovedComponentState | None = None
    map_color:                   int                      | RemovedComponentState | None = None
    map_decorations:             dict                     | RemovedComponentState | None = None
    map_id:                      int                      | RemovedComponentState | None = None
    max_damage:                  int                      | RemovedComponentState | None = None
    max_stack_size:              int                      | RemovedComponentState | None = None
    minimum_attack_charge:       float                    | RemovedComponentState | None = None
    mob_visibility:              dict                     | RemovedComponentState | None = None
    note_block_sound:            str                      | RemovedComponentState | None = None
    ominous_bottle_amplifier:    int                      | RemovedComponentState | None = None
    piercing_weapon:             dict                     | RemovedComponentState | None = None
    pot_decorations:             list[str]                | RemovedComponentState | None = None
    potion_contents:             str | dict               | RemovedComponentState | None = None
    potion_duration_scale:       float                    | RemovedComponentState | None = None
    profile:                     dict | str               | RemovedComponentState | None = None
    provides_banner_patterns:    str | dict               | RemovedComponentState | None = None
    provides_pottery_pattern:    str | dict               | RemovedComponentState | None = None
    provides_trim_material:      str | dict               | RemovedComponentState | None = None
    rarity:                      str                      | RemovedComponentState | None = None
    recipes:                     list[str]                | RemovedComponentState | None = None
    repair_cost:                 int                      | RemovedComponentState | None = None
    repairable:                  dict                     | RemovedComponentState | None = None
    sign_text_back:              dict                     | RemovedComponentState | None = None
    sign_text_front:             dict                     | RemovedComponentState | None = None
    stored_enchantments:         dict                     | RemovedComponentState | None = None
    sulfur_cube_content:         dict                     | RemovedComponentState | None = None
    suspicious_stew_effects:     list[dict]               | RemovedComponentState | None = None
    swing_animation:             dict                     | RemovedComponentState | None = None
    tool:                        dict                     | RemovedComponentState | None = None
    tooltip_display:             dict                     | RemovedComponentState | None = None
    tooltip_style:               str                      | RemovedComponentState | None = None
    trim:                        dict                     | RemovedComponentState | None = None
    unbreakable:                 dict                     | RemovedComponentState | None = None
    use_cooldown:                dict                     | RemovedComponentState | None = None
    use_effects:                 dict                     | RemovedComponentState | None = None
    use_remainder:               dict                     | RemovedComponentState | None = None
    villager_food:               dict                     | RemovedComponentState | None = None
    waxed:                       dict                     | RemovedComponentState | None = None
    weapon:                      dict                     | RemovedComponentState | None = None
    writable_book_content:       dict                     | RemovedComponentState | None = None
    written_book_content:        dict                     | RemovedComponentState | None = None

    _other_components:           dict[str, ValidComponentValue] = field(default_factory=dict)
    "All components in the component stack that cannot be accessed by attribution. Complementary to `._builtin_components`"

    def __str__(self) -> str:
        return str(self.asDict())

    def __getitem__(self, query: str) -> ValidComponentValue:
        return self.get_component(component=query)

    def __setitem__(self, query: str, value: ValidComponentValue) -> None:
        self.set_component(component=query, value=value)

    @property
    def _builtin_components(self) -> dict[str, ValidComponentValue]:
        "All components in the component stack that can be accessed by attribution. Complementary to `._other_components`"
        return {
            field.name: getattr(self, field.name)
            for field
            in fields(self)
            if field.name not in ["_other_components"]
        }

    def set_component(self, component: str, value: ValidComponentValue) -> None:
        ensureComponent(component)
        id = component.split("minecraft:")[-1]
        
        if id in self._builtin_components:
            setattr(self, id, value)
        else:
            self._other_components[component] = value

    def get_component(self, component: str) -> ValidComponentValue:
        id = component.split("minecraft:")[-1]
        return (
            getattr(self, id)
            if id in self._builtin_components
            else self._other_components.get(component)
        )
    
    @classmethod
    def empty(cls):
        return cls()
     
    @classmethod
    def fromDict(cls, data: dict[str, ValidValueInComponent], /):
        """Create an ItemComponents instance from a dictionary.
        
        The type of dictionary required is like the ones used in every JSON definition of item components like in recipes, item modifiers and loot tables,<br>
        whereby the keys are the names of the components which can have a leading `!` and their values are the components values.
        """
        instance: ItemComponents = cls()

        for component, value in data.items():
            if component.startswith("!"):
                value = REMOVED
            instance.set_component(component, value)
        return instance
    
    @classmethod
    def fromVanillaItem(cls, id: str, /):
        """Create an ItemComponents instance from the data of a vanilla item.
        
        This will issue a HTTP request (~800 kB).

        If no data is found for the specified item id, an empty ItemComponents instance is returned.
        """
        import requests

        query = id.split(":")[-1]
        url = "https://raw.githubusercontent.com/misode/mcmeta/summary/item_components/data.json"
        res = requests.get(url)
        res.raise_for_status()
        data: dict[str, dict] = res.json()

        if query not in data:
            return cls()
        
        return cls.fromDict(data[query])

    def asDict(self) -> dict[str, ValidValueInComponent]:
        """Return the item components as a dictionary.
        
        The type of dictionary produced is like the ones used in every JSON definition of item components like in recipes, item modifiers and loot tables, 
        whereby the keys are the names of the components which can have a leading `!` and their values are the components values.
        """
        out = {}

        for component, value in self._builtin_components.items():
            if value is not REMOVED and value is not None:
                out["minecraft:" + component] = value
            elif value is REMOVED and value is not None:
                out["!minecraft:" + component] = {}

        for component, value in self._other_components.items():
            if value is not REMOVED and value is not None:
                out[component] = value
            elif value is REMOVED and value is not None:
                out["!" + component] = {}
        
        return out
    