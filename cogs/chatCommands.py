import discord
from discord.ext import commands
import giphy_client
from giphy_client.rest import ApiException
import random
import os
from dotenv import load_dotenv

class ChatCommands(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    # makes the bot ready to take cog commands
    @commands.Cog.listener()
    async def on_ready(self):
        print("> chat Cog is loaded")

    
    # replys to user with a ferwell message
    @commands.command(aliases = ["Bye", "cya", "Cya"])
    async def bye(self, ctx):

        ferwells = ["Bye for now!", "See you later!", "bye!"]

        await ctx.send(random.choice(ferwells))
    
    # sends the user a discord invite
    @commands.command(aliases = ["inv", "Inv"])
    async def invite(self, ctx):
        #server_invites = ["https://discord.gg/wcbJgPCnKh", "https://discord.gg/aHF6ezJphZ", "https://discord.gg/UwzhXr6hwb", "https://discord.gg/kWzxXBEjFA"]
        await ctx.send(f"Heres the invite to our support server https://discord.gg/9F5Z9MExdw.") # \n{random.choice(server_invites)
    
    # sends the bots inite link
    @commands.command(aliases = ["botinv", "botInvite", "botinvite"])
    async def botInv(self, ctx):
        bot_invite = "https://discord.com/api/oauth2/authorize?client_id=938071040544878593&permissions=8&scope=bot"
        await ctx.send(f"Here's the invite for the bot! you can add it to any server you have modderator permisions in!\n{bot_invite}")
    

    # replys to a message 
    @commands.command()
    async def lz(self, ctx):
        reply = ("Lz + Ratio! Get bullied nered. Rip Bozo 1-0 im up", 
        "Lz", "1-0 im up", "No you!")
        await ctx.send(random.choice(reply))

    # plays a game with user 
    # * takes multipull arguments as 1 argument
    @commands.command(aliases = ['8ball', 'eightball', '8bal'])
    async def _8ball(self, ctx, *, question):
        responses = ["As I see it, yes.", "Ask again later.", "Better not tell you now.", "Cannot predict now.", "Concentrate and ask again.",
        "Don’t count on it.", "It is certain.", "It is decidedly so.", "Most likely.", "My reply is no.", "My sources say no.",
        "Outlook not so good.", "Outlook good.", "Reply hazy, try again.", "Signs point to yes.", "Very doubtful.", "Without a doubt.",
        "Yes.", "Yes - definitely.", "You may rely on it."]
    
        await ctx.send(f"Question: {question}\nAnswer: {random.choice(responses)}")

    # sends gifs to the server when called
    @commands.command()
    async def gif(self, ctx, *, q ="pig"):

        load_dotenv()
        apiKey = os.getenv('GIFAPIKEY')
        apiInstanse = giphy_client.DefaultApi()
        
        try:

            apiResponse = apiInstanse.gifs_search_get(apiKey, q, limit = 5, rating = "g")
            gifList = list(apiResponse.data)
            gif = random.choice(gifList)

            await ctx.send(gif.embed_url)
        
        except ApiException as e:

            print("\n> API ERROR - error quering Gif API\n")
            await ctx.send(f"It seeems like I cant do that right now :( sorry")


    # repeats a message
    @commands.command()
    async def repeat(self, ctx, *, msg):
        await ctx.send(msg)


    # command for announcing a kill
    @commands.command()
    async def kill(self, ctx, victim: discord.Member):
        await ctx.send(f"{ctx.author.mention} just killed {victim.mention}.")
    
    @commands.command()
    async def revive(self, ctx, victim: discord.Member):
        await ctx.send(f"no worries {ctx.author.mention} just revived {victim.mention}.")
    

    # Annouces a custom action on a user
    @commands.command(aliases = ["Action"])
    async def action(self, ctx, action,  user: discord.Member, target: discord.Member):
        
        if user == target:
            await ctx.send(f"{user.mention} just {action}(ed) themselves lmao.")
        
        else:
            await ctx.send(f"{user.mention} just {action}(ed) {target.mention}")

    # a command for announcing messages to @everyone
    @commands.command(aliases = ["anouncment", "Announce"])
    @commands.has_permissions(manage_roles = True)
    async def announce(self, ctx, isBroadcast = True, *, message):
        announceEmbed = discord.Embed(
            title = "Announcment",
            description = "This is an automated message",
            color = discord.Color.greyple()
        )

        announceEmbed.add_field(name="Anouncment:", value=f"{message}", inline=False)
        announceEmbed.set_footer(text=f"Requested by - {ctx.author}", icon_url=ctx.author.avatar_url)

        if isBroadcast == True:
            await ctx.send(f"||@everyone||", embed = announceEmbed)
        
        else:
            await ctx.send(f"||Messege bellow is hoisted in from \"{ctx.guild}\"||", embed = announceEmbed)

    @commands.command(aliases = ["Gen", "gen", "GenPass", "Generate", "generate"])
    async def genpass(self, ctx, charLimit):

        uppercaseLetters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        lowercaseLetters = uppercaseLetters.lower()
        didgits = "0123456789"
        specialChrs =  "!?_#@:;\\/*."

        upper, lower, nums, special = True, True, True, True

        all = ""
        if upper:
            all += uppercaseLetters
        if lower:
            all += lowercaseLetters
        if nums:
            all += didgits
        if special:
            all += specialChrs


        length = charLimit

        try:
            length = int(length)
        
        except Exception as e:
            await ctx.send("Please enter a number")
            print(f"User Error: {e}")

        if length > 3 and length < 25:

            password = "".join(random.sample(all, length))

            genEmbed = discord.Embed(
                title = "Password",
                description = "Generated by Awack",
                color = discord.Color.greyple()
            )

            genEmbed.add_field(name="Password:", value=f"{password}", inline=False)
            genEmbed.set_footer(text=f"Requested by - {ctx.author}", icon_url=ctx.author.avatar_url)
        
            await ctx.author.send(f"Reply from {ctx.guild}", embed = genEmbed)

            await ctx.send(f"{ctx.author} your password has been sent to you in your Direct Messages. If this function was helpful check out .Info")

        else:
            await ctx.send("Please keep the length between 4 and 24. \n")
            print("User Error: Password failed to generate (to short)")
    


# sends the commands
def setup(client):
    client.add_cog(ChatCommands(client))