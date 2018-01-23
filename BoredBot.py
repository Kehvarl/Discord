import discord
# import asyncio
import re
import random
import datetime


client = discord.Client()

allowed_channels = [
    "general",
    "main", "main-overflow1", "main-overflow2",
    "nsfw"
]

bored = [
    "{0.mention}, what do you mean bored? Go try {1}",
    "Well, {0.mention}, what do you intend to do about that? Maybe... {1}",
    "Bah!  With all the things you could be doing, {0.mention}? I mean, there's {1}",
    "{0.mention}, did you make your posts yet? And if you have, have you tried {1}"
]

links = [
    'https://www.iwakuroleplay.com/forums/roleplay-help-discussion.277/',
    'https://www.iwakuroleplay.com/forums/roleplay-mechanics.242/',
    'https://www.iwakuroleplay.com/forums/developing-characters-cultures.382/',
    'https://www.iwakuroleplay.com/forums/creating-worlds-settings.383/',
    'https://www.iwakuroleplay.com/forums/refining-writing.304/',
    'https://www.iwakuroleplay.com/forums/character-portrait-studio.198/',
]

bard = {
    'prefix': 'Thou',
    'a': ["artless", "bawdy", "beslubbering", "bootless", "churlish",
          "cockered", "clouted", "craven", "currish", "dankish",
          "dissembling", "droning", "errant", "fawning", "fobbing",
          "froward", "frothy", "gleeking", "goatish", "gorbellied",
          "impertinent", "infectious", "jarring", "loggerheaded",
          "lumpish", "mammering", "mangled", "mewling", "paunchy",
          "pribbling", "puking", "puny", "quailing", "rank", "reeky",
          "roguish", "ruttish", "saucy", "spleeny", "spongy",
          "surly", "tottering", "unmuzzled", "vain", "venomed",
          "villainous", "warped", "wayward", "weedy", "yeasty"],
    'b': ["base-court", "bat-fowling", "beef-witted",
          "beetle-headed", "boil-brained", "clapper-clawed",
          "clay-brained", "common-kissing", "crook-pated",
          "dismal-dreaming", "dizzy-eyed", "doghearted",
          "dread-bolted", "earth-vexing", "elf-skinned",
          "fat-kidneyed", "fen-sucked", "flap-mouthed", "fly-bitten",
          "folly-fallen", "fool-born", "full-gorged", "guts-griping",
          "half-faced", "hasty-witted", "hedge-born", "hell-hated",
          "idle-headed", "ill-breeding", "ill-nurtured",
          "knotty-pated", "milk-livered", "motley-minded",
          "onion-eyed", "plume-plucked", "pottle-deep",
          "pox-marked", "reeling-ripe", "rough-hewn",
          "rude-growing", "rump-fed", "shard-borne",
          "sheep-biting", "spur-galled", "swag-bellied",
          "tardy-gaited", "tickle-brained", "toad-spotted",
          "urchin-snouted", "weather-bitten"],
    'c': ["apple-john", "baggage", "barnacle", "bladder", "boar-pig",
          "bugbear", "bum-bailey", "canker-blossom", "clack-dish",
          "clotpole", "coxcomb", "codpiece", "death-token",
          "dewberry", "flap-dragon", "flax-wench", "flirt-gill",
          "foot-licker", "fustilarian", "giglet", "gudgeon",
          "haggard", "harpy", "hedge-pig", "horn-beast",
          "hugger-mugger", "jolthead", "lewdster", "lout",
          "maggot-pie", "malt-worm", "mammet", "measle", "minnow",
          "miscreant", "moldwarp", "mumble-news", "nut-hook",
          "pigeon-egg", "pignut", "puttock", "pumpion", "ratsbane",
          "scut", "skainsmate", "strumpet", "varlet", "vassal",
          "whey-face", "wagtail"]
}

bad = {
    'prefix': 'You Are Such A',
    'a': ["Lazy", "Stupid", "Insecure", "Idiotic", "Slimy", "Slutty",
          "Smelly", "Pompous", "Communist", "Dicknose", "Pie-Eating",
          "Racist", "Elitist", "White Trash", "Drug-Loving", "Butterface",
          "Tone Deaf", "Ugly", "Creepy"],
    'b': ["Douche", "Ass", "Turd", "Rectum", "Butt", "Cock", "Shit",
          "Crotch", "Bitch", "Prick", "Slut", "Taint", "Fuck", "Dick",
          "Boner", "Shart", "Nut", "Sphincter"],
    'c': ["Pilot", "Canoe", "Captain", "Pirate", "Hammer", "Knob", "Box",
          "Jockey", "Nazi", "Waffle", "Goblin", "Blossom", "Biscuit",
          "Clown", "Socket", "Monster", "Hound", "Balloon"]
}

pattern_bored = re.compile('[Bb]+[Oo]+[Rr]+[Ee]+[Dd]+')

pattern_bard = re.compile('[Bb]+[Aa]+[Rr]+[Dd]+')

pattern_hard = re.compile('[Hh]+[Aa]+[Rr]+[Dd]+')

pattern_bad = re.compile('[Bb]+[Aa]+[Dd]+')


@client.event
async def on_ready():
    print('--QuestBot--')
    print('Logged in as: {0.display_name} ({0.id})'.format(client.user))
    tmp = client.get_all_channels()
    print('Channels Available To Me:')
    for chan in tmp:
        print(chan.server, chan.name, chan.type)
    print('------')


@client.event
async def on_message(message: discord.Message):
    if message.author.id != client.user.id and message.channel.name in allowed_channels:
        if pattern_bored.search(message.content):
            print("{0.display_name} was bored at {1} in {2}".format(message.author,
                                                                    datetime.datetime.now().time().isoformat(),
                                                                    message.channel.name))
            response = random.choice(bored)
            link = random.choice(links)
            await client.send_message(message.channel, response.format(message.author, link))
        elif pattern_bard.search(message.content):
            await client.send_message(message.channel, insult(bard))
        elif pattern_bad.search(message.content):
            await client.send_message(message.channel, insult(bad))
        elif pattern_hard.search(message.content):
            await client.send_message(message.channel, insult(bad))


def insult(source=bard):
    if source is None:
        return "Error"
    return "{} {} {} {}!".format(source['prefix'],
                                 random.choice(source['a']),
                                 random.choice(source['b']),
                                 random.choice(source['c']))

# Add Discord Token
client.run()

