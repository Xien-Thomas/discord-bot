import discord
import json

import os
from discord.ext import tasks, commands
from dotenv import load_dotenv
from twitchAPI.twitch import Twitch
from discord.utils import get

intents = discord.Intents.all()
client = commands.Bot(command_prefix = 'dps.', intents = intents)

# Authentication with Twitch API.
client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('SECRET')
twitch = Twitch(client_id, client_secret)
twitch.authenticate_app([])
TWITCH_STREAM_API_ENDPOINT_V5 = "https://api.twitch.tv/kraken/streams/{}"
API_HEADERS = {
    'Client-ID': client_id,
    'Accept': 'application/vnd.twitchtv.v5+json',
}

def checkuser(user):
    try:
        userid = twitch.get_users(logins=[user])['data'][0]['id']
        url = TWITCH_STREAM_API_ENDPOINT_V5.format(userid)
        try:
            req = requests.Session().get(url, headers=API_HEADERS)
            jsondata = req.json()
            if 'stream' in jsondata:
                if jsondata['stream'] is not None:
                    return True
                else:
                    return False
        except Exception as e:
            print("Error checking user: ", e)
            return False
    except IndexError:
        return False

@client.event
async def on_member_join(member):
    await client.send_message(f"""Welcome to the server (member.mention)!""")

@client.event
async def on_message(message):
    channels = ["promo-streams","youtube-videos","commands"]
    if message.author == client.user:
        return
    if message.channel in channels:
        if message.content.startswith('dps.commands'):
            await message.channel.send('Use the word \' dps \' follow by one of the command below')

        if message.content.startswith('dps.addYT'):
            await message.channel.send('Hello!')

@client.event
async def on_ready():
    print('Loading streamers now ...')
    live_notifs_loop.start()
    #Search for streamers online every 10 secs
    
@tasks.loop(seconds=10)
async def live_notifs_loop():
    #open json file
    with open('streamers.json', 'r') as file:
        streamers = json.loads(file.read())

    if streamers is not None:
        guild_discord = client.get_guild(748008969154592828)
        channel = client.get_channel(819447435226251274)
        role = get(guild_discord.roles, id = 851483543900913775)

        for user_id, twitch_name in streamers.items():
            #status checks 'are they live?'
            status = checkuser(twitch_name)

            user = client.get_user(int(user_id))

            if status is True:
                async for message in channel.history(limit=200):
                    if str(user.mention) in message.context and "is now streaming" in message.context:
                        break
                    else:
                        async for member in guild_discord.fetch_members(limit=None):
                            if member.id == int(user_id):
                                await member.add_roles(role)
                        
                        await channel.send(
                            f":red_circle: **LIVE**\n{user.mention} is now strreaming on Twitch!"
                            f"\nhttps://www.twitch.tv/{twitch_name}"
                        )
                        print(f"{user} started streaming. sending notification.")
                        break
            else:
                async for member in guild_discord.fetch_members(limit=None):
                    if member.id == int(user_id):
                        await member.remove(role)
                async for message in channel.history(limit=200):
                    if str(user.mention) in message.content and "is now streaming" in message.content:
                            await message.delete()

# Command to add Twitch usernames to the json.
@client.command(name='addtwitch', help='Adds your Twitch to the live notifs.', pass_context=True)
async def add_twitch(ctx, twitch_name):
    # Opens and reads the json file.
    with open('streamers.json', 'r') as file:
        streamers = json.loads(file.read())
    
    # Gets the users id that called the command.
    user_id = ctx.author.id
    # Assigns their given twitch_name to their discord id and adds it to the streamers.json.
    streamers[user_id] = twitch_name
    
    # Adds the changes we made to the json file.
    with open('streamers.json', 'w') as file:
        file.write(json.dumps(streamers))
    # Tells the user it worked.
    await ctx.send(f"Added {twitch_name} for {ctx.author} to the notifications list.")


def main():
    load_dotenv()
    
    client.run(os.getenv('TOKEN'))
    print("Hello World")



if __name__ == "__main__":
    main()