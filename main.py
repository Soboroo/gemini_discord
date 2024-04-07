import asyncio

import discord
from discord.ext import commands
import google.generativeai as genai

intents = discord.Intents.default()
intents.message_content = True

genai.configure(api_key='API_KEY')
model = genai.GenerativeModel('gemini-pro')

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    await bot.tree.sync()
    await bot.change_presence(activity=discord.Game(name="/gemini [question]"))
    print(f"Logged in as {bot.user}")


@bot.tree.command(name="gemini", description="Ask anything to gemini")
@discord.app_commands.describe(message="Your message to ask gemini")
async def slash_command(interaction: discord.Interaction, message: str):
    await interaction.response.defer()
    try:
        async with asyncio.timeout(10):
            response = model.generate_content(message, safety_settings=[
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_NONE",
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_NONE",
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_NONE",
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_NONE",
            },
        ])
    except asyncio.TimeoutError:
        await interaction.followup.send("Timeout")
        return
    await interaction.followup.send('An answer for **' + message + '**.\n\n'+response.text)


bot.run('TOKEN')

