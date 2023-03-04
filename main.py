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

@bot.tree.command(name='submit')
@app_commands.describe(name="Provide the team name.", members="Provide list of members with name and Discord ID separated by commas.", description="Provide a brief description of your project.", link="Provide a GitHub link to your project.")
async def submit(interaction: discord.Interaction, name: str, members: str, description: str, link: str):
    members_list = members.split(",")
    members_str = "\n".join(members_list)
    
    embed = discord.Embed(title=f"{name} Project Submission", description=f"`{description}`", color=0x7289da)
    embed.add_field(name="Team Members", value=members_str, inline=False)
    embed.add_field(name="GitHub Link", value=f"[{link}]({link})", inline=False)
    embed.set_footer(text="Thanks for submitting! Administrators will get to your submission shortly.")
    
    await interaction.response.send_message(embed=embed)
    channel = bot.get_channel(1077647771059888241)
    message = f"{name} has posted their project submission in <#{interaction.channel_id}>.\nPlease check the description for approval.\nMembers: {members_str}"
    role = channel.guild.get_role(1049411275735695402)
    await channel.send(f"{role} {message}")

@bot.tree.command(name="help")
async def help(interaction: discord.Interaction):
    embed = discord.Embed(title="Help", description="This is a list of commands you can use in the bot.", color=0x7289da)
    embed.add_field(name="/submit", value="Use this command to submit your project. You will be prompted to provide the team name, list of members, a brief description of your project, and a GitHub link to your project.", inline=False)
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="ping")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("Pong!")

bot.run(TOKEN)
