import discord
from discord.ext import commands

class test(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    # makes the bot ready to take cog commands
    @commands.Cog.listener()
    async def on_ready(self):
        print("> test Cog is loaded")

    @commands.command()
    async def test(self, ctx):
        await ctx.send("This command is used to check the functionality of the load and unload\nfeature for command extensions.")
    
    
# sends the commands
def setup(client):
    client.add_cog(test(client))