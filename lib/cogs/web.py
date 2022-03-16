## Discord imports
import discord
from discord import Embed, colour
from discord.ext import commands
## Async lib imports
import asyncio
import async_timeout
from aiohttp import request
## Util imports
import json
import requests
from datetime import datetime

with open('secrets.json', 'r') as secrets:
    data = secrets.read()
keys = json.loads(data)

def chase_redirects(url):
    while True:
        yield url
        r = requests.head(url)
        if 300 < r.status_code < 400:
            url = r.headers['location']
        else:
            break

class web(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.urlRegex =  r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]" \
        "{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>" \
        "]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"

    @commands.command(name="statuscheck", description="Retrieve the status of a website/URL", aliases=["webstatus","webstat","httpstat"])
    async def statusCheck(self, ctx, url):
        async with request("HEAD", url) as resp:
            await ctx.send(f"Website returned: {resp.status}")

    @statusCheck.error
    async def websiteStatus_error(self, ctx, error):
        text = f"Usage: {discord.PREFIX}statuscheck [url]"
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"```{text}```")
        else:
            await ctx.send(f"```An unknown error has occured!\n{text}```")
            raise error

    @commands.command(name="emailchecker", description="Verifies if an email is real or not", aliases=["emailverify", "emailinfo"])
    async def emailchecker(self, ctx, email: str):
        apikey = keys['hunteriokey']
        url = f"https://api.hunter.io/v2/email-verifier?email={email}&api_key={apikey}"
        async with request("GET", url, headers={}) as response:
            if response.status == 200:
                data = await response.json()
                embed = Embed(title="Email check",
                              description=f"checking {email}",
                              colour=discord.Colour.red())
                embed.add_field(name="Status: ", value=data['data']['status'])
                embed.add_field(name="Result: ", value=data['data']['result'])
                embed.add_field(name="Score: ", value=data['data']['score'])
                if data['data']['regexp'] is False:
                    embed.add_field(name="Valid format?", value="Invalid email format")
                elif data['data']['regexp'] is True:
                    embed.add_field(name="Valid format?", value="Valid email format")
                else:
                    embed.add_field(name="Valid format?", value="Unable to check!")

                if data['data']['smtp_server'] is False:
                    embed.add_field(name="SMTP check: ", value="Invalid SMTP server")
                elif data['data']['smtp_server'] is True:
                    embed.add_field(name="SMTP check: ", value="Valid SMTP server")
                else:
                    embed.add_field(name="SMTP check: ", value="Unable to validate!")

                if data['data']['mx_records'] is False:
                    embed.add_field(name="MX Records?", value="No available records")
                elif data['data']['mx_records'] is True:
                    embed.add_field(name="MX Records?", value="Existing records")
                else:
                    embed.add_field(name="MX Records?", value="Unable to check!")

                if data['data']['gibberish'] is False:
                    embed.add_field(name="Gibberish email?", value="Looks like it makes sense")
                elif data['data']['gibberish'] is True:
                    embed.add_field(name="Gibberish email?", value="Complete nonsense m8")
                else:
                    embed.add_field(name="Gibberish email?", value="Unable to check!")

                time = ctx.message.created_at
                embed.set_footer(text=f"Asked by {ctx.author.name} " + time.strftime("%d/%m/%y %X"))
                await ctx.send(embed=embed)
            elif response.status == 400:
                await ctx.send("```That's not an email!\nUsage: {discord.PREFIX}emailchecker [email]```")
            else:
                await ctx.send("There was an issue with the API!")

    @emailchecker.error
    async def emailchecker_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("```Usage: {discord.PREFIX}emailchecker [email]```")
        else:
            raise

    @commands.command(name="RedirectChaser", description="Finds all redirects associated with a link", aliases=["wheregoes", "RedirectChecker"])
    async def redirectchaser(self, ctx, url=None):
        text = f"Usage: {discord.PREFIX}wheregoes [URL]"
        try:
            requests.get(url)
        except requests.ConnectionError:
            await ctx.send(f"Unable to connect to {url}\n{text}")
        urls = []
        for url_redirects in chase_redirects(url):
            urls.append(url_redirects)
        embed = Embed(title=f"Redirects for {url}",
                      colour=discord.Colour.red())
        num = 1
        for url in urls:
            embed.add_field(name=f"Redirect #{num}", value=url, inline=False)
            num += 1
        await ctx.send(embed=embed)

    @redirectchaser.error
    async def redirectchaser_error(self, ctx, error):
        text = f"Usage: {discord.PREFIX}wheregoes [URL]"
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"```{text}```")
        else:
            await ctx.send(f"```An unknown error has occured\n{text}```")
            raise error

    @commands.command(name="subdomain", description="Find subdomains", aliases=["sdomains"])
    async def findsubdomains(self, ctx, domain):
        text = f"Usage: {discord.PREFIX}subdomain [domain]"
        url = f"https://api.securitytrails.com/v1/domain/{domain}/subdomains"
        querystring = {"children_only": "false", "include_inactive": "true"}
        headers = {"Accept": "application/json", "apikey": keys['securitytrails']}
        async with request("GET", url, headers=headers, params=querystring) as response:
            if response.status == 200:
                data = await response.json()
                Found_Subdomains = data['subdomains']
                if len(Found_Subdomains) == 0:
                    await ctx.send(f"```No subdomain records found!\n{text}```")
                else:
                    subdomains = "First 10 subdomains:"
                    for sub in Found_Subdomains[:20]:
                        subdomains += f"\n{sub}.{domain}"
                    await ctx.send(f"```{subdomains}```")
            else:
                await ctx.send(f"```There was an issue with the API\n{text}```")

    @findsubdomains.error
    async def findsubdomains_error(self, ctx, error):
        text = f"Usage: {discord.PREFIX}subdomain [domain]"
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"```{text}```")
        else:
            await ctx.send(f"```An unknown error has occured\n{text}```")

def setup(client):
    client.add_cog(web(client))
