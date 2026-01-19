import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from threading import Thread
from flask import Flask

# This small server tells the hosting provider that the bot is alive.
app = Flask('')

@app.route('/')
def home():
    return "Bot is running!"

def run():
    # Use the port provided by the host or default to 8080
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()


load_dotenv()
token = os.getenv('DISCORD_TOKEN')

# Wordle Bot Discord ID
wordle_bot_id = 891466532977258537

# Wordle Winning Role
role_name = "Wordle Winner"

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')


@bot.event
async def on_message(message: discord.Message):
    
    if message.author.id != wordle_bot_id:
        return
    
    if "👑" not in message.content:
        return
    
    guild = message.guild
    if guild is None:
        return
    
    role = discord.utils.get(guild.roles, name=role_name)
    if role is None:
        role = await guild.create_role(name=role_name)
        print(f"Created role: {role_name}")

    for member in role.members:
        await member.remove_roles(role)        
    
    if not message.mentions:
        print("No mentions found in the message.")
        return
    
    winners = []
    print("Wordle Winner found:")
    for member in message.mentions:
        await member.add_roles(role)
        winners.append(member.mention)
        print(f"- {member.display_name}")

 
    if winners:
        winner_text = ", ".join(winners)
        await message.channel.send(f"🏆 **Congratulations!** The **{role_name}** role has been reassigned to: {winner_text}")

        if "2/6" in message.content:
            await message.channel.send("Stop cheating Ria...")

    await bot.process_commands(message)

if __name__ == "__main__":
    keep_alive()
    bot.run(token)