import discord
import aiosqlite
import time
import random
import string
from discord import Emoji, PartialEmoji
from datetime import datetime
from discord.ext import commands


class Feedback(commands.Cog, name="Feedback"):
    """Submit feedback"""

    def __init__(self, client):
        self.client = client

    @commands.group(invoke_without_command=True, aliases=['suggest', 'fb', 'idea'])
    async def feedback(self, ctx):
        pass

    @feedback.command()
    @commands.cooldown(1, 1800, type=commands.BucketType.user)
    async def new(self, ctx, *, content):
        ": Create a new idea"
        db = await aiosqlite.connect('marvin.db')
        cursor = await db.cursor()
        try:
            idea_id = ''.join(random.SystemRandom().choice(
                string.ascii_uppercase + string.digits) for _ in range(6))
            created = int(datetime.utcnow().timestamp())
            sql = (
                'INSERT INTO feedback(idea_id, author, content, created) VALUES(?,?,?,?)')
            val = (idea_id, str(ctx.message.author.id), str(content), created)
            await cursor.execute(sql, val)
            await db.commit()
        except:
            idea_id = ''.join(random.SystemRandom().choice(
                string.ascii_uppercase + string.digits) for _ in range(6))
            created = int(datetime.utcnow().timestamp())
            sql = (
                'INSERT INTO feedback(idea_id, author, content, created) VALUES(?,?,?,?)')
            val = (idea_id, str(ctx.message.author.id), str(content), created)
            await cursor.execute(sql, val)
            await db.commit()

        embed = discord.Embed(colour=0x74ff90, description=f"{content}")
        embed.set_author(
            name=f"Feedback by {ctx.message.author.name}#{ctx.message.author.discriminator}  | {idea_id}", icon_url=f"{ctx.message.author.avatar_url}")
        embed.add_field(name="No Response", value="N/A")
        embed.timestamp = datetime.utcnow()
        embed.set_footer(text="Marvin", icon_url=f'{self.client.user.avatar_url}')

        sql = ('SELECT feedback_channel FROM guilds WHERE guild_id = ?')
        val = (str(610914837039677471),)
        await cursor.execute(sql, val)

        channel_id = await cursor.fetchone()
        channel = self.client.get_channel(int(channel_id[0]))
        feedback_message = await channel.send(embed=embed)
        print(feedback_message, feedback_message.id, idea_id)

        sql = ('UPDATE feedback SET message_id = ? WHERE idea_id = ?')
        val = (str(feedback_message.id), str(idea_id))
        await cursor.execute(sql, val)
        await db.commit()
        await cursor.close()
        await db.close()

        await feedback_message.add_reaction('⬇️')
        await feedback_message.add_reaction('⬆️')
        await ctx.message.delete()

    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    @feedback.command()
    async def setchannel(self, ctx):
        ": Sets the channel feedback is sent to"
        db = await aiosqlite.connect('marvin.db')
        cursor = await db.cursor()
        sql = ('UPDATE guilds SET feedback_channel = ? WHERE guild_id = ?')
        val = (str(ctx.channel.id), str(ctx.guild.id))
        await cursor.execute(sql, val)
        await db.commit()
        await cursor.close()
        await db.close()


def setup(client):
    client.add_cog(Feedback(client))
    print('@COG: Feedback Cog loaded \n---------------------')