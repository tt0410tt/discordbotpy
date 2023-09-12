from cmath import log
from distutils.sysconfig import PREFIX
import discord
from dotenv import load_dotenv
import os
import asyncio
import datetime
import requests
from bs4 import BeautifulSoup
from discord.ext import commands, tasks
load_dotenv()

#PREFIX = os.environ['PREFIX']
TOKEN = os.environ['TOKEN']

discord_intents = discord.Intents.default()
discord_intents.message_content = True
discord_intents.members = True
client = commands.Bot(intents=discord_intents, status=discord.Status.online, command_prefix='!')
is_striming_on = False
strimg_name = ""

@client.event
async def on_ready():
    print(f'Logged in as {client.user}.')
    client.loop.create_task(Get_Info(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return


async def Get_Info(client: discord.ext.commands.Bot):
    strimg_name = ""
    while True:
        now = datetime.datetime.now()
        if 0 == now.minute % 5:
            url = 'https://play.afreecatv.com/jymin2174'
            response = requests.post(url)
            if response.status_code == 200:
                html = response.text
                soup = BeautifulSoup(html, 'html.parser')
                a = soup.find_all("meta")
                for i in range(len(a)):
                    if "og:title" in str(a[i]):
                        print("확인용\t\t" + str(a[i])[15:-23])
                        if strimg_name == str(a[i])[15:-23]:
                            print(now)
                            print("2")
                            break
                        else:
                            strimg_name = str(a[i])[15:-23]
                            if "방송중이지 않습니다." == str(a[i])[15:-23]:
                                is_striming_on = False
                                await client.get_channel(1145229621764313138).send("방송off")
                                break
                            elif not is_striming_on:
                                is_striming_on = True
                                await client.get_channel(1145229621764313138).send("방송on")
                            print(now)
                            print("1")

                            await client.get_channel(1145229472333844511).send(str(a[i])[15:-23])
                            await client.get_channel(1145229472333844511).send(now)
                            break
        else:
            pass
        await asyncio.sleep(60)



try:
    client.run(TOKEN)
except Exception as e:
    print(e)
