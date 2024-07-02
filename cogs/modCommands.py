import discord
from discord.ext import commands
from discord.ext.commands.core import command
from discord.utils import get
import json

class modCommands(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("> modderator Cog is Loaded")
    
    
    # cleares the channel the comand was called in if the user has requierd permissions
    @commands.command(aliases =["delete", "c", "purge"])
    @commands.has_permissions(manage_messages = True)
    async def clear(self, ctx, amount = 20):
        if amount <= 0:
            await ctx.send("I cant delete 0 messages! :man_facepalming:")
            
        elif amount >= 1 and amount <= 1000:
            await ctx.channel.purge(limit = amount + 1)
            
        else:
            await ctx.send("I cant delete that amount off messages.\nMy range is 1 to 1000 messages.")


    # bans user if permisions are correct and the botts role is above the users role
    @commands.command(aliases =["Ban", "b", "banuser"])
    @commands.has_permissions(ban_members = True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        await member.ban(reason=reason)
        await ctx.send(f'User {member.mention} has been banned')



    # kicks user if permisions are correct and the botts role is above the users role
    @commands.command(aliases =["Kick", "k", "kickuser", "remove"])
    @commands.has_permissions(kick_members = True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        await member.kick(reason = reason)
        await ctx.send(f'User {member.mention} has been kicked')
    


    # allows user to unban users if permissions are correct and the botts role is above the users role
    @commands.command(aliases =["Unban"])
    @commands.has_permissions(administrator = True)
    async def unban(self, ctx, *, member):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split("#")
        
        for ban_entry in banned_users:
            user = ban_entry.user
            
        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'Unbanned {user.mention}')
            return

    # adds role to user
    @commands.command(aliases = ["adrole"])
    @commands.has_permissions(manage_roles = True)   
    async def addrole(self, ctx, role: discord.Role, user: discord.Member):
        await ctx.send(f"Loading ...")
        await user.add_roles(role)
        await ctx.send(f"sucsesfuly gave {role.mention} to {user.mention}")

        # example .adrole @Members @Eva | Security | Pvt | 🇬🇧


    # adds role to user
    @commands.command(aliases = ["rmrole"])
    @commands.has_permissions(manage_roles = True)   
    async def removerole(self, ctx, role: discord.Role, user: discord.Member):
        await ctx.send(f"Loading ...")
        await user.remove_roles(role)
        await ctx.send(f"sucsesfuly removed {role.mention} from {user.mention}")

        # example .rmrole @PPSO Crt * 1 @Eva | Security | Pvt | 🇬🇧

    # mutes member
    # https://github.com/JacobA2000/Discord-Bot-Tutorial/blob/master/Episode%209/tutorial.py
    @commands.command(aliases = ["Mute"])
    @commands.has_permissions(manage_roles=True)
    async def mute(self, ctx, member: discord.Member, *, reason=None):
        guild = ctx.guild
        mutedRole = discord.utils.get(guild.roles, name="AMuted")
        

        if not mutedRole:
            permissionsList = discord.Permissions.none()
            permissionsList.send_messages=False
            permissionsList.speak=False
            mutedRole = await guild.create_role(name="AMuted", hoist = True, permissions = permissionsList)
            

            for channel in guild.channels:
                await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_message_history=True, read_messages=False)

        
        await member.add_roles(mutedRole, reason=reason)
        
        await ctx.send(f"{member.mention} has been muted by {ctx.author} for reason {reason}")
        
        await member.send(f"You were muted in the server {guild.name} by {ctx.author} for {reason}")

    # Unmutes Members
    # https://github.com/JacobA2000/Discord-Bot-Tutorial/blob/master/Episode%209/tutorial.py
    @commands.command(aliases = ["Unmute", "unMute", "UnMute"])
    @commands.has_permissions(manage_roles=True)
    async def unmute(self, ctx, member: discord.Member):
        mutedRole = discord.utils.get(ctx.guild.roles, name="AMuted")

        await member.remove_roles(mutedRole)
        await ctx.send(f"{member.mention} was unmuted")
        await member.send(f"You were unmuted in the server {ctx.guild.name} by {ctx.author}")

    # Removes the targets ability to send messages, see messages and connect to vcs
    @commands.command(aliases = ["Quarantine", "DQ"])
    @commands.has_permissions(manage_roles=True)
    async def quarantine(self, ctx, target: discord.Member, *, reason=None):
        guild = ctx.guild
        quarantineRole = discord.utils.get(guild.roles, name="Quarantine")
        

        if not quarantineRole:
            permissionsList = discord.Permissions.none()
            permissionsList.view_channel=False
            permissionsList.send_messages=False
            permissionsList.speak=False
            mutedRole = await guild.create_role(name="Quarantine", hoist = True, permissions = permissionsList)
            

            for channel in guild.channels:
                await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_message_history=True, read_messages=False, view_channel = False)

        for role in target.roles:
            try:
                await target.remove_roles(role)
            except Exception as e:
                print(e)

        await target.add_roles(quarantineRole, reason=reason)

        
        await ctx.send(f"{target.mention} has been quarantined by {ctx.author} for reason {reason}")
        
        await target.send(f"You were quarantined in the server {guild.name} by {ctx.author} for {reason}")

    @commands.command(aliases = ["Unquarantine", "UQ"])
    @commands.has_permissions(manage_roles=True)
    async def unquarantine(self, ctx, target: discord.Member):
        mutedRole = discord.utils.get(ctx.guild.roles, name="Quarantine")

        await target.remove_roles(mutedRole)
        await ctx.send(f"{target.mention} was unquarantined")
        await target.send(f"You were unquarantined in the server {ctx.guild.name} by {ctx.author}")

    @commands.command(aliases = ["whoIs", "WhoIs"])
    async def who(self, ctx, victim: discord.Member):
        joinTime = victim.joined_at.date()
        print(f"> User Action - joined at command used by {ctx.author} on {victim}")

        roleList = []
        for role in victim.roles:
            if role.name != "@everyone":
                roleList.append(role.mention)

        b = ",".join(roleList)

        whoIsEmbed = discord.Embed(
            title = "User Info",
            description = f"Find out details about {victim} from {ctx.guild}",
            color = discord.Color.random()
        )

        whoIsEmbed.add_field(name="Details", value=f"User - {victim} Joined at - {joinTime}", inline=False)
        whoIsEmbed.add_field(name="ID:", value=f"{victim.id}", inline=False)
        whoIsEmbed.add_field(name="Name:", value=f"{victim.display_name}", inline=False)
        whoIsEmbed.add_field(name="Created At:", value=f"{victim.created_at}", inline=False)
        whoIsEmbed.add_field(name="Joined at:", value=f"{victim.joined_at}", inline=False)
        whoIsEmbed.add_field(name=f"Roles: ({len(roleList)})", value=f"".join([b]), inline=False)
        whoIsEmbed.add_field(name="Top role: ", value=f"{victim.top_role.mention}")
        whoIsEmbed.add_field(name="Bot account?:", value=f"{victim.bot}", inline=False)
        whoIsEmbed.set_thumbnail(url=f"{victim.avatar_url}")
        whoIsEmbed.set_footer(text=f"Requested by - {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed = whoIsEmbed)

    # sends users pfp to chat
    @commands.command()
    async def pfp(self, ctx, victim: discord.Member):

        await ctx.send(f"{victim.avatar_url}")

# sends the commands
def setup(client):
    client.add_cog(modCommands(client))