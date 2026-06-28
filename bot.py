from __future__ import annotations

import os
import asyncio
import logging

import discord
from discord.ext import commands
from dotenv import load_dotenv

import database as db

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
CLIENT_ID = int(os.getenv("DISCORD_CLIENT_ID"))

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

log = logging.getLogger("PremiumBot")

COGS = [
    "cogs.help",
    "cogs.utility",
    "cogs.tickets",
    "cogs.moderation",
    "cogs.welcome",
    "cogs.logging",
    "cogs.automod",
    "cogs.reactionroles",
    "cogs.leveling",
    "cogs.suggestions",
    "cogs.giveaway",
    "cogs.applications",
]


class PremiumBot(commands.Bot):

    def __init__(self):

        intents = discord.Intents.default()

        intents.guilds = True
        intents.members = True
        intents.messages = True
        intents.message_content = True

        super().__init__(
            command_prefix="!",
            intents=intents,
            application_id=CLIENT_ID,
            help_command=None,
        )

    async def setup_hook(self):

        await db.init_db()

        for cog in COGS:

            try:

                await self.load_extension(cog)

                log.info(f"Loaded {cog}")

            except Exception as e:

                log.error(f"Failed to load {cog}: {e}")

        synced = await self.tree.sync()

        log.info(f"Synced {len(synced)} commands")

    async def on_ready(self):

        await self.change_presence(

            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name="🌸 Protecting Your Server",
            )
        )

        log.info(f"Logged in as {self.user}")
        log.info(f"Serving {len(self.guilds)} servers")


bot = PremiumBot()


async def main():

    async with bot:
        await bot.start(TOKEN)


asyncio.run(main())
