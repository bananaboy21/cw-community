import discord
import os
import io
import traceback
import sys
import asyncio
import random
import aiohttp
import random
from discord.ext import commands
bot = commands.Bot(command_prefix=commands.when_mentioned_or('c.'),description="A specialized bot made for Balkan War Community\n\nHelp Commands",owner_id=277981712989028353)
bot.remove_command("help")



@bot.event
async def on_ready():
    print('Bot is online, and ready to ROLL!')
    await bot.change_presence(game=discord.Game(name="c.help"))


@bot.command()
async def help(ctx):
	color = discord.Color(value=0x00ff00)
	em = discord.Embed(color=color, title="Balkan War Community Bot Help")
	em.add_field(name='ping', value="Gets the bot's websocket latency.")
	em.add_field(name='invite', value='Gets an invite link to add the bot to your server!')
	em.add_field(name='kick [mention user]', value='Kicks a member. Requires the Kick Members permission.')
	em.add_field(name='ban [mention user]', value='Bans a member. Requires the Ban Members permission.')
	em.add_field(name='purge [number of msgs]', value='Deletes a number of messages. Requires the Manage Messages permission.')
	em.add_field(name='mute [mention user]', value='Stops a user from sending messages to the channel. Requires the Ban Members permission.')
	em.add_field(name='unmute [mention user]', value='Allows the user to send messages to the channel, if they were previously muted. Requires the Ban Members permission.')
	em.set_thumbnail(url="https://media.discordapp.net/attachments/417802059610456084/417806626599206912/JPEG_20180226_222959.jpg")
	await ctx.send(embed=em)


@bot.command()
async def ping(ctx):
    """Premium ping pong giving you a websocket latency."""
    color = discord.Color(value=0x00ff00)
    em = discord.Embed(color=color, title='Ping! Pong! Latency:')
    em.description = f"{bot.latency * 1000:.4f} ms"
    await ctx.send(embed=em)


@bot.command()
async def invite(ctx):
    """Allow my bot to join the hood. YOUR hood."""
    await ctx.send("Another server, huh? https://discordapp.com/oauth2/authorize?client_id=417807256437129216&scope=bot&permissions=8") 


@bot.command()
@commands.has_permissions(kick_members = True)
async def kick(ctx, user: discord.Member = None):
	"""Kicks someone."""
	if user is None:
		await ctx.send("Please tag a person to kick! Usage: c.kick [user]")
	else:
		try:
			await user.kick()
			await ctx.send(f"Oof! Looks like {user.name} got kicked! Sucks to be them.")
		except discord.Forbidden:
			await ctx.send("Looks like I'm missing permissions to kick this user.")


@bot.command()
@commands.has_permissions(ban_members = True)
async def ban(ctx, user: discord.Member = None):
	"""Bans a bad boi."""
	if user is None:
		await ctx.send("Please tag a person to ban! Usage: c.ban [user]")
	else:
		try:
			await user.ban()
			await ctx.send(f"Oof! Looks like {user.name} was hit by the ban hammer.")
		except discord.Forbidden:
			await ctx.send("Looks like I'm missing permissions to swing the ban hammer.")


@bot.command()
@commands.has_permissions(manage_messages = True)
async def purge(ctx, number: int = None):
	try: 
	    if num is None:
	        await ctx.send("How many messages would you like me to delete? Usage: *purge [number of msgs]")
	    else:
	        try:
	            float(num)
	        except ValueError:
	            return await ctx.send("The number is invalid. Make sure it is valid! Usage: *purge [number of msgs]")
	        await ctx.channel.purge(limit=num+1)
	        msg = await ctx.send(f"Done. Purged {number} messages.")
	        await asyncio.sleep(3)
	        await msg.delete()
	except discord.Forbidden:
	    await ctx.send("Purge unsuccessful. The bot does not have Manage Msgs permission.")


@bot.command()
@commands.has_permissions(ban_members=True)
async def mute(ctx, user: discord.Member = None):
    '''Forces someone to shut up. Usage: *mute [user] [time in mins]'''
    if user is None:
    	return await ctx.send("Please tag a user to mute them!")
    try:
        await ctx.channel.set_permissions(user, send_messages=False)
        await ctx.send(f"{user.mention} is now muted. Time to shut up.")
    except discord.Forbidden:
        return await ctx.send("I could not mute the user. Make sure I have the manage channels permission.")


@bot.command()
@commands.has_permissions(ban_members=True)
async def unmute(ctx, user: discord.Member = None):
	'''Un-shuts someone up.'''
	if user is None:
		return await ctx.send("Please tag a uesr to unmute them!")
	try:
		await ctx.channel.set_permissions(user, send_messages=True)
		await ctx.send(f"{user.mention} can now talk again!")
	except discord.Forbidden:
		await ctx.send("Could not unmute the user. Make sure I have the manage channels permission.")





if not os.environ.get('TOKEN'):
    print("no token found REEEE!")
bot.run(os.environ.get('TOKEN').strip('"'))
