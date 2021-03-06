from logging import error
from discord.embeds import Embed
from discord.enums import Enum
from rustplus import RustSocket
import json
import discord
from discord.ext import commands
import asyncio
from discord.ext import tasks
import pathlib
from urllib.parse import urljoin
from urllib.request import pathname2url
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
    recreatedTeamEvent.start()
    recreatedInfoEvent.start()
    statusTask.start()
    autoRestart.start()
#IMPORTANT to keep the connection alive!
@tasks.loop(seconds=600)
async def autoRestart():
    socket.disconnect()
    socket.connect()
    print(Fore.LIGHTGREEN_EX + "-----------reconected!------------")
#IMPORTANT to keep the connection alive!
    
    
@tasks.loop(seconds=0)
async def statusTask():
    dict = socket.getInfo()
    team = socket.getTeamInfo()
    onlineMembers = 0
    maxMembers = 0
    for member in team.members:
        maxMembers += 1
        if member.isOnline == True:
            onlineMembers += 1
    while True:
#        print(Fore.LIGHTWHITE_EX + "Changed Staus to: " + Fore.RESET + Fore.WHITE + f"Pop: {dict['currentPlayers']}/{dict['maxPlayers']}")
        await client.change_presence(status=discord.Status.idle, activity=discord.Game(f"Pop: {dict['currentPlayers']}/{dict['maxPlayers']}"))
        await asyncio.sleep(7.4)
#        print(Fore.LIGHTWHITE_EX + "Changed Staus to: " + Fore.RESET + Fore.WHITE + f"our team: {onlineMembers}/{maxMembers}")
        await client.change_presence(status=discord.Status.idle, activity=discord.Game(f"our team: {onlineMembers}/{maxMembers}"))
        await asyncio.sleep(7.4)
#        print(Fore.LIGHTWHITE_EX + "Changed Staus to: " + Fore.RESET + Fore.WHITE + f"{dict['name']}")
        await client.change_presence(status=discord.Status.idle, activity=discord.Game(f"{dict['name']}"))
        await asyncio.sleep(7.4)

@client.command()
async def map(ctx):
    socket.getMap(addIcons = True, addEvents = True, addVendingMachines= True).save("database/pictures/RustMap.PNG")
    file = discord.File('database/pictures/RustMap.PNG')
    await ctx.send(file=file)
    
@client.command()
async def events(ctx):
    with open("database/json/rust-msg.json", "r") as file:
        data = json.load(file)
    events = socket.getCurrentEvents()
    msg = await ctx.send("Refreshes every `60` seconds")
    if events:
        print("eventevent(Events)")
        exp = False
        ch = False
        lc = False
        cargo = False
        for event in events:


            embed = discord.Embed(title="Server Events:")


            if event.type == 2:
                embed.add_field(name=("Explosion: `???`" if event.type == 2 else "Explosion ???"), value="Bradley or Patrol got taken!", inline = False)
                exp = True
            if event.type == 4:
                embed.add_field(name=("Chinnok: `???`" if event.type == 4 else "Chinnok ???"), value="Chinook is out!", inline = False)
                ch = True
            if event.type == 6:
                embed.add_field(name=("Locked Crate: `???`" if event.type == 6 else "Locked Crate ???"), value="Locked crate is out!", inline = False)
                lc = True
            if event.type == 5:
                embed.add_field(name=("Cargo ship: `???`" if event.type == 5 else "Cargo ship ???"), value="Cargo ship is out!", inline = False)
                cargo = True
            
        if exp == False:
            embed.add_field(name="Explosion: `???`", value="There is no explosion!", inline = False)
        if ch == False:
            embed.add_field(name="Chinnok: `???`", value="Chinook is not out!", inline = False)
        if lc == False:
            embed.add_field(name="Locked Crate: `???`", value="There is no locked crate!", inline = False)
        if cargo == False:
            embed.add_field(name="Cargo ship: `???`", value="Cargo is not out!", inline = False)

    if not events:
        embed = discord.Embed(title="Server Events:")
        embed.add_field(name="Explosion: `???`", value="There is no explosion!", inline = False)
        embed.add_field(name="Chinnok: `???`", value="Chinook is not out!", inline = False)
        embed.add_field(name="Locked Crate: `???`", value="There is no locked crate!", inline = False)
        embed.add_field(name="Cargo ship: `???`", value="Cargo is not out!", inline = False)
        print("eventevent(noEvent)")


    await msg.edit(embed=embed)
                

    data["events-channel-id"] = ctx.channel.id
    data["events-msg-id"] = msg.id
    with open("database/json/rust-msg.json", "w") as file:
        data = json.dump(data,file,indent=4)

