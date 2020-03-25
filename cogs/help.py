import discord
from datetime import datetime
from discord.ext import commands

class Help(commands.Cog, name="help"):
    """Help me!"""
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def help(self, ctx):
        embed = discord.Embed(colour=0x74ff90,
                              description="[] = required argument\n<> = optional argument\nThe `|` means you can use either word for the command.\nFor example to submit a ticket you can use `m.ticket` **or** `m.report`,\nwhich is shown below using `|`.", icon_url="https: // i.imgur.com/aCkiWNY.png")
        embed.set_author(name="InfinityCraft 2.∞ Discord Help", icon_url="https://i.imgur.com/aCkiWNY.png")
        embed.add_field(name="**Ticket Help**",
                        value="`m.ticket|report new [content]` - Create a new ticket or report.\n**Please submit tickets and reports in a direct message to Marvin.**", inline=False)
        embed.add_field(name="**Server Info Help**",
                        value="`m.server status` - Displays whether the server is online with player count.\n`m.server ip` - Displays the server IP.\n`m.rules` - List the Discord and Minecraft Server rules.", inline=False)
        embed.add_field(name="Other Help",
                        value="`m.mojang` - Check the status of Mojang & Minecraft services.", inline=False)
        embed.timestamp = datetime.utcnow()
        embed.set_footer(
            text="Marvin", icon_url=f'{self.client.user.avatar_url}')
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Help(client))
    print('@COG: Help Cog loaded \n---------------------')