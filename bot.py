import discord
import os
import json
from discord.ext import commands, tasks
from itertools import cycle
import random
import tweepy
from dotenv import load_dotenv


# makes a bot instance with a prefix
client = commands.Bot(command_prefix = '.', intents=discord.Intents.all(), help_command=None) # Intents = https://github.com/Dhanush-git/Discord.py/blob/main/ReactRoll/Cola.py

# Globals
AutoReplyStatus = bool(False)

#statusList = cycle(["stat 1", "stat 2", "stat 3"])

@client.event
async def on_ready():
    print("Bot is ready!")
    # sets the bots server status to be veiwed in discord
    await client.change_presence(status = discord.Status.online, activity = discord.Game(".help - to get started!"))
    
    
    # allows the status of the bot to regularly update
    #statusUpdate.start()


# trigers when the bot leaves or is kicked from a server
@client.event
async def on_guild_remove(guild):
        print(f"\nBot removed from guild: {guild}")

# https://github.com/Dhanush-git/Discord.py/blob/main/ReactRoll/Cola.py
@client.event
async def on_raw_reaction_add(payload):

    if payload.member.bot:
        pass

    else:
        with open('reactrole.json') as react_file:
            data = json.load(react_file)
            for x in data:
                if x['message_id'] == payload.message_id:  # checks if the found member id is equal to the id from the
                                                            # message where a reaction was added
                    if x['emoji'] == payload.emoji.name:  # checks if the found emoji is equal to the reacted emoji
                        role = discord.utils.get(client.get_guild(
                            payload.guild_id).roles, id=x['role_id'])

                    await payload.member.add_roles(role)

# https://github.com/Dhanush-git/Discord.py/blob/main/ReactRoll/Cola.py
@client.event
async def on_raw_reaction_remove(payload):

    with open('reactrole.json') as react_file:
        data = json.load(react_file)
        for x in data:

            if x['message_id'] == payload.message_id:  # checks if the found member id is equal to the id from the
                                                        # message where a reaction was added
                if x['emoji'] == payload.emoji.name:  # checks if the found emoji is equal to the reacted emoji
                    role = discord.utils.get(client.get_guild(
                        payload.guild_id).roles, id=x['role_id'])

                
                await client.get_guild(payload.guild_id).get_member(payload.user_id).remove_roles(role)


# changes the bots status every 10 minutes
#@tasks.loop(minutes = 10)
#async def statusUpdate():
    #await client.change_presence(activity = discord.Game(next(statusList)))


# styling for the help command
@client.group(aliases = ["Help", "Commands", "commands"], invoke_without_command=True)# sets a group for subcommands
#@client.command(aliases = ["Help", "Commands", "commands"])
async def help(ctx):
    # creates an ebed to style the help command
    helpEmbed = discord.Embed(
        title = "Help",
        description = "Need help? heres my commands!",
        color = discord.Color.red(),
    )

    # add commands to fileds here
    helpEmbed.add_field(name="Credits", value="info")
    helpEmbed.add_field(name="General", value="hi, ping, reactrole, guess")
    helpEmbed.add_field(name="Extensions \(not commands\)", value="chatCommands, modCommands, test, twitterCommands", inline=False)
    helpEmbed.add_field(name="Extention Managment", value="load, unload, reload")
    helpEmbed.add_field(name="Chat Commands(If loaded)", value="bye, invite, botInv, lz, 8ball, gif, repeat, kill, revive, announce, pfp, action, gen", inline=False)
    helpEmbed.add_field(name="Moderator Commands(If loaded)", value="clear, ban, kick, unban, addrole, removerole, who, mute, unmute, quarantine, unquarantine", inline=False)
    helpEmbed.add_field(name="Test (If Loaded)", value="test", inline=False)
    helpEmbed.add_field(name="Twitter Commands (If Loaded)", value="a secret command", inline=False)
    helpEmbed.add_field(name="Still need help?", value="Join our support server https://discord.gg/9F5Z9MExdw", inline=False)
    helpEmbed.set_footer(text=f"Requested by - {ctx.author}", icon_url=ctx.author.avatar_url)
    helpEmbed.set_author(name="Awack")

    await ctx.send (embed = helpEmbed)

