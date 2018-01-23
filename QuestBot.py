import discord
# import asyncio


client = discord.Client()


@client.event
async def on_ready():
    print('--QuestBot--')
    print('Logged in as: {0.display_name} ({0.id})'.format(client.user))
    print('------')
    client.logout()


@client.event
async def on_message(message: discord.Message):
    print('{0.id} {0.display_name}'.format(message.author))


# Add Discord Token
client.run()
