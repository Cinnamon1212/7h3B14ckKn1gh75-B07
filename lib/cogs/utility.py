## Discord imports
import discord
from discord import Embed, colour
from discord import AppInfo
from discord.ext import commands, tasks
from pygicord import Paginator
## Async lib imports
import asyncio
import aiofiles
from asyncio import TimeoutError
## Util imports
import art
import base64
import os
import random
import re
import time
import qrcode as qr
import passgen
import psutil
import subprocess
import math
import platform
import sys
from itertools import cycle
from datetime import datetime, timedelta
from urllib.parse import quote_plus

start_time = time.time()
version = "Beta 1.0"
owner = "SYN"
OS_Name = subprocess.check_output(["uname", "-a"]).decode('utf-8')

class utility(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.morse_code = morse_code = {'A': '.-', 'B': '-...',
                                        'C': '-.-.', 'D': '-..', 'E': '.',
                                        'F': '..-.', 'G': '--.', 'H': '....',
                                        'I': '..', 'J': '.---', 'K': '-.-',
                                        'L': '.-..', 'M': '--', 'N': '-.',
                                        'O': '---', 'P': '.--.', 'Q': '--.-',
                                        'R': '.-.', 'S': '...', 'T': '-',
                                        'U': '..-', 'V': '...-', 'W': '.--',
                                        'X': '-..-', 'Y': '-.--', 'Z': '--..',
                                        '1': '.----', '2': '..---', '3': '...--',
                                        '4': '....-', '5': '.....', '6': '-....',
                                        '7': '--...', '8': '---..', '9': '----.',
                                        '0': '-----', ', ': '--..--', '.': '.-.-.-',
                                        '?': '..--..', '/': '-..-.', '-': '-....-',
                                        '(': '-.--.', ')': '-.--.-'}

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"""
Bot online!
Latency: {round(self.client.latency * 1000)} ms
            """)

    @commands.command(name="passgen", description="generates a number of passwords with a given length", aliases=["passwordgenerator", "password"])
    async def passwords(self, ctx, length: int, number=1):
        text = f"Usage: {discord.PREFIX}passgen [length] (number)"
        if number <= 25 and number >= 1:
            if length <= 25 and length >= 4:
                embed = Embed(title="Passwords ",
                              description=f"{number} passwords of {length} length",
                              colour=discord.Colour.red())
                i = 0
                num = 0
                passwords = set({})
                while i != number:
                    output = passgen.passgen(length=length, punctuation=True, digits=True, letters=True, case='both')
                    passwords.add(output)
                    i += 1
                for password in passwords:
                    embed.add_field(name=f"Password {num + 1}", value=password, inline=False)
                    num += 1
                time = ctx.message.created_at
                embed.set_footer(text=f"Asked by {ctx.author.name} " + time.strftime("%d/%m/%y %X"))
                await ctx.author.send(embed=embed)
                await ctx.send("Passwords were send to your DMs!")
            else:
                await ctx.send(f"```Length must be between 4 and 25\n{text}```")
        else:
            await ctx.send(f"```You must have between 1 and 25 passwords\n{text}```")

    @passwords.error
    async def passgen_error(self, ctx, error):
        text = f"Usage: {discord.PREFIX}passgen [amount] [length]"
        if isinstance(error, commands.BadArgument):
            await ctx.send(f"```Invalid number of passwords or length\n{text}```")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"```Please enter the number of passwords and the length\n{text}```")
        else:
            raise

    @commands.command(name="textconverter", description="Converts some text to another", aliases=["textto", "text", "txtconvert"])
    async def textconverter(self, ctx, conversion=None, *, message=None):
        text = f"""
Usage: {discord.PREFIX}textto [conversion] [message]
Available conversions:
==== ASCII ====
[+] ascii2text (ASCII to text)
[+] text2ascii (Text to ASCII)
[+] ascii852text (ASCII 85 to text)
[+] text2acii85 (Text to ASCII 85)
==== Base ====
[+] base642text (Base64 to text)
[+] text2base64 (Text to base64)
[+] base322text (Base32 to text)
[+] text2base32 (Text to base32)
[+] base162text (Base16 to text)
[+] text2base16 (Text to bas16)
==== Binary ====
[+] bin2dec (Binary to decimal)
[+] dec2bin (Decimal to binary)
[+] bin2text (Binary to text)
[+] text2bin (Text to binary)
==== Hex ====
[+] hex2text (Hexidecimal to text)
[+] text2hex (Text to hexidecimal)
[+] hex2binary (Hexidecimal to binary)
[+] binary2hex (Binary to hexidecimal)
[+] dec2hex (Decimal to Hexidecimal)
[+] hex2dec (Hexidecimal to decimal)
[+] rgb2hex (RGB to Hexidecimal) // Currently only supports one at a time
[+] hex2rgb (Hexidecimal to RGB)
==== Asciify ====
[+] aprint (ASCII art for keyword) // use {discord.PREFIX}textto aprint help for link to art dictionary
[+] text2art (text to ASCII font, bot will prompt you for font) // use {discord.PREFIX}textto aprint help for a link to font dictionaries
[+] decor (ASCII decor for keyword) // use {discord.PREFIX}textto decor help for a link to decor dictionary
==== Other ====
[+] lowercase (Converts message to all lowercase)
[+] uppercase (Converts message to all uppercase)
[+] randomcase (Random cases a message)
[+] spoilertext (Converts message to spoiler text)
[+] text2morse (Converts text to morse code)
[+] morse2text (Converts morse code to text)
[+] urlsafe (URL safes a given URL)
        """
        if conversion is None or message is None:
            await ctx.send(f"```{text}```")
        else:
            conversion = conversion.lower()
            if conversion == "ascii2text":
                if "," in message:
                    split = message.split(",")
                else:
                    split = message.split(" ")
                ascii_chars = []
                for char in split:
                    try:
                        char = int(char)
                        ascii_chars.append(char)
                        check = True
                    except ValueError:
                        await ctx.send(f"{char} is not an ASCII character\n{text}")
                        check = False
                        break
                if check is True:
                    string = ''.join(map(chr, ascii_chars))
                    await ctx.send(f"```{string}```")
            elif conversion == "text2ascii":
                ascii_chars = [ord(c) for c in message]
                string = ""
                for c in ascii_chars:
                    string += f" {c}"
                if len(string) <= 1994:
                    await ctx.send(f"```{string}```")
                else:
                    filename = await writetofile(string)
                    await ctx.send(file=discord.File(filename))
                    os.remove(filename)
            elif conversion == "ascii852text":
                MsgBytes = base64.a85decode(message.encode('ascii'))
                encoded = MsgBytes.decode('ascii')
                if len(encoded) <= 1994:
                    await ctx.send(f"```{encoded}```")
                else:
                    filename = await writetofile(encoded)
                    await ctx.send(file=discord.File(filename))
                    os.remove(filename)
            elif conversion == "text2ascii85":
                MsgBytes = base64.a85encode(message.encode('ascii'))
                encoded = MsgBytes.decode('ascii')
                if len(encoded) <= 1994:
                    await ctx.send(f"```{encoded}```")
                else:
                    filename = await writetofile(encoded)
                    await ctx.send(file=discord.File(filename))
                    os.remove(filename)
            elif conversion == "base642text":
                try:
                    MsgBytes = base64.b64decode(message.encode('ascii'))
                    Decoded = MsgBytes.decode('ascii')
                    check = True
                except:
                    await ctx.send(f"Unable to convert base64 to text\n{text}")
                    check = False
                if check is True:
                    if len(Decoded) <= 5994:
                        await ctx.send(f"```{Decoded}```")
                    else:
                        filename = await writetofile(Decoded)
                        await ctx.send(file=discord.File(filename))
                        os.remove(filename)
            elif conversion == "text2base64":
                B64Bytes = base64.b64encode(message.encode('ascii'))
                encoded_str = B64Bytes.decode('ascii')
                if len(encoded_str) <= 1994:
                    await ctx.send(f"```{encoded_str}```")
                else:
                    filename = await writetofile(encoded_str)
                    await ctx.send(file=discord.File(filename))
                    os.remove(filename)
            elif conversion == "base322text":
                MsgBytes = base64.b32decode(message.encode('ascii'))
                Decoded = MsgBytes.decode('ascii')
                if len(Decoded) <= 1994:
                    await ctx.send(f"```{Decoded}```")
                else:
                    filename = await writetofile(Decoded)
                    await ctx.send(file=discord.File(filename))
                    os.remove(filename)
            elif conversion == "text2base32":
                MsgBytes = base64.b32encode(message.encode('ascii'))
                encoded = MsgBytes.decode('ascii')
                if len(encoded) <= 1994:
                    await ctx.send(f"```{encoded}```")
                else:
                    filename = await writetofile(encoded)
                    await ctx.send(file=discord.File(filename))
                    os.remove(filename)
            elif conversion == "base162text":
                MsgBytes = base64.b16decode(message.encode('ascii'))
                Decoded = MsgBytes.decode('ascii')
                if len(Decoded) <= 1994:
                    await ctx.send(f"```{Decoded}```")
                else:
                    filename = await writetofile(Decoded)
                    await ctx.send(file=discord.File(filename))
                    os.remove(filename)
            elif conversion == "text2base16":
                MsgBytes = base64.b16encode(message.encode('ascii'))
                encoded = MsgBytes.decode('ascii')
                if len(encoded) <= 1994:
                    await ctx.send(f"```{encoded}```")
                else:
                    filename = await writetofile(encoded)
                    await ctx.send(file=discord.File(filename))
                    os.remove(filename)
            elif conversion == "bin2dec":
                try:
                    message = int(message)
                    decimal = await bin2dec(message)
                    await ctx.send(f"```{decimal}```")
                except ValueError:
                    await ctx.send(f"```Invalid decimal\n{text}```")
            elif conversion == "bin2text":
                try:
                    bits = int(message, 2)
                    check = True
                except ValueError:
                    await ctx.send(f"```Invalid bianry\n{text}```")
                    check = False
                if check is True:
                    string = bits.to_bytes((bits.bit_length() + 7) // 8, 'big').decode()
                    await ctx.send(f"```{string}```")
            elif conversion == "text2bin":
                binary = bin(int.from_bytes(message.encode(), 'big'))
                if len(binary) <= 1996:
                    await ctx.send(f"```{binary}```")
                else:
                    filename = await writetofile(binary)
                    await ctx.send(file=discord.File(filename))
                    os.remove(filename)
            elif conversion == "dec2bin":
                try:
                    dec = int(message)
                    check = True
                except ValueError:
                    await ctx.send(f"Invalid decimal!\n{text}")
                    check = False
                if check is True:
                    binary = bin(dec).replace("0b", "")
                    if len(binary) <= 1994:
                        await ctx.send(f"```{binary}```")
                    else:
                        filename = await writetofile(binary)
                        await ctx.send(file=discord.File(filename))
                        os.remove(filename)
            elif conversion == "hex2text":
                removed0x = message.split("0x")
                newmessage = ''.join(str(e) for e in removed0x)
                print(newmessage)
                try:
                    decoded = bytearray.fromhex(newmessage).decode()
                    await ctx.send(f"```{decoded}```")
                except ValueError:
                    await ctx.send(f"Invalid hex value!\n{text}")
            elif conversion == "text2hex":
                hexxed = ''.join([hex(ord(i)) for i in message])
                if len(hexxed) <= 1994:
                    await ctx.send(f"```{hexxed}```")
                else:
                    filename = await writetofile(hexxed)
                    await ctx.send(file=discord.File(filename))
                    os.remove(filename)
            elif conversion == "hex2binary":
                if "," in message:
                    split = message.split(",")
                else:
                    split = message.split(" ")
                try:
                    binary = []
                    for c in split:
                        binary.append(bin(int(c, 16))[2:])
                    binary = ' '.join(binary)
                    check = True
                except ValueError:
                    await ctx.send(f"Invalid hex provided\n{text}")
                    check = False
                if check is True:
                    if len(binary) <= 1994:
                        await ctx.send(f"```{binary}```")
                    else:
                        filename = await writetofile(binary)
                        await ctx.send(file=discord.File(filename))
                        os.remove(filename)
            elif conversion == "binary2hex":
                if "," in message:
                    binary = message.split(",")
                else:
                    binary = message.split(" ")
                try:
                    hexxed = []
                    for c in binary:
                        hexxed.append(hex(int(c, 2)))
                    hexxed = " ".join(hexxed)
                    await ctx.send(f"```{hexxed}```")
                except ValueError:
                    await ctx.send(f"```Invalid binary provided\n{text}```")
            elif conversion == "dec2hex":
                if "," in message:
                    split = message.split(",")
                else:
                    split = message.split(" ")
                hexxed = []
                try:
                    for x in split:
                        hexxed.append(hex(int(x)))
                    check = True
                except ValueError:
                    await ctx.send(f"```Invalid decimal!\n{text}```")
                    check = False
                if check is True:
                    hexxed = ' '.join(hexxed)
                    if len(hexxed) <= 1994:
                        await ctx.send(f"```{hexxed}```")
                    else:
                        filename = await writetofile(hexxed)
                        await ctx.send(file=discord.File(filename))
                        os.remove(filename)
            elif conversion == "hex2dec":
                if "," in message:
                    split = message.split(",")
                else:
                    split = message.split(" ")
                decimals = []
                try:
                    for x in split:
                        decimals.append(int(x, 16))
                    check = True
                except ValueError:
                    await ctx.send(f"```Invalid hex value\n{text}```")
                    check = False
                if check is True:
                    str_decimals = ""
                    for x in decimals:
                        str_decimals += f"{x} "
                    await ctx.send(str_decimals)
            elif conversion == "hex2rgb":
                if "," in message:
                    hexxed = message.split(",")
                else:
                    hexxed = message.split(" ")
                RGBs = []
                try:
                    for x in hexxed:
                        value = x.lstrip('#')
                        lv = len(value)
                        RGBs.append(tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3)))
                    check = True
                except ValueError:
                    await ctx.send(f"Invalid hex value!\n{text}")
                RGB = ""
                for x in RGBs:
                    if len(RGBs) != 1:
                        RGB += f"{x}, "
                    else:
                        RGB += f"{x}"
                if len(RGB) <= 1994:
                    await ctx.send(f"```{RGB[:len(RGB) - 2]}```")
                else:
                    filename = writetofile(RGB)
                    await ctx.send(file=discord.File(filename))
                    os.remove(filename)
            elif conversion == "rgb2hex":
                RGBs = message.split(",")
                if len(RGBs) != 3:
                    await ctx.send(f"```Invalid RGB value\n{text}```")
                else:
                    try:
                        r, g, b = RGBs[0], RGBs[1], RGBs[2]
                        rgb = "#{:02x}{:02x}{:02x}".format(int(r),int(g),int(b))
                        await ctx.send(f"```{rgb}```")
                    except ValueError:
                        if len(message) <= 1975:
                            await ctx.send(f"```Invalid RGB value {message}\n{text}```")
                        else:
                            await ctx.send(f"```Invalid RGB value\n{text}```")
            elif conversion == "lowercase":
                message = message.lower()
                if len(message) <= 1994:
                    await ctx.send(f"```{message}```")
                else:
                    filename = await writetofile(message)
                    await ctx.send(file=discord.File(filename))
                    os.remove(filename)
            elif conversion == "uppercase":
                message = message.upper()
                if len(message) <= 1994:
                    await ctx.send(f"```{message}```")
                else:
                    filename = await writetofile(message)
                    await ctx.send(file=discord.File(filename))
                    os.remove(filename)
            elif conversion == "randomcase":
                randomized = []
                for x in message:
                    choice = random.randint(0, 1)
                    if choice == 0:
                        x = x.lower()
                    else:
                        x = x.upper()
                    randomized.append(x)
                message = ""
                for x in randomized:
                    message += x
                if len(message) <= 1994:
                    await ctx.send(f"```{message}```")
                else:
                    filename = await writetofile(message)
                    await ctx.send(file=discord.File(filename))
                    os.remove(filename)
            elif conversion == "spoilertext":
                spoilermessage = ""
                for x in message:
                    spoilermessage += f"||{x}||"
                if len(spoilermessage) <= 1994:
                    await ctx.send(f"```{spoilermessage}```")
                else:
                    filename = await writetofile(spoilermessage)
                    await ctx.send(file=discord.File(filename))
                    os.remove(filename)
            elif conversion == "text2morse":
                cipher = ""
                for x in message:
                    x = x.upper()
                    if x != ' ':
                        cipher += self.morse_code[x] + ' '
                    else:
                        cipher += ' '
                if len(cipher) <= 1994:
                    await ctx.send(cipher)
                else:
                    filename = await writetofile(cipher)
                    await ctx.send(file=discord.File(filename))
                    os.remove(filename)
            elif conversion == "morse2text":
                message += ' '
                decipher = ''
                citext = ''
                for x in message:
                    if(x != ' '):
                        i = 0
                        citext += x
                    else:
                        i += 1
                        if i == 2:
                            decipher += ' '
                        else:
                            decipher += list(self.morse_code.keys())[list(self.morse_code.values()).index(citext)]
                            citext = ''
                if len(decipher) <= 1994:
                    await ctx.send(f"```{decipher}```")
                else:
                    filename = await writetofile(decipher)
                    await ctx.send(file=discord.File(filename))
                    os.remove(filename)
            elif conversion == "urlsafe":
                regex = re.compile(
                        r'^(?:http|ftp)s?://'
                        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
                        r'localhost|'
                        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
                        r'(?::\d+)?'
                        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
                if re.match(regex, message) is not None:
                    safeurl = quote_plus(message)
                    if len(safeurl) <= 1994:
                        await ctx.send(f"```{safeurl}```")
                    else:
                        filename = await writetofile(safeurl)
                        await ctx.send(file=discord.File(filename))
                        os.remove(filename)
                else:
                    await ctx.send(f"```Invalid URL!\n{text}```")
            elif conversion == "aprint":
                if message == "help":
                    await ctx.send("https://github.com/sepandhaghighi/art/blob/master/art/art_dic.py")
                else:
                    try:
                        ascii_art = art.art(message)
                        await ctx.send(f"```{ascii_art}```")
                    except art.artError:
                        await ctx.send(f"```Unable to generate art for provided keywords\n{text}```")
            elif conversion == "text2art":
                if message == "help":
                    urls = """
https://github.com/sepandhaghighi/art/blob/master/art/text_dic1.py
https://github.com/sepandhaghighi/art/blob/master/art/text_dic2.py
https://github.com/sepandhaghighi/art/blob/master/art/text_dic3.py
                    """
                    await ctx.send(urls)
                await ctx.send("Which ASCII font would you like to use?")
                try:
                    font = await self.client.wait_for(
                                "message",
                                timeout=20,
                                check=lambda message: message.author == ctx.author and message.channel == ctx.channel)
                    check = True
                except TimeoutError:
                    await ctx.send("text2art timed out", delete_after=10)
                    check = False
                if check is True:
                    asciified = art.text2art(message, font.content)
                    if len(asciified) <= 1994:
                        await ctx.send(f"```{asciified}```")
                    else:
                        filename = writetofile(asciified)
                        await ctx.send(file=discord.File(filename))
                        os.remove(filename)
            elif conversion == "decor":
                if message == "help":
                    await ctx.send("https://github.com/sepandhaghighi/art/blob/master/art/decor_dic.py")
                else:
                    try:
                        decor = art.decor(message)
                        await ctx.send(f"```{decor}```")
                    except art.artError:
                        await ctx.send(f"```Unable to find decor for keyword\n{text}```")

            else:
                await ctx.send(f"```Invalid conversion type!\n{text}```")

    @commands.command(name="QRCodeGenerator", description="Generates QR code from a message", aliases=["QRGen", "QRGenerator", "QRCodeGen", "text2QR"])
    async def QRGen(self, ctx, *, message=None):
        text = f"""
Usage: {discord.PREFIX}QRGen [message]
Colours must be entered by name ('black', 'white', etc)"""
        if message is None:
            await ctx.send(f"```{text}```")
        else:
            img = qr.make(message)
            now = datetime.now()
            filename = f"{discord.PREFIX}conversions/{ctx.author.id}_{now}.png"
            img.save(filename)
            await ctx.send(file=discord.File(filename))
            os.remove(filename)

    @commands.command(name="latency", aliases=['botping', 'bping'], description="Tests the latency of the bot")
    async def ping(self, ctx):
        await ctx.send(f'Pong! {round(self.client.latency * 1000)} ms')

    @commands.command(name="listofroles", description="Gives a list of roles", aliases=["roles", "serverroles"])
    async def listofroles(self, ctx):
        roles = ctx.guild.roles
        roles.reverse()
        roles.pop(-1)
        roleslist = [roles[x:x+25] for x in range(0, len(roles), 25)]
        pagecount = math.ceil(len(roles) / 25)
        paginator = Paginator(pages=get_pages(pagecount, roleslist))
        await paginator.start(ctx)

    @listofroles.error
    async def listofroles_error(self, ctx, error):
        text = f"{discord.PREFIX}listofroles"
        await ctx.send(f"```An unknown error has occured!\n{text}```")



    @commands.command(name="credits", description="Info on the bot creator!", aliases=["owner", "creator", "credit"])
    async def credits(self, ctx):
        embed = Embed(title="Credits", colour=discord.Colour.dark_purple())
        embed.set_thumbnail(url=self.client.user.avatar_url)
        embed.add_field(name="Creator: ", value=owner)
        embed.add_field(name="Github: ", value="https://github.com/Cinnamon1212", inline=False)
        embed.add_field(name="Website: ", value="https://synisl33t.com", inline=False)
        embed.add_field(name="Email: ", value="syn@synisl33t.com", inline=False)
        embed.set_footer(text="Feel free to check out my other projects on Github!\n")
        await ctx.send(embed=embed)

    @commands.command(name="stats", description="Bot statistics", aliases=["statistics", "botstats", "botinfo", "bot", "version"])
    async def stats(self, ctx):
        current_time = time.time()
        difference = int(round(current_time - start_time))
        text = str(timedelta(seconds=difference))
        embed=Embed(title=f"{self.client.user} stats",
                    colour=discord.Colour.random())
        embed.set_thumbnail(url=self.client.user.avatar_url)
        embed.add_field(name="Uptime: ", value=text, inline=False)
        embed.add_field(name="Version: ", value=version, inline=False)
        embed.add_field(name="Number of servers: ", value=len(self.client.guilds), inline=False)
        embed.add_field(name="Total channels: ", value=sum(1 for g in self.client.guilds for _ in g.channels), inline=False)
        cached = sum(1 for m in self.client.cached_messages)
        if cached == 1000:
            cached = "Max"
        embed.add_field(name="Number of cached messages: ", value=cached, inline = False)
        embed.add_field(name="Github: ", value="https://github.com/Cinnamon1212/", inline=False)
        embed.add_field(name="Email: ", value="syn@synisl33t.com", inline=False)
        embed.add_field(name="OS: ", value=OS_Name, inline=False)
        process = psutil.Process(os.getpid())
        embed.add_field(name="Memory usage: ", value=f"{round(process.memory_info().rss / 1024 ** 2, 2)} Mbs", inline=False)
        embed.add_field(name="CPU usage:", value=f"{psutil.cpu_percent()}%", inline=False)
        embed.add_field(name="Python version: ", value=sys.version, inline=False)
        embed.add_field(name="Discord.py version: ", value=discord.__version__)
        mtime = ctx.message.created_at
        embed.set_footer(text=f"Asked by {ctx.author.name} " + mtime.strftime("%d/%m/%y %X"))
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(utility(client))
