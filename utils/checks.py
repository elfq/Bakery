import discord
import os
from os import environ
from discord.ext import commands


owners = 738604939957239930


def is_owner(ctx):
    return ctx.author.id in owners
