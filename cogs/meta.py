import discord
import datetime
import aiosqlite
from discord.ext import commands


class Meta(commands.Cog, name="meta"):

    def __init__(self, client):
        self.client = client

    @commands.command(hidden=True, aliases=['kill', 'stop'])
    @commands.is_owner()
    async def kill_bot(self, ctx):
        ": Shuts down the bot on the server"
        await ctx.send('Shutting down...')
        await ctx.send('Goodbye')
        await self.client.logout()

    @commands.command()
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def ping(self, ctx, ping=None):
        ": Check latency to Marvin"
        if not ping:
            await ctx.send(f'Pong! Latency to Marvin: `{round(self.client.latency * 1000)}ms`')
        else:
            await ctx.send('no ping for you')

    @commands.command(hidden=True)
    @commands.is_owner()
    async def addguild(self, ctx):
        ": Adds guild to db !Should not need to use!"
        db = await aiosqlite.connect('marvin.db')
        cursor = await db.cursor()
        sql = ('INSERT INTO guilds(guild_id, guild_owner) VALUES(?,?)')
        val = (str(ctx.guild.id), str(ctx.guild.owner.id))
        await cursor.execute(sql, val)
        await db.commit()
        await cursor.close()
        await db.close()

    @commands.command(hidden=True)
    async def support(self, ctx):
        pass

    @commands.command(hidden=True)
    async def guildowner(self, ctx):
        ": displays the current owner of the current guild"
        guild_owner = ctx.guild.owner
        await ctx.send(guild_owner)

    @commands.command()
    async def welcomemessage(self, ctx):
        join_message = """:small_orange_diamond: Welcome to InfinityCraft 2.∞! If you need help make sure to check out the #help channel or run the command `m.help` to get Marvin(me) to give you command help within the server. 
:small_orange_diamond: I may take some time to respond to your command so please be patient. I am a cactus after all. 
:small_blue_diamond: Make sure to run the command `/discord link` in Minecraft to link your Minecraft and Discord account and follow the directions given. You should get the Voyager rank as well as some other perks. 
:small_blue_diamond: To submit a report or ticket, check out the #ticket channel. 
:small_blue_diamond: Last of all, make sure to follow all the rules posted in the #rules channel. 
:small_blue_diamond: If you have any further questions, feel free to ask a staff member or other members of the community.

Server IP: `mc.gamersgrove.net`
Website: https://infinity.gamersgrove.net/
Discord Invite Link: https://discordapp.com/invite/v67aGnq or https://discord.gamersgrove.net"""
        await ctx.send(join_message)

    @commands.command()
    async def rules(self, ctx):
        ": View the rules of the server"
        embed = discord.Embed(colour=0x74ff90,
                              description="These rules appy both to the Discord, Minecraft, and other InfinityCraft 2.∞ entities unless otherwised stated.\nRules are subject to change without notice. It is up the the player(you) to keep updated with them.")
        embed.set_author(name="InfinityCraft 2.∞ Rules",
                         icon_url="https://i.imgur.com/aCkiWNY.png")
        embed.add_field(name="**Minecraft Server Rules**",
                        value="1. Do not spam the chat\n2. Do not use excessive explicit language towards other players\n3. Do not use derogatory, racist, or otherwise bigoted language\n4. Do not advertise. This includes: servers, websites, etc.. If you have something out would like to post in chat, ask a staff member\n5. Do not cheat in any way, using external mods or ingame exploits is not allowed\n6. Greifing is not allowed, but players are responsible for protecting their own property. See 'Land Calim instructions' using /landclaim\n7. Land Calims must be at least 100 blocks of the nearest person of notice. Except in cases where players have an agreement\n8. Do not create, or use AFK machines. If you are idle, use /afk", inline=False)
        embed.add_field(name="**Discord Rules**",
                        value=f"1. The use of `@everyone` or other rank tagging is strictly forbidden\n2. Do not spam any of the text channels\n3. Do not send direct messages to staff members unless otherwise instructed to, or you will be ignored\n4. Do not ping staff members, your question will eventually be answered. If it is an emegerncy, submit a ticket\n5. Do not post or send pornographic, illegal or other NSFW content\n6. Do not spam or abuse commands provided by {self.client.user.mention}\n\nAny Minecraft Server rules that are relevant, such as excessive explicit language, advertising, etc., apply in the Discord Server as well", inline=False)
        embed.set_footer(
            text="Marvin", icon_url=f'{self.client.user.avatar_url}')
        await ctx.send(embed=embed)

    @commands.command(hidden=True)
    async def rulesnoformat(self, ctx):
        rules_no_format = f"""**Minecraft Server Rules**
1. Do not spam the chat
2. Do not use excessive explicit language towards other players
3. Do not use derogatory, racist, or otherwise bigoted language
4. Do not advertise. This includes: servers, websites, etc.. If you have something out would like to post in chat, ask a staff member
5. Do not cheat in any way, using external mods or ingame exploits is not allowed
6. Greifing is not allowed, but players are responsible for protecting their own property. See 'Land Calim instructions' using /landclaim
7. Land Calims must be at least 100 blocks of the nearest person of notice. Except in cases where players have an agreement
8. Do not create, or use AFK machines. If you are idle, use /afk 

**Discord Server Rules**
1. The use of `@everyone` or other rank tagging is strictly forbidden
2. Do not spam any of the text channels
3. Do not send direct messages to staff members unless otherwise instructed to, or you will be ignored
4. Do not ping staff members, your question will eventually be answered. If it is an emegerncy, submit a ticket
5. Do not post or send pornographic, illegal or other NSFW content
6. Do not spam or abuse commands provided by {self.client.user.mention}

Any Minecraft Server rules that are relevant, such as excessive explicit language, advertising, etc., apply in the Discord Server as well
"""
        await ctx.send(rules_no_format)

    @ping.error
    async def ping_error(self, ctx, error):
        embed = discord.Embed(
            title=f" Try again in {int(error.retry_after)} seconds.", colour=0xd95454)
        embed.set_author(name=f"You are on a cooldown for this command!")
        # time_left = int(error.retry_after//60)
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Meta(client))
    print('@COG: Meta Cog loaded \n---------------------')
