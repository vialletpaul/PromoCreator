# -*- coding: utf-8  -*-

import discord
import json
from discord.ext import commands

version = "0.1"

description = "PromoCreator allow you to initialize a discord server for your school on the EPITA's 2023 template"

bot = commands.Bot(command_prefix="//", description=description)

roles = []
categories = []


def get_role(server_roles, name):
    for e in server_roles:
        if e.name == name:
            return e


def get_category(server_channels, name):
    for e in server_channels:
        if e.name == name:
            return e


def get_permissions(category, guild):
    permissions = {}
    for permission in category["permissions"]:
        role = get_role(guild.roles, permission["role"])
        permissions[role] = {}

        for perm, value in permission["permissions"].items():
            permissions[role][perm] = bool(value)

        permissions[role] = discord.PermissionOverwrite(**permissions[role])
    return permissions


@bot.event
async def on_ready():
    global roles, categories
    print('Loading roles JSON...')
    with open('json/roles.json') as j:
        roles = json.load(j)["roles"]
    with open('json/channels.json') as j:
        categories = json.load(j)["categories"]


@bot.command(pass_context=True)
async def create_roles(ctx: commands.context.Context):
    guild = ctx.message.guild
    print("===Roles Creation===")
    for role in roles:
        color = discord.Colour.default()
        permissions = discord.Permissions(int(role["permissions"]))
        hoist = False
        mentionable = True

        if role["color"]:
            color = eval("discord.Colour." + role["color"] + "()")
        if role["mentionable"]:
            mentionable = eval(role["mentionable"])
        if role["hoist"]:
            hoist = eval(role["hoist"])

        print("Role added: " + role["name"])

        await guild.create_role(name=role["name"], colour=color, permissions=permissions, hoist=hoist,
                                mentionable=mentionable)


@bot.command(pass_context=True)
async def create_channels(ctx: commands.context.Context, log=False):
    if log:  # TODO: logging using logger
        await ctx.send("Log is enable will narrate my process")
    guild = ctx.message.guild
    print("Channel Creation")
    for category in categories:

        if log:
            await ctx.send("Creating a new category: " + category["name"])
        permissions = get_permissions(category, guild)

        name = category["name"]

        await guild.create_category(name, overwrites=permissions)

        if log:
            await ctx.send("Creation success, I will now create sub-channels !")
        for chan in category["channels"]:
            if log:
                await ctx.send("Creating a new channel: " + chan["name"])
            permissions = get_permissions(chan, guild)
            await guild.create_text_channel(chan["name"], overwrites=permissions,
                                            category=get_category(guild.channels, name))
        if log:
            await ctx.send("Creation success, jumping to next one !")

    await ctx.send("Operation success")
bot.run(token)
