import json
import os


def BuildFile(guildid):
    filepath = "./data/{}.json".format(guildid)
    with open(filepath, "r+") as jsonFile:
        data = json.load(jsonFile)

    datastring = "Agenda - {}/{}/{}.\n\n".\
        format(data['day'], data['month'], data['year'])

    counter = 0
    runningstring = ""
    for m in data['items']:
        if m['urgent'] == 1:
            counter = counter + 1
            runningstring += "{username}: {content}.\n".\
                format(content=m['content'], username=m['username'])
    if counter > 0:
        datastring += "URGENT:\n"
        datastring += runningstring

    counter = 0
    runningstring = ""
    for m in data['items']:
        if m['urgent'] == 0:
            counter = counter + 1
            runningstring += "{username}: {content}.\n".\
                format(content=m['content'], username=m['username'])
    if counter > 0:
        datastring += "\nMain:\n"
        datastring += runningstring

    counter = 0
    runningstring = ""
    for m in data['items']:
        if m['urgent'] == -1:
            counter = counter + 1
            runningstring += "{username}: {content}.\n".\
                format(content=m['content'], username=m['username'])
    if counter > 0:
        datastring += "\nLast on the Agenda:\n"
        datastring += runningstring

    datastring += "\nEND OF FILE\n"
    return datastring


def ExportToFile(runningstring, guildid):
    filepath = "./data/{}.txt".format(guildid)
    file = open(filepath, "w")
    file.write(runningstring)
    file.close()


def MoveJSON(guildid):
    src = "./data/{}.json".format(guildid)
    dst = "./data/{}.old".format(guildid)
    if os.path.isfile(dst):
        os.remove(dst)
    os.rename(src, dst)


def StartBuild(guildid):
    runningstring = BuildFile(guildid)
    ExportToFile(runningstring, guildid)
    MoveJSON(guildid)
