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
    members_str = "\n".join(members_list)
    
    embed = discord.Embed(title=f"{name} Project Submission", description=f"`{description}`", color=0x7289da)
    embed.add_field(name="Team Members", value=members_str, inline=False)
    embed.add_field(name="GitHub Link", value=f"[{link}]({link})", inline=False)
    embed.set_footer(text="Thanks for submitting! Administrators will get to your submission shortly.")
    
    await interaction.response.send_message(embed=embed)
    channel = bot.get_channel(1049411277434388493)
    
    message = f"{name} has posted their project submission in <#{interaction.channel_id}>.\nPlease check the description for approval.\nMembers: {members_str}"
    
    role = channel.guild.get_role(1049411275735695402)
    
    await channel.send(f"{message}")

@bot.tree.command(name='approve')
@commands.has_role('Administrator')
@app_commands.describe(name="Provide the team name.")
async def approve(interaction: discord.Interaction, name: str):
    check_channel_id = 1049411277434388493
    check_channel = bot.get_channel(check_channel_id)
    approval_channel_id = 1078004744137756703
    approval_channel = bot.get_channel(approval_channel_id)

    async for message in check_channel.history():
        if message.author.bot and name in message.content:
            members_str = message.content.split('\n')[1]
            members = [member.strip() for member in members_str.split(',')]
            mentions = message.mentions
            mention_str = ' '.join(f'<@{m}>' for m in mentions)

            approval_message = f"{mention_str}"
            approval_embed = discord.Embed(title=f"{name} Project Approved", description=f"Your project has been approved by <@{interaction.user.id}>!", color=0x84eb80)
            await approval_channel.send(content=approval_message, embed=approval_embed)
            await interaction.response.send_message(f"Approved {name} project submission.")
            return

    await interaction.response.send_message(f"Could not find submission for {name}.")

@bot.tree.command(name='reject')
@commands.has_role('Administrator')
@app_commands.describe(name="Provide the team name and a reason for the rejection.")
async def reject_submission(interaction: discord.Interaction, name: str, reason: str):
    check_channel_id = 1049411277434388493
    check_channel = bot.get_channel(check_channel_id)
    rejection_channel_id = 1078004744137756703
    rejection_channel = bot.get_channel(rejection_channel_id)

    async for message in check_channel.history():
        if message.author.bot and name in message.content:
            members_str = message.content.split('\n')[1]
            members = [member.strip() for member in members_str.split(',')]
            mentions = message.mentions
            mention_str = ' '.join(f'<@{m}>' for m in mentions)

            rejection_message = f"{mention_str}"
            rejection_embed = discord.Embed(title=f"{name} Project Rejected", description=f"Your project has been rejected by <@{interaction.user.id}> for the following reason:\n\n{reason}\n\nPlease see the feedback and feel free to submit a revised version.", color=0xE84E4E)
            await rejection_channel.send(content=rejection_message, embed=rejection_embed)
            await interaction.response.send_message(f"Rejected {name} project submission with reason: {reason}.")
            return

    await interaction.response.send_message(f"Could not find submission for {name}.")


@bot.tree.command(name="ping")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("Pong!")

bot.run(TOKEN)