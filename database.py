import sqlite3
from sqlite3 import Error

db_file = "serverinfo.db"

try:
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    print("Connected to SQL")
except Error as e:
    print(e)


def GetServer(guildid):
    c.execute("SELECT * FROM {tn} WHERE {idf}={my_id}".\
        format(tn="server", idf="ID", my_id=guildid))
    return c.fetchone()


def ClearServer(guildid, ownerid):
    c.execute("INSERT INTO server (id, DefaultChannel, Prefix, OwnerID) VALUES ({id}, {cname}, {pfix} , {ownerid})".\
        format(id=guildid, cname="agenda", pfix="!!", ownerid=ownerid))
    conn.commit()


def SetServer(guildid, channelname, prefix, ownerid):
    c.execute("INSERT INTO server (id, DefaultChannel, Prefix, OwnerID) VALUES ({id}, {cname}, {pfix} , {ownerid})".\
        format(id=guildid, cname=channelname, pfix=prefix, ownerid=ownerid))
    conn.commit()


def FindUser(id):
    c.execute("SELECT * FROM {tn} WHERE {idf}={my_id}".\
            format(tn='users', idf='UserID', my_id=id))
    return c.fetchone()


def SetPrefix(prefix, server):
    input = "'{}'".format(prefix)
    var = "UPDATE server SET Prefix = {data} WHERE ID = {serverid}".format(data=input, serverid=server)
    c.execute(var)
    conn.commit()


def SetDefaultChannel(channel, server):
    input = "'{}'".format(channel)
    var = "UPDATE server SET DefaultChannel = {data} WHERE ID = {serverid}".format(data=input, serverid=server)
    c.execute(var)
    conn.commit()


def AddAdmin(id, role, server):
    var = "UPDATE server SET {role2} = {userid} WHERE ID = {serverid}".format(role2=role, userid=id, serverid=server)
    c.execute(var)
    conn.commit()


def RemoveAdmin(role, server):
    var = "UPDATE server SET {role2} = {userid} WHERE ID = {serverid}".format(role2=role, userid='null', serverid=server)
    c.execute(var)
    conn.commit()


def InsertUser(userid, name):
    input = "'{}'".format(name)
    var = "INSERT INTO {tn} ({col0}, {col1}) VALUES ({id}, {user})".\
        format(tn='users', col0='UserID', col1='Username', id=userid, user=input)
    c.execute(var)
    conn.commit()


def RemoveUser(userid):
    c.execute("DELETE FROM users WHERE UserID = {0}".format(userid))
    conn.commit()
