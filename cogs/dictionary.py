#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Filename: dictionary.py
Author: Jarisse Escubido
Created: 2025-02-25
Description: 
    Implements a dictionary class to get definition and word of the day
        using Merriam Webster Dictionary API.

    Merriam Webster API does not provide Word of the Day so scraped their
        website to extract WOTD information
"""

# Import statements
import os
import requests
from discord.ext import commands
from dotenv import load_dotenv
from bs4 import BeautifulSoup

# Load environment variables
load_dotenv()
DICT_TOKEN = os.getenv("DICT_TOKEN")

if DICT_TOKEN:
    print("Merriam Webster Dictionary token loaded successfully")
else:
    print("Merriam Webster Dictionary token not found!")


class Dictionary(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def get_wotd(self):
        """Scraping Word of the Day Page"""
        url = "https://www.merriam-webster.com/word-of-the-day"
        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")

            # Extract word
            word_element = soup.find("h2", class_="word-header-txt")
            word = word_element.text.strip() if word_element else "Cannot extract word information"

            #Extract definition
            definition_element = soup.find("p")
            definition = definition_element.text.strip() if word_element else "Cannot extract definition information"

            return f"**Word of the Day: {word}**\n Definition: {definition}"
        
        else:
            return "Failed to fetch the Word of the Day"

    def get_definition(self, word):
        """Create request to fetch word from API"""
        url = f"https://dictionaryapi.com/api/v3/references/collegiate/json/{word}?key={DICT_TOKEN}"
        response = requests.get(url)

        if response.status_code == 200: # Code 200 means OK
            data = response.json()
            if isinstance(data, list) and len(data) > 0 and isinstance(data[0], dict):
                word = data[0].get('meta', {}).get('id', word)
                definitions_data = data[0].get('shortdef', ["No definition found."])
                definition = "\n".join([f"{i+1}. {defn}" for i, defn in enumerate(definitions_data)])
                return f"**Word: {word.capitalize()}**\n\n Definition(s): \n{definition}"
            else:
                return "Word not found! Please check spelling... or you just made up a word."
        else:
            return "Error fetching data from Merriam Webster Dictionary"
            
###################### END OF DICTIONARY CLASS ##################################################################
    
    """
    Creating Bot Commands
    """
    @commands.command()
    async def define(self, ctx, word: str):
        """Fetch and sends the definition of a word"""
        definition = self.get_definition(word)
        await ctx.send(definition)

    @commands.command()
    async def wotd(self, ctx):
        word_of_the_day = self.get_wotd()
        await ctx.send(word_of_the_day)

"""
Connecting API/database and initializing environment for the cogs
"""
async def setup(bot):
    await bot.add_cog(Dictionary(bot))
            