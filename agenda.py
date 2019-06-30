import discord
import os
import compilejson
import agendacommands
import database
import helpmenu
from os.path import join, dirname
from dotenv import load_dotenv
command = agendacommands
client = discord.Client()
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)


@client.event
async def on_message(message):
    prefix = "!!"
    defaultRoom = "agenda"
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return
    # used to grab default channel and prefix, if server doesnt exist insert it
    if message.author != client.user:
        if type(message.channel) is not discord.channel.DMChannel:
            id_exists = database.GetServer(message.guild.id)
            if id_exists:
                defaultRoom = id_exists[1]
                prefix = id_exists[2]
            else:
                database.SetServer(message.guild.id, "agenda", "!!",
                    message.guild.owner_id)

    if message.content.startswith(prefix):
        if type(message.channel) is not discord.channel.DMChannel:
            if message.channel.name != defaultRoom:
                await command.ChannelCheck(message, defaultRoom)
                await command.MessageCleanup(message)
                return

    if message.content.startswith(prefix + "register"):
        temp = message.content
        try:
            temp = temp.split(" ")[1]
            await command.Userlookup(message, temp)
        except:
            await message.author.send("Unable to process, ensure you have entered a name at the end")
        await command.MessageCleanup(message)
        return

    if message.content.startswith(prefix + "unregister"):
        await command.UserRemove(message)
        await command.MessageCleanup(message)
        return

    if message.content.startswith(prefix + "create"):
        if command.VerifyRole(message.author.id, message.guild.id, 1):
            if message.channel.name == defaultRoom:
                await command.CreateAgenda(message)
            return

    if message.content.startswith(prefix + "setdate"):
        if command.VerifyRole(message.author.id, message.guild.id, 1):
            if message.channel.name == defaultRoom:
                await command.ModifyDate(message)
                return

    if message.content.startswith(prefix + "additem"):
        if message.channel.name == defaultRoom:
            await command.AddToAgend(message)
            return

    if message.content.startswith(prefix + "end"):
        if command.VerifyRole(message.author.id, message.guild.id, 1):
            if command.FileCheck(message):
                compilejson.StartBuild(message.guild.id)
                await command.PostAgendaTXT(message)
            else:
                await message.channel.send("No agenda active.")
        return

    if message.content.startswith(prefix + "getagenda"):
        await command.PostAgendaTXT(message)
        return

    if message.content.startswith(prefix + "forceend"):
        if command.VerifyRole(message.author.id, message.guild.id, 1):
            await compilejson.MoveJSON(message.guild.id)
        else:
            await command.ErrorPrivilege(message)
        return

    if message.content.startswith(prefix + "delete"):
        await command.DeleteItems(message)

    if message.content.startswith(prefix + "addadmin"):
        if command.VerifyRole(message.author.id, message.guild.id, 0):
            await command.AddAdmin(message)
            return

    if message.content.startswith(prefix + "removeadmin"):
        if command.VerifyRole(message.author.id, message.guild.id, 0):
            await command.AddAdmin(message)
            return
# FINISH ME
# FINISH ME
# FINISH ME
    if message.content.startswith(prefix + "setchannel"):
        if command.VerifyRole(message.author.id, message.guild.id, 0):
            print("coming soon")
            return

    if message.content.startswith(prefix + "setprefix"):
        if command.VerifyRole(message.author.id, message.guild.id, 0):
            await command.SetPrefix(message)
            return

    if message.content.startswith("!!setprefix"):
        if command.VerifyRole(message.author.id, message.guild.id, 0):
            await command.SetPrefix(message)
            return

    if message.content.startswith(prefix + "viewadmins"):
        if command.VerifyRole(message.author.id, message.guild.id, 0):
            await command.ViewAdmins(message)
        return

    if message.content.startswith(prefix + "defaultchannel"):
        await command.ViewDefaultChannel(message)
        return

    if message.content.startswith(prefix + "setlevel"):
        await command.SetLevel(message)
        return

    if message.content.startswith(prefix + "view"):
        if message.channel.name == defaultRoom:
            await command.ViewAgenda(message)
        return

    if message.content.startswith(prefix + "clearserver"):
        if command.VerifyRole(message.author.id, message.guild.id, 0):
            database.ClearServer(message.guildid, message.guild.owner_id)

    if message.content.startswith(prefix + "help"):
        var = 0
        if command.VerifyRole(message.author.id, message.guild.id, 1):
            var = 1
        if command.VerifyRole(message.author.id, message.guild.id, 0):
            var = 2
        await helpmenu.HelpMenu(message, var)
        await command.MessageCleanup(message)
        return


@client.event
async def on_guild_join(var):
    id_exists = database.GetServer(var.id)
    if id_exists is False:
        database.SetServer(var.id, "agenda", "!!",
            var.owner_id)


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

TOKEN = os.environ.get("DISCORD_BOT_SECRET")
client.run(TOKEN)