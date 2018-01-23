import datetime

import discord
from discord.ext.commands import Bot


fate_keeper = Bot(command_prefix="!", description='FATE-Keeper bot for working with FATE style RPs')
fate_aspects = {}


@fate_keeper.event
async def on_ready():
    print('Logged in as:')
    print('Username: ' + fate_keeper.user.name)
    print('ID: ' + fate_keeper.user.id)
    print('------')
    if not hasattr(fate_keeper, 'uptime'):
        fate_keeper.uptime = datetime.datetime.utcnow()

#
# @fate_keeper.command(pass_context=True)
# async def aspect(ctx, user: discord.Member, *, fate_aspect):
#     await fate_keeper.delete_message(ctx.message)
#     if user.name not in fate_aspects:
#         fate_aspects[user.name] = list()
#     if fate_aspect not in fate_aspects[user.name]:
#         fate_aspects[user.name].append(fate_aspect)
#         await fate_keeper.say('{0.display_name} gained {1}'.format(user, fate_aspect))
#
#
# @fate_keeper.command(pass_context=True)
# async def show(ctx, user: discord.Member):
#     await fate_keeper.delete_message(ctx.message)
#     for fate_aspect in fate_aspects[user.name]:
#         await fate_keeper.say(fate_aspect)


@fate_keeper.group(pass_context=True)
async def aspect(ctx):
    """Work with FATE style Aspects"""
    if ctx.invoked_subcommand is None:
        await fate_keeper.say('')


@aspect.command(pass_context=True)
async def room(ctx, *, fate_aspect=None):
    """Add or List FATE style Aspects for the room"""
    await fate_keeper.delete_message(ctx.message)
    if ctx.message.channel.id not in fate_aspects:
        fate_aspects[ctx.message.channel.id] = list()
    if fate_aspect is None:
        for fate_aspect in fate_aspects[ctx.message.channel.id]:
            await fate_keeper.say(fate_aspect)
    else:
        if fate_aspect not in fate_aspects[ctx.message.channel.id]:
            fate_aspects[ctx.message.channel.id].append(fate_aspect)
            await fate_keeper.say('{0} gained {1}'.format(ctx.message.channel.name, fate_aspect))


@aspect.command(pass_context=True)
async def char(ctx, user:discord.Member, *, fate_aspect=None):
    """Add or List FATE style Aspects for the chosen user"""
    await fate_keeper.delete_message(ctx.message)
    if user.name not in fate_aspects:
        fate_aspects[user.name] = list()
    if fate_aspect is None:
        for fate_aspect in fate_aspects[user.name]:
            await fate_keeper.say(fate_aspect)
    else:
        if fate_aspect not in fate_aspects[user.name]:
            fate_aspects[user.name].append(fate_aspect)
            await fate_keeper.say('{0.display_name} gained {1}'.format(user, fate_aspect))


fate_keeper.run('MjAzNjg1NjgzMTg4MDcyNDQ5.Cmsgkw.wzLh8dNAzUhdBmtCbRHAB6PUckI')