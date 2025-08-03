import disnake 
from disnake.ext import commands
from bot import temp_voice_channels


class VoiceChannels(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    
    @commands.slash_command(description="Создать временый голосовой канал с теми же участниками")
    async def create_voice(self, inter: disnake.ApplicationCommandInteraction, name: str) -> None:
        author = inter.author

        if not author.voice or not author.voice.channel:
            await inter.response.send_message("Вы должны находиться в голосом канале!", ephemeral=True)
            return
    
        old_channel = author.voice.channel
        guild = inter.guild

        new_channel = await guild.create_voice_channel(
            name=f'{name}',
            category=old_channel.category,
            user_limit=old_channel.user_limit,
            bitrate=old_channel.bitrate
        )
        temp_voice_channels.add(new_channel.id)

        for member in old_channel.members:
            try:
                await member.move_to(new_channel)
            except Exception as e:
                await inter.channel.send(f"Ошибка при перемещении {member.display_name}: {e}")

        await inter.response.send_message(f"Создан канал {new_channel.name} и участники перемещены.", ephemeral=True) 



def setup(bot):
    bot.add_cog(VoiceChannels(bot))