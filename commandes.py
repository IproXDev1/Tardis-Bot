import discord
from discord.ext import commands
import random
import time

def setup(bot):
    # 📜 Commandes générales
    @bot.command(help="Affiche la liste des commandes disponibles.")
    async def help(ctx):
        help_message = "**📜 Liste des commandes :**\n"
        for command in bot.commands:
            help_message += f"➡️ `{ctx.prefix}{command.name}` - {command.help}\n"
        await ctx.send(help_message)

    @bot.command(help="Vérifie la latence du bot.")
    async def ping(ctx):
        await ctx.send(f"Pong! 🏓 Latence : {round(bot.latency * 1000)}ms")

    @bot.command(help="Affiche des informations sur le serveur.")
    async def serverinfo(ctx):
        server = ctx.guild
        embed = discord.Embed(title=f"🌍 Infos du serveur {server.name}", color=discord.Color.green())
        embed.add_field(name="👥 Membres :", value=server.member_count, inline=False)
        embed.add_field(name="📆 Créé le :", value=server.created_at.strftime("%d/%m/%Y"), inline=False)
        embed.set_thumbnail(url=server.icon.url)
        await ctx.send(embed=embed)

    @bot.command(help="Affiche des infos sur un membre.")
    async def userinfo(ctx, member: discord.Member = None):
        member = member or ctx.author
        embed = discord.Embed(title=f"👤 Infos de {member.name}", color=discord.Color.blue())
        embed.add_field(name="🆔 ID :", value=member.id, inline=False)
        embed.add_field(name="📆 A rejoint le :", value=member.joined_at.strftime("%d/%m/%Y"), inline=False)
        embed.set_thumbnail(url=member.avatar.url)
        await ctx.send(embed=embed)

    @bot.command(help="Montre l’avatar d’un membre.")
    async def avatar(ctx, member: discord.Member = None):
        member = member or ctx.author
        embed = discord.Embed(title=f"🖼️ Avatar de {member.name}", color=discord.Color.purple())
        embed.set_image(url=member.avatar.url)
        await ctx.send(embed=embed)

    @bot.command(help="Donne des infos sur le bot.")
    async def botinfo(ctx):
        embed = discord.Embed(title="🤖 Infos du bot", description="Créé par IproXDev", color=discord.Color.blue())
        embed.add_field(name="👥 Serveurs :", value=len(bot.guilds), inline=False)
        embed.set_thumbnail(url=bot.user.avatar.url)
        await ctx.send(embed=embed)

    @bot.command(help="Affiche depuis combien de temps le bot est en ligne.")
    async def uptime(ctx):
        await ctx.send(f"⏳ Le bot est en ligne depuis {time.strftime('%H heures, %M minutes, %S secondes')}.")

    @bot.command(help="Envoie le lien d’invitation du bot.")
    async def invite(ctx):
        await ctx.send("🔗 **Invitez-moi ici :** https://discord.com/oauth2/authorize?client_id=VOTRE_BOT_ID&permissions=8&scope=bot")

    @bot.command(help="Fournit un lien vers le serveur de support du bot.")
    async def support(ctx):
        await ctx.send("📞 **Serveur de support :** https://discord.gg/ybQzw9B5Yj") #Ne pas remplacer si tu a un soucis contacte

    @bot.command(help="Crée un sondage avec réactions.")
    async def poll(ctx, *, question):
        message = await ctx.send(f"📊 **Sondage :** {question}")
        await message.add_reaction("✅")
        await message.add_reaction("❌")

    @bot.command(help="Donne le lien du modpack.")
    async def mdp(ctx):
        """Envoie le lien du modpack."""
        lien = "https://www.mediafire.com/file/i2ftxwzivn92xzb/MDP.zip/file" #Remplace le lien par le tien !
        await ctx.send(f"📥 **Téléchargez le modpack ici :** {lien}")

    # ⚙ Commandes d'administration
    @bot.command(help="Supprime un certain nombre de messages.")
    @commands.has_permissions(manage_messages=True)
    async def clear(ctx, amount: int):
        await ctx.channel.purge(limit=amount + 1)
        await ctx.send(f"🧹 {amount} messages supprimés !", delete_after=5)

    @bot.command(help="Bannit un membre du serveur.")
    @commands.has_permissions(ban_members=True)
    async def ban(ctx, member: discord.Member, *, reason="Aucune raison fournie"):
        await member.ban(reason=reason)
        await ctx.send(f"⛔ {member.mention} a été banni ! Raison : {reason}")

    @bot.command(help="Expulse un membre du serveur.")
    @commands.has_permissions(kick_members=True)
    async def kick(ctx, member: discord.Member, *, reason="Aucune raison fournie"):
        await member.kick(reason=reason)
        await ctx.send(f"👢 {member.mention} a été expulsé ! Raison : {reason}")

    @bot.command(help="Active ou désactive le slowmode.")
    @commands.has_permissions(manage_channels=True)
    async def slowmode(ctx, seconds: int):
        await ctx.channel.edit(slowmode_delay=seconds)
        await ctx.send(f"🐌 Mode lent activé : {seconds} secondes.")

    @bot.command(help="Verrouille un canal texte.")
    @commands.has_permissions(manage_channels=True)
    async def lock(ctx):
        await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
        await ctx.send("🔒 Ce canal est verrouillé.")

    @bot.command(help="Déverrouille un canal texte.")
    @commands.has_permissions(manage_channels=True)
    async def unlock(ctx):
        await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
        await ctx.send("🔓 Ce canal est déverrouillé.")

    # 🎉 Commandes de fun
    @bot.command(help="Répond à une question par oui ou non.")
    async def _8ball(ctx, *, question: str):
        responses = ["Oui, bien sûr ! ✅", "Non, jamais. ❌", "Peut-être... 🤔", "Demande plus tard. ⏳", "Je n'en suis pas sûr. 🤷‍♂️"]
        await ctx.send(f"🎱 **Question :** {question}\n🎱 **Réponse :** {random.choice(responses)}")

    @bot.command(help="Lance un dé (ex: !roll 6)")
    async def roll(ctx, nombre: int = 6):
        if nombre < 1:
            await ctx.send("❌ Le nombre doit être supérieur à 1.")
            return
        result = random.randint(1, nombre)
        await ctx.send(f"🎲 Le dé est lancé... Résultat : **{result}** !")

    @bot.command(help="Pile ou face.")
    async def flip(ctx):
        result = random.choice(["Pile", "Face"])
        await ctx.send(f"🪙 Résultat : **{result}** !")

    @bot.command(help="Simule un combat entre deux membres.")
    async def fight(ctx, member: discord.Member):
        result = random.choice(["a gagné 💪", "a perdu 😢", "match nul ⚖️"])
        await ctx.send(f"🥊 {ctx.author.mention} vs {member.mention}... {result} !")
        
    @bot.command(name="404", help="Active/désactive le mode maintenance.")
    async def maintenance(ctx):
        if not hasattr(bot, "maintenance_mode"):
            bot.maintenance_mode = False  

        bot.maintenance_mode = not bot.maintenance_mode
        status = "activé 🚧" if bot.maintenance_mode else "désactivé ✅"
        await ctx.send(f"⚠️ Mode maintenance {status} !")
