from typing import ClassVar
from beet import Context, NamespaceFileScope, PngFile
from beet.contrib.optifine import OptifineTexture, optifine

class ConnectedTexture(OptifineTexture):
    scope: ClassVar[NamespaceFileScope] = ("optifine", "ctm")
    extension: ClassVar[str] = ".png"


def beet_default(ctx: Context):
    ctx.require(optifine)
    ctx.assets.extend_namespace.remove(OptifineTexture)
    ctx.assets.extend_namespace += [
        ConnectedTexture
    ]