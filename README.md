# AgendaBot
AgendaBot is a simple bot designed to allow users who have access to an assigned discord channel to be able to view, modify and change an agenda.

## Dependencies
You will require the following Python 3.6.X or newer, pip3 and the following dependencies...
```
pip3 install python-dotenv discord.py
```
Also requires the following that should already be included with python
- os
- datetime
- json
- sqlite3

## Setup and Installation
To get setup and running you will need todo the following...
1. Create a discord bot, [follow this link](https://discordpy.readthedocs.io/en/latest/discord.html).
2. On Discord Developer -> Application -> Bot, you will need to enable SERVER MEMBERS INTENT and PRESENCE INTENT.
3. Download or clone the repo, preferably use a release build.
4. Navigate to the root file.
5. Copy all the files in the setup folder into the root directory.
6. Edit .env file and copy your bots secret id after the equals sign.
7. Ensure you have serverinfo.db file in the root directory, if not either download it or run ```git lfs pull```.
8. Start the bot with ```python3 agenda.py```
9. Invite the bot to your server.
10. Run !!help to get the bot command lists.

## Notice
This bot is not under active development, if you have an issue you can raise it however dont expect immediate support, otherwise you can contribute fixes and updates to the repo for review.

## Limitations
This was my first time designing a low server coupling bot, as in it could join any server and not be tied to it. In theory it can join, have its default values modified and this should have zero effect on any other server.

## Changes to be made
- Allow multiple agendas
- Post agenda on closing
