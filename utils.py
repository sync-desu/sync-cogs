from typing import Callable, List

import discord
from discord.ext import commands


def chunk(iterable: Iterable, /, *, per: int = 1988) -> List:
    """
    Takes an iterable and returns chunks of that iterable
    according to the `per` value.
    """
    return [iterable[i:i + per] for i in range(0, len(iterable), per)]


def bot_permissions(**perms: bool) -> Callable:
    """
    Re-implemented commands.bot_has_permissions with a few
    permissions that default to True.
    """
    perms.update({"read_message_history": True,
                 "send_messages": True, "view_channel": True})
    invalid: set = set(perms) - set(discord.Permissions.VALID_FLAGS)
    if invalid:
        raise TypeError(f"Invalid permission(s): {', '.join(invalid)}")

    def predicate(ctx: commands.Context) -> bool:
        permissions: discord.Permissions = ctx.channel.permissions_for(ctx.me)
        missing: list = [perm for perm, value in perms.items(
        ) if getattr(permissions, perm) != value]
        if not missing:
            return True
        raise commands.MissingPermissions(missing)
    return commands.check(predicate)
