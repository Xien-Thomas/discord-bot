import discord
import os
from dotenv import load_dotenv
client = discord.Client()


@client.event
async def on_ready():
    print('Hello {0.user}'.format(client))

# client.run(os.getenv('TOKEN'))
def main():
    load_dotenv()
    
    client.run(os.getenv('TOKEN'))
    print("Hello World")



if __name__ == "__main__":
    main()