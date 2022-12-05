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

@bot.tree.command(name="hey")
@app_commands.describe(arg = "What should I say?")
async def say(interaction: discord.Interaction, arg: str):
    await interaction.response.send_message(f"{interaction.user.name} said: `{arg}`")

# create a slash command to increment a counter by 1 when using the command count
@bot.tree.command(name="yeayea")
async def count(interaction: discord.Interaction):
    # get the counter value from the interaction
    counter = interaction.data.get("options", {}).get("counter", 0)
    # increment the counter by 1
    counter += 1
    # send the new counter value
    await interaction.response.send_message(f"Counter: {counter}")


bot.run(TOKEN)