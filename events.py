import discord
import random
from discord.ext import commands

bad_words = ["insulte1", "insulte2", "spam"]  # Liste de mots interdits
user_xp = {}  # Stocke l'XP des membres

def setup(bot):
    @bot.event
    async def on_message_delete(message):
        """Log les messages supprimés."""
        log_channel = discord.utils.get(message.guild.channels, name="logs")
        if log_channel:
            embed = discord.Embed(title="🗑 Message supprimé", color=discord.Color.red())
            embed.add_field(name="Auteur", value=message.author.mention, inline=True)
            embed.add_field(name="Contenu", value=message.content, inline=False)
            embed.set_footer(text=f"Salon: {message.channel.name}")
            await log_channel.send(embed=embed)

    @bot.event
    async def on_member_join(member):
        """Kick les comptes récents pour éviter les raids."""
        if (discord.utils.utcnow() - member.created_at).days < 5:
            await member.kick(reason="Compte trop récent - Possible Raid")
            log_channel = discord.utils.get(member.guild.channels, name="logs")
            if log_channel:
                await log_channel.send(f"🚨 **{member.name}** a été kick (compte trop récent).")

    @bot.event
    async def on_message(message):
        """Supprime les insultes et ajoute de l'XP aux membres."""
        if message.author.bot:
            return

        # Suppression des insultes
        if any(word in message.content.lower() for word in bad_words):
            await message.delete()
            await message.channel.send(f"{message.author.mention}, ton message a été supprimé 🚫 !")
            return

        # Système d'XP
        user = message.author
        user_xp[user.id] = user_xp.get(user.id, 0) + random.randint(5, 15)  # Ajoute de l'XP aléatoire
        level = user_xp[user.id] // 100  # 100 XP = 1 niveau

        if user_xp[user.id] % 100 < 15:  # Si c'est un nouveau niveau
            await message.channel.send(f"🎉 {user.mention} est maintenant **niveau {level}** !")

        await bot.process_commands(message)  # Permet aux autres commandes de fonctionner
