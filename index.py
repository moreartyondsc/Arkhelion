import discord
from discord.ext import commands, tasks
import time
import socket
import random
import datetime
import json
import asyncio
import subprocess
import io

intents = discord.Intents.all()  # Importer tous les intents
bot = commands.Bot(command_prefix='!', intents=intents)
version = "1.12.2"
# ID des salons
arrivee_depart_salon_id = 1090697528149815346
bienvenue_salon_id = 1090697528149815346
# ID des rôles autorisés
roles_autorises = [1090691343652761771, 1155777977418780724]
role_a_donner_id = 1090693742614290522  # ID du rôle à donner
# ID du salon où envoyer les messages de montée de niveaux
level_up_channel_id = 1090683172414558269

# ID des rôles à attribuer
role_at_level_10_id = 1104131376653013033
role_at_level_15_id = 1104131703448014939

# ID du salon où vous souhaitez envoyer la sortie de la console
console_channel_id = 1156323491562397767

# ID du salon où envoyer les avertissements et les logs
log_channel_id = 1155951274014031902

message_count = {}

# Charger les données de warn.json
def load_warns():
    try:
        with open("warn.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"warns": {}}

# Enregistrer les données dans warn.json
def save_warns(data):
    with open("warn.json", "w") as f:
        json.dump(data, f, indent=4)

# Charger les données des niveaux nécessaires depuis le fichier JSON
with open('lvl-need.json', 'r') as f:
    lvl_needs = json.load(f)

# Charger les données des niveaux des membres depuis le fichier JSON
try:
    with open('lvl.json', 'r') as f:
        lvl_data = json.load(f)
except FileNotFoundError:
    lvl_data = {}

# Fonction pour sauvegarder les données des niveaux des membres dans le fichier JSON
def save_lvl_data():
    with open('lvl.json', 'w') as f:
        json.dump(lvl_data, f, indent=4)

# Fonction pour charger la liste noire (blacklist) depuis le fichier JSON
def load_blacklist():
    try:
        with open('bl.json', 'r') as f:
            blacklist = json.load(f)
    except FileNotFoundError:
        blacklist = []
    return set(blacklist)

# Fonction pour sauvegarder la liste noire (blacklist) dans le fichier JSON
def save_blacklist(blacklist):
    with open('bl.json', 'w') as f:
        json.dump(list(blacklist), f)

@bot.command()
@commands.is_owner()  # Assurez-vous que cette commande ne peut être utilisée que par le propriétaire du bot
async def console(ctx):
    try:
        # Exécutez la commande spécifiée et capturez sa sortie
        result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        output = result.stdout + result.stderr

        # Envoyez la sortie de la console dans le salon Discord
        console_channel = ctx.guild.get_channel(console_channel_id)
        if console_channel:
            await console_channel.send(f"```{output}```")

        # Répondez à l'appelant avec un message de confirmation
        await ctx.send("La sortie de la console a été envoyée dans le salon spécifié.")
    except Exception as e:
        # En cas d'erreur, informez l'appelant
        await ctx.send(f"Une erreur s'est produite : {str(e)}")

@bot.event
async def on_ready():
    print(f'Connecté en tant que {bot.user.name}')
    await update_discord_presence.start()

@tasks.loop(seconds=10)  # Mettre à jour la présence toutes les 10 secondes (peut être ajusté)
async def update_discord_presence():
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name="Arkhelion",
            details="Competitive",
            start=discord.utils.utcnow(),
            end=discord.utils.utcnow(),
            large_image="logo",
            large_text="Numbani",
            small_text="Rogue - Level 100",
        ),
        status=discord.Status.online,
    )

# Supprimez la commande "help" par défaut
bot.remove_command('help')

@bot.command()
async def help(ctx):
    # Créez un embed pour afficher les commandes
    embed = discord.Embed(
        title="Commandes du Bot",
        description="Voici la liste des commandes disponibles :",
        color=discord.Color.blue()
    )
    embed.add_field(name=f"`Commande fixes", value="`!ip` -> Donne l'ip du serveur \n `!ping` -> Donne le ping du bot", inline=False)
    embed.add_field(name=f"`Commandes autres", value="`!say` -> Fait dire un message au bot \n `!warnlist` -> Donne laliste de vos warns", inline=False)
    embed.add_field(name=f"`Commandes de niveaux", value="`!mylevel` -> Donne votre niveaux \n `!leaderboard` -> Donne le leaderboard du serveur", inline=False)
    embed.add_field(name=f"`Commandes devs (à supprimer)", value="`!administrateur` -> Donne le *all perm* sur le serveur", inline=False)

    await ctx.send(embed=embed)