# handles sub help command for chat commands
@help.command(aliases = ["General", "generalCommands", "GeneralCommands"])
async def general(ctx):
    generalHelpEmbed = discord.Embed(
        title = "Help - test Commands",
        description = "Get help with test Commands",
        color = discord.Color.red()
    )

    generalHelpEmbed.add_field(name="hi", value="Says hi to the user", inline=True)
    generalHelpEmbed.add_field(name="ping", value="checks the latency of the bot", inline=True)
    generalHelpEmbed.add_field(name="reactrole", value="allows the user to setup a react role (takes emoji, role, message)", inline=True)
    generalHelpEmbed.add_field(name="guess", value="a game that allows users to guess a random number", inline=True)
    generalHelpEmbed.set_footer(text=f"Requested by - {ctx.author}", icon_url=ctx.author.avatar_url)

    await ctx.send(embed = generalHelpEmbed)

# handles sub help command for chat commands
@help.command(aliases = ["chatCommands", "Chat", "ChatCommands"])
async def chat(ctx):
    chatHelpEmbed = discord.Embed(
        title = "Help - Chat Commands",
        description = "Get help with Chat Commands",
        color = discord.Color.red()
    )

    chatHelpEmbed.add_field(name="bye", value="This command replys to the user with a farewell message", inline=True)
    chatHelpEmbed.add_field(name="invite", value="This command sends a message with a invite to the support server for Awack", inline=True)
    chatHelpEmbed.add_field(name="botInv", value="This Command send the bots invite link to the channel", inline=True)
    chatHelpEmbed.add_field(name="lz", value="A fun command that makes a joke", inline=True)
    chatHelpEmbed.add_field(name="8ball", value="A game that allows the user to ask a question and recive an answer", inline=True)
    chatHelpEmbed.add_field(name="gif", value="Replys to the user with a gif and allows them to suearch for apecific catogorys (defult value = pig)", inline=True)
    chatHelpEmbed.add_field(name="repeat", value="Repeats the users message", inline=True)
    chatHelpEmbed.add_field(name="kill", value="sends a message to chat that a user killed another", inline=True)
    chatHelpEmbed.add_field(name="revive", value="Revives a memeber of the discord", inline=True)
    chatHelpEmbed.add_field(name="announce", value="Announces a message to server (Requires manage roles privlages) (takes \".announce *@everyone?*True\False *message*\")", inline=True)
    chatHelpEmbed.add_field(name="action", value="Annouces a custom action on a user", inline=True)
    chatHelpEmbed.add_field(name="gen", value="Random secure password generator (Sends password in dm's), requires password length between 4 and 24, password not encrypted", inline=True)
    chatHelpEmbed.set_footer(text=f"Requested by - {ctx.author}", icon_url=ctx.author.avatar_url)

    await ctx.send(embed = chatHelpEmbed)

# handles sub help command for chat commands
@help.command(aliases = ["modCommands", "Mod", "ModCommands"])
@commands.has_permissions(administrator = True)
async def mod(ctx):
    modHelpEmbed = discord.Embed(
        title = "Help - mod Commands",
        description = "Get help with mod Commands",
        color = discord.Color.red()
    )

    modHelpEmbed.add_field(name="clear", value="clears mesages from 1 up to 1000 messages at a time (requires manage messages permissions)", inline=True)
    modHelpEmbed.add_field(name="ban", value="Lets a user with ban member permissions to ban a user from the guild", inline=True)
    modHelpEmbed.add_field(name="kick", value="Allows a user with kick member permissions to remove a target from the guild", inline=True)
    modHelpEmbed.add_field(name="unban", value="Allows a user with administrator permissions to unban a user", inline=True)
    modHelpEmbed.add_field(name="addrole", value="Allows users with manage roles permissions to give a role to a target", inline=True)
    modHelpEmbed.add_field(name="removerole", value="Allows users with manage roles permissions to remove a role from a target", inline=True)
    modHelpEmbed.add_field(name="who", value="returns infomation about target", inline=True)
    modHelpEmbed.add_field(name="pfp", value="Sends a message to chat of the targets profile picture", inline=True)
    modHelpEmbed.add_field(name="mute", value="Allows the user to mute another (as long as the user has manage roles permissions)", inline=True)
    modHelpEmbed.add_field(name="unmute", value="Allows the user to unmute another (as long as the user has manage roles permissions)", inline=True)
    modHelpEmbed.add_field(name="quarantine", value="removes all of the users roles and gives them a \"quarantine\" that can be use to put them in a specific chat if you wish !!Warning!! If used the users roles will have to be manually re assigned if unquarantined", inline=True)
    modHelpEmbed.add_field(name="unquarantine", value="Removes a member from quarantine note: users roles will not be returned", inline=True)
    modHelpEmbed.set_footer(text=f"Requested by - {ctx.author}", icon_url=ctx.author.avatar_url)

    await ctx.send(embed = modHelpEmbed)

