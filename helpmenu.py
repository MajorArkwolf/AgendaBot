import discord


async def HelpMenu(message, permission):
    messageUser = discord.Embed(title="Help Menu - Regular Commands", color=0x00ff00)
    var = "Remove all [] from commands, just used to depict data fields"
    messageUser.add_field(name="Information", value=var, inline=False)
    var = "Register the user into the database and “Name” will be what the server will identify them as.\n"
    var += "Example: !!register Peter"
    messageUser.add_field(name="!!register: [username]", value=var, inline=False)

    var = "Removes a user registered with the current discord ID from the database. Useful if you would like to reset the users name.\n"
    messageUser.add_field(name="!!unregister", value=var, inline=False)

    var = "The user who uses this command MUST be registered using the !!register “Name” command. Once this is done that user in the default channel will be able to add things onto the agenda.\n"
    messageUser.add_field(name="!!additem [message]", value=var, inline=False)

    var = "Will display a list of current items on the agenda with an index number you can attempt to modify.\n"
    messageUser.add_field(name="!!setlevel ", value=var, inline=False)

    var = "Replace index with a value you wish to change.\n"
    var += "Priorty sets how it will be displayed on the agenda.\n"
    var += "Priorty = 1: urgent and is placed at the top of the agenda.\n"
    var += "Priorty = 0: Set to this by default, means its placed into the middle of agenda in order of submission.\n"
    var += "Priorty = -1: places the item at the bottom of the agenda for when something needs to be bought up that is important to close on.\n"
    messageUser.add_field(name="!!setlevel [index] [priority]", value=var, inline=False)

    var = "Will post what is currently on the active agenda ordered in such a way that will be displayed once printed into a document.\n"
    messageUser.add_field(name="!!view", value=var, inline=False)

    var = "Will post a list of current agenda items which you may attempt to delete.\n"
    messageUser.add_field(name="!!delete", value=var, inline=False)

    var = "Placing an index number will attempt to delete an item from the agenda, permissions are required to delete other peoples items.\n"
    messageUser.add_field(name="!!delete [index number]", value=var, inline=False)

    var = "The bot will DM you the servers current registered channel.\n"
    messageUser.add_field(name="!!defaultchannel", value=var, inline=False)

    await message.author.send(embed=messageUser)
    if permission >= 1:
        messageUser = discord.Embed(title="Help Menu - Admin Commands", color=0x00ff00)

        var = "Creates a new agenda ONLY if no current agenda is active. 1 agenda per server. Date must be equal to or later than the current date. The date is the closed date for the agenda.\n"
        messageUser.add_field(name="!!create [DD/MM/YYYY]", value=var, inline=False)

        var = "Changes the current date of the agenda to the new one, date must be the same date or later than the current date. This date is the close date for the agenda.\n"
        messageUser.add_field(name="!!setdate [DD/MM/YYYY]", value=var, inline=False)

        var = "Ends the current active agenda and archives it, then it will post the ended agenda as a txt document into the default channel.\n"
        messageUser.add_field(name="!!end", value=var, inline=False)

        var = "Will forcibly move the current agenda and archive it, this will overwrite an archived agenda and once force ended will not be able to be converted into an agenda txt file.\n"
        messageUser.add_field(name="!!forceend", value=var, inline=False)

        await message.author.send(embed=messageUser)

    if permission >= 2:
        messageUser = discord.Embed(title="Help Menu - Super Admin Commands.", color=0x00ff00)

        var = "Clears all the data stored about the server in the database, used when discord server owner changes. This resets the server id and owner id and removes all admins, prefix and default channels.\n"
        messageUser.add_field(name="!!clearserver", value=var, inline=False)

        var = "This will allow you to add an admin to one of the 3 slots, number must be a number between 1 and 3 and the discord id must be taken via right clicking the user with developer mod on and pasting the id in like so.\n"
        var += "number is between 1 and 3, 1 is a super admin while 2 and 3 are regular admins."
        var += "Example: !!addadmin 2 574102412911181844"
        messageUser.add_field(name="!!addadmin [number] [discord id]", value=var, inline=False)

        var = "Displays the current 3 admins set on the server including ID and username if they are sit in the server.\n"
        messageUser.add_field(name="!!viewadmins", value=var, inline=False)

        var = "Will remove admin from that current index number.\n"
        var += "President = 1.\n Vice President = 2.\n Secretary = 3.\n"
        messageUser.add_field(name="!!removeadmin [number]", value=var, inline=False)

        await message.author.send(embed=messageUser)
