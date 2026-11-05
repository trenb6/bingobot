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

        self.challenges = challenges

        # Each challenge stores the Discord users who completed it.
        # Format: {challenge_index: {user_id: display_name}}
        self.completed = {
            i: {} for i in range(len(challenges))
        }

        for i, challenge in enumerate(challenges):
            button = discord.ui.Button(
                label=self.button_label(i),
                style=discord.ButtonStyle.secondary,
                row=i // 5
            )

            button.callback = self.create_callback(i)
            self.add_item(button)

    def button_label(self, index):
        challenge = self.challenges[index]
        count = len(self.completed[index])

        # Discord button labels have an 80-character limit.
        short_challenge = challenge
        if len(short_challenge) > 55:
            short_challenge = short_challenge[:52] + "..."

        return f"{count} done | {short_challenge}"

    def create_callback(self, index):

        async def callback(interaction: discord.Interaction):
            user_id = interaction.user.id

            # If the user has already completed it, undo their completion.
            if user_id in self.completed[index]:
                del self.completed[index][user_id]
            else:
                self.completed[index][user_id] = (
                    interaction.user.display_name
                )

            # Update the button label and colour.
            button = self.children[index]
            button.label = self.button_label(index)

            if self.completed[index]:
                button.style = discord.ButtonStyle.success
            else:
                button.style = discord.ButtonStyle.secondary

            # Update the embed and buttons for everyone.
            await interaction.response.edit_message(
                embed=self.create_embed(),
                view=self
            )

        return callback

    def create_embed(self):
        embed = discord.Embed(
            title="Challenge Bingo",
            description="Click a challenge when you complete it. "
                        "Click again to undo your completion.",
            color=discord.Color.blue()
        )

        for i, challenge in enumerate(self.challenges):
            users = self.completed[i]

            if users:
                completed_by = ", ".join(users.values())
                status = f"✅ {len(users)} completed: {completed_by}"
            else:
                status = "⬜ Nobody has completed this yet"

            embed.add_field(
                name=f"{i + 1}. {challenge}",
                value=status,
                inline=False
            )

        return embed


@client.command(name='bingo')
async def bingo(ctx):
    players_list = ['emma', 'gerard', 'tren', 'tim', 'wessel']

    challenges = challenge_updated.large_bingo_draw(
        players_list,
        len(players_list)
    )

    view = BingoCard(challenges)

    await ctx.send(
        embed=view.create_embed(),
        view=view
    )

client.run(TOKEN)