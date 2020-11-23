import discord

from classes.ascii import Ascii
from classes.message import Message


class Client(discord.Client):
    async def on_ready(self):
        await self.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='!asc -h'))
        self.ascii = Ascii()
        self.message = Message()
        self.fonts = self.ascii.getAvailableFonts()
        self.discordLineLength = 122

    async def on_message(self, message):
        content = message.content
        if content.startswith('!asc '):
            if content[5:7] == '-h':
                await message.channel.send(embed=self.message.help())
                return
            elif content[5:7] == '-l':
                await message.channel.send(embed=self.message.listFonts(self.ascii.getAvailableFontsToString()))
                return
            elif content[5:7] == '-f':
                content = content[8:]
                splitted = content.split(' ')
                font = splitted[0] + ".json"
                if font not in self.fonts:
                    await message.channel.send(embed=self.message.unavailableFontError(splitted[0]))
                    return
                self.ascii.setFont(font)
                content = splitted[1]
            else:
                content = content[5:]
            await self.doArt(content, message.channel)

    async def doArt(self, content, channel):
        x = 0
        ascii_art = "```\n"
        available_letters = self.ascii.getAvailableLetters()
        while x < self.ascii.getDepth():
            line = ""
            for letter in content:
                lower_letter = letter.lower()
                if lower_letter == 'ã' or lower_letter == 'á' or lower_letter == 'à':
                    lower_letter = 'a'
                elif lower_letter == 'ê' or lower_letter == 'é' or lower_letter == 'è':
                    lower_letter = 'e'
                elif lower_letter == 'í' or lower_letter == 'ì':
                    lower_letter = 'i'
                elif lower_letter == 'õ' or lower_letter == 'ó' or lower_letter == 'ò':
                    lower_letter = 'o'
                elif lower_letter == 'ú' or lower_letter == 'ù':
                    lower_letter = 'u'
                elif lower_letter == 'ç':
                    lower_letter = 'c'
                if lower_letter in available_letters:
                    line += self.ascii.getLetter(lower_letter)[x]
                else:
                    line += "  "
                if self.checkLineSize(line):
                    await channel.send(embed=self.message.limitError())
                    return
            ascii_art += line+"\n"
            x += 1
        ascii_art += "```"
        await channel.send(ascii_art)

    def checkLineSize(self, line):
        return len(line) > self.discordLineLength
