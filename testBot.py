import asyncio
import json
import random
import urllib.request

import discord

client = discord.Client()

drink_image = "**{0[strDrink]}** {0[strDrinkThumb]}"
drink_format = "{} provides {} with a {}"
api_drink = 'http://www.thecocktaildb.com/api/json/v1/1/random.php'
api_drink_i = "http://www.thecocktaildb.com/api/json/v1/1/filter.php?i={}"
api_drink_s = "http://www.thecocktaildb.com/api/json/v1/1/search.php?s={}"

dances = [
    "{} grabs {} and proceeds to tango!",
    "{} waltzes with {}",
    "{} shows off on the dance floor"
]


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    tmp = client.get_all_channels()
    for chan in tmp:
        print(chan.server, chan.name, chan.type)
    print('------')


@client.event
async def on_message(message):
    if message.content.startswith('!Kehv count'):
        counter = 0
        tmp = await client.send_message(message.channel, 'Calculating messages...')
        async for log in client.logs_from(message.channel, limit=100):
            if log.author == message.author:
                counter += 1
        await client.edit_message(tmp, 'You have {} message.'.format(counter))
    elif message.content.startswith('!Kehv dance'):
        await client.send_message(message.channel,
                                  random.choice(dances).format(client.user.name,
                                                               message.author.name))
    elif message.content.startswith('!Kehv sleep'):
        tmp = await client.send_message(message.channel, 'ZZZ..')
        delay = random.randint(3, 7)
        for num in range(1, delay):
            await asyncio.sleep(1)
            await  client.edit_message(tmp, "...ZzZ...")
        await  client.edit_message(tmp, "...Zz... Huh?  I'm awake!")
    elif message.content.startswith('!bar'):
        await client.send_message(message.channel, "Hey {}! What can I get for you?".format(message.author.name))
        await client.delete_message(message)

        def drink_check(m):
            return True # len(m) > 0

        order = await client.wait_for_message(timeout=10.0, author=message.author,
                                              check=drink_check)
        if order is None:
            await client.send_message(message.channel, 'Sorry, you too too long to order.')
            return
        if 'with' in order.content:
            ingredient = next_word('with', order.content)
            with urllib.request.urlopen(api_drink_i.format(ingredient)) as response:
                drink_data = response.read().decode('utf-8')
                drinks = json.loads(drink_data)['drinks']
                drink = random.choice(drinks)
                await client.send_message(message.channel,
                                          drink_format.format(client.user.name,
                                                              message.author.name,
                                                              drink_image.format(drink)))
        elif 'anything' in order.content \
                or 'surprise me' in order.content:
            with urllib.request.urlopen(api_drink) as response:
                drink_data = response.read().decode('utf-8')
                drink = json.loads(drink_data)['drinks'][0]
                await client.send_message(message.channel,
                                          drink_format.format(client.user.name,
                                                              message.author.name,
                                                              drink_image.format(drink)))
        else:
            with urllib.request.urlopen(api_drink_s.format(order.content.replace(" ", "_"))) as response:
                drink_data = response.read().decode('utf-8')
                drink = json.loads(drink_data)['drinks'][0]
                await client.send_message(message.channel,
                                          drink_format.format(client.user.name,
                                                              message.author.name,
                                                              drink_image.format(drink)))


def next_word(target, source):
    sl = source.split()
    for index, word in enumerate(sl):
        if word == target:
            return sl[index + 1]

# Add Discord Token
client.run()
