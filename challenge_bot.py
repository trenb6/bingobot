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
        await ctx.send('GOOD LUCK HAVE FUN! :D')
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
        await ctx.send('GOOD LUCK HAVE FUN! :D')
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
        await ctx.send('GOOD LUCK HAVE FUN! :D')
    except:
        await ctx.send("Please gives names separated by commas, example: !small_bingo_draw tren,tim,wessel")

@client.command(name='reroll_challenge', help='Rerolls a challenge based on input number')
async def reroll_challenge(ctx, challenge_number: int):

    async for message in ctx.channel.history(limit=50):

        if message.author == client.user and message.content.startswith(f"{challenge_number}."):

            challenge_type = message.content.split('. ', 1)[1].split(': ', 1)[0]

            try:
                new_challenge = challenge_updated.draw_one_challenge(challenge_type)

                await message.edit(
                    content=f"{challenge_number}. {new_challenge}"
                )

                await ctx.message.add_reaction("✅")
                # await ctx.send(f"Challenge number {challenge_number} has been rerolled to: {new_challenge}")


            except ValueError as e:
                await ctx.send(str(e))

            return

    await ctx.send(f"Challenge number {challenge_number} not found in the last 50 messages.")

import discord

class BingoCard(discord.ui.View):

    def __init__(self, challenges):
        super().__init__(timeout=None)

        self.completed = set()
        self.challenges = challenges

        for i, challenge in enumerate(challenges):
            button = discord.ui.Button(
                label=f"{i + 1}",
                style=discord.ButtonStyle.secondary,
                row=i // 5
            )

            button.callback = self.create_callback(i)
            self.add_item(button)

    def create_callback(self, index):

        async def callback(interaction: discord.Interaction):

            if index in self.completed:
                self.completed.remove(index)
                self.children[index].style = discord.ButtonStyle.secondary

            else:
                self.completed.add(index)
                self.children[index].style = discord.ButtonStyle.success

            await interaction.response.edit_message(view=self)

        return callback

@client.command(name='bingo')
async def bingo(ctx):

    players_list = ['emma', 'gerard', 'tren', 'tim', 'wessel']

    challenges = challenge_updated.large_bingo_draw(
        players_list,
        len(players_list)
    )

    view = BingoCard(challenges)

    embed = discord.Embed(
        title="Challenge Bingo",
        description="Click a challenge when it has been completed!",
        color=discord.Color.blue()
    )

    for i, challenge in enumerate(challenges):
        embed.add_field(
            name=f"{i + 1}.",
            value=challenge,
            inline=True
        )

    await ctx.send(embed=embed, view=view)
            
client.run(TOKEN)