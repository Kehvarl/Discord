import datetime
import random
import discord
from discord.ext.commands import Bot

amor_manager = Bot(command_prefix="!", description='Do cool things for AMOR')


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


@amor_manager.command(pass_context=True)
async def botname(ctx, *, new_name=None):
    if ctx.message.channel.name.lower() not in bot_channels:
        return

    member_roles = ctx.message.author.roles
    member_admin = discord.utils.find(lambda r: r.name.lower() in admin_roles, member_roles)
    if member_admin is not None:
        bot_member = discord.utils.find(lambda m: m.id == amor_manager.user.id, ctx.message.server.members)
        await amor_manager.change_nickname(bot_member, new_name)


@amor_manager.command(pass_context=True)
async def nogroup(ctx):
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
    if ctx.message.channel.name.lower() not in bot_channels:
        return

    # Can't be group-less
    if new_group is None:
        new_group = random.choice(changeable_groups)
    new_group = new_group.lower()
    author = ctx.message.author
    roles = author.roles
    server_roles = ctx.message.server.roles

    # Clear the ugly command away
    # await amor_manager.delete_message(ctx.message)

    if new_group in changeable_groups:
        # Remove the old group the user was in
        for role in roles:
            if role.name.lower() in changeable_groups:
                roles.remove(role)
        # Get the proper object for the user's new group
        role = discord.utils.find(lambda r: r.name.lower() == new_group, server_roles)
        if role is not None:
            roles.append(role)
            await(amor_manager.replace_roles(author, *roles))
            await amor_manager.say('{0} moved to group {1}'.format(author.name, new_group))
    else:
        suggest = random.choice(changeable_groups)
        await amor_manager.say("`{0}` is not a color group you're allowed to join.   Why not try `{1}`".format(new_group, suggest))



