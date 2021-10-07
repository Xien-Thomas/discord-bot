import discord
import os
from dotenv import load_dotenv
client = discord.Client()

@client.event
async def on_member_join(member):
    await client.send_message(f"""Welcome to the server (member.mention)!""")

@client.event
async def on_ready():
    print('Hello {0.user}'.format(client))

@client.event
async def on_message(message):
    channels = ["promo-streams","youtube-videos","commands"]
    if message.author == client.user:
        return
    if meesage.channel in channels:
        if message.content.startswith('dps.commands'):
            await message.channel.send('Use the word \' dps \' follow by one of the command below')

        if message.content.startswith('dps.addYT'):
            await message.channel.send('Hello!')

        
# client.run(os.getenv('TOKEN'))
def main():
    load_dotenv()
    
    client.run(os.getenv('TOKEN'))
    print("Hello World")



if __name__ == "__main__":
    main()