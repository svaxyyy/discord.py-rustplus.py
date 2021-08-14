from discord.embeds import Embed
from discord.enums import Enum
from rustplus import RustSocket
import json
import discord
from discord.ext import commands
import asyncio

with open("database/json/fcm-listen-output.json", "r")as file:
    output = json.load(file)





_IP = str(output["ip"])
_PORT = str(output["port"])
_STEAMID = int(output["playerId"])
_PLAYERTOKEN = int(output["playerToken"])



intents = discord.Intents.default()
intents.members = True


color = 0xffffff

# json



socket = RustSocket(_IP, _PORT, _STEAMID, _PLAYERTOKEN)
_CONNECT = socket.connect() 


def load():
    with open("database/json/bot_config.json", "r") as file:
        return json.load(file)

data = load()

client = commands.Bot(command_prefix=data["prefix"], intents=intents)


@client.event
async def on_ready():

    print('We have logged in as {0.user}'.format(client))
    _CONNECT
    team_info = socket.getTeamInfo()

    await asyncio.create_task(recreatedTeamEvent())




        
        

#advancing later
async def runningEvents(ctx):
    _LOOP = True

    while _LOOP:
        await asyncio.sleep(60)
        if events:
            embed = discord.Embed(title="These event are Running right now:")
            for event in events:
                embed.add_field(name="Event:", value=event.name)
            
            await ctx.send(embed=embed)

        else:
            embed = discord.Embed(title="There are no events running right now!")
            await ctx.send(embed=embed)


@client.command()
async def map(ctx):
    socket.getMap(addIcons = True, addEvents = True, addVendingMachines= True).save("database/pictures/RustMap.PNG")
    file = discord.File('database/pictures/RustMap.PNG')
    await ctx.send(file=file)
   


@client.command()
async def events(ctx):
    events = socket.getCurrentEvents()
    if events:
        embed = discord.Embed(title="These event are Running right now:")
        for event in events:
            embed.add_field(name="Event:", value=event.type.value)
        
        await ctx.send(embed=embed)

    else:
        embed = discord.Embed(title="There are no events running right now!")
        await ctx.send(embed=embed)


@client.command()
async def pop(ctx):
    dict = socket.getInfo()
    embed=Embed(title="Server Pop", description="Pop: " + "`" + str(dict['currentPlayers']) + "/" + str(dict['maxPlayers']) + "`" + "\n\nQueue: " + "`" + str(dict['queuedPlayers']) + "`" + "\n\nServer: " + "`" + str(dict['name']) + "`")
    await ctx.send(embed=embed)

    
@client.command()
async def team(ctx):
    with open("database/json/rust-msg.json", "r") as file:
        data = json.load(file)
    team = socket.getTeamInfo()
    memberNames = []
    guild = ctx.guild
    msg = await ctx.send("Refreshes every `60` seconds")

    if not guild.id in data:
        data[str(guild.id)] = {}
        data[str(guild.id)]["team-channel-id"] = ctx.channel.id
        data[str(guild.id)]["team-msg-id"] = msg.id

    data[str(guild.id)]["team-channel-id"] = ctx.channel.id
    data[str(guild.id)]["team-msg-id"] = msg.id

    with open("database/json/rust-msg.json", "w") as file:
        data = json.dump(data,file,indent=4)
    def getLeaderName():
        for member in team.members:
            if member.steamId == team.leaderSteamId:
                return member.name

    embed=Embed(title="Team Info", description=f"Leader steam id: `{getLeaderName()}`")




    for member in team.members:
        memberNames.append(member.name)

        embed.add_field(name=member.name, value=f'steam-id: `{member.steamId}` \n\nStatus: {("`🟢 Online`" if member.isOnline else "`🔴 Offline`")}\n\nSpawntime: `{member.spawnTime}`\n\nis alive: `{("`✅ alive`" if member.isAlive else f"`☠️ Death ({member.deathTime} seconds)`")}`')

    await msg.edit(embed=embed)

    

async def recreatedTeamEvent():

    while True:
        
        with open("database/json/rust-msg.json", "r") as file:
            data = json.load(file)
        team = socket.getTeamInfo()
        
        for guild in client.guilds:

            memberNames = []
            teamMsgId = data[str(guild.id)]["team-msg-id"]
            teamChannelId = data[str(guild.id)]["team-channel-id"]
            mChannel = client.get_channel(teamChannelId)
            mMsg = await mChannel.fetch_message(teamMsgId)

            def getLeaderName():
                for member in team.members:
                    if member.steamId == team.leaderSteamId:
                        return member.name

            embed=Embed(title="Team Info", description=f"Leader Name: `{getLeaderName()}`")

            for member in team.members:
                memberNames.append(member.name)

                embed.add_field(name=member.name, value=f'steam-id: `{member.steamId}` \n\nStatus: {("`🟢 Online`" if member.isOnline else "`🔴 Offline`")}\n\nSpawntime: `{member.spawnTime}`\n\nis alive: `{("`✅ alive`" if member.isAlive else f"`☠️ Death ({member.deathTime} seconds)`")}`')

            await mMsg.edit(embed=embed)
            print("recreatedTeamEvent() ran!")
            await asyncio.sleep(60)



client.run(data["token"])
