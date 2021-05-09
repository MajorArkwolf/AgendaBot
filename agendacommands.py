import discord
import os
import datechecker
import json
import database
import datetime
import compilejson


client = discord.Client()


def FindUser(id):
    return database.FindUser(id)


def FileCheck(message):
    filepath = "./data/{}.json".format(message.guild.id)
    exists = os.path.isfile(filepath)
    if exists is True:
        return True
    else:
        return False


async def ErrorPrivilege(message):
    await message.author.send("You dont not have permission for this command.")


async def Userlookup(message, name):
    id_exists = database.FindUser(message.author.id)
    if id_exists:
        await message.author.send("Already in the Database.")
    else:
        database.InsertUser(message.author.id, name)
        await message.author.send("{} added to the register.".format(name))
    return


async def UserRemove(message):
    id_exists = database.FindUser(message.author.id)
    if id_exists:
        database.RemoveUser(message.author.id)
        await message.author.send("You have removed yourself from the"
                                  " register.")
    else:
        await message.author.send("Userid: {0}, not stored in the Database."
                                  .format(message.author.id))
    return


async def MessageCleanup(message):
    if type(message.channel) is not discord.channel.DMChannel:
        await message.delete()
    return


async def ChannelCheck(message, defaultRoom):
    if type(message.channel) is not discord.channel.DMChannel:
        var = "Do not post agenda items outside of {0}!".format(defaultRoom)
        messageUser = discord.Embed(title="WARNING", color=0x00ff00)
        messageUser.add_field(name="Wrong Chat", value=var, inline=False)
        await message.author.send(embed=messageUser)


async def CreateAgenda(message):
    filepath = "./data/{}.json".format(message.guild.id)
    exists = os.path.isfile(filepath)
    if exists is False:
        date = message.content.split(" ")[1]
        day, month, year = date.split("/")
        if datechecker.day_check(int(month), int(day)) and datechecker.month_check(int(month)) and datechecker.year_check(year):
            if datechecker.valid_date(int(day), int(month), int(year)):
                date = {}
                data = {'day': day, 'month': month, 'year': year, 'items': []}
                with open(filepath, 'w') as outfile:
                    json.dump(data, outfile)
                await message.channel.send("Agenda Created for {}/{}/{}.".format(day, month, year))
            else:
                await message.channel.send("Date must be after the current date.")
        else:
            await message.channel.send("Date must be valid: DD/MM/YYYY.")
    else:
        await message.channel.send("Active Agenda found")


async def ModifyDate(message):
    filepath = "./data/{}.json".format(message.guild.id)
    exists = os.path.isfile(filepath)
    if exists is True:
        date = message.content.split(" ")[1]
        day, month, year = date.split("/")
        if datechecker.day_check(int(month), int(day)) and datechecker.month_check(int(month)) and datechecker.year_check(year):
            if datechecker.valid_date(int(day), int(month), int(year)):
                with open(filepath, "r+") as jsonFile:
                    data = json.load(jsonFile)
                data['day'] = day
                data['month'] = month
                data['year'] = year
                with open(filepath, "w") as jsonFile:
                    json.dump(data, jsonFile)
            else:
                await message.channel.send("Date must be after the current date.")
        else:
            await message.channel.send("Date must be valid: DD/MM/YYYY.")
    else:
        await CreateAgenda(message)
        await message.channel.send("No Agenda found, new agenda created.")


async def AutoEnd(file, client):
    filepath = "./data/{}".format(file)
    exists = os.path.isfile(filepath)
    if exists is True:
        today = datetime.date.today()
        with open(filepath, "r+") as jsonFile:
            data = json.load(jsonFile)
        if int(data['year']) == today.year:
            if int(data['month']) == today.month:
                if int(data['day']) == today.day:
                    id = file.split(".")[0]
                    serverinfo = database.GetServer(id)
                    # Build JSON File
                    compilejson.StartBuild(serverinfo[0])
                    # Prep message unique for server
                    guild = client.get_guild(int(serverinfo[0]))
                    channel = discord.utils.get(guild.text_channels, name=serverinfo[1])
                    filepath = "./data/{}.txt".format(id)
                    await channel.send(content="Auto: Agenda Locked.\nCurrent formatted Agenda", file=discord.File(filepath))


