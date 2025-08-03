import disnake 
from disnake.ext import commands
from bot import temp_voice_channels


class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    
    @commands.Cog.listener()
    async def on_ready(self) -> None:
        print(f"Bot {self.bot.user} is ready to work!")


    @commands.Cog.listener()
    async def on_voice_state_update(self, member: disnake.Member, before: disnake.VoiceState, after: disnake.VoiceState) -> None:
        if before.channel and before.channel != after.channel:
            voice_channel = before.channel

            if voice_channel.id in temp_voice_channels and len(voice_channel.members) == 0:
                try:
                    await voice_channel.delete()
                    print(f"Удалён пустой канал: {voice_channel.name}")
                except disnake.Forbidden:
                    print("Нет прав для удаления канала.")
                except Exception as e:
                    print(f"Ошибка при удалении канала: {e}")   


    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = self.bot.get_channel(1333273530909069342)
        embed = disnake.Embed(
            title="👋 Добро пожаловать!",
            description=f"{member.mention}, рады видеть тебя на сервере!",
            color=0x799ed1
        )
        embed.set_image(url="https://i.pinimg.com/originals/25/93/4f/25934f82c4e78f171ca27995f3ec9c17.gif") 
        embed.set_footer(text="Нас становится больше! ❤️")
        embed.timestamp = disnake.utils.utcnow()

        await channel.send(embed=embed) 

    
def setup(bot):
    bot.add_cog(Events(bot))