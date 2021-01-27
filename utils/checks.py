import discord
import os
from os import environ
from discord.ext import commands
from utils import default


owners = environ.get("DEVELOPERS")


def is_owner(ctx):
    """ Checks if the author is one of the owners """
    return ctx.author.id in owners


async def check_permissions(ctx, perms, *, check=all):
    """ Checks if author has permissions to a permission """
    if ctx.author.id in owners:
        return True

    resolved = ctx.channel.permissions_for(ctx.author)
    return check(getattr(resolved, name, None) == value for name, value in perms.items())


def has_permissions(*, check=all, **perms):
    """ discord.Commands method to check if author has permissions """
    async def pred(ctx):
        return await check_permissions(ctx, perms, check=check)
    return commands.check(pred)