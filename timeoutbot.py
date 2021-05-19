"""Time Out Bot

This is a Discord bot that gives an admin (specified by the variable ADMIN) the
ability to put members in timeout. The member is moved to a channel named by
TIMEOUT_CHANNEL. To run, you'll also need to grab your Token, guild name, and
text channel you want the bot to communicate in. These variables will go in a
file '.env'. Follow https://realpython.com/how-to-make-a-discord-bot-python/
for an example.

Author:
    Justin Spidell <justintspidell@gmail.com>

Functions:

    on_ready
    timeout
    quote
"""
import os
import discord
from discord.ext import commands
from discord.ext.commands.errors import MemberNotFound
from discord.errors import HTTPException
from dotenv import load_dotenv
import random
import asyncio


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
TEXT_CHANNEL = os.getenv('DISCORD_CHANNEL')
client = discord.Client()
client = commands.Bot(command_prefix='-')

ADMIN = "justin"
TIMEOUT_CHANNEL = "Timeout"


@client.event
async def on_ready():
    """
    This function prints some info when the bot is booted.

        Parameters:
            None

        Returns:
            None
    """
    guild = discord.utils.get(client.guilds, name=GUILD)
    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'

    )


@client.command(name='timeout', help='Puts a member in timeout')
async def timeout(ctx, member=None, minutes=None):
    """
    This function moves a member from a voice channel to the channel specified
    by TIMEOUT_CHANNEL. It server mutes and server deafens the user for the
    given amount of time.

        Parameters:
            member (str): The Discord id or nickname of the member to be put in
                timeout
            minutes (str): The amount of time put the user into timeout for

        Returns:
            Sends a response to the channel specified by DISCORD_CHANNEL
    """
    if member is None or minutes is None:
        response = "I need a Member and a # of minutes to work :("
    else:
        guild = discord.utils.get(client.guilds, name=GUILD)
        _channel = discord.utils.get(guild.voice_channels,
                                     name=TIMEOUT_CHANNEL)

        _admin = await commands.converter.MemberConverter().convert(ctx, ADMIN)

        if _admin == ctx.author:
            try:
                _member = await commands.converter.MemberConverter().convert(
                    ctx, member)

                try:
                    _old_channel = _member.voice.channel
                except AttributeError:
                    _old_channel = ""

                try:
                    await _member.edit(voice_channel=_channel,
                                       mute=True,
                                       deafen=True,
                                       reason="They were very naughty")
                    response = str(f"I put {member} in timeout for {minutes} "
                                   "minutes")
                    await ctx.send(response)
                    await asyncio.sleep(int(int(minutes) * 60))
                    await _member.edit(voice_channel=_old_channel,
                                       mute=False, deafen=False)
                    response = f"{member} is out of timeout"
                    await ctx.send(response)

                except HTTPException:
                    response = "User is not connected to voice"
                    await ctx.send(response)

            except MemberNotFound:
                response = f"I couldn't not find {member}"
                await ctx.send(response)
        else:
            response = str("Sorry, you don't have the power to put someone in"
                           " timeout")
            await ctx.send(response)


@client.command(name='quote', help='Spits back a random quote')
async def quote(ctx):
    """
    Spits back a random quote

        Parameters:
            None

        Returns:
            Sends a response quote to the channel specified by DISCORD_CHANNEL
    """
    quotes = ["i kinda just want fat pussy",
              "if i can't ride, whats the point at all",
              "Did you just say butt chad??", "the barble",
              "jarod sorum was a pump and dump scheme",
              "i'm gonna funnel you money till you get fat pussy",
              "you miss all the shots you take",
              str("honestly, i'd let thanos destroy half the population, i "
                  "like my chances"),
              "michael, don't make me put you on the leash for that",
              "les mis the movie is ass on a fucking tricycle",
              "It is such a nut when you cut it off in the right spot",
              str("i grew up an only child in the suburban neighborhood of sex"
                  " mountain"),
              "'what's your sex' 'idk doggy style maybe'",
              "I was pissing really hard, trying to push it out",
              "I eat indians"]

    response = random.choice(quotes)
    await ctx.send(response)


client.run(TOKEN)
