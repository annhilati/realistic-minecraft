""""""
# DEVELOPER NOTE:
# What should be thought of:
# In beet, files are abstract. There is only one Texture class for all kinds of texture. What classes should be defined for OptiFine?

import javaproperties
from dataclasses import dataclass
from PIL.Image import Image
from typing import ClassVar
from beet import Context, NamespaceFileScope, PngFile
from beet.core.file import ValueType, DataModelBase, FileDeserialize
from beet.core.utils import JsonDict

# ╭────────────────────────────────────────────────────────────────────────────────╮
# │                                beet.core.file                                  │ 
# ╰────────────────────────────────────────────────────────────────────────────────╯

class PropertiesFileBase(DataModelBase[ValueType]):
    """Base class for properties files."""

    def __post_init__(self):
        super().__post_init__()
        if not self.encoder:
            self.encoder = javaproperties.dumps
        if not self.decoder:
            self.decoder = javaproperties.loads


@dataclass(eq=False, repr=False)
class PropertiesFile(PropertiesFileBase[JsonDict]):
    """Class representing a properties file."""

    data: ClassVar[FileDeserialize[JsonDict]] = FileDeserialize()

    @classmethod
    def default(cls) -> JsonDict:
        return {}
    
# ╭────────────────────────────────────────────────────────────────────────────────╮
# │                             beet.contrib.optifine                              │ 
# ╰────────────────────────────────────────────────────────────────────────────────╯

__all__ = ["ConnectedTexture"]

class OptifineProperties(PropertiesFile):
    """Class representing an unspecified OptiFine texture properties file."""
    scope: ClassVar[NamespaceFileScope] = ("optifine",)
    extension: ClassVar[str] = ".properties"


class OptifineTexture(PngFile):
    """Class representing an unspecified OptiFine texture file."""
    scope: ClassVar[NamespaceFileScope] = ("optifine",)
    extension: ClassVar[str] = ".png"


class ConnectedTexture(OptifineTexture):
    """Class representing an OptiFine connected texture."""
    scope: ClassVar[NamespaceFileScope] = ("optifine", "ctm")
    extension: ClassVar[str] = ".png"

    @property
    def sliced_tiles(self) -> list[Image]:
        "Return the tiles when slicing the texture"

        ratios = {
            7/3: (7,  3),
            3.0: (12, 4),
            4.0: (4,  1),
            5.0: (5,  1),
            7.0: (7,  1),
        }

        image: Image = self.image
        w, h = image.size

        if ratios.get(w / h) is None:
            return image
        
        tiles_x, tiles_y = ratios[w / h]
        
        w_tile = w // tiles_x
        h_tile = h // tiles_y

        return [
            image.crop((i * w_tile, j * h_tile, (i + 1) * w_tile, (j + 1) * h_tile))
            for j in range(tiles_y)
            for i in range(tiles_x)
        ]

def beet_default(ctx: Context):
    # ctx.require(optifine)
    # ctx.assets.extend_namespace.remove(OptifineTexture)
    ctx.assets.extend_namespace += [
        OptifineProperties,
        ConnectedTexture,
    ]

# CustomEntityModel
# CustomEntityPart
# CustomItemTexture
# Colormap
# ConnectedTexture
# CustomAnimation
# CustomGUI
# Lightmap
# CustomSky
# 