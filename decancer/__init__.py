from discord.ext import commands

from .decancer import DecancerCog


async def setup(client: commands.Bot) -> None:
    await client.add_cog(DecancerCog(client))