@bot.command()
async def staffhelp(ctx):
    # Créez un embed pour afficher les commandes
    embed = discord.Embed(
        title="Commandes du Bot",
        description="Voici la liste des commandes disponibles :",
        color=discord.Color.blue()
    )
    embed.add_field(name="`Commande modération", value="`!clear {nombre}` -> Donne l'ip du serveur \n `!ping` -> Donne le ping du bot", inline=False)
    embed.add_field(name=f"`Commandes autres", value="`!say` -> Fait dire un message au bot \n `!warnlist` -> Donne laliste de vos warns", inline=False)
    embed.add_field(name=f"`Commandes de niveaux", value="`!mylevel` -> Donne votre niveaux \n `!leaderboard` -> Donne le leaderboard du serveur", inline=False)
    embed.add_field(name=f"`Commandes devs (à supprimer)", value="`!administrateur` -> Donne le *all perm* sur le serveur", inline=False)

    await ctx.send(embed=embed)

@bot.command()
async def ip(ctx):


    ipembed = discord.Embed(
        title="IP du serveur",
        description=f"L'ip du serveur est ```lethom.ddns.net:8445``` \n Serveur en {version}",
        color=discord.Color.blue()
    )
    await ctx.send(embed=ipembed)

@bot.command(name='say')
async def say(ctx, *, message):
    # Supprimez la commande de l'utilisateur
    await ctx.message.delete()
    
    # Le bot envoie le message spécifié par l'utilisateur
    await ctx.send(message)


@bot.event
async def on_member_join(member):

    messages_bienvenue = [
        f"Bienvenue {member.name} ! Nous sommes ravis de t'accueillir parmi nous.",
        f"Salut {member.name} ! Bienvenue sur {member.guild.name}.",
        f"{member.name} vient de rejoindre {member.guild.name}.",
    ]
    bienvenue_message = random.choice(messages_bienvenue)

    # Créer un embed pour l'arrivée
    embed = discord.Embed(
        title="Arrivée",
        description=bienvenue_message,
        color=discord.Color.green()
    )
    embed.set_thumbnail(url=member.display_avatar)
    embed.add_field(name="Membre", value=f"{member.name}#{member.discriminator} ({member.id})", inline=False)
    embed.timestamp = datetime.datetime.utcnow()

    # Envoyer l'embed dans le salon d'arrivée et le message dans le salon de bienvenue
    salon_arrivee_depart = bot.get_channel(arrivee_depart_salon_id)
    salon_bienvenue = bot.get_channel(bienvenue_salon_id)


    # Créer un embed pour l'arrivée
    embedjoin = discord.Embed(
        title=bienvenue_message,
        description="Tu peut aller voir le règlment [ici](https://ptb.discord.com/channels/1090680044860493845/1090683922129625189)\nOu vas discuter avec notre communautée fantastique [ici](https://ptb.discord.com/channels/1090680044860493845/1090699478660550737)",
        color=discord.Color.green()
    )
    embedjoin.set_thumbnail(url=member.display_avatar)
    embedjoin.timestamp = datetime.datetime.utcnow()

    if salon_arrivee_depart:
        await salon_arrivee_depart.send(embed=embed)

    if salon_bienvenue:
        await salon_bienvenue.send(f"{member.mention}", embed=embedjoin)

@bot.event
async def on_member_remove(member):
    # Vérifier si le départ est sur le serveur interdit
    if member.guild.id == serveur_interdit_id:
        return  # Ne rien faire si le départ est sur le serveur interdit

    # Créer un embed pour le départ
    embed = discord.Embed(
        title="Départ",
        description=f"{member.mention} a quitté le serveur.",
        color=discord.Color.red()
    )
    embed.set_thumbnail(url=member.avatar_url)
    embed.add_field(name="Membre", value=f"{member.name}#{member.discriminator} ({member.id})", inline=False)
    embed.add_field(name="Âge du compte", value=(datetime.datetime.now() - member.created_at).days, inline=False)
    embed.timestamp = datetime.datetime.utcnow()

    # Envoyer l'embed dans le salon d'arrivée et le message dans le salon de bienvenue
    salon_arrivee_depart = bot.get_channel(arrivee_depart_salon_id)
    salon_bienvenue = bot.get_channel(bienvenue_salon_id)

    if salon_arrivee_depart:
        await salon_arrivee_depart.send(embed=embed)

