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
    # Split members string into a list
    members_list = members.split(",")
    # Create a formatted string with each member on a separate line
    members_str = "\n".join(members_list)
    
    embed = discord.Embed(title=f"{name} Project Submission", description=f"`{description}`", color=0x38DE4C)
    embed.add_field(name="Team Members", value=members_str, inline=False)
    embed.add_field(name="GitHub Link", value=f"[{link}]({link})", inline=False)
    embed.set_footer(text="Thanks for submitting! Administrators will get to your submission shortly.")
    
    # Send the embed to the interaction channel
    await interaction.response.send_message(embed=embed)
    
    # Send a notification to the submissions channel
    channel = bot.get_channel(1049411277434388493)
    role = channel.guild.get_role(1049411275735695402)

    embed = discord.Embed(title=f"{name} Project Submission", description=f"{name} has posted their project submission in <#{interaction.channel_id}>. Please check the description for approval.", color=0x7289da)

    await channel.send(role.mention, embed=embed)


# @bot.tree.command(name='approve')
# @commands.has_role('Administrator')
# @app_commands.describe(name="Provide the team name.")
# async def approve(interaction: discord.Interaction, name: str):
#     print("Inside approve function.")
#     submissions_channel = bot.get_channel(1078018927877169204)
#     async for embed in submissions_channel.history():
#         if embed.author == bot.user:
#             continue
#         if len(embed.embeds) > 0:
#             embed = embed.embeds[0]
#             print(f"Checking embed with title: {embed.title}")
#             if name in embed.title:
#                 print("Found matching submission.")
#                 team_members = embed.fields[0].value.replace('**Team Members:** ', '').split('\n')
#                 team_mention = ' '.join([f"<@{member.split(' ')[-1]}>" for member in team_members])
#                 approved_embed = discord.Embed(title=f"`{name} Project Approved!`", color=0x38DE4C)
#                 approved_embed.add_field(name="Team Members", value=embed.fields[0].value, inline=False)
#                 approved_embed.add_field(name="Project Description", value=embed.fields[1].value, inline=False)
#                     continue
#                 approved_embed.add_field(name="Project Link", value=embed.fields[2].value, inline=False)
#                 approved_embed.set_footer(text="Congratulations! Your project has been approved.")
#                 await interaction.response.send_message(embed=approved_embed)
#                 message = f"Project submission by {name} has been approved! {team_mention}"
#                 approval_channel = bot.get_channel(1078004744137756703)
#                 await approval_channel.send(message)
#                 return
#     print("No matching submission found.")
#     await interaction.response.send_message(f"No project submission found with the name {name}")

@bot.tree.command(name="ping")
async def ping(interaction: discord.Interaction):
    # send a message to the user
    await interaction.response.send_message("Pong!")

bot.run(TOKEN)