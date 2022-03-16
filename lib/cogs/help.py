import discord, math, re
from discord.ext import commands
from discord import Embed
from pygicord import Paginator

def syntax(command):
    cmd_and_aliases = " | ".join([str(command), *command.aliases])
    params = []

    for key, value in command.params.items():
        if key not in ("self", "ctx"):
            params.append(f"({key})" if "NoneType" in str(value) else f"[{key}]")

    params = " ".join(params)
    return f"`{cmd_and_aliases} {params}`"

class help(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.client.remove_command('help')

    @commands.command(name="help", aliases=["commands", "h"], description="Displays this command")
    async def help(self, ctx):
        pages = []
        # MAIN MENU
        main = Embed(title="Command help", colour=discord.Colour.random())
        main.add_field(name="```(1) Main```", value="Main page", inline=False)
        main.add_field(name="```(2) Network```", value="Networking utilities", inline=False)
        main.add_field(name="```(3) Website ```", value="Website utilities")
        main.add_field(name="```(4) Recourses```", value="A list of programming and hacking recourses", inline=False)
        main.add_field(name="```(5) OSINT```", value="OSINT Utilities")
        main.add_field(name="```(6) Administration```", value="General administration commands", inline=False)
        main.add_field(name="```(7) Maths```", value="Math utilities", inline=False)
        main.add_field(name="```(8) Utility```", value="General purpose utility commands", inline=False)
        main.add_field(name="```(9) Exploit ```", value="Exploit research commands", inline=False)
        main.add_field(name="```(10) Encoding```", value="Hashing, crypto, encoding", inline=False)
        main.set_footer(text="Please use the 🔢 button to jump to a page (page 1 out of 10)")
        pages.append(main)

        # HACKING AND NETWORKING UTILS
        utils = Embed(title="Networking utilities", colour=discord.Colour.random())
        for command in self.client.get_cog("networking").walk_commands():
            if command.hidden:
                continue
            elif command.parent is not None:
                continue
            else:
                utils.add_field(name=f"**{command.name}**", value=f"{command.description} - Format: {syntax(command)}", inline=False)

        utils.set_footer(text="Please use the 🔢 button to jump to a page (page 2 out of 11)")
        pages.append(utils)

        # WEBSITE AND CRYPTO UTILS
        web = Embed(title="Website and cryptography utilities", colour=discord.Colour.random())
        for command in self.client.get_cog("web").walk_commands():
            if command.hidden:
                continue
            elif command.parent is not None:
                continue
            else:
                web.add_field(name=f"**{command.name}**", value=f"{command.description} - Format: {syntax(command)}", inline=False)
        web.set_footer(text="Please use the 🔢 button to jump to a page (page 3 out of 11)")
        pages.append(web)

        # RECOURSES
        recourses = Embed(title="Recourses", colour=discord.Colour.random())
        for command in self.client.get_cog("recourses").walk_commands():
            if command.hidden:
                continue
            elif command.parent is not None:
                continue
            else:
                recourses.add_field(name=f"**{command.name}**", value=f"{command.description} - Format: {syntax(command)}", inline=False)
        recourses.set_footer(text="Please use the 🔢 button to jump to a page (page 4 out of 11)")
        pages.append(recourses)

        # OSINT
        OSINT = Embed(title="OSINT utilities", colour=discord.Colour.random())
        for command in self.client.get_cog("osint").walk_commands():
            if command.hidden:
                continue
            elif command.parent is not None:
                continue
            else:
                OSINT.add_field(name=f"**{command.name}**", value=f"{command.description} - Format: {syntax(command)}", inline=False)
        OSINT.set_footer(text="Please use the 🔢 button to jump to a page (page 5 out of 11)")
        pages.append(OSINT)

        # ADMIN
        admin = Embed(title="General administration commands", colour=discord.Colour.random())
        for command in self.client.get_cog("admin").walk_commands():
            if command.hidden:
                continue
            elif command.parent is not None:
                continue
            else:
                admin.add_field(name=f"**{command.name}**", value=f"{command.description} - Format: {syntax(command)}", inline=False)
        admin.set_footer(text="Please use the 🔢 button to jump to a page (page 6 out of 11)")
        pages.append(admin)

        # MATHS
        maths = Embed(title="Math utilities", colour=discord.Colour.random())
        for command in self.client.get_cog("maths").walk_commands():
            if command.hidden:
                continue
            elif command.parent is not None:
                continue
            else:
                maths.add_field(name=f"**{command.name}**", value=f"{command.description} - Format: {syntax(command)}", inline=False)
        maths.set_footer(text="Please use the 🔢 button to jump to a page (page 7 out of 11)")
        pages.append(maths)

        # CONVERSIONS
        utils = Embed(title="General purpose utilities", colour=discord.Colour.random())
        for command in self.client.get_cog("utility").walk_commands():
            if command.hidden:
                continue
            elif command.parent is not None:
                continue
            else:
                utils.add_field(name=f"**{command.name}**", value=f"{command.description} - Format: {syntax(command)}", inline=False)
        utils.set_footer(text="Please use the 🔢 button to jump to a page (page 8 out of 11)")
        pages.append(utils)

        # FUN
        exploit = Embed(title="exploit research commands", colour=discord.Colour.random())
        for command in self.client.get_cog("exploits").walk_commands():
            if command.hidden:
                continue
            elif command.parent is not None:
                continue
            else:
                exploit.add_field(name=f"**{command.name}**", value=f"{command.description} - Format: {syntax(command)}", inline=False)
        exploit.set_footer(text="Please use the 🔢 button to jump to a page (page 9 out of 11)")
        pages.append(exploit)

        # AI
        encoding = Embed(title="Hashing, crypto and encoding", colour=discord.Colour.random())
        for command in self.client.get_cog("encoding").walk_commands():
            if command.hidden:
                continue
            elif command.parent is not None:
                continue
            else:
                encoding.add_field(name=f"**{command.name}**", value=f"{command.description} - Format: {syntax(command)}", inline=False)
        encoding.set_footer(text="Please use the 🔢 button to jump to a page (page 10 out of 11)")
        pages.append(encoding)

        paginator = Paginator(pages=pages)
        await paginator.start(ctx)
def setup(client):
    client.add_cog(help(client))