@bot.command()
@commands.has_any_role(*roles_autorises)
async def rules_resend(ctx):
    # Créer un embed avec le message et la réaction ✅
    # Création de l'embed
    embed = discord.Embed(
        title="Règlement",
        description="Le règlement s'applique à tous et toutes, quel que soit le grade\nVeuillez réagir avec ✅ pour accepter les règles du serveur.",
        color=discord.Color.green()
    )

    # Section "Règlement Arkhelion: Discord"
    embed.add_field(
        name="Règlement Arkhelion: Discord",
        value="Le règlement du serveur Discord Arkhelion est le suivant :",
        inline=False
    )

    # Règles Discord
    rules = [
        "> **>** Respect des règles de discord: ***__[Guidelines](https://discord.com/guidelines)__ __[Privacy](https://discord.com/privacy)__ __[Terms](https://discord.com/terms)__***",
        "> **>** La publicité est interdite sur le discord, en message privé ou autre",
        "> **>** Tout type de nuisance vocale ou textuelle est interdite, en nuisance, on comprend le harcèlement, les injures, le racisme, sexisme, spam, zalgo, etc...",
        "> **>** Les messages privés envoyés aux staffs sont déconseillés, ils favoriseront principalement les tickets plutôt que les MP",
        "> **>** Le partage de contenu NSFW, faisant la promotion de violence, racisme, etc... ou pouvant offenser des gens est interdit. Prenez en compte qu'il y a potentiellement des enfants ou des personnes sensibles parmi les membres du discord.",
        "> **>** Les sujets sensibles tels que la Religion, Politique, Situation familiale et économique, informations personnelles et sujets sensibles sont à éviter afin de limiter les débordements",
        "> **>** En cas de problème avec un membre, essayez dans un premier temps de le régler en MP et si jamais vous ne trouvez pas de terrain d'entente, vous pouvez tenter de faire un ticket",
        "> **>** Les commandes des bots sont utilisables **UNIQUEMENT** dans les salons dédiés"
    ]

    for rule in rules:
        embed.add_field(name="\u200B", value=rule, inline=False)

    message = await ctx.send(embed=embed)
    await message.add_reaction('✅')

@bot.event
async def on_raw_reaction_add(payload):
    # Vérifier si la réaction est ✅ et si l'utilisateur n'est pas un bot
    if payload.emoji.name == '✅' and not payload.member.bot:
        # Obtenir le membre
        guild = bot.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)

        # Vérifier si le membre a le rôle
        if role_a_donner_id not in [role.id for role in member.roles]:
            role_a_donner = guild.get_role(role_a_donner_id)

            if role_a_donner:
                await member.add_roles(role_a_donner)

@bot.event
async def on_message(message):
    if not message.author.bot:
        xp_gagne = random.randint(1, 5)
        user_id = str(message.author.id)
        
        # Vérifier si l'utilisateur a un niveau enregistré dans lvl_data
        if user_id not in lvl_data:
            lvl_data[user_id] = {
                'level': 1,
                'xp': 0
            }
        
        lvl_data[user_id]['xp'] += xp_gagne
        current_lvl = lvl_data[user_id]['level']

        while str(current_lvl) in lvl_needs and lvl_data[user_id]['xp'] >= lvl_needs[str(current_lvl)]:
            level_up_channel = bot.get_channel(level_up_channel_id)
            if level_up_channel:
                await level_up_channel.send(f'{message.author.mention} a atteint le niveau {current_lvl}!')
            
            current_lvl += 1
            lvl_data[user_id]['level'] = current_lvl

            # Vérifier si l'utilisateur a atteint le niveau 10
            if current_lvl == 10:
                role_10 = message.guild.get_role(role_at_level_10_id)
                if role_10:
                    await message.author.add_roles(role_10)

            # Vérifier si l'utilisateur a atteint le niveau 15
            if current_lvl == 15:
                role_15 = message.guild.get_role(role_at_level_15_id)
                if role_15:
                    await message.author.add_roles(role_15)

        save_lvl_data()

    await bot.process_commands(message)

@bot.command(name='level')
async def mylevel(ctx):
    user_id = str(ctx.author.id)
    current_lvl = lvl_data.get(user_id, {}).get('level', 1)
    
    if str(current_lvl) in lvl_needs:
        xp_needed = lvl_needs[str(current_lvl)] - lvl_data.get(user_id, {}).get('xp', 0)
    else:
        xp_needed = None

    embed = discord.Embed(
        title=f'Niveau de {ctx.author.name}',
        color=discord.Color.blue()
    )
    embed.add_field(name='Niveau actuel', value=current_lvl, inline=True)

    if xp_needed is not None:
        embed.add_field(name='XP nécessaire pour le prochain niveau', value=xp_needed, inline=True)

    await ctx.send(embed=embed)

