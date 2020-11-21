from classes.disc import Client
import sys

# https://discordapp.com/api/oauth2/authorize?client_id=779439176411381800&permissions=1074265152&scope=bot
if len(sys.argv) == 2:
    Client().run(sys.argv[1])
else:
    print('Error. Usage: python3.6 <YOUR_BOT_TOKEN>')