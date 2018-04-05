import datetime
import random
import discord
import json
from discord.ext.commands import Bot
from credentials import Credentials

amor_manager = Bot(command_prefix="!", description='Do cool things for AMOR')


required_role = "amor citizen"

admin_roles = [
    "dragon",
    "sovereign",
    "royal guard"
]

changeable_groups = [
    "roc",
    "manticore",
    "griffin",
    "wyvern",
    "kraken",
    "unicorn",
    "basilisk",
    "ash",
    "moon",
    "owl"
]

bot_channels = [
    "science",
    "bot_commands"
]

tod_channels = [
    "hideyourscreen",
    "bot_commands"
]

user_tags = {}

tod_games = {}


@amor_manager.event
async def on_ready(announce=False):
    print('Logged in as:')
    print('Username: ' + amor_manager.user.name)
    print('ID: ' + amor_manager.user.id)
    print('------')
    if not hasattr(amor_manager, 'up_time'):
        amor_manager.up_time = datetime.datetime.utcnow()
    server = next(iter(amor_manager.servers))
    if announce:
        channel = discord.utils.find(lambda c: c.name.lower() == "bot_commands", server.channels)
        await amor_manager.send_message(channel, "`Has logged in`")


@amor_manager.listen()
async def on_message(message):
    if message.author.bot:
        return

    if message.channel.is_private:
        return

    if message.channel.name.lower() not in bot_channels:
        pass

    if not message.content.startswith(amor_manager.command_prefix):
        # await self._check_for_reactions(message)
        if "#" in message.content:
            tags = [t for t in message.content.split() if "#" in t[0:1]]
            for tag in tags:
                if not user_tags.get(message.author.name):
                    user_tags[message.author.name] = {'name': message.author.display_name, 'tags': {}}
                if not user_tags[message.author.name]['tags'].get(tag):
                    user_tags[message.author.name]['tags'][tag] = 0
                user_tags[message.author.name]['tags'][tag] += 1
                user_tags[message.author.name]['name'] = message.author.display_name
                print(user_tags[message.author.name]['name'], ":", json.dumps(user_tags[message.author.name]['tags']))


@amor_manager.command(pass_context=True)
async def mytags(ctx):
    """
    View the tags you've used since the last bot restart
    """
    if ctx.message.channel.name.lower() not in bot_channels:
        return
    display = ctx.message.author.display_name
    display_tags = []
    if not user_tags.get(ctx.message.author.name, None):
        return
    for tag_key, tag_count in user_tags[ctx.message.author.name]['tags'].items():
        display_tags.append("{0} ({1})".format(tag_key, tag_count))
    await amor_manager.say("{0}'s tag usage: \n ```{1}```".format(display, "\n".join(display_tags)))


@amor_manager.command(pass_context=True)
async def botname(ctx, *, new_name=None):
    """
    Restricted to admins.
    Change the bot's nickname on this server
    """
    if ctx.message.channel.name.lower() not in bot_channels:
        return

    member_roles = ctx.message.author.roles
    member_admin = discord.utils.find(lambda r: r.name.lower() in admin_roles, member_roles)
    if member_admin is not None:
        bot_member = discord.utils.find(lambda m: m.id == amor_manager.user.id, ctx.message.server.members)
        await amor_manager.change_nickname(bot_member, new_name)


@amor_manager.command(pass_context=True)
async def vouch(ctx, *, member_name=None):
    if ctx.message.channel.name.lower() not in bot_channels:
        return

    server = ctx.message.server
    member_roles = ctx.message.author.roles
    member_admin = discord.utils.find(lambda r: r.name.lower() in admin_roles, member_roles)
    if member_admin is not None:
        member = discord.utils.find(lambda c: c.name.lower() == member_name.lower(), server.members)
        roles = member.roles
        new_role = discord.utils.find(lambda r: r.name.lower() == required_role, server.roles)
        roles.append(new_role)
        await amor_manager.replace_roles(member, *roles)
        await amor_manager.say('{0} granted citizenship'.format(member.name))


@amor_manager.command(pass_context=True)
async def nogroup(ctx):
    """
    Remove yourself from all color groups (Back to pink)
    """
    if ctx.message.channel.name.lower() not in bot_channels:
        return

    author = ctx.message.author
    roles = author.roles
    for role in roles:
        if role.name.lower() in changeable_groups:
            roles.remove(role)
    await amor_manager.replace_roles(author, *roles)
    await amor_manager.say('{0} removed from color groups'.format(author.name))


@amor_manager.command(pass_context=True)
async def group(ctx, *, new_group=None):
    """
    Place yourself in the specified color group.  Leave new_group blank for a random assignment.
    Allowed Color Groups:
    Roc = Red
    Manticore = Orange
    Griffin = Gold
    Wyvern = Green
    Kraken = Blue
    Unicorn = Pinkish
    Basilisk = Grey
    Ash = Light Grey
    Moon = Light Blue
    Owl = Tan
    """
    if ctx.message.channel.name.lower() not in bot_channels:
        return

    # Can't be group-less
    if new_group is None:
        new_group = random.choice(changeable_groups)
    new_group = new_group.lower()
    author = ctx.message.author
    member_roles = author.roles
    server_roles = ctx.message.server.roles

    member_allowed = discord.utils.find(lambda r: r.name.lower() == required_role, member_roles)

    if not member_allowed:
        need_citizen = "You must be a member of the {0} role to join a color group"
        await amor_manager.say(need_citizen.format(required_role.title()))
        return

    if new_group in changeable_groups:
        # Remove the old group the user was in
        new_roles = [r for r in member_roles if not r.name.lower() in changeable_groups]
        # Get the proper object for the user's new group
        role = discord.utils.find(lambda r: r.name.lower() == new_group, server_roles)
        if role is not None:
            new_roles.append(role)
            await(amor_manager.replace_roles(author, *new_roles))
            await amor_manager.say('{0} moved to group {1}'.format(author.name, new_group))
    else:
        suggest = random.choice(changeable_groups)
        cant_join = "`{0}` is not a color group you're allowed to join.   Why not try `{1}`"
        await amor_manager.say(cant_join.format(new_group, suggest))


