import discord, datetime
from discord.ext import commands
from discord.ui import Button, View

intents = discord.Intents.all()
bot = commands.Bot(command_prefix = ']', intents=intents)

with open("TOKEN.token", "r") as f:
    token = f.readlines()[0]
    
@bot.tree.command(name="findfamiliar")
@discord.app_commands.checks.has_permissions(administrator=True)
async def findfamiliar(interaction: discord.Interaction, user: str = None, reason: str = None):
    if not interaction.user.guild_permissions.administrator:
        return await interaction.response.send_message("Nope!")
    if user is None:
        return await interaction.response.send_message("You didn't specify a user.")
    if reason is None:
       reason = "Kicked by findfamiliar command." 

    discordServerGuild = bot.get_guild(interaction.guild_id)
    similarUsers = []

    for member in discordServerGuild.members:
        if user.lower() in member.name.lower():
            similarUsers.append(member)
        embed = discord.Embed(color=0xec0000)

    if len(similarUsers) != 0:
        embed.title=f"Users with similar names to `{user}` found:"
        embed.timestamp = datetime.datetime.now()
    else:
        embed.title=f"No users found"
        return await interaction.response.send_message(embed=embed)
    for user in similarUsers:
        embed.add_field(name="", value=user.mention, inline=False)
    
    class buttonView(View):
        @discord.ui.button(label="Kick listed users", style=discord.ButtonStyle.red, emoji="💥")
        async def button_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
            log = ''
            button.label = "Users kicked."
            button.emoji="🤯"
            button.disabled = True
            log += f"## Kicking log ##\nReason for kick: {reason}\n--------\n"
            for user in similarUsers:
                try:
                    log += f"{user}\n"
                    await user.kick(reason=str(reason))
                except Exception as e:
                    log += f"error kicking {user}, reason: {e}"
                    continue 
            count = len(similarUsers)
            similarUsers.clear()
            await interaction.response.edit_message(content=f"`{count}` Users kicked ```{log}```", view=self)
    view = buttonView()
    return await interaction.response.send_message(embed=embed, view=view)

@bot.event
async def on_ready():
    print("hello!")
    synced = await bot.tree.sync()

bot.run(token)
