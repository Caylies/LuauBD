from typing import Any

import pluau

from bd_models.models import Player

from .core import LuauClass, LuauModel, luaumethod

__all__ = ("BigInt", "Context", "PlayerModel", "ctx_print")


class BigInt(LuauClass):
    name = "bigint"

    @luaumethod()
    def new(self, value: pluau.String):
        return self.construct(value=value)

    def _to_lua(self, value: dict[str, Any]):
        return self.new(value["value"])


class Context(LuauClass):
    name = "Context"

    def __init__(self, *args, **kwargs):
        super().__init__(*args)
        self.ctx = kwargs["ctx"]

    @luaumethod()
    async def send(self, content: pluau.String):
        await self.ctx.send(str(content))


class PlayerModel(LuauModel):
    name = "Player"
    model = Player

    async def _to_python(self, value: pluau.Table):
        return await Player.objects.aget(discord_id=value.get("discord_id"))

    def _to_lua(self, value: Player):
        return {"discordId": str(value.discord_id), "money": value.money}


def ctx_print(ctx):
    async def ctx_print(*args):
        text = " ".join(str(argument) for argument in args)
        await ctx.send(f"```lua\n{text}\n```")

    return ctx_print