@tasks.loop(seconds=60)
async def recreatedEventsEvent():
    with open("database/json/rust-msg.json", "r") as file:
        data = json.load(file)
    events = socket.getCurrentEvents()
    

            
    for guild in client.guilds:
        try:
            if not data["events-msg-id"]:
                return print("Returned at eventevent()")
            memberNames = []
            eventsMsgId = data["events-msg-id"]
            eventsChannelId = data["events-channel-id"]
            mChannel = client.get_channel(eventsChannelId)
            mMsg = await mChannel.fetch_message(eventsMsgId)

            if events:
                print("eventevent(Events)")
                exp = False
                ch = False
                lc = False
                cargo = False
                for event in events:


                    embed = discord.Embed(title="Server Events:")


                    if event.type == 2:
                        embed.add_field(name=("Explosion: `???`" if event.type == 2 else "Explosion ???"), value="Bradley or Patrol got taken!", inline = False)
                        exp = True
                    if event.type == 4:
                        embed.add_field(name=("Chinnok: `???`" if event.type == 4 else "Chinnok ???"), value="Chinook is out!", inline = False)
                        ch = True
                    if event.type == 6:
                        embed.add_field(name=("Locked Crate: `???`" if event.type == 6 else "Locked Crate ???"), value="Locked crate is out!", inline = False)
                        lc = True
                    if event.type == 5:
                        embed.add_field(name=("Cargo ship: `???`" if event.type == 5 else "Cargo ship ???"), value="Cargo ship is out!", inline = False)
                        cargo = True
                    
                if exp == False:
                    embed.add_field(name="Explosion: `???`", value="There is no explosion!", inline = False)
                if ch == False:
                    embed.add_field(name="Chinnok: `???`", value="Chinook is not out!", inline = False)
                if lc == False:
                    embed.add_field(name="Locked Crate: `???`", value="There is no locked crate!", inline = False)
                if cargo == False:
                    embed.add_field(name="Cargo ship: `???`", value="Cargo is not out!", inline = False)

            if not events:
                embed = discord.Embed(title="Server Events:")
                embed.add_field(name="Explosion: `???`", value="There is no explosion!", inline = False)
                embed.add_field(name="Chinnok: `???`", value="Chinook is not out!", inline = False)
                embed.add_field(name="Locked Crate: `???`", value="There is no locked crate!", inline = False)
                embed.add_field(name="Cargo ship: `???`", value="Cargo is not out!", inline = False)
                print("eventevent(noEvent)")


            await mMsg.edit(embed=embed)
                



        except Exception:
            print("\nrecreatedTeamEvent() --> ERROR!")
            print(error(msg = "Error:\n", exc_info = True))


@client.command()
async def pop(ctx):
    dict = socket.getInfo()
    embed=Embed(title="Server Pop", description="Pop: " + "`" + str(dict['currentPlayers']) + "/" + str(dict['maxPlayers']) + "`" + "\n\nQueue: " + "`" + str(dict['queuedPlayers']) + "`" + "\n\nServer: " + "`" + str(dict['name']) + "`")
    await ctx.send(embed=embed)

@client.command()
async def teamchat(ctx):
    chat = socket.getTeamChat()
    embed = Embed(title="Team Chat")
    msgCount = 0
    for message in chat:
        msgCount += 1
        if msgCount == 50:
            break
        embed.add_field(name=f"{message.senderName}:", value=f"```{message.message}```")
    await ctx.send(embed=embed)

@client.command()
async def team(ctx):
    with open("database/json/rust-msg.json", "r") as file:
        data = json.load(file)
    team = socket.getTeamInfo()
    memberNames = []
    guild = ctx.guild
    msg = await ctx.send("Refreshes every `60` seconds")



    data["team-channel-id"] = ctx.channel.id
    data["team-msg-id"] = msg.id

    with open("database/json/rust-msg.json", "w") as file:
        data = json.dump(data,file,indent=4)
    def getLeaderName():
        for member in team.members:
            if member.steamId == team.leaderSteamId:
                return member.name

    embed=Embed(title="Team Info", description=f"Leader steam id: `{getLeaderName()}`")




    for member in team.members:
        memberNames.append(member.name)

        embed.add_field(name=member.name, value=f'steam-id: `{member.steamId}` \nStatus: {("`???? Online`" if member.isOnline else "`???? Offline`")}\nSpawntime: `{member.spawnTime}`\nis alive: `{("`??? alive`" if member.isAlive else f"`?????? Death ({member.deathTime} seconds)`")}`')

    await msg.edit(embed=embed)



