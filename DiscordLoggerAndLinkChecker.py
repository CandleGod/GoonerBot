from typing import Final
import os
from dotenv import load_dotenv
from discord import Intents, Client, Message
import discord
import requests
import time
from discord.ext import commands

origTOKEN = ('') # Put token here
origURLSCAN_API_KEY = ('') # API key here make an account here https://urlscan.io

load_dotenv()
TOKEN = os.getenv(origTOKEN)
URLSCAN_API_KEY = os.getenv(origURLSCAN_API_KEY)

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

client = discord.Client(intents=intents)

def check_url(url):
    headers = {
        'API-Key': origURLSCAN_API_KEY,
        'Content-Type': 'application/json',
    }
    data = {
        'url': url,
    }
    response = requests.post('https://urlscan.io/api/v1/scan/', headers=headers, json=data)
    return response.json()

def get_scan_result(scan_id):
    headers = {
        'API-Key': origURLSCAN_API_KEY,
    }
    response = requests.get(f'https://urlscan.io/api/v1/result/{scan_id}/', headers=headers)
    return response.json()

@client.event
async def on_ready():
    print(f'Currently goofing around as {client.user}')

# LINK CHECKER
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    print(f'Received message: {message.content}')

    for word in message.content.split():
        if word.startswith('http://') or word.startswith('https://'):
            if not word.endswith(('.gif', '.GIF')):  # Ignore GIFs
                channel = client.get_channel(1234567890)  # Replace with the channel ID you want to send to
                await channel.send(f'Checking URL: {word}')
                scan_result = check_url(word)
                print(f'This is the scan_result {scan_result}')
                if scan_result.get('message') == 'Submission successful':
                    scan_id = scan_result.get('uuid')
                    await channel.send(f'URL {word} is submitted for scanning. Please wait...')

                    # Wait for a short period to allow the scan to complete
                    time.sleep(15)

                    # Fetch the scan result
                    scan_result_data = get_scan_result(scan_id)

                    # Analyze the scan result to check if the link is real
                    if 'verdicts' in scan_result_data and scan_result_data['verdicts']['overall']['malicious'] == False:
                        await channel.send(f'The URL {word} appears to be safe.')
                    else:
                        await channel.send(f'The URL {word} might be dangerous. Please proceed with caution.')
                else:
                    await channel.send(f'URL {word} could not be scanned. Please check manually. If this keeps happening contact Candle')

# MESSAGE LOGGER
deleted_messages_channel_id = 12345678901 # Replace with logger channel
@client.event
async def on_message_delete(message):
    if message.author.bot:
        return

    channel = message.channel
    content = message.clean_content
    author = message.author

    embed = discord.Embed(
        title=f"Deleted Message in #{channel.name}",
        description=content if content else "[No content]",
        color=0xff0000
    )
    embed.set_author(name=author.name, icon_url=author.avatar.url)
    embed.set_footer(text=f"Author ID: {author.id}")

    deleted_messages_channel = client.get_channel(deleted_messages_channel_id)
    if deleted_messages_channel:
        await deleted_messages_channel.send(embed=embed)

client.run(origTOKEN)
