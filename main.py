import discord
from discord import app_commands
from discord.ext import commands
from config import TOKEN

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

@bot.event
async def on_ready():
    print('Bot is ready')
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)

@bot.tree.command(name='project')
@app_commands.describe(name="Provide the team name.", members="Provide list of members with name and Discord ID separated by commas.", description="Provide a brief description of your project.", link="Provide a GitHub link to your project.")
async def project(interaction: discord.Interaction, name: str, members: str, description: str, link: str):
    embed = discord.Embed(title=f"`{name} Project Submission`", color=0x38DE4C)
    embed.add_field(name="Team Members", value=members.replace(",","\n"), inline=False)
    embed.add_field(name="Project Description", value=f"{description}", inline=False)
    embed.add_field(name="Project Link", value=link, inline=False)
    embed.set_footer(text="Thanks for submitting!")
    await interaction.response.send_message(embed=embed)

    channel = bot.get_channel(1049411277434388493)
    
    message = f"{name} has posted their project submission in <#{interaction.channel_id}>, please check the description for approval."
    
    role = channel.guild.get_role(1049411275735695402)
    
    await channel.send(f"{role.mention} {message}")




#recreate the above command but make the output look nice, have the team member names on different lines, the description on a new line, etc, just make it look cool

@bot.tree.command(name="ping")
async def ping(interaction: discord.Interaction):
    # send a message to the user
    await interaction.response.send_message("Pong!")

bot.run(TOKEN)