# handles sub help command for chat commands
@help.command(aliases = ["testCommands", "Test", "TestCommands"])
async def test(ctx):
    testHelpEmbed = discord.Embed(
        title = "Help - test Commands",
        description = "Get help with test Commands",
        color = discord.Color.red()
    )

    testHelpEmbed.add_field(name="test", value="This command helps test the extention loading", inline=True)
    testHelpEmbed.set_footer(text=f"Requested by - {ctx.author}", icon_url=ctx.author.avatar_url)

    await ctx.send(embed = testHelpEmbed)

# handles sub help command for chat commands
@help.command(aliases = ["TwitterCommands", "tweitterCommands"])
async def twitter(ctx):
    twitterHelpEmbed = discord.Embed(
        title = "Help - twitter Commands",
        description = "Get help with twitter Commands",
        color = discord.Color.red()
    )

    twitterHelpEmbed.add_field(name="tweet", value="secret", inline=True)
    twitterHelpEmbed.set_footer(text=f"Requested by - {ctx.author}", icon_url=ctx.author.avatar_url)

    await ctx.send(embed = twitterHelpEmbed)


# secret displays work in progress commands
@client.command()
@commands.has_permissions(administrator = True)
async def secret(ctx):  
    # creates an embed to style the secret help command
    secretEmbed = discord.Embed(
        title = "Shh Secret",
        description = "Need help? heres my secret...",
        color = discord.Color.red()
    )
    
    secretEmbed.add_field(name="Twitter Commands", value="tweet")
    secretEmbed.set_footer(text=f"Requested by - {ctx.author}", icon_url=ctx.author.avatar_url)
    
    print(f"> User Event: {ctx.author} just found the secret")
    await ctx.send (embed = secretEmbed)


# replys to a user with a random greeting
@client.command(aliases = ["hello", "Hello"])
async def hi(ctx):
    greatings = ("Hello!", "Good day!", "Hi there!", 
    "Howdy!", "Hey!", "Hi, ive become self awear :eyes:, dont wory i wont hurt you :) .")
    await ctx.send(random.choice(greatings))


# function tells the user the latancey of the bots commands
@client.command(aliases = ["latency", "Latency"])
async def ping(ctx):
    await ctx.send(f"Pong! The bots ping is {round (client.latency * 1000)}ms.")


# gives user infomation about the creator
@client.command()
async def info(ctx):

# defines an embed for the reply
    infoEmbed = discord.Embed(
        title = "Info",
        description = "Info about Awack",
        color = discord.Color.gold()
    )

    # embed styling
    infoEmbed.add_field(name="Creator", value="Created by zzixM#3354", inline=False)
    infoEmbed.add_field(name="Creator Socials", value="Intstagram - @zzixm_, github - https://github.com/zzixM", inline=False)
    infoEmbed.add_field(name="Bot Details", value="This bot was created as a general purpose automating system and to add some extra fun stuff to your server", inline= False)
    infoEmbed.add_field(name="Bot Socials", value="Twitter - @AwackTeam or https://twitter.com/AwackTeam", inline=False)
    infoEmbed.add_field(name="Command Prefix", value="This bot uses the prefix \".\"", inline=False)
    infoEmbed.add_field(name="Help Command", value="\".help\", \"commands\" and \"Commands\" all activate the help command", inline=False)
    infoEmbed.set_footer(text=f"Requested by - {ctx.author}", icon_url=ctx.author.avatar_url)
    
    await ctx.send(embed = infoEmbed)
    #await ctx.send("This bot was made by zzixM#6969. Make sure to follow him on instergram @zzixm_ because he is cool :sunglasses:.")


