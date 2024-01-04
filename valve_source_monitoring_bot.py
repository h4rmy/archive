import discord
from discord.ext import commands, tasks
import a2s
import asyncio
import json
import time

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='/', intents=intents)

last_message = None

whitelist = 1191494430717399123     # role
channel_id = 1192139263672864818    # channel

ips = ["94.228.168.193", "208.73.206.90", "20.203.145.65"]
info = {
  "servers": [
  ]
}

async def CurrentTime():
    t = time.localtime()
    current_time = time.strftime("%Y-%m-%d %H:%M:%S", t)
    return current_time

async def QueryServer(ips):
    for ip in ips:
        try:
            a = await a2s.ainfo((ip, 27015))
        except asyncio.exceptions.TimeoutError:
            print(f"{ip} is offline")
            a = None
        if a:
            srv = {"address": ip, "name": a.server_name, "plr": a.player_count, "maxplr": a.max_players, "map": a.map_name, "game": a.game}
            yield srv
        else:
            yield None

async def BuildJson(query_response):
    info["servers"].append(query_response)
    

async def BuildEmbeds(json_data):
    global embedList
    embedList = []
    timestamp = await CurrentTime()
    wtf = json.loads(json_data)
    for i in wtf["servers"]:
        embed=discord.Embed(title=f"**{i['name']}**", description=f"Connect: steam://connect/{i['address']}:27015", color=0xf0ba4a)
        embed.add_field(name="**Status**", value="**🟢 Online**", inline=True)
        embed.add_field(name="**Address:Port**", value=f"`{i['address']}:27015`", inline=True)
        embed.add_field(name="**Country**", value="kurdistan", inline=True)
        embed.add_field(name="**Game**", value=f"{i['game']}", inline=True)
        embed.add_field(name="**Current map**", value=f"{i['map']}", inline=True)
        embed.add_field(name="**Players**", value=f"{i['plr']}/{i['maxplr']}", inline=True)
        embed.set_footer(text=f"ClassicCounter Server Monitoring | flashboost.ru | Last update: {timestamp}", icon_url="https://cdn.discordapp.com/icons/1083325391269281794/73af4cdc473d39b1e0995bdc73a8f84d.webp?size=96",)
        embedList.append(embed)

async def update_message():
    global last_message
    if last_message:
        async for huina in QueryServer(ips):
            await BuildJson(huina)
        builtjson = json.dumps(info)
        info["servers"].clear()
        await BuildEmbeds(builtjson)
        await last_message.edit(embeds=embedList)

@bot.event
async def on_ready():
    print(f'logged in as {bot.user.name}')
    update_task.start()

@bot.command(name='start')
async def start(ctx):
    global last_message, channel
    channel = bot.get_channel(channel_id)
    if discord.utils.get(ctx.author.roles, id=whitelist) and (ctx.channel.id == channel_id):
        async for huina in QueryServer(ips):
            await BuildJson(huina)
        builtjson = json.dumps(info)
        info["servers"].clear()
        await BuildEmbeds(builtjson)
        last_message = await channel.send(embeds=embedList)

@tasks.loop(seconds=15)
async def update_task():
    await update_message()
if __name__ == "__main__":
    bot.run('tokin')