import discord
import requests
import os
import subprocess
import asyncio

def download(title, url):
    try:
        r = requests.get(url)
        with open("sound.mp3", mode="wb") as f:
            f.write(r.content)
    except requests.exceptions.RequestException:
            print("Error")

client = discord.Client(intents=discord.Intents.all())

@client.event
async def on_ready():
    print("logged in as " + client.user.name)
    print("------")

@client.event
async def on_message(message):
    if message.author.bot:
        pass

    if "/funya" in message.content.split():
        file = message.attachments[0]
        download(file.filename, file.url)
        
        subprocess.run(["ffmpeg", "-i", "sound.mp3", "-filter_complex", "[0:a]vibrato=f=10:d=1[out_a]", "-map", "[out_a]", "out.mp3"], shell=True)
        while not os.path.exists("out.mp3"):
            await asyncio.sleep(0.1)

        await message.channel.send(file=discord.File("out.mp3"))

        await message.delete()

        os.remove("out.mp3")
        os.remove("sound.mp3")

client.run("YOUR_TOKEN")