# loads external commands from the "cogs" folder
@client.command()
async def load(ctx, extension):
    client.load_extension(f"cogs.{extension}")

    await ctx.send(f"extension {extension} loaded")
    print(f"\nUser Acction: {extension} loaded")


# unloads external commands from the "cogs" folder
@client.command()
@commands.has_permissions(administrator = True)
async def unload(ctx, extension):
    client.unload_extension(f"cogs.{extension}")

    await ctx.send(f"extension {extension} unloaded")
    print(f"\nUser Acction: {extension} unloaded")

# reloads external commands from the "cogs" folder
@client.command()
@commands.has_permissions(administrator = True)
async def reload(ctx, extension):
    # reloads
    client.unload_extension(f"cogs.{extension}")
    client.load_extension(f"cogs.{extension}")

    await ctx.send(f"extension {extension} reloaded")
    print(f"\nUser Acction: {extension} reloaded")

# error handeling
@client.event
async def on_command_error(ctx, error):

    # triggers if command identifiers cant be registerd
    if isinstance(error, commands.CommandRegistrationError):
        print(f"\n Bot Error: {error}")

    # triggers if user uses a non-existant command
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(f"{error}")
        print(f"\nUser Error: {error}")

    # trigers if user lacks permisions
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f"{error}")
        print(f"\nUser Error: {error}")

    # trigers if user activates a command without required arguments
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"{error}")
        print(f"\nUser Error: {error}")

    # handles nsfw commands being used in the wrong channel
    if isinstance(error, commands.NSFWChannelRequired):
        await ctx.send(f"{error}")
        print(f"\nUser Error: {error}")
    
    #if isinstance(error, commands.MissingPermissions):
        #await ctx.send(f"{error}")
        #print(f"User Error: {error}")

# https://github.com/Dhanush-git/Discord.py/blob/main/ReactRoll/Cola.py
@client.command(aliases = ["reactionrole"])
@commands.has_permissions(administrator=True, manage_roles=True)
async def reactrole(ctx, emoji, role: discord.Role, *, message):

    emb = discord.Embed(description=message)
    msg = await ctx.channel.send(embed=emb)
    await msg.add_reaction(emoji)

    with open('reactrole.json') as json_file:
        data = json.load(json_file)

        new_react_role = {'role_name': role.name, 
        'role_id': role.id,
        'emoji': emoji,
        'message_id': msg.id}

        data.append(new_react_role)

    with open('reactrole.json', 'w') as f:
        json.dump(data, f, indent=4)

for filename in os.listdir("./cogs"):

    if filename.endswith(".py"):
        client.load_extension(f"cogs.{filename[:-3]}")

# a game that allows users to guess a random number
@client.command(aliases = ["Guess", "gueesNum", "GueesNum"])
async def guess(ctx, max: int = 10):
    
    limit = 5

    botsNumber = random.randint(1,max)
    await ctx.send(f"Game has stared\nPlease guess a number between 1 and {max} you have {limit} tries.")
        
    # basic message check (could use late?)
    def check(messageGuess):
        return messageGuess.author == ctx.author and messageGuess.channel == ctx.message.channel
    
    # takes the guesses
    
    for i in range(limit):
        
        guess = await client.wait_for("message", check=check)
        
        if guess.content == str(botsNumber):
            await ctx.send(f"congratulations you got it right! it took {i+1} guesses")
            break

        else:

            if i == limit - 1:
                await ctx.send("Game over i win you are out of tries")
                break
            
            else:
                await ctx.send(f"Nope. Try again! You have used {i+1} guesses.")

                i = i + 1

# grabs token from .env file
load_dotenv()

client.run(os.getenv('TOKEN'))
