import disnake 
from disnake.ext import commands
from datetime import datetime


class BasicCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    
    @commands.command()
    async def help(self, ctx: commands.Context) -> None:
        embed = disnake.Embed(
        title="📚 Помощь по командам",
        description="Доступные команды бота:\n\n"
                    "**Основные команды:**\n"
                    "`!ping` - Проверка связи с ботом\n"
                    "`!info` - Информация о боте\n\n"
                    "**Голосовые каналы:**\n"
                    "`/create_voice` - Создать временный голосовой канал\n\n"
                    "**Модерация:**\n"
                    "`/kick` - Исключить участника\n"
                    "`/ban` - Забанить участника\n"
                    "`/mute` - Замьютить участника\n"
                    "`/unmute` - Размьютить участника\n\n"
                    "**Музыка:**\n"
                    "`/play` - Воспроизвести музыку\n"
                    "`/stop` - Остановить музыку\n\n"
                    "**ИИ и прочее:**\n"
                    "`/ai` - Запрос к искусственному интеллекту\n"
                    "`/translate` - Перевести текст\n"
                    "`/userinfo` - Информация о пользователе",
                    
        color=disnake.Color.dark_theme()
        )
    
        embed.set_footer(
            text=f"Запросил: {ctx.author.display_name}",
            icon_url=ctx.author.avatar.url if ctx.author.avatar else None
        )
    
        embed.set_thumbnail(url=self.bot.user.avatar.url if self.bot.user.avatar else None)
    
        await ctx.send(embed=embed)


    @commands.slash_command(description="Показать информацию о пользователе")
    async def userinfo(self, inter: disnake.ApplicationCommandInteraction, member: disnake.Member):
        member = member or inter.author

        embed = disnake.Embed(
            title=f"Профиль: {member.display_name}",
            color=0x799ed1,
            timestamp=datetime.utcnow()
        )

        avatar_url = member.avatar.url if member.avatar else member.default_avatar.url
        embed.set_thumbnail(url=avatar_url)
        embed.set_footer(text=f"ID: {member.id}")

        embed.add_field(name="🆔 Уникальный ID", value=str(member.id), inline=True)
        embed.add_field(name="📅 Присоединился", value=member.joined_at.strftime("%d.%m.%Y"), inline=True)
        embed.add_field(name="💼 Роли", value=", ".join([role.mention for role in member.roles[1:]]) or "Нет", inline=False)

        await inter.response.send_message(embed=embed)


def setup(bot):
    bot.add_cog(BasicCommands(bot))