async def AddToAgend(message):
    if FileCheck(message) is False:
        await message.channel.send("No Active Agenda.")
        return
    try:
        memo = message.content.split(" ", 1)[1]
    except:
        await message.channel.send("Invalid format to send message.")
        return
    try:
        user = FindUser(message.author.id)
    except:
        await message.author.send("You are not registered.")
        return

    filepath = "./data/{}.json".format(message.guild.id)
    with open(filepath, "r+") as jsonFile:
        data = json.load(jsonFile)
    data['items'].append({'userid': message.author.id, 'username': user[1], "urgent": 0, 'content': memo})
    await message.channel.send("Added to the agenda.")
    with open(filepath, "w") as jsonFile:
        json.dump(data, jsonFile)


async def ViewAgenda(message):
    if FileCheck(message) is False:
        await message.channel.send("No Active Agenda. You may need to create one.")
        return

    filepath = "./data/{}.json".format(message.guild.id)
    with open(filepath, "r+") as jsonFile:
        data = json.load(jsonFile)

    datestring = "Closes midnight on the {}/{}/{}.".format(data['day'], data['month'], data['year'])
    embed = discord.Embed(title="Current Agenda", description=datestring, color=0x00ff00)

    counter = 0
    runningstring = ""
    index = 0
    for m in data['items']:
        index = index + 1
        if m['urgent'] == 1:
            counter = counter + 1
            runningstring += "[{indexV}] {username}: {content}.\n".format(indexV=index, content=m['content'], username=m['username'])
    if counter > 0:
        embed.add_field(name="URGENT", value=runningstring, inline=False)

    counter = 0
    index = 0
    runningstring = ""
    for m in data['items']:
        index = index + 1
        if m['urgent'] == 0:
            counter = counter + 1
            runningstring += "[{indexV}] {username}: {content}.\n".format(indexV=index, content=m['content'], username=m['username'])
    if counter > 0:
        embed.add_field(name="Regular Items", value=runningstring, inline=False)

    counter = 0
    index = 0
    runningstring = ""
    for m in data['items']:
        index = index + 1
        if m['urgent'] == -1:
            counter = counter + 1
            runningstring += "[{indexV}] {username}: {content}.\n".format(indexV=index, content=m['content'], username=m['username'])
    if counter > 0:
        embed.add_field(name="Final Items", value=runningstring, inline=False)
    await message.channel.send(embed=embed)


async def ViewModAgenda(message):
    if FileCheck(message) is False:
        await message.channel.send("No Active Agenda.")
        return

    filepath = "./data/{}.json".format(message.guild.id)
    with open(filepath, "r+") as jsonFile:
        data = json.load(jsonFile)

    embed = discord.Embed(title="Current Agenda", color=0x00ff00)

    counter = 0
    runningstring = ""
    for m in data['items']:
        runningstring += "[{count}] {username}: {content}.\n".format(content=m['content'], username=m['username'], count=(counter + 1))
        counter = counter + 1
    if counter > 0:
        embed.add_field(name="URGENT", value=runningstring, inline=False)
    await message.channel.send(embed=embed)


async def PostAgendaTXT(message):
    try:
        filepath = "./data/{}.txt".format(message.guild.id)
        await message.channel.send(content="Current formatted Agenda", file=discord.File(filepath))
    except:
        if FileCheck(message):
            await message.channel.send("Ensure you have ended the current Agenda File.")
        else:
            await message.channel.send("Unable to find an Agenda file.")


async def DeleteItems(message):
    temp = message.content
    temp = temp.split(" ")[-1]

    if temp == "!!delete":
        await ViewModAgenda(message)
    else:
        index = int(temp) - 1
        if index < 0:
            await message.channel.send("Invalid item")
            return

        filepath = "./data/{}.json".format(message.guild.id)
        with open(filepath, "r+") as jsonFile:
            data = json.load(jsonFile)
        try:
            if data['items'][index]['userid'] == message.author.id:
                remove = True
            elif VerifyRole(message.author.id, message.guild.id, 1):
                remove = True
            else:
                remove = False
            if(remove is True):
                message.channel.send("{} has been deleted".format(data['items'][index]))
                del data['items'][index]
                with open(filepath, "w") as jsonFile:
                    json.dump(data, jsonFile)
            else:
                await message.channel.send("You do not have permission to delete this.")
        except IndexError:
            await message.channel.send("Invalid item")


async def AddAdmin(message):
    temp = message.content
    rank = int(temp.split(" ")[1])
    id = int(temp.split(" ")[2])
    if rank == 1 or rank == 2 or rank == 3:
        if rank == 1:
            role = "President"
        elif rank == 2:
            role = "VicePresident"
        elif rank == 3:
            role = "Secretary"
        database.AddAdmin(id, role, message.guild.id)
        await message.channel.send("Admin {} has been added succesfully.".format(rank))
    else:
        await message.channel.send("Invalid message format.")


