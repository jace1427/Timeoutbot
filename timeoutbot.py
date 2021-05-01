"""Time Out Bot

Author:
    Justin Spidell
"""
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import random


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
TEXT_CHANNEL = os.getenv('DISCORD_CHANNEL')
client = discord.Client()
client = commands.Bot(command_prefix='-')


@client.event
async def on_ready():
    guild = discord.utils.get(client.guilds, name=GUILD)
    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'

    )


@client.command(name='timeout', help='Puts a member in timeout')
async def timeout(ctx, member=None, minutes=None):
    if member is None or minutes is None:
        response = "I need a Member and a # of minutes to work :("
    else:
        guild = discord.utils.get(client.guilds, name=GUILD)

        _channel = discord.utils.get(guild.voice_channels, name="Timeout")
        _member = await commands.converter.MemberConverter().convert(ctx, member)

        print(_member)

        await _member.edit(voice_channel=_channel)
        response = f"{member} has been put in timeout for {minutes} minutes"
        await response


@client.command(name='quote', help='Spits back random quote')
async def quote(ctx):
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
              "I was pissing really hard, trying to push it out"]

    response = random.choice(quotes)
    await ctx.send(response)

client.run(TOKEN)
