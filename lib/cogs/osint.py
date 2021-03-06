import discord, json, magic, os, aiofiles, re, imageio
from bs4 import BeautifulSoup
from PIL import Image, ExifTags
from discord import Embed
from discord.ext import commands
from aiohttp import request
from pygicord import Paginator
from datetime import datetime

with open('secrets.json', 'r') as secrets:
    data = secrets.read()
keys = json.loads(data)
apikey = keys['googleapi']
builtwithkey = keys['builtwith']


async def get_imagemeta(file):
    pic = imageio.imread(file)
    type = Image.open(file)
    megapixels = (type.size[0]*type.size[1]/1000000)
    d = re.sub(r'[a-z]', '', str(pic.dtype))
    t = len(Image.Image.getbands(type))

    results = f"""

Format: {type.format}
Data type: {pic.dtype}
Bit depth (per channel): {d}
Bit depth (per pixel): {int(d)*int(t)}
Mode: {type.mode}
Palette: {type.palette}
Width: {type.size[0]}
Height: {type.size[1]}
Megapixels: {megapixels}

"""
    return results



class osint(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.url_regex = re.compile(
                r'^(?:http|ftp)s?://'
                r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
                r'localhost|'
                r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
                r'(?::\d+)?'
                r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    @commands.command(name="instagramlookup", description="Search for Instagram users", aliases=["instausers", "insta", "iglookup", "ig"])
    async def instagramlookup(self, ctx, *, username=None):
        text = f"{discord.PREFIX}instagramlookup [username]"
        if username is None:
            await ctx.send(f"```{text}```")
        else:
            links = ""
            if username[0] == "@":
                username = username[1:]
            q = username
            cx = "c4cc3b449edaa17c2"
            url = f"https://www.googleapis.com/customsearch/v1?key={apikey}&cx={cx}&q={q}&start=1"
            async with request("GET", url) as response:
                data = await response.json()
            try:
                account_links = data['items']
                for link in account_links[:30]:
                    links += f"+ {link['formattedUrl']}\n"
                await ctx.send(f"""```diff
{links}```""")
            except KeyError:
                if links == "":
                    await ctx.send(f"```No search results found for {username}\n{text}```")
                else:
                    await ctx.send(f"```diff\nOne result found from direct instagram search:\n{links}```")

    @commands.command(name="facebooklookup", description="Search for Facebook users", aliases=["fbusers"])
    async def facebooklookup(self, ctx, *, username=None):
        text = f"Usage: {discord.PREFIX}facebooklookup [username]"
        if username is None:
            await ctx.send(f"```{text}```")
        else:
            q = username
            cx = "09982abed469e58ff"
            url = f"https://www.googleapis.com/customsearch/v1?key={apikey}&cx={cx}&q={q}&start=1"
            async with request("GET", url) as response:
                search_response = await response.json()
            try:
                account_links = ""
                x = 1
                for item in search_response['items']:
                    if item['formattedUrl'] not in account_links:
                        account_links += f"\n+ {item['formattedUrl']}"
                    if x == 30:
                        break
                    x += 1

                await ctx.send(f"""
```diff
{account_links}```""")
            except KeyError:
                await ctx.send(f"```No search results found for {username}\n{text}```")

    @commands.command(name="twitterlookup", description="Search for Twitter users", aliases=["twitterusers"])
    async def twitterlookup(self, ctx, *, username=None):
        text = f"Usage: {discord.PREFIX}twitterlookup [username]"
        if username is None:
            await ctx.send(f"```{text}```")
        else:
            q = username
            cx = "fd1dde45779087b24"
            url = f"https://www.googleapis.com/customsearch/v1?key={apikey}&cx={cx}&q={q}&start=1"
            async with request("GET", url) as response:
                search_response = await response.json()
            try:
                account_links = ""
                x = 1
                for item in search_response['items']:
                    if item['formattedUrl'] not in account_links:
                        account_links += f"\n+ {item['formattedUrl']}"
                    if x == 30:
                        break
                    x += 1

                await ctx.send(f"""
```diff
{account_links}```""")
            except KeyError:
                await ctx.send(f"```No search results found for {username}\n{text}```")


    @commands.command(name="getdomain", description="Find detailed information for a domain", aliases=["domaininfo"])
    async def getdomain(self, ctx, domain=None):
        text = f"Usage: {discord.PREFIX}getdomain [domain]\n\nNote that only the root domain will be checked."
        if domain is None:
            await ctx.send(f"```{text}```")
        else:
            url = f"https://api.builtwith.com/free1/api.json?KEY={builtwithkey}&LOOKUP={domain}"
            async with request("GET", url) as response:
                if response.status == 200:
                    data = await response.json()
                else:
                    await ctx.send(f"```Website returned code: {response.status}, please try again later\n{text}```")
                    data = None
            if data is not None:
                embeds = []
                embed = Embed(title=data['domain'], colour=discord.Colour.red())
                embed.add_field(name="First time domain was indexed: ", value=datetime.fromtimestamp(data['first']), inline=False)
                embed.add_field(name="Last time domain was indexed: ", value=datetime.fromtimestamp(data['last']), inline=False)
                embed.add_field(name="Number of groups: ", value=len(data['groups']), inline=False)
                embeds.append(embed)
                x = 1
                for group in data['groups']:
                    embed = Embed(title=f"Group #{x}: {group['name']}", colour=discord.Colour.red())
                    embed.add_field(name="Group name", value=group['name'], inline=False)
                    if len(group['categories']) >= 22:
                        categories = group['categories'][22:]
                    else:
                        categories = group['categories']
                    y = 1
                    for category in categories:
                        embed.add_field(name=f"Category #{y}: ", value=category['name'], inline=False)
                        embed.add_field(name="Live technologies: ", value=category['live'], inline=False)
                        embed.add_field(name="Dead technologies: ", value=category['dead'], inline=False)
                        y += 1
                    embeds.append(embed)
                    x += 1
                paginator = Paginator(pages=embeds)
                await paginator.start(ctx)

    @commands.command(name="imagedata", description="Retrieve image data", aliases=["imagemeta"])
    async def imagedata(self, ctx, url=None):
        text = f"""
Usage: {discord.PREFIX}imagedata [url/attach file to message]
If you pass a URL, ensure the URL links directly to the image"""
        images_extensions = ['.jpg', '.jpeg', '.jpe', '.jif', ' .jfif',
                             '.jfi', '.png', '.gif', '.webp', '.tiff', '.tif'
                             '.psd', '.raw', '.arw', '.cr2', '.nrw', '.k25',
                             '.bmp', '.dib', '.heif', '.heic', '.ind', '.indd',
                             '.indt', '.jp2', '.j2k', '.jpf', '.jpx', '.jpm',
                             '.mj2', '.svg', '.svgz']
        if ctx.message.attachments:
            attachment_name = ctx.message.attachments[0].filename
            extension = f".{attachment_name.split('.')[-1]}"
            if '/' in attachment_name:
                await ctx.send(f"```File names may not contain /\'s\n{text}```")
            elif extension not in images_extensions:
                await ctx.send(f"```Unaccepted file extension\n{text}```")
            else:
                attachment_url = ctx.message.attachments[0].url
                async with request("GET", attachment_url) as r:
                    file_content = await r.read()
                file_path = f"{discord.PREFIX}exiftool/{ctx.author.id}_{attachment_name}"
                async with aiofiles.open(file_path, 'ab') as f:
                    await f.write(file_content)
                if "image/" in magic.from_file(file_path, mime=True).lower():
                    check = True
                else:
                    await ctx.send(f"```Unsupported mime type\n{text}```")
                    os.remove(file_path)
                    check = False
        else:
            if url is not None:
                if re.match(self.url_regex, url) is not None:
                    extension = f".{url.split('.')[-1]}"
                    if extension not in images_extensions:
                        await ctx.send(f"```Unaccepted file extension\n{text}```")
                    else:
                        async with request("GET", url) as resp:
                            if resp.status == 200:
                                if "image/" not in resp.content_type.lower():
                                    await ctx.send(f"```URL is not an image file\n{text}```")
                                    file_content = None
                                else:
                                    try:
                                        if int(resp.headers['Content-Length']) < 8000000:
                                            file_content = await resp.read()
                                    except KeyError:
                                        file_content = None
                                        await ctx.send(f"```Unable to verify file size\n{text}```")
                            else:
                                await ctx.send(f"```URL returned {resp.status}\n{text}```")
                                file_content = None
                        if file_content is not None:
                            file_path = f"{discord.PREFIX}exiftool/{ctx.author.id}.{resp.content_type.lower().split('/')[1]}"
                            async with aiofiles.open(file_path, 'ab') as f:
                                await f.write(file_content)
            else:
                file_path = None
                await ctx.send(f"```{text}```")

        if file_path is not None:
            metadata = await get_imagemeta(file_path)
            await ctx.send(f"```{metadata}```")


def setup(client):
    client.add_cog(osint(client))
