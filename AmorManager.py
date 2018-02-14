import datetime
import random
import discord
from discord.ext.commands import Bot

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


@amor_manager.event
async def on_ready():
    print('Logged in as:')
    print('Username: ' + amor_manager.user.name)
    print('ID: ' + amor_manager.user.id)
    print('------')
    if not hasattr(amor_manager, 'up_time'):
        amor_manager.up_time = datetime.datetime.utcnow()
    server = next(iter(amor_manager.servers))
    channel = discord.utils.find(lambda c: c.name.lower() == "bot_commands", server.channels)
    await amor_manager.send_message(channel, "`Has logged in`")


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
    await amor_manager.say('{0} removed from color groups'.format(author.display_name))


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
        await amor_manager.say("You must be a member of the {0} role to join a color group".format(required_role.title()))
        return

    if new_group in changeable_groups:
        # Remove the old group the user was in
        new_roles = [r for r in member_roles if not r.name.lower() in changeable_groups]
        # Get the proper object for the user's new group
        role = discord.utils.find(lambda r: r.name.lower() == new_group, server_roles)
        if role is not None:
            new_roles.append(role)
            await(amor_manager.replace_roles(author, *new_roles))
            await amor_manager.say('{0} moved to group {1}'.format(author.display_name, new_group))
    else:
        suggest = random.choice(changeable_groups)
        await amor_manager.say("`{0}` is not a color group you're allowed to join.   Why not try `{1}`".format(new_group, suggest))