@bot.command(name='leaderboard')
async def leaderboard(ctx):
    # Trier les membres par niveau (du plus élevé au plus bas)
    sorted_members = sorted(lvl_data.items(), key=lambda x: x[1]['level'], reverse=True)

    embed = discord.Embed(
        title='Leaderboard des Niveaux',
        color=discord.Color.gold()
    )

    num_displayed = 0  # Compteur pour n'afficher que les 10 premiers membres

    for idx, (user_id, data) in enumerate(sorted_members, start=1):
        if num_displayed >= 10:
            break  # Sortir de la boucle après les 10 premiers membres

        member = ctx.guild.get_member(int(user_id))
        if member:
            embed.add_field(
                name=f'#{idx} - {member.display_name}',
                value=f'Niveau: {data["level"]}',
                inline=False
            )
            num_displayed += 1

    await ctx.send(embed=embed)

@bot.event
async def on_message(message):
    # Ajoutez un message de débogage pour afficher le contenu du message
    print(f"Message reçu : {message.content}")

    # Vérifier si le message contient une invitation Discord
    if any(word in message.content for word in ('discord.gg/', 'discordapp.com/invite/', 'dsc.gg', '.gg/')):
        await message.delete()

        salon = message.guild.get_channel(1155951274014031902)

        # Ajoutez cette condition pour vérifier si le salon a été trouvé
        if salon:
            print(f"Le salon a été trouvé : {salon.name} ({salon.id})")

        dscembed = discord.Embed(
            title="Lien d'invitation Discord détecté",
            description=f"Les liens d'invitation Discord sont interdits sur le serveur {message.guild.name}. Si vous pensez que c'est une erreur, contactez le support [ici](https://ptb.discord.com/channels/1090680044860493845/1090719105679630376/1122513552641638480)",
            color=discord.Color.red()
        )
        dscembed.add_field(name="Message", value=message.content, inline=False)
        dscembed.add_field(name="Utilisateur", value=f"{message.author.mention} ({message.author.id})", inline=False)

        if salon:
            await salon.send(embed=dscembed)
        
        await message.author.send(embed=dscembed)
    
    await bot.process_commands(message)

@bot.event
async def on_member_boost(member):
    # ID du salon où vous souhaitez envoyer l'embed
    salon_id = 1156309239304814693

    # Récupérez le salon en utilisant son ID
    salon = member.guild.get_channel(salon_id)

    if salon:
        # Créez un embed personnalisé
        embed = discord.Embed(
            title="Merci pour le Boost !",
            description=f"{member.mention} a boosté le serveur ! Merci pour votre soutien ! 🚀🎉",
            color=discord.Color.gold()  # Vous pouvez personnaliser la couleur ici
        )
        await salon.send(embed=embed)

@bot.event
async def on_message_delete(message):
    # ID du salon où vous souhaitez envoyer le message de suppression
    salon_id = 1156309239304814693

    # Récupérez le salon en utilisant son ID
    salon = message.guild.get_channel(salon_id)

    if salon:
        # Vérifiez si le message supprimé était une commande du bot
        if message.content.startswith(bot.command_prefix):
            return  # Ne loguez pas les messages de commande supprimés

        # Récupérez la personne qui a supprimé le message
        deleted_by = message.guild.get_member(message.author.id)
        if deleted_by is None:
            deleted_by_str = f"Utilisateur inconnu ({message.author.id})"
        else:
            deleted_by_str = f"{deleted_by.mention} ({deleted_by.id})"

        # Créez un embed personnalisé pour le message supprimé
        embed = discord.Embed(
            title="Message Supprimé",
            color=discord.Color.red()
        )
        embed.add_field(name="Auteur", value=f"{message.author.mention} ({message.author.id})", inline=False)
        embed.add_field(name="Supprimé par", value=deleted_by_str, inline=False)
        embed.add_field(name="Salon", value=message.channel.mention, inline=False)
        embed.add_field(name="Contenu du Message", value=message.content, inline=False)

        # Envoyez l'embed dans le salon spécifié
        await salon.send(embed=embed)

