import disnake 
from disnake.ext import commands
import yt_dlp
import asyncio


ytdl_format_options = {
    "format": "bestaudio/best",
    "quiet": True,
    "no_warnings": True,
    "noplaylist": True,
    "simulate": True,  # Не скачивать, только получать информацию
    "forceurl": True,  # Получать прямую ссылку на аудио
    "skip_download": True,  # Пропустить скачивание
    "extractaudio": True,  # Извлекать аудио
    "audioformat": "mp3",
    "extract_flat": True,  # Для Spotify/VK
    "socket_timeout": 10,
    "extract_flat": True,
    "geo-bypass": True,
    "force-generic-extractor": True,
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

ffmpeg_options = {
    "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
    "options": "-vn -filter:a volume=0.8"
}

ytdl = yt_dlp.YoutubeDL(ytdl_format_options)


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.slash_command(description="Воспроизвести музыку")
    async def play(self, inter: disnake.ApplicationCommandInteraction, url):
        if not inter.author.voice or not inter.author.voice.channel:
            await inter.response.send_message("Ты должен быть в голосовом канале!", ephemeral=True)
            return

        channel = inter.author.voice.channel

        voice_client = inter.guild.voice_client

        if voice_client is None:
            voice_client = await channel.connect()
        elif voice_client.channel != channel:
            await voice_client.move_to(channel)

        await inter.response.defer()  

        loop = asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=False))
        audio_url = data['url']
        title = data.get('title', 'Без названия')

        source = disnake.FFmpegPCMAudio(audio_url, **ffmpeg_options)
        voice_client.play(source, after=lambda e: print(f"Ошибка: {e}") if e else None)

        await inter.followup.send(f"🎵 Сейчас играет: **{title}**")

    
    @commands.slash_command(description="Остановить музыку")
    async def stop(self, inter: disnake.ApplicationCommandInteraction):
        voice_client = inter.guild.voice_client
        if voice_client:
            await voice_client.disconnect()
            await inter.response.send_message("⏹️ Остановлено.")
        else:
            await inter.response.send_message("Бот не в голосовом канале.")


def setup(bot):
    bot.add_cog(Music(bot))