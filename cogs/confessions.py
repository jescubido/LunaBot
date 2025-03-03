#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Filename: confess.py
Author: Jarisse Escubido
Created: 2025-03-03
Description: 
    Implements a command that allows anonymous messages.
"""

# Import statements
import discord
from discord.ext import commands

class Confessions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def confess(self, ctx, *, msg:str):
        await ctx.message.delete()

        embed = discord.Embed(
            title="Confession",
            description=msg,
            color=discord.Color(int('586ba4', 16))
        )

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Confessions(bot))