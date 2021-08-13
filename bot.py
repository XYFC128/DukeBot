#!/usr/bin/python3
import os

import discord

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

with open('token.txt', 'r') as f:
    client.run(f.read())