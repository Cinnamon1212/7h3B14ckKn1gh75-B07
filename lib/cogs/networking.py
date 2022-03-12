## Discord imports
import discord
from discord import Embed, colour
from discord.ext import commands
## Async lib imports
import asyncio
import nest_asyncio
import async_timeout
import asyncdns
from aiohttp import request
## Util imports
from datetime import datetime
import socket

nest_asyncio.apply()

async def ping_f(ip, count):
    args = f"ping -c {count} {ip}"
    cmd = await asyncio.create_subprocess_shell(args, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    stdout, stderr = await cmd.communicate()
    output = str(stdout, 'utf-8')
    return output

async def bannergrab_f(ip, port):
    try:
        async with async_timeout.timeout(2):
            r, w = await asyncio.open_connection(ip, port)
    except asyncio.TimeoutError:
        return "target timed out"
    except ConnectionRefusedError:
        return "port closed"
    try:
        async with async_timeout.timeout(2):
            banner = await r.read(1024)

        w.close()
        if banner.decode().strip() == "":
            return "Port did not return a banner"
        return banner.decode().strip()
    except asyncio.TimeoutError:
        return "Port open but took too long to return a banner"

class utils:
    def validate_ip(s):
        if s is not None:
            restricted = ["127.0.", "0.0.0."]
            a = s.split('.')
            if len(a) != 4:
                return False
            for x in a:
                if not x.isdigit():
                    return False
                i = int(x)
                if i < 0 or i > 255:
                    return False
            firstsix = s[0:6]
            check = any(r in firstsix for r in restricted)
            if check is True:
                return False
            elif s[0:2] == "127":
                return False
            else:
                return True

    def validate_port(s):
        try:
            s = int(s)
        except ValueError:
            return False
        if s <= 65535:
            return True
        else:
            return False


class networking(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.common_ports = [21, 22, 23, 25, 53, 80, 110, 111, 135, 139, 143,
                             443, 445, 993, 995, 1723, 3306, 3389, 5900, 8080]

    @commands.command(name="iplookup", aliases=["geoip","ip","ipinfo"], description="Find information on an IP address")
    async def iplookup(self, ctx, ip=""):
        text = "Usage: ./iplookup <IP Address>"
        url = f"http://ip-api.com/json/{ip}"
        async with request("GET", url) as response:
            if response.status == 200:
                data = await response.json()
                if data["status"] == "success":
                    embed = Embed(title=f"IP Info {ip}",
                                  colour=discord.Colour.red(),
                                  inline=False)
                    embed.set_thumbnail(url="https://www.omnivisiondesign.com/wp-content/uploads/2013/06/IP_address.jpg")
                    embed.add_field(name="Country: ", value=data['country'])
                    embed.add_field(name="Country code: ", value=data['countryCode'])
                    embed.add_field(name="Region: ", value=data['regionName'])
                    embed.add_field(name="City: ", value=data['city'])
                    embed.add_field(name="Organisation: ", value=data['org'])
                    embed.add_field(name="ISP: ", value=data['isp'])
                    time = ctx.message.created_at
                    embed.set_footer(text=f"Asked by {ctx.author.name} " + time.strftime("%d/%m/%y %X"))
                    await ctx.send(embed=embed)
                else:
                    await ctx.send(f"```Could not find {ip}\n{text}```")
            elif response.status == 429:
                await ctx.send(f"```Daily iplookup limit reached```")
            else:
                await ctx.send(f"```There was an issue with the API, please try again later!\n{text}```")


    @commands.command(name="ping", description="Pings any provided IP")
    async def ping(self, ctx, ip: str, count: int = 3):
        text = "Usage: ./ping [ip] (count)\nMax count is 10"
        try:
            ip = socket.gethostbyname(ip)
        except socket.gaierror:
            await ctx.send(f"```Unable to resolve {ip} to a valid IP address\n{text}```")
        else:
            if utils.validate_ip(ip) is True:
                if count <= 10:
                    output = await ping_f(ip, count)
                    await ctx.send(f"```{output}```")
                else:
                    await ctx.send(f"```You may only have up to 10 ping requests\n{text}```")
            else:
                await ctx.send(f"```Please enter a valid IP address\n{text}```")

    @ping.error
    async def ping_error(self, ctx, error):
        text = "Usage: ./ping [ip] (count)\nMax count is 10"
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"```{text}```")
        else:
            await ctx.send(f"```An unknown error has occured!\n{text}```")
            raise error

    @commands.command(name="bannergrab", description="Grabs a banner from a port", aliases=["service"])
    async def bannergrab(self, ctx, ip, port):
        text = "Usage: ./bannergrab [IP] [Port]"
        try:
            ip = socket.gethostbyname(ip)
            if utils.validate_ip(ip) is True:
                if utils.validate_port(port) is True:
                    banner = await bannergrab_f(ip, port)
                    negatives = ["Port did not return a banner", "port closed", "target timed out"]
                    if banner in negatives:
                        response = f"""```diff
- {ip}:{port}:{banner} ```"""
                    else:
                        response = f"""```diff
+ {ip}:{port}:{banner} ```"""
                    await ctx.send(f"{response}")
                else:
                    await ctx.send(f"```Invalid port selected\n{text}```")
            else:
                await ctx.send(f"```Invalid IP\n{text}```")
        except socket.gaierror:
            await ctx.send(f"```Unable to connect to IP\n{text}```")

    @bannergrab.error
    async def bannergrab_error(self, ctx, error):
        text = "Usage: ./bannergrab [IP] [Port]"
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"```{text}```")
        else:
            await ctx.send(f"```An unknown error has occured!\n{text}```")
            raise error

    @commands.cooldown(2, 30, commands.BucketType.user)
    @commands.command(name="portscan", description="Scan for open ports", aliases=["servicescan"])
    async def portscan(self, ctx, ip, *, ports=None):
        text = """
Usage: ./portscan [ip] (ports)
Please seperate ports with ','
Note: Default ports are top 20 most common, max is 100"""
        try:
            ip = socket.gethostbyname(ip)
            check = utils.validate_ip(ip)
        except socket.gaierror:
            check = False
        if check is True:
            if ports is None:
                ports = self.common_ports
                valid = True
            else:
                ports = ports.split(",")
                if len(ports) <= 100:
                    for port in ports:
                        valid = utils.validate_port(port)
                        if valid is False:
                            await ctx.send(f"```Invalid port: {port}\n{text}```")
                            break

                else:
                    await ctx.send(f"```You may only scan up to 100 ports\n{text}```")
                    valid = False
            if valid is not False:
                results = []
                scanned_ports = []
                for port in ports:
                    if port not in scanned_ports:
                        scanned_ports.append(port)
                        results.append([port, await bannergrab_f(ip, int(port))])
                results_str = ""
                for x in results:
                    if x[1] == "port closed":
                        results_str += f"- {x[0]}: {x[1]}\n"
                    else:
                        results_str += f"+ {x[0]}: {x[1]}\n"
                if len(results_str) <= 1992:
                    await ctx.send(f"```diff\n{results_str}```")
                else:
                    filename = f"./scans/{ctx.author.id}.txt"
                    async with aiofiles.open(filename, 'a') as f:
                        await f.write(results_str)
                        await ctx.send(file=discord.File(filename))
                    os.remove(filename)

        else:
            await ctx.send(f"```Invalid IP or bot was unable to resolve IP from domain name\n{text}```")

    @portscan.error
    async def portscan_error(self, ctx, error):
        text = """
Usage: ./portscan [ip] (ports)
Please seperate ports with ','
Note: Default ports are top 20 most common, max is 100"""
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f"```Command is on cooldown, please wait {round(error.retry_after, 2)} seconds\n{text}```")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"```{text}```")
        else:
            await ctx.send(f"```An unknown error has occured\n{text}```")
            raise error

    @commands.command(name="dnslookup", description="Run DNS query on a host", aliases=["dns","nslookup"])
    async def dnsquery(self, ctx, domain, query):
        # https://github.com/al45tair/asyncdns.git
        text = """Usage: ./dnslookup [Domain name] [Query]
Valid Queries:
A, NS, CNAME, SOA, TXT, MX, AAAA, ANY
"""
        queryDict = {"a":1,"ns":2,"cname":5,"soa":6,"mx":15,"txt":16,"aaaa":28,"loc":29,"any":255}
        try:
            record = queryDict[query.lower()]
        except KeyError:
            await ctx.send(f"```{query} is not a valid query\n{text}```")
        else:
            resolver = asyncdns.Resolver()
            loop = asyncio.get_event_loop()
            x = asyncdns.Query(domain,record, asyncdns.IN)
            f = resolver.lookup(x, servers=[("8.8.8.8",53), ("8.8.4.4", 53)])
            loop.run_until_complete(f)
            print(f.result())
            await ctx.send(f"```{f.result()}```")

    @dnsquery.error
    async def dnsquery_error(self, ctx, error):
        text = """Usage: ./dnslookup [Domain name] [Query]
Valid Queries:
A, NS, CNAME, SOA, TXT, MX, AAAA, ANY
"""
        await ctx.send(f"```An unknown error has occured\n{text}```")
        raise error



def setup(client):
    client.add_cog(networking(client))
