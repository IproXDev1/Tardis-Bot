import asyncio
import discord
import socket
from discord.ext import tasks, commands
from config import CONFIG

class ServerStatus(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.server_status_task = None  # Stocke la tâche de vérification

    async def check_server_status(self):
        """Vérifie et envoie l'état du serveur dans un canal Discord."""
        await self.bot.wait_until_ready()
        channel = self.bot.get_channel(CONFIG["STATUS_CHANNEL_ID"])
        if not channel:
            return

        while not self.bot.is_closed():
            if getattr(self.bot, "maintenance_mode", False):  # Vérifie si le mode maintenance est actif
                await channel.send("⚠️ **Le serveur est actuellement en maintenance.** 🚧")
            else:
                await channel.send("✅ **Le serveur est en ligne !** 🟢")

            await asyncio.sleep(60)  # Vérifie toutes les minutes

    @commands.Cog.listener()
    async def on_ready(self):
        """Lance la vérification du serveur une fois que le bot est prêt."""
        if not self.server_status_task:
            self.server_status_task = self.bot.loop.create_task(self.check_server_status())

def setup(bot):
    bot.add_cog(ServerStatus(bot))  # Ajoute la classe au bot
