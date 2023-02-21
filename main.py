import discord
from discord import app_commands
from discord.ext import commands
from config import TOKEN

bot = commands.Bot(command_prefix='!', intents = discord.Intents.all())

@bot.event
async def on_ready():
    print('Bot is ready')
    try: 
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)

@bot.tree.command(name="hello")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f"Hey {interaction.user.mention}! This is a slash command!", ephemeral=True)

@bot.tree.command(name="say")
@app_commands.describe(arg = "What should I say?")
async def say(interaction: discord.Interaction, arg: str):
    await interaction.response.send_message(f"{interaction.user.name} said: `{arg}`")

# become funny
@bot.tree.command(name="become")
@app_commands.describe(arg = "What should I become?")
async def become(interaction: discord.Interaction, arg: str):
    await interaction.response.send_message(f"{interaction.user.name} became: `{arg}`")
    

# create a slash command to ping itself
@bot.tree.command(name="ping")
async def ping(interaction: discord.Interaction):
    # send a message to the user
    await interaction.response.send_message("Pong!")

#create a slash command to incrememnt a counter
counter = 0
@bot.tree.command(name="counter")
async def counter(interaction: discord.Interaction):
    global counter
    counter += 1
    await interaction.response.send_message(f"Counter: {counter}")

bot.run(TOKEN)