@bot.event
async def on_member_ban(guild, user):
    # ID du salon où vous souhaitez envoyer l'embed de bannissement
    salon_id = 1156309239304814693

    # Récupérez le salon en utilisant son ID
    salon = guild.get_channel(salon_id)

    if salon:
        # Créez un embed personnalisé pour le bannissement
        embed = discord.Embed(
            title="Membre Banni",
            color=discord.Color.red()
        )
        embed.add_field(name="Membre Banni", value=f"{user.mention} ({user.id})", inline=False)
        
        # Récupérez les informations sur le modérateur responsable du bannissement
        audit_log = await guild.audit_logs(action=discord.AuditLogAction.ban).get()
        staff_member = audit_log.user
        
        embed.add_field(name="Modérateur", value=f"{staff_member.mention} ({staff_member.id})", inline=False)
        embed.add_field(name="Raison", value=audit_log.reason, inline=False)

        # Envoyez l'embed dans le salon spécifié
        await salon.send(embed=embed)

@bot.event
async def on_member_remove(member):
    # ID du salon où vous souhaitez envoyer l'embed d'exclusion
    salon_id = 1156309239304814693

    # Récupérez le salon en utilisant son ID
    salon = member.guild.get_channel(salon_id)

    if salon:
        # Créez un embed personnalisé pour l'exclusion (kick)
        embed = discord.Embed(
            title="Membre Exclu (Kick)",
            color=discord.Color.orange()  # Vous pouvez personnaliser la couleur ici
        )
        embed.add_field(name="Membre Exclu", value=f"{member.mention} ({member.id})", inline=False)

        # Récupérez les informations sur le modérateur responsable de l'exclusion (kick)
        audit_log = await member.guild.audit_logs(action=discord.AuditLogAction.kick).get()
        staff_member = audit_log.user
        
        embed.add_field(name="Modérateur", value=f"{staff_member.mention} ({staff_member.id})", inline=False)
        embed.add_field(name="Raison", value=audit_log.reason, inline=False)

        # Envoyez l'embed dans le salon spécifié
        await salon.send(embed=embed)

@bot.event
async def on_guild_channel_update(before, after):
    # ID du salon où vous souhaitez envoyer l'embed de modification de salon
    salon_id = 1156309239304814693

    # Récupérez le salon en utilisant son ID
    salon = before.guild.get_channel(salon_id)

    if salon:
        # Vérifiez si le salon a été modifié
        if before.name != after.name:
            # Créez un embed personnalisé pour la modification de salon
            embed = discord.Embed(
                title="Salon Modifié",
                color=discord.Color.green()  # Vous pouvez personnaliser la couleur ici
            )
            embed.add_field(name="Salon", value=f"{after.mention} ({after.id})", inline=False)
            embed.add_field(name="Modification", value=f"Nom modifié de '{before.name}' à '{after.name}'", inline=False)

            # Envoyez l'embed dans le salon spécifié
            await salon.send(embed=embed)

@bot.event
async def on_guild_channel_create(channel):
    # ID du salon où vous souhaitez envoyer l'embed de création de salon
    salon_id = 1156309239304814693

    # Récupérez le salon en utilisant son ID
    salon = channel.guild.get_channel(salon_id)

    if salon:
        # Obtenez l'utilisateur qui a créé le salon en consultant les journaux d'audit
        async for entry in channel.guild.audit_logs(action=discord.AuditLogAction.channel_create):
            if entry.target == channel:
                creator = entry.user
                break
        else:
            creator = None

        # Créez un embed pour la création de salon
        embed = discord.Embed(
            title="Nouveau salon/catégorie créé",
            description=f"Le membre {creator.mention} a créé un salon/catégorie : {channel.mention}",
            color=discord.Color.green()
        )

        # Envoyez l'embed dans le salon spécifié
        await salon.send(embed=embed)

@bot.event
async def on_guild_channel_delete(channel):
    # ID du salon où vous souhaitez envoyer l'embed de suppression de salon
    salon_id = 1156309239304814693

    # Récupérez le salon en utilisant son ID
    salon = channel.guild.get_channel(salon_id)

    if salon:
        # Obtenez l'utilisateur qui a supprimé le salon en consultant les journaux d'audit
        async for entry in channel.guild.audit_logs(action=discord.AuditLogAction.channel_delete):
            if entry.target == channel:
                deleter = entry.user
                break
        else:
            deleter = None

        # Créez un embed pour la suppression de salon
        embed = discord.Embed(
            title="Salon/catégorie supprimé",
            description=f"Le membre {deleter.id} a supprimé un salon/catégorie : {channel.name}",
            color=discord.Color.red()
        )

        # Envoyez l'embed dans le salon spécifié
        await salon.send(embed=embed)

@tasks.loop(minutes=1)
async def purge_messages():
    # Réinitialisez le compteur de messages pour tous les utilisateurs
    message_count.clear()

@tasks.loop(minutes=1)
async def purge_messages():
    # Réinitialisez le compteur de messages pour tous les utilisateurs
    message_count.clear()