@amor_manager.command(pass_context=True)
async def date(ctx):
    d0 = datetime.date(1993, 9, 1)
    d1 = datetime.date.today()
    delta = d1 - d0
    day = ordinal(delta.days + 1)
    september_strings = [
        "Today is the {} of September, 1993!",
        "It is {} September, 1993.",
        "I greet you on this day: September the {} 1993.",
        "The {} day of The September That Never Ends.",
        "Eternal September: {} day and counting."
    ]
    await amor_manager.say(random.choice(september_strings).format(day))


@amor_manager.command(pass_context=True)
async def roll(ctx, *, dice: str):
    if ctx.message.channel.name.lower() not in bot_channels:
        return

    """Rolls a dice in NdN format."""
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await amor_manager.say('Format has to be in NdN!')
        return

    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await amor_manager.say(result)


@amor_manager.group(pass_context=True)
async def tod(ctx):
    """Truth Or Dare"""
    if ctx.invoked_subcommand is None:
        pass


@tod.command(pass_context=True)
async def new(ctx):
    if ctx.message.channel.name.lower() not in tod_channels:
        return

    room = ctx.message.channel.name.lower()
    host = ctx.message.author
    if room not in tod_games:
        tod_games[room] = {'host': host.name, 'host_id': host.name, 'participants': {}, 'last': None}
        await amor_manager.say("New Game of Truth Or Dare started in {}".format(room))
    else:
        host = tod_games[room]['host']
        await amor_manager.say("Truth or Dare already in progress in {}.  Game host: {}".format(room, host))


@tod.command(pass_context=True)
async def end(ctx):
    if ctx.message.channel.name.lower() not in tod_channels:
        return

    room = ctx.message.channel.name.lower()
    if room not in tod_games:
        await amor_manager.say("Truth Or Dare not in progress in {}".format(room))
    else:
        host = tod_games[room]['host']
        await amor_manager.say("Game Over in {}!  Thank you to {} for hosting this game!".format(room, host))
        del tod_games[room]


@tod.command(pass_context=True)
async def join(ctx):
    if ctx.message.channel.name.lower() not in tod_channels:
        return

    room = ctx.message.channel.name.lower()
    if room not in tod_games:
        await amor_manager.say("Truth Or Dare not in progress in {}".format(room))
    else:
        player = ctx.message.author.name
        tod_games[room]['participants'][player.lower()] = {'spins': 0}
        await amor_manager.say("{} has joined Truth or Dare!".format(player))


@tod.command(pass_context=True)
async def leave(ctx):
    if ctx.message.channel.name.lower() not in tod_channels:
        return

    room = ctx.message.channel.name.lower()
    if room not in tod_games:
        await amor_manager.say("Truth Or Dare not in progress in {}".format(room))
    else:
        player = ctx.message.author.name
        if player not in list(tod_games[room]['participants'].keys()):
            await amor_manager.say("{}, you cannot leave the game if you have not joined".format(player))
        else:
            del tod_games[room]['participants'][player.lower()]
            await amor_manager.say("{} has left Truth or Dare.".format(player))


@tod.command(pass_context=True)
async def spin(ctx):
    if ctx.message.channel.name.lower() not in tod_channels:
        return

    room = ctx.message.channel.name.lower()
    if room not in tod_games:
        await amor_manager.say("Truth Or Dare not in progress in {}".format(room))
    else:
        participants = list(tod_games[room]['participants'].keys())
        player = ctx.message.author.name
        spin = random.choice(participants)
        if spin == player.lower() or spin == tod_games[room]['last'].lower():
            spin = random.choice(participants)
        tod_games[room]['last'] = player
        tod_games[room]['current'] = spin
        tod_games[room]['participants'][player.lower()]['spins'] += 1
        await amor_manager.say("{0} has spun {1}!  {1}, Truth or Dare?".format(player, spin))


@tod.command(pass_context=True)
async def turn(ctx):
    if ctx.message.channel.name.lower() not in tod_channels:
        return

    room = ctx.message.channel.name.lower()
    if room not in tod_games:
        await amor_manager.say("Truth Or Dare not in progress in {}".format(room))
    else:
        await amor_manager.say("Current Player is {}".format(tod_games[room]['current']))


SUFFIXES = {1: 'st', 2: 'nd', 3: 'rd'}


def ordinal(num):
    # I'm checking for 10-20 because those are the digits that
    # don't follow the normal counting scheme.
    if 10 <= num % 100 <= 20:
        suffix = 'th'
    else:
        # the second parameter is a default.
        suffix = SUFFIXES.get(num % 10, 'th')
    return str(num) + suffix


amor_manager.run(Credentials.amor)
