import discord
from discord import DiscordException, Embed
from discord.ext import commands
from pydis_core import BotBase
from pydis_core.utils import scheduling
from pydis_core.utils.logging import get_logger

from sir_lancebot import constants, exts  # Changed from 'bot' to 'sir_lancebot'

log = get_logger(__name__)

__all__ = ("Bot",)


class Bot(BotBase):
    """
    Base bot instance.
    """

    name = constants.Client.name

    @property
    def member(self) -> discord.Member | None:
        """Retrieves the guild member object for the bot."""
        guild = self.get_guild(constants.Client.guild)
        if not guild:
            return None
        return guild.me

    async def on_command_error(self, context: commands.Context, exception: DiscordException) -> None:
        """Check command errors for UserInputError and reset the cooldown if thrown."""
        if isinstance(exception, commands.UserInputError):
            context.command.reset_cooldown(context)
        else:
            await super().on_command_error(context, exception)

    async def log_to_dev_log(self, title: str, details: str | None = None, *, icon: str | None = None) -> None:
        """Send an embed message to the dev-log channel."""
        devlog = self.get_channel(constants.Channels.devlog)

        if not icon:
            icon = self.user.display_avatar.url

        embed = Embed(description=details)
        embed.set_author(name=title, icon_url=icon)

        await devlog.send(embed=embed)

    async def setup_hook(self) -> None:
        """Default async initialisation method for discord.py."""
        await super().setup_hook()
        scheduling.create_task(self.load_extensions(exts))

    async def invoke_help_command(self, ctx: commands.Context) -> None:
        """Invoke the help command or default help command if help extensions is not loaded."""
        if "sir_lancebot.exts.core.help" in ctx.bot.extensions:  # Changed from 'bot' to 'sir_lancebot'
            help_command = ctx.bot.get_command("help")
            await ctx.invoke(help_command, ctx.command.qualified_name)
            return
        await ctx.send_help(ctx.command)

