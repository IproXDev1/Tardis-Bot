import discord
from discord.ext import commands
import config
import commandes
import events
import os
import platform
import datetime
import asyncio

# Initialisation du bot
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=config.CONFIG["PREFIX"], intents=intents, help_command=None)

# Charger les commandes et événements
commandes.setup(bot)
events.setup(bot)

# Charger le module de surveillance APRÈS la définition du bot
import status_checker
status_checker.setup(bot)

@bot.event
async def on_ready():
    os.system("cls" if os.name == "nt" else "clear")

    commandTable = "\n".join([f"   ➡️  {config.CONFIG['PREFIX']}{command.name} - {command.help}" for command in bot.commands])
    os_info = f"{platform.system()} {platform.release()}"
    python_version = platform.python_version()
    bot_start_time = datetime.datetime.now().strftime("%H:%M:%S")
    
    @bot.event
    async def on_ready():
        print("✅ Bot connecté !")
        print("📜 Commandes chargées :", [cmd.name for cmd in bot.commands])


    btl_text = f"""
    ██████╗     ████████╗    ██╗     
    ██╔══██╗    ╚══██╔══╝    ██║     
    ██████╔╝       ██║       ██║     
    ██╔══██╗       ██║       ██║     
    ██████╔╝       ██║       ███████╗
    ╚═════╝        ╚═╝       ╚══════╝

        BOT B.T.L ACTIVÉ !

    🔹 Créé par IproXDev - Béta 2.0
    🔹 Agrégation Ipro-Tech for Tardis-Life

    👋 Bonjour IproXDev & Nyyxtra ! #Il y a que ca que tu peux modifier

    📜 Commandes disponibles :
{commandTable}

    ⏰ Démarré à : {bot_start_time}
    🖥️ Infos système :
       💻 OS : {os_info}
       🐍 Python : {python_version}
    """

    print(btl_text)

# Démarrer le bot
bot.run(config.CONFIG["TOKEN"])
