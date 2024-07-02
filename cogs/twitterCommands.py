import discord
from discord.ext import commands
import tweepy
import os
from dotenv import load_dotenv


# handles logging in and posting of the tweets
def tweetfunc(message: str, image_path=None, poster = None):
    # issue here was that the async loop of discord constantly logged into the api so limiting the login to once per system loggin fix the issue
    track = 0
    while track == 0:
        try:
            # new 
            load_dotenv()
            api_key = os.getenv('APIKEY')
            api_secret = os.getenv('APISECRET')
            bearer_token_= os.getenv('BEARERTOKEN')
            access_token = os.getenv('ACCESSTOKEN')
            access_token_secret = os.getenv('ACCESSTOKENSECRET')

            auth = tweepy.OAuthHandler(api_key, api_secret)
            auth.set_access_token(access_token, access_token_secret)
            api = tweepy.API(auth)

        except Exception as e:
            print(e)
        track = 1
        print("> System Event: Twitter API Loggin success")
    
    print("Flag 1: breaks loop")

    post = (f"{message} posted from discord by {poster}")
    
    # tweets
    api.update_status(post, possibly_sensitive = False)
    print(f"> User Action: Tweet -- {message} -- by {poster}")

class twitterCommands(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    # makes the bot ready to take cog commands
    @commands.Cog.listener()
    async def on_ready(self):
        print("> twitter Cog is loaded")

    # handles the command activation of the tweet command
    @commands.command()
    @commands.has_guild_permissions(administrator = True)
    async def tweet(self, ctx, *, msg):
        tweetfunc(msg, poster = ctx.author)
        await ctx.send(f"If all goes well \"{msg}\" should be tweeted soon.\n check it out at https://twitter.com/AwackTeam.")

# sends the commands
def setup(client):
    client.add_cog(twitterCommands(client))
    