@tasks.loop(seconds=60)
async def recreatedTeamEvent():
    with open("database/json/rust-msg.json", "r") as file:
        data = json.load(file)
    team = socket.getTeamInfo()
    

            
    for guild in client.guilds:
        if not data["team-msg-id"]:
            return
        try:
            memberNames = []
            teamMsgId = data["team-msg-id"]
            teamChannelId = data["team-channel-id"]
            mChannel = client.get_channel(teamChannelId)
            mMsg = await mChannel.fetch_message(teamMsgId)

            def getLeaderName():
                for member in team.members:
                    if member.steamId == team.leaderSteamId:
                        return member.name

            embed=Embed(title="Team Info", description=f"Leader Name: `{getLeaderName()}`")

            for member in team.members:
                memberNames.append(member.name)
                
                embed.add_field(name=member.name, value=f'steam-id: `{member.steamId}` \nStatus: {("`???? Online`" if member.isOnline else "`???? Offline`")}\nSpawntime: `{member.spawnTime}`\nis alive: `{("`??? alive`" if member.isAlive else f"`?????? Death ({member.deathTime} seconds)`")}`')

            await mMsg.edit(embed=embed) 
            print("teamevent()")

        except Exception:
            print("\nrecreatedTeamEvent() --> ERROR!")
            print(error)
        else:
            return


@client.command()
async def info(ctx):
    with open("database/json/rust-msg.json", "r") as file:
        data = json.load(file)
    try:
        dict = socket.getInfo()
        guild = ctx.guild
        msg = await ctx.send("Refreshes every `60 seconds`")
        socket.getMap(addIcons = True, addEvents = False, addVendingMachines= False).save("database/pictures/RustMap.PNG")
        file = discord.File('database/pictures/RustMap.PNG')
        msg1 = await ctx.send(file=file)

        data["info-channel-id"] = ctx.channel.id
        data["info-msg-id"] = msg.id
        with open("database/json/rust-msg.json", "w") as file:
            data = json.dump(data,file,indent=4)
        embed=Embed(title=str(dict['name']), description=f"Pop: `{dict['currentPlayers']} / {dict['maxPlayers']}` \n\nQueue: `{dict['queuedPlayers']}` \n\nMap: `{dict['map']}` \n\nMap Size: `{dict['size']}`" + "\n\nServer URL: " + str(dict['url']) + "\n\nMap Seed: " + "`" + str(dict['seed']) + "`")
        await msg.edit(embed=embed)

    except Exception:
        print("\nrecreatedInfoEvent() --> ERROR!")
        print(error(msg="ERROR",exc_info=True))
        


@tasks.loop(seconds=60)
async def recreatedInfoEvent():
    
    dict = socket.getInfo()
    with open("database/json/rust-msg.json", "r") as file:
        data = json.load(file)

    

            
    for guild in client.guilds:
        if not data["info-msg-id"]:
            return

        try:
            def path2url():
                return urljoin('file:', pathname2url("database/pictures/RustMap.PNG"))
            infoMsgId = data["info-msg-id"]
            infoMsgId1 = data["info-msgImage-id"]
            infoChannelId = data["info-channel-id"]
            mChannel = client.get_channel(infoChannelId)
            mMsg = await mChannel.fetch_message(infoMsgId)

            embed=Embed(title=str(dict['name']), description=f"Pop: `{dict['currentPlayers']} / {dict['maxPlayers']}` \n\nQueue: `{dict['queuedPlayers']}` \n\nMap: `{dict['map']}` \n\nMap Size: `{dict['size']}`" + "\n\nServer URL: " + str(dict['url']) + "\n\nMap Seed: " + "`" + str(dict['seed']) + "`")
            await mMsg.edit(embed=embed)
            print("infoevent()")

        except Exception:
            print("\nrecreatedInfoEvent() --> ERROR!")
            print(error(msg="ERROR",exc_info=True))
        else:
            return



@client.command()
async def tc(ctx):
    tc = socket.getTCStorageContents(19262248, combineStacks = True)
    
    embed= Embed(title="TC Info", description=f"Upkeep: `{tc['protectionTime']}`")
    
    for item in tc['contents']:
        embed.add_field(name=f"{item.name}:", value=f"{item.quantity}",inline=False)
    await ctx.send(embed=embed)


client.run(data["token"])
