import discord
from discord.ext import commands
from asyncio import sleep

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

logs_channel_id = 1114231080556433458  # Replace YOUR_LOGS_CHANNEL_ID with the ID of your desired logs channel

@bot.event
async def on_ready():
    await change_streaming_status()
    print(f'Bot is ready and logged in as {bot.user}')

async def change_streaming_status():
    status_names = ['BRS ON TOP✨', 'DIMA BRS']
    while True:
        await bot.change_presence(activity=discord.Streaming(name=status_names[0], url='https://www.twitch.tv/BRSONTOP'))
        await sleep(30)  # Change the duration (in seconds) for the first streaming status
        await bot.change_presence(activity=discord.Streaming(name=status_names[1], url='https://www.twitch.tv/BRSONTOP'))
        await sleep(5)  # Change the duration (in seconds) for the second streaming status

@bot.command()
@commands.has_role(1107780235539271730)  # Replace with the role ID or mention of the specified role
async def assign(ctx, member: discord.Member, role: discord.Role):
    specified_role = discord.utils.get(ctx.guild.roles, id=1107780235539271730)
    
    if role.position >= specified_role.position:
        await ctx.send("You can't give this role.")
        return
    
    if role.position >= ctx.author.top_role.position:
        await ctx.send('You do not have permission to assign this role.')
        return

    if role in member.roles:
        await ctx.send(f'{member.mention} already has the {role.name} role.')
    else:
        await member.add_roles(role)
        await ctx.send(f'{member.mention} has been given the {role.name} role.')
        await log_action(ctx.guild, ctx.author, member, f'assigned the {role.name} role')

@bot.command()
@commands.has_role(1107780235539271730)  # Replace with the role ID or mention of the specified role
async def remove(ctx, member: discord.Member, role: discord.Role):
    specified_role = discord.utils.get(ctx.guild.roles, id=1107780235539271730)
    
    if role.position >= specified_role.position:
        await ctx.send("You can't remove this role.")
        return
    
    if role.position >= ctx.author.top_role.position:
        await ctx.send('You do not have permission to remove this role.')
        return

    if role not in member.roles:
        await ctx.send(f'{member.mention} does not have the {role.name} role.')
    else:
        await member.remove_roles(role)
        await ctx.send(f'{member.mention} has had the {role.name} role removed.')
        await log_action(ctx.guild, ctx.author, member, f'removed the {role.name} role')

async def log_action(guild, author, member, action):
    logs_channel = guild.get_channel(logs_channel_id)
    if logs_channel:
        message = f'{author.mention} has {action} from {member.mention}.'
        await logs_channel.send(message)

@bot.command()
async def customhelp(ctx):
    embed = discord.Embed(title='Bot Commands', description='List of available commands:')
    embed.add_field(name='!assign <member> <role>', value='Assign a role to a member', inline=False)
    embed.add_field(name='!remove <member> <role>', value='Remove a role from a member', inline=False)
    await ctx.send(embed=embed)
