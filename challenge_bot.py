import asyncio
import discord
from discord.ext import commands

import challenge_updated

import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

client = commands.Bot(command_prefix='!', intents=intents)


@client.event
async def on_ready():
    print(f"Logged in as {client.user}")

    if client.guilds:
        server_name = client.guilds[0].name
    else:
        server_name = "Discord"

    activity = discord.Activity(
        name=server_name,
        type=discord.ActivityType.listening
    )

    await client.change_presence(activity=activity)


def parse_players(players_string):
    return [
        player.strip()
        for player in players_string.split(',')
        if player.strip()
    ]


@client.command(name='big_bingo_draw', help='Returns 25 challenges for players x,y,z,etc', )
async def big_bingo_draw(ctx, players_string):
    try:
        players = players_string.split(',')
        number_of_players = len(players)
        challenge_list = challenge_updated.large_bingo_draw(players, number_of_players)
        for i in range(0, len(challenge_list)):
            await ctx.send(str(i+1) + '. ' + challenge_list[i])
            await asyncio.sleep(0.1)
        await ctx.send('GOOD LUCK HAVE FUN!')
    except:
        await ctx.send("Please gives names separated by commas, example: !big_bingo_draw tren,tim,wessel")

@client.command(name='medium_bingo_draw', help='Returns 16 challenges for players x,y,z,etc', )
async def medium_bingo_draw(ctx, players_string):
    try:
        players = players_string.split(',')
        number_of_players = len(players)
        challenge_list = challenge_updated.medium_bingo_draw(players, number_of_players)
        for i in range(0, len(challenge_list)):
            await ctx.send(str(i+1) + '. ' + challenge_list[i])
            await asyncio.sleep(0.1)
        await ctx.send('GOOD LUCK HAVE FUN!')
    except:
        await ctx.send("Please gives names separated by commas, example: !medium_bingo_draw tren,tim,wessel")

@client.command(name='small_bingo_draw', help='Returns 9 challenges for players x,y,z,etc', )
async def small_bingo_draw(ctx, players_string):
    try:
        players = players_string.split(',')
        number_of_players = len(players)
        challenge_list = challenge_updated.small_bingo_draw(players, number_of_players)
        for i in range(0, len(challenge_list)):
            await ctx.send(str(i+1) + '. ' + challenge_list[i])
            await asyncio.sleep(0.1)
        await ctx.send('GOOD LUCK HAVE FUN!')
    except:
        await ctx.send("Please gives names separated by commas, example: !small_bingo_draw tren,tim,wessel")

client.run(TOKEN)