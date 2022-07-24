"""
Heavy inspiration from https://github.com/kablekompany/Kable-Kogs/tree/master/decancer
This cog definitely needs refactoring, feel free to PR or open issues.

This cog has an implemented cog_check method.
"""
from copy import copy
from typing import List, Optional, Tuple

import discord
from discord.ext import commands

# global utils
from utils import bot_permissions, chunk

# cog utils
from .utils import new_nick


class DecancerCog(commands.Cog, name="Decancer"):
    __slots__: Tuple[str] = ("client")

    def __init__(self, client: commands.Bot) -> None:
        self.client = client

    async def cog_check(ctx: commands.Context) -> bool:
        return ctx.me.guild_permissions.

    @staticmethod
    def __build_message__(_tr: list, _nc: list, _uc: list, _su: int, _to: int, _rs: str) -> List[str]:
        term: str = f"\n- Not found: {', '.join(_tr)}" if _tr else ""
        nonc: str = f"\n- Non-cancerous: {', '.join(_nc)}" if _nc else ""
        unsuc: str = f"\n- Failed: {', '.join(_uc)}" if _uc else ""
        return chunk((f"Decancer successful for ({_su} of {_to}) member(s), with "
                      f"reason: \"{_rs}\"{term}{nonc}{unsuc}"))

    @commands.command(name="decancer", aliases=["dc"])
    @bot_permissions()
    async def _decancer(self, ctx: commands.Context, members: commands.Greedy[int], /, reason: str = None) -> None:
        _tr: list = []  # Terminated
        _nc: list = []  # Non-Cancerous
        _uc: list = []  # Unsuccessful
        partial_reason: str = reason or "Cancerous nickname"
        full_reason: str = (f"Action requested by: {ctx.author.id}"
                            f"\nReason for action: {partial_reason}")
        for member_id in members:
            if not (member := ctx.guild.get_member(member_id)):
                _tr.append(f"`{member_id}`")
                continue
            if not (nickname := new_nick(member.display_name)):
                _nc.append(f"`{member}`")
                continue
            try:
                await member.edit(nick=nickname, reason=full_reason)
            except Exception:
                _uc.append(f"`{member}`")
        _su: int = len(members) - (len(_nc) + len(_uc) +
                                   len(_tr))  # Total successful
        msg = ctx.message
        for x in self.__build_message__(_tr, _nc, _uc, _su, len(members), partial_reason):
            msg = await msg.reply(x)
