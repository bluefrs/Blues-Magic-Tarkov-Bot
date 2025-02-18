# Blues-Magic-Tarkov-Bot
Twitch bot for getting Flea price info and Ammo damage data


Blues Magic Tarkov Bot Documentation
Overview
The Blues Magic Tarkov Bot is a Python-based bot designed to assist users with Tarkov game data, including ammo information and flea market prices. The bot can be run through a simple graphical user interface (GUI) built using Tkinter, and it uses a GraphQL API to retrieve the data. This bot allows users to query ammo information and flea market prices by using simple commands within Twitch chat.

Setup Instructions

1. Download and Installation
To install the Blues Magic Tarkov Bot, follow the steps below:
-For Windows Users:
 -Download the latest executable from the official release page or wherever it is hosted.
-Run the Executable:
 -The program is packaged as a standalone .exe file, so no installation of Python is necessary. Simply double-click the .exe file to start the bot.

2. Setting Up the Bot (GUI)
-Run the Executable:
 -In the GUI, you’ll see two input fields:
  -BOT Token: This is the OAuth token for your Twitch bot. You can get this from the Twitch OAuth Token Generator. https://twitchtokengenerator.com/
  -Channel Name: This is the Twitch channel that the bot will connect to.
-Start the Bot:
 -After filling in the BOT Token and Channel Name, click the Start Bot button to start the bot. The status will change to "Bot Started" and then to "Logged in as:<channel name>"
-Stop the Bot:
 -To stop the bot, click the Stop Bot button. The status will change to "Bot Stopped".

-Features
 -!ammo <ammo_name>: This command will return information about a ammo type, including damage, fragmentation chance, and penetration power. The ammo data is fetched from an embedded ammo_offsets.xlsx file that contains data on Tarkov ammo types.
  -NOTE: Currently the <ammo_name> is case sensitive and only works for the short name such as PS, BS, PPBS, etc. if any other info such as 7.62, 7.62x39, 7.62x39mm etc. is input then the output will be "Ammo type '<input>' not found in the database.".
  -Example command: !ammo PPBS
   -Response: 5.45x39mm PPBS gs Igolnik: Damage: 42, Penetration: 29, Fragmentation Chance: 23.0%
 -!flea <item_name>: This command will return the 24-hour average price and lowest available price for a specific item on the flea market. The data is fetched using the Tarkov API.
  -This command is not case sensitive and only requires 3 characters minimum.
  -Example command: !flea LEDX
   -Response: LEDX Skin Transilluminator 24A: ₽682,696 LowestOffer: ₽610,000
  -Example command with multiple results: !flea milk
   -Response1: Can of condensed milk 24A: ₽19,563 LowestOffer: ₽18,000 
   -Response2: Pack of milk 24A: ₽26,387 LowestOffer: ₽29,999 
   -Response3: Milkor M2A1 grenade launcher reflex sight 24A: ₽11,961 LowestOffer: ₽11,900
  -Example command with 5 or more responses: !flea M4A1
   -Response: Query too broad. Please be more specific

What Files/Folders Are Created
The Blues Magic Tarkov Bot creates a config file and 2 log files into C:\Users\<user>\Documents\Blues_Magic_Tarkov_Bot upon first run and logs will update during regular use.

1. Configuration File
-File Name: config.json
 -Location: Documents\Blues_Magic_Tarkov_Bot\config.json
 -Purpose: Stores the BOT Token and Channel Name for future use, so the bot doesn’t have to ask for them every time.

2. Log Files
-Normal Log File: normal_log.txt
 -Location: Documents\Blues_Magic_Tarkov_Bot\normal_log.txt
 -Purpose: Stores general logs of bot activities, such as successful queries and responses to commands.
-Error Log File: error_log.txt
 -Location: Documents\Blues_Magic_Tarkov_Bot\error_log.txt
 -Purpose: Stores error messages and issues encountered during bot operation, such as failed API requests or incorrect queries.

How the Bot Operates
-API: The bot uses the Tarkov API (GraphQL) to fetch flea market item prices and ammo stats. https://api.tarkov.dev/graphql
-Queries: The bot listens for commands in Twitch chat that begin with !ammo or !flea. When one of these commands is typed, the bot will query the appropriate data source.
-Logging: The bot logs all interactions in the normal_log.txt file and any errors in the error_log.txt file.
-Configuration: On the first run, the bot stores the BOT Token and Channel Name in config.json so you don’t have to enter them every time.

Troubleshooting
-Bot Not Starting
 -Ensure that you've entered a valid BOT Token and Channel Name.
  -If there’s an issue with the token, you may need to generate a new OAuth token from Twitch OAuth Token Generator.
-Bot Not Responding to Commands
 -Make sure the bot is correctly connected to the Twitch channel.
  -Verify that the bot has the appropriate permissions in the channel to read and respond to messages.
-Check the error_log.txt file for details on any issues.

Conclusion
The Blues Magic Tarkov Bot is a useful tool for Tarkov players, offering quick access to ammo stats and flea market prices. It features a simple, easy-to-use GUI and requires minimal setup. The bot is capable of running directly from an .exe file, creating essential configuration and log files for each user.

If you encounter any issues or have questions, please refer to the error_log.txt for more information or here for assistance. I am not sure how much i am going to be updating this.
