import discord, datetime 
from discord.ext import commands
from discord.ui import Button, View

intents = discord.Intents.all()
bot = commands.Bot(command_prefix = ']', intents=intents)

with open("TOKEN.token", "r") as f:
    token = f.readlines()
    
@bot.tree.command(name="findfamiliar")
@discord.app_commands.checks.has_permissions(administrator=True)
async def findfamiliar(interaction: discord.Interaction, user: str = None):
    if not interaction.user.guild_permissions.administrator:
        return await interaction.response.send_message("Nope!")
    similarUsers = []
    if user is None:
        return await interaction.response.send_message("You didn't specify a user.")
    discordServerGuild = bot.get_guild(interaction.guild_id)
    for member in discordServerGuild.members:
        if user.lower() in member.name.lower():
            similarUsers.append(member)

    embed = discord.Embed(title=f"Users with similar names to `{user}` found:", color=0xec0000)
    embed.timestamp = datetime.datetime.now()
    for user in similarUsers:
        embed.add_field(name="", value=user.mention, inline=False)
    
    button = Button(label="Kick listed users", style=discord.ButtonStyle.red, emoji="💥")

    async def button_callback(interaction):
        for user in similarUsers:
            print(f"{user} has been kicked.")
            await user.kick(reason=None)
        await interaction.response.send_message("Users have been kicked.")

    button.callback = button_callback

    view = View()
    view.add_item(button)
    await interaction.response.send_message(embed=embed, view=view)

@bot.event
async def on_ready():
    print("hello!")
    synced = await bot.tree.sync()

bot.run(token[0])
