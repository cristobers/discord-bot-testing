import discord, datetime, asyncio
from discord.ext import commands
from discord.ui import Button, View

intents = discord.Intents.all()
bot = commands.Bot(command_prefix = ']', intents=intents)

with open("TOKEN.token", "r") as f:
    token = next(iter(f.readlines()))

async def kick_users(similarUsers: list):
    count, timeout = 0, 0
    for user in similarUsers:
        count += 1
        try:
            print("Time between kicks: ", timeout)
            await user.kick(reason=str(reason))
            await asyncio.sleep(timeout) # makes discord endpoints happier :)
            print(f"Kicking {user}")
            timeout = 1 << count
        except Exception as e:
            print("Error kicking user {user}, reason: {e}")
            continue
    similarUsers.clear()
    return count

@bot.tree.command(name="findfamiliar")
@discord.app_commands.checks.has_permissions(administrator=True)
async def findfamiliar(interaction: discord.Interaction, user: str = None, reason: str = None):
    if not interaction.user.guild_permissions.administrator:
        return await interaction.response.send_message("🍅")
    if user is None:
        return await interaction.response.send_message("You didn't specify a user.")
    if reason is None:
       reason = "Kicked by findfamiliar command." 

    discordServerGuild = bot.get_guild(interaction.guild_id)
    similarUsers = []

    for member in discordServerGuild.members:
        if user.lower() in member.name.lower():
            similarUsers.append(member)

    if len(similarUsers) != 0:
        embed = discord.Embed(color=0xec0000)
        embed.title=f"Users containing `{user}`:"
        embed.timestamp = datetime.datetime.now()
    else:
        embed.title="No users found"
        return await interaction.response.send_message(embed=embed)
    for user in similarUsers:
        embed.add_field(name="", value=user.mention, inline=False)

    class buttonView(View):
        @discord.ui.button(label="Kick listed users", style=discord.ButtonStyle.red, emoji="💥")
        async def button_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
            if not interaction.user.guild_permissions.administrator:
                return # dont click my buttons if you aint an admin!!!
            button.label = "Users kicked."
            button.emoji="🤯"
            button.disabled = True
            kick_users_task = asyncio.create_task(kick_users(similarUsers))
            return await interaction.response.edit_message(content=f"😃", view=self)
    view = buttonView()
    return await interaction.response.send_message(embed=embed, view=view)

@bot.event
async def on_ready():
    print("bot is online! :O")
    synced = await bot.tree.sync()
bot.run(token)