async def SetPrefix(message):
    temp = message.content
    temp = temp.split(" ")[-1]

    if "setprefix" in temp:
        await message.channel.send("Invalid message format.")
    else:
        database.SetPrefix(temp, message.guild.id)
        await message.channel.send("New Prefix set to {}.".format(temp))


async def RemoveAdmin(message):
    temp = message.content
    rank = int(temp.split(" ")[1])
    if rank == 1 or rank == 2 or rank == 3:
        if rank == 1:
            role = "President"
        elif rank == 2:
            role = "VicePresident"
        elif rank == 3:
            role = "Secretary"
        database.RemoveAdmin(role, message.guild.id)
        await message.channel.send("User Removed.")
    else:
        await message.channel.send("Invalid message format.")


async def ViewDefaultChannel(message):
    info = database.GetServer(message.guild.id)
    messageUser = discord.Embed(title="Current Server Info", color=0x00ff00)
    messageUser.add_field(name="ServerID", value=info[0], inline=False)
    messageUser.add_field(name="Default Channel", value=info[1], inline=False)
    messageUser.add_field(name="Prefix", value=info[2], inline=False)
    owner = message.guild.get_member(message.guild.owner_id)
    var = "ID: {id}.\nUsername: {username}".format(id=info[3], username=owner)
    messageUser.add_field(name="Server Owner", value=var, inline=False)
    await message.channel.send(embed=messageUser)



async def ViewAdmins(message):
    info = database.GetServer(message.guild.id)
    messageUser = discord.Embed(title="Current Admin", color=0x00ff00)
    owner = message.guild.get_member(info[3])
    president = message.guild.get_member(info[4])
    vicepresident = message.guild.get_member(info[5])
    secretary = message.guild.get_member(info[6])
    if owner:
        var = "ID: {id}.\nUsername: {username}".format(id=info[3], username=owner)
        messageUser.add_field(name="Owner", value=var, inline=False)
    if president:
        var = "ID: {id}.\nUsername: {username}".format(id=info[4], username=president)
        messageUser.add_field(name="President", value=var, inline=False)
    if vicepresident:
        var = "ID: {id}.\nUsername: {username}".format(id=info[5], username=vicepresident)
        messageUser.add_field(name="Vice President", value=var, inline=False)
    if secretary:
        var = "ID: {id}.\nUsername: {username}".format(id=info[6], username=secretary)
        messageUser.add_field(name="Secretary", value=var, inline=False)
    await message.channel.send(embed=messageUser)


async def SetLevel(message):
    temp = message.content
    temp2 = temp.split(" ")[-1]

    if "setlevel" in temp2:
        await ViewModAgenda(message)
    else:
        index = int(temp.split(" ")[1]) - 1
        priority = int(temp.split(" ")[2])
        if index < 0:
            await message.channel.send("Invalid item")
            return

        filepath = "./data/{}.json".format(message.guild.id)
        with open(filepath, "r+") as jsonFile:
            data = json.load(jsonFile)
        try:
            if data['items'][index]['userid'] == message.author.id:
                edit = True
            elif VerifyRole(message.author.id, message.guild.id, 1):
                edit = True
            else:
                edit = False
            if(edit is True):
                if(priority >= -1 and priority <= 1):
                    data['items'][index]['urgent'] = priority
                    with open(filepath, "w") as jsonFile:
                        json.dump(data, jsonFile)
            else:
                await message.channel.send("You do not have permission to modify this.")
        except IndexError:
            await message.channel.send("Invalid item")


async def SetChannel(message):
    temp = message.content
    temp = temp.split(" ")[-1]

    if "setchannel" in temp:
        await message.channel.send("Invalid message format.")
    else:
        database.SetDefaultChannel(temp, message.guild.id)
        await message.channel.send("New channel set to {}.".format(temp))


def VerifyRole(id, guildid, level):
    # level 0 = owner and president only
    # level 1 = all admins
    server = database.GetServer(guildid)
    owner = get_guild(guildid).owner_id
    admin1 = server[4]
    admin2 = server[5]
    admin3 = server[6]
    if owner != None:
        if owner == id:
            return True
    elif id == admin1:
        return True
    elif id == admin2 or id == admin3:
        if level == 1:
            return True
    else:
        return False
