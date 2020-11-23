import discord


class Message:
    def help(self):
        return discord.Embed(
            title='Ascii: Help Me',
            description='**Usage**\n`!asc <command> [arguments]`\n\n**Available Commands**\n- `!asc -h` - Print help\n- `!asc -l` - Print available fonts\n- `!asc -f [font] [input]` - Print ascii art with font\n- `!asc [input]` - Print ascii art',
            color=discord.Color.blue()
        )

    def listFonts(self, fonts):
        return discord.Embed(
            title='Ascii: Available Fonts',
            description=fonts,
            color=discord.Color.blue()
        )

    def limitError(self, size, discordSize):
        return discord.Embed(
            title='Ascii: Limit Error :(',
            description=f'Sorry, this text is **larger** than the maximum line size of the **discord**.\nThe line supports **{discordSize}** characters, and the text you typed is **{size}**.',
            color=discord.Color.red()
        )

    def unavailableFontError(self, font):
        return discord.Embed(
            title='Ascii: Font Error :(',
            description=f'Sorry, **{font}** isn\'t available!',
            color=discord.Color.red()
        )
