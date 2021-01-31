import discord as dc 
from dotenv import load_dotenv
from os import getenv
import datetime as dt
import json

#*#*# pathVariables #*#*#
config_relative_path = r'2021\q1\USIS_PythonBot\config.json'
database_relative_path = r'2021\q1\USIS_PythonBot\db.json'
#*#*#*#*#*#*#*#*#*#*#*#*#

load_dotenv()
token = getenv("TOKEN")

with open(config_relative_path) as f:
    cfg = json.load(f)
with open(database_relative_path) as f:
    db = json.load(f)

class BOT(dc.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.prefix = cfg['prefix']
        self.perms = cfg['perms']

    async def on_ready(self):
        for guild in self.guilds:
            print(f"{self.user} connected to {guild.name}, id: {guild.id}")
        print(f"{self.user.name} is alive!")

    async def on_message(self, message):
        if message.author == self.user:
            return
        if message.content.startswith(self.prefix):
            await self.command(message)
        elif (self.user.name+" ssie") in message.content or (self.user.name+" sucks") in message.content:
            await message.reply("૮( ᵒ̌▱๋ᵒ̌ )ა ?!")

    async def command(self, message):
        content = message.content[len(self.prefix):]
        args = content.split()[1::] if len(content.split()) > 1 else [None]
        command = content.split()[0]

        if content == "hi":
            await message.reply("hi!")

        # user info embed getter
        elif content.startswith("me"):
            await self.getMeEmbed(message)

        # role/channel ID getter
        elif command == "id":
            if len(args) == 1:
                if len(message.role_mentions) == 1:
                    await message.channel.send(f"id: `{message.role_mentions[0].id}`")
                elif len(message.channel_mentions) == 1:
                    await message.channel.send(f"id: `{message.channel_mentions[0].id}`")

        # avatar getter
        elif command == "avatar" or command == "av" :
            if message.mentions: 
                avatar_url = self.getAvatarURL(message.mentions[0])
            else: avatar_url = self.getAvatarURL(message.author)
            await message.reply(avatar_url)

        # perms getter/setter
        elif command == "perms" or command == "permissions":
            if args[0] == "add":
                if self.checkPerms(message.author, 2):
                    try:
                        lvl = args[1]
                        roleID = message.channel_mentions[0]
                    except:
                        await message.reply(f"{message.author.mention} please specify a permission level and role to assign the permission to.")
                else:
                    await message.reply("Your permission level is too low to use this command!")
            else:
                perm_lvl = self.getUserPerms(message.author)
                await message.reply(f"your permission level: `{perm_lvl}`")
        
        # bot prefix setter
        elif command == "prefix":
            if args[0]:
                self.setPrefix(args[0])
                await message.channel.send(f"prefix successfully set to: `{args[0]}`")


    def getUserPerms(self, user):
        lvls = [0]
        for permLvl in db['rolePerms']:
            if any([role.id in permLvl.values() for role in user.roles]):
                lvls.append(int(list(permLvl.keys())[0]))
        return max(lvls)

    def checkPerms(self, user, perm_lvl):
        return self.getUserPerms(user) >= perm_lvl

    def getAvatarURL(self, user):
        base = "https://cdn.discordapp.com/avatars/"
        return base+str(user.id)+"/"+str(user.avatar)

    async def getMeEmbed(self, message, user = None):
        embed = dc.Embed(title="User info")
        if not user:
            user = message.author
        embed.color = user.color
        embed.set_image(url=self.getAvatarURL(user))

        joined_info = f"Account created on: `{user.joined_at.strftime('%Y, %m, %d')}`"
        joined_info += f"\nUsed discord for: `{str(dt.datetime.now() - user.joined_at)} days`"

        user_roles = [role.name for role in user.roles if role.name != "@everyone"].reverse()
        if not user_roles:
            roles_info = "No roles to see here!"
        else:
            roles_info = ", ".join(user_roles)

        embed.add_field(name="Join Date", value=joined_info, inline=False)
        embed.add_field(name="User Roles", value=roles_info, inline=False)
        await message.channel.send(embed=embed)

    def setPrefix(self, new_prefix):
        cfg["prefix"] = new_prefix
        with open(config_relative_path) as f:
            json.dump(cfg, f)
        self.prefix = new_prefix

bot_client = BOT()
bot_client.run(token)


