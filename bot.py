#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Filename: bot.py
Author: Jarisse Escubido
Created: 2025-02-25
Description: 
    Creating a simple bot to do simple things.
"""

# Import statements
import os
import asyncio
import discord
from discord.ext import commands
from dotenv import load_dotenv

"""
Establishing initial connections to discord server
"""
# Loading environment variables from .env
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Establishing token connections
if BOT_TOKEN:
    print("Discord token loaded successfully")
else:
    print("Discord token not found!")


# Establishing Intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix=("!"),intents=intents) # Commands are executed following '!'

# Loading cogs files
async def load_cogs():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f'cogs.{filename[:-3]}')

# Establishing connection to Discord
@bot.event
async def on_ready() -> None:
    print(f"{bot.user} has connected to Discord")

async def main():
    async with bot:
        await load_cogs()
        await bot.start(os.getenv("BOT_TOKEN"))

##############################################################

if __name__ == "__main__":
    asyncio.run(main())