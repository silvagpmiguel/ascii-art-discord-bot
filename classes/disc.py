import discord
import logging
from classes.message import Message
from classes.ascii import Ascii


class Client(discord.Client):
    async def on_ready(self):
        await self.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='!asc -h'))
        self.ascii = Ascii()
        self.message = Message()
        self.fonts = self.ascii.getAvailableFonts()
        self.discordLineLength = 121
        logger = logging.getLogger('discord')
        logger.setLevel(logging.WARNING)
        logging.basicConfig(
            format='%(asctime)s, %(levelname)s -> %(message)s', datefmt='%d/%m/%Y %I:%M:%S %p', filename='running.log',
            filemode='a', level=logging.INFO
        )

    async def on_message(self, message):
        content = message.content
        if content.startswith('!asc '):
            logging.info(
                '%s, %s, %s: %s',
                message.guild.name, message.channel.name, message.author.name, content
            )
            if content[5:7] == '-h' and len(content) == 7:
                logging.info('Help Message')
                await message.channel.send(embed=self.message.help())
                return
            elif content[5:7] == '-l' and len(content) == 7:
                logging.info('List Fonts')
                await message.channel.send(embed=self.message.listFonts(self.ascii.getAvailableFontsToString()))
                return
            elif content[5:8] == '-f ':
                content = content[8:]
                splitted = content.split(' ', 1)
                font = splitted[0] + ".json"
                if font not in self.fonts:
                    logging.error('Font Error: %s is not available', font)
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
                elif lower_letter == ' ' or lower_letter == '\n' or lower_letter == '\t':
                    line += ' '
            if self.checkLineSize(line):
                logging.error(
                    'Error: Max line size reached (%d > %d)',
                    len(line), self.discordLineLength
                )
                await channel.send(embed=self.message.limitError(len(line), self.discordLineLength))
                return
            ascii_art += line+"\n"
            x += 1
        ascii_art += "```"
        await channel.send(ascii_art)

    def checkLineSize(self, line):
        return len(line) > self.discordLineLength