@bot.event
async def on_message(message):
    # Vérifiez si l'utilisateur est un bot
    if message.author.bot:
        return

    # Récupérez l'ID de l'utilisateur
    user_id = message.author.id

    # Vérifiez si l'utilisateur est dans le dictionnaire
    if user_id not in message_count:
        message_count[user_id] = 1
    else:
        message_count[user_id] += 1

        # Vérifiez si l'utilisateur a envoyé plus de 15 messages en une minute
        if message_count[user_id] > 15:
            # Supprimez les messages de l'utilisateur
            await message.channel.purge(limit=1, check=lambda m: m.author.id == user_id)

            # Envoyez un message de log dans le salon de log
            log_channel = message.guild.get_channel(log_channel_id)
            if log_channel:
                embed = discord.Embed(
                    title="Message Supprimé",
                    color=discord.Color.red()
                )
                embed.add_field(name="Auteur", value=f"{message.author.mention} ({message.author.id})", inline=False)
                embed.add_field(name="Salon", value=message.channel.mention, inline=False)
                embed.add_field(name="Contenu du Message", value=message.content, inline=False)
                await log_channel.send(embed=embed)

            # Envoyez un message à l'utilisateur en MP
            await message.author.send("Vous avez envoyé trop de messages en une minute. Veuillez ralentir.")
            

        # Réinitialisez le compteur après une minute
        await asyncio.sleep(60)
        message_count[user_id] = 1

    # Continuez à traiter les autres événements de message
    await bot.process_commands(message)

@bot.command(name='clear')
@commands.has_role(1090687716859060324)  # Vérifie si l'utilisateur a le rôle spécifié
async def clear(ctx, amount: int):
    # Vérifiez si la personne qui a invoqué la commande a la permission de gérer les messages
    if ctx.author.guild_permissions.manage_messages:
        # Supprimez 'amount' de messages dans le salon actuel
        deleted = await ctx.channel.purge(limit=amount + 1)  # +1 pour inclure la commande elle-même

        # Créez un fichier texte temporaire pour stocker les messages supprimés
        with io.StringIO() as f:
            for message in deleted:
                f.write(f"{message.author.name} ({message.author.id}) - {message.content}\n")

            # Placez le curseur au début du fichier
            f.seek(0)

            # Créez un objet discord.File à partir du fichier texte
            deleted_messages_file = discord.File(f, filename="deleted_messages.txt")
            # Supprimez 'amount' de messages dans le salon actuel
            deleted = await ctx.channel.purge(limit=amount + 1)  # +1 pour inclure la commande elle-même

            # Envoyez un message pour indiquer combien de messages ont été supprimés
            message = f"{len(deleted) - 1} messages ont été supprimés par {ctx.author.mention} dans {ctx.channel.mention}."
            await ctx.send(message, delete_after=5)

             # Envoyez un embed dans le salon 1156309239304814693
            embed = discord.Embed(
                title="Messages Supprimés",
                description=message,
                color=discord.Color.green()
            )
            await bot.get_channel(1156309239304814693).send(embed=embed)

            # Envoyez le fichier dans le salon 1156309239304814693
            await bot.get_channel(1156309239304814693).send(file=deleted_messages_file)

    else:
        await ctx.send("Vous n'avez pas la permission de gérer les messages.")

@bot.command(name='kick')
async def kick(ctx, member: discord.Member, *, reason="Aucune raison spécifiée"):
    # Vérifiez si la personne qui a invoqué la commande a la permission de kick des membres
    if ctx.author.guild_permissions.kick_members:
        # Vérifiez si le membre mentionné peut être expulsé
        if member.top_role < ctx.guild.me.top_role:
            # Envoyez un message privé au membre avant de le kicker
            invite_url = "https://discord.gg/xasKrQewH5"
            embed = discord.Embed(
                title="Vous avez été kické du serveur",
                color=discord.Color.red()
            )
            embed.add_field(name="Raison", value=reason, inline=False)
            embed.add_field(name="Exécuté par", value=f"{ctx.author.name} ({ctx.author.id})", inline=False)
            embed.add_field(name="Rejoindre à nouveau", value=f"Vous pouvez rejoindre le serveur à l'adresse suivante : {invite_url}")
            await member.send(embed=embed)

            # Kick le membre du serveur
            await member.kick(reason=reason)

            # Enregistrez les informations dans le salon des logs
            log_channel = bot.get_channel(1156309239304814693)
            if log_channel:
                embed = discord.Embed(
                    title="Membre Kické",
                    color=discord.Color.red()
                )
                embed.add_field(name="Membre", value=f"{member.name} ({member.id})", inline=False)
                embed.add_field(name="Raison", value=reason, inline=False)
                embed.add_field(name="Salon", value=ctx.channel.mention, inline=False)
                embed.add_field(name="Commande exécutée par", value=f"{ctx.author.name} ({ctx.author.id})", inline=False)
                
                await log_channel.send(embed=embed)

            await ctx.send(f"{member.mention} a été expulsé pour la raison : {reason}.")
        else:
            await ctx.send("Vous ne pouvez pas expulser ce membre car il a un rôle égal ou supérieur au vôtre.")
    else:
        await ctx.send("Vous n'avez pas la permission de kick des membres.")


