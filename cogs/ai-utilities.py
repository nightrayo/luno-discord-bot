import disnake 
from disnake.ext import commands
from openai import OpenAI
import os
from dotenv import load_dotenv
from deep_translator import GoogleTranslator


load_dotenv()

AI_TOKEN = os.getenv("AI_TOKEN")

client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key=AI_TOKEN,
)


class UserSlashCMD(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.slash_command(description="Запрос к ИИ")
    async def ai(self, inter: disnake.ApplicationCommandInteraction, content: str):
        await inter.response.defer()

        try:
            completion = client.chat.completions.create(
            model="deepseek/deepseek-chat-v3-0324:free",
            messages=[
                {
                    "role": "user",
                    "content": content
                }
            ]
            )    
            response_text = completion.choices[0].message.content

            if len(response_text) <= 2000:
                await inter.edit_original_response(content=response_text)
            else:
                chunks = [response_text[i:i+2000] for i in range(0, len(response_text), 2000)]
                await inter.edit_original_response(content=chunks[0])
                for chunk in chunks[1:]:
                    await inter.followup.send(chunk)
        except Exception as e:
            await inter.edit_original_response(content=f"❌ Ошибка: {str(e)}")


    @commands.slash_command(description="Переводит текст")
    async def translate(self, inter: disnake.ApplicationCommandInteraction, text, target='fr'):
        await inter.response.send_message(GoogleTranslator(source='auto', target=target).translate(text), ephemeral=True)

def setup(bot):
    bot.add_cog(UserSlashCMD(bot))