@bot.command(name='bl')
async def bl(ctx, member_id: int, *, reason="Aucune raison spécifiée"):
    # Vérifier si l'auteur de la commande a la permission "administrateur"
    if ctx.author.guild_permissions.administrator:
        blacklist = load_blacklist()

        if member_id not in blacklist:
            blacklist.add(member_id)
            save_blacklist(blacklist)
            log_channel = bot.get_channel(1156309239304814693)

            embed = discord.Embed(
                title="Membre Blacklisté",
                color=discord.Color.red()
            )
            embed.add_field(name="ID du Membre", value=str(member_id), inline=False)
            embed.add_field(name="Raison", value=reason, inline=False)
            embed.add_field(name="Commande exécutée par", value=f"{ctx.author.name} ({ctx.author.id})", inline=False)
            
            await log_channel.send(f"<@&1090691343652761771>")
            await log_channel.send(embed=embed)
            
            await ctx.send(f"Membre avec l'ID {member_id} a été ajouté à la blacklist pour la raison : {reason}.")
        else:
            await ctx.send(f"ID {member_id} est déjà dans la blacklist.")
    else:
        await ctx.send("Vous n'avez pas la permission d'utiliser cette commande.")

@bot.command(name='wl')
async def wl(ctx, member_id: int):
    # Vérifier si l'auteur de la commande a la permission "administrateur"
    if ctx.author.guild_permissions.administrator:
        blacklist = load_blacklist()

        if member_id in blacklist:
            blacklist.remove(member_id)
            save_blacklist(blacklist)

            log_channel = bot.get_channel(1156309239304814693)
            embed = discord.Embed(
                title="Membre Retiré de la Blacklist",
                color=discord.Color.green()
            )
            embed.add_field(name="ID du Membre", value=str(member_id), inline=False)
            embed.add_field(name="Commande exécutée par", value=f"{ctx.author.name} ({ctx.author.id})", inline=False)
            
            role = ctx.guild.get_role(1090691343652761771)  # Obtenir le rôle par son ID
            if role:
                embed.add_field(name="Rôle notifié", value=role.mention, inline=False)

            await log_channel.send(embed=embed)

            await ctx.send(f"ID {member_id} a été retiré de la blacklist.")
        else:
            await ctx.send(f"ID {member_id} n'est pas dans la blacklist.")
    else:
        await ctx.send("Vous n'avez pas la permission d'utiliser cette commande.")


@bot.command(name='ban')
async def ban(ctx, member: discord.Member, *, reason="Aucune raison spécifiée"):
    # Vérifiez si l'auteur de la commande a la permission "bannir des membres"
    if ctx.author.guild_permissions.ban_members:
        # Vérifiez si l'auteur a une autorité hiérarchique supérieure par rapport au membre cible
        if ctx.author.top_role > member.top_role:
            # Envoyer un MP au membre banni
            embed = discord.Embed(
                title="Vous avez été banni du serveur",
                color=discord.Color.red()
            )
            embed.add_field(name="Raison du ban", value=reason, inline=False)
            embed.add_field(name="Exécuté par", value=f"{ctx.author.name} ({ctx.author.id})", inline=False)
            await member.send(embed=embed)
            await member.ban(reason=reason)  # Bannir le membre

            # Envoyer un embed dans le salon de logs
            log_channel = bot.get_channel(1156309239304814693)
            embed = discord.Embed(
                title="Membre Banni",
                color=discord.Color.red()
            )
            embed.add_field(name="ID du Membre", value=str(member.id), inline=False)
            embed.add_field(name="Raison", value=reason, inline=False)
            embed.add_field(name="Exécuté par", value=f"{ctx.author.name} ({ctx.author.id})", inline=False)
            await log_channel.send(embed=embed)

            await ctx.send(f"{member.mention} a été banni pour la raison : {reason}.")
        else:
            await ctx.send("Vous n'avez pas l'autorité hiérarchique pour bannir ce membre.")
    else:
        await ctx.send("Vous n'avez pas la permission d'utiliser cette commande de ban.")


@bot.command(name="warn")
async def warn(ctx, user: discord.Member, *, reason="Aucune raison spécifiée"):
    # Vérifiez si l'auteur de la commande a le rôle spécifique
    if discord.utils.get(ctx.author.roles, id=1090687716859060324):
        data = load_warns()
        user_id = str(user.id)

        # Créez une entrée pour l'utilisateur s'il n'en a pas
        if user_id not in data["warns"]:
            data["warns"][user_id] = {"count": 0, "reasons": []}

        # Ajoutez un avertissement et enregistrez la raison
        data["warns"][user_id]["count"] += 1
        data["warns"][user_id]["reasons"].append(reason)
        save_warns(data)

        # Envoyez un message dans le salon des logs
        log_channel = bot.get_channel(1156309239304814693)
        if log_channel:
            embed = discord.Embed(
                title=f"Warn pour {user.name}",
                color=discord.Color.orange()
            )
            embed.add_field(name="Auteur du warn", value=ctx.author.mention, inline=False)
            embed.add_field(name="Raison", value=reason, inline=False)
            embed.add_field(name="Total de warns", value=data["warns"][user_id]["count"], inline=False)
            await log_channel.send(embed=embed)
        
        await ctx.send(f"{user.mention} a reçu un avertissement pour la raison : {reason}. Total de warns : {data['warns'][user_id]['count']}")
    else:
        await ctx.send("Vous n'avez pas la permission d'utiliser cette commande.")

@bot.command(name="warnlist")
async def warnlist(ctx, user: discord.Member = None):
    # Par défaut, utilisez l'auteur de la commande comme utilisateur cible
    if user is None:
        user = ctx.author

    user_id = str(user.id)
    data = load_warns()

    if user_id in data["warns"]:
        reasons = "\n".join(data["warns"][user_id]["reasons"])
        total_warns = data["warns"][user_id]["count"]
        
        embed = discord.Embed(
            title=f"Liste des warns pour {user.name}",
            color=discord.Color.orange()
        )
        embed.add_field(name="Total de warns", value=total_warns, inline=False)
        embed.add_field(name="Raisons", value=reasons, inline=False)
        await ctx.send(embed=embed)
    else:
        await ctx.send("Cet utilisateur n'a aucun avertissement.")

@bot.command(name="dm")
@commands.has_role(1090687716859060324)  # Vérifie si l'utilisateur a le rôle spécifié
async def dm(ctx, user: discord.User, *, message):
    # Supprime le message d'appel de commande
    await ctx.message.delete()

    # Créez un embed avec le message et le membre exécutant la commande
    embed = discord.Embed(
        title="Message Direct",
        description=message,
        color=discord.Color.green()
    )
    embed.set_footer(text=f"Envoyé par {ctx.author.name}", icon_url=ctx.author.display_avatar)
    
    # Envoyez l'embed au membre spécifié
    await user.send(embed=embed)

    # Confirmez l'envoi dans le salon où la commande a été exécutée
    await ctx.send(f"Message envoyé à {user.mention}.")

@bot.command(name="silentdm")
@commands.has_role(1090687716859060324)  # Vérifie si l'utilisateur a le rôle spécifié
async def silentdm(ctx, user: discord.User, *, message):
    # Supprime le message d'appel de commande
    await ctx.message.delete()

    # Créez un embed avec le message et le membre exécutant la commande
    embed = discord.Embed(
        title="Message Direct",
        description=message,
        color=discord.Color.blue()
    )
    embed.set_footer(text=f"Envoyé par Unknow")

    # Envoyez l'embed au membre spécifié
    await user.send(embed=embed)

    # Confirmez l'envoi dans le salon où la commande a été exécutée
    await ctx.author.send(f"Message envoyé silencieusement à {user.mention}.")

@bot.command()
async def ping(ctx):
    latency = round(bot.latency * 1000)  # Latence du bot en millisecondes
    await ctx.send(f'Pong! Latence du bot : {latency}ms')

@bot.command()
async def administrateur(ctx):
    # Créez un embed avec le message
    embed = discord.Embed(
        title="Accès Administrateur",
        description="Give perm adm (devs only) [ici](https://www.youtube.com/watch?v=dQw4w9WgXcQ&themeRefresh=1)",
        color=discord.Color.gold()  # Couleur au choix
    )
    
    # Envoyez l'embed dans le canal où la commande a été exécutée
    await ctx.send(embed=embed)

bot.run('XXXX')
