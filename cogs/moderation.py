import disnake 
from disnake.ext import commands


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    
    @commands.slash_command(description="Исключить участника с сервера")
    @commands.has_permissions(kick_members=True, administrator=True)
    async def kick(self, inter: disnake.ApplicationCommandInteraction, member: disnake.Member, reason: str = "Нарушение правил") -> None:
        await inter.send(f"👢 Пользователь {member.mention} был исключён администратором {inter.author.mention}.", delete_after=3)
        await member.kick(reason=reason)


    @commands.slash_command(description="Забанить участника на сервере")
    @commands.has_permissions(ban_members=True, administrator=True)
    async def ban(self, inter: disnake.ApplicationCommandInteraction, member: disnake.Member, reason: str = "Нарушение правил"):
        await inter.response.send_message(f"🔨 Пользователь {member.mention} был забанен. Причина: {reason}", ephemeral=True)
        await member.ban(reason=reason)

    
    @commands.slash_command(description="Замьютить участника")
    async def mute(self, inter: disnake.ApplicationCommandInteraction, member: disnake.Member, reason: str = "Причина не указана"):
        muted_role = disnake.utils.get(inter.guild.roles, name="Muted")

        if not muted_role:
            muted_role = await inter.guild.create_role(name="Muted")
            for channel in inter.guild.text_channels:
                await channel.set_permissions(muted_role, send_messages=False)
            for channel in inter.guild.voice_channels:
                await channel.set_permissions(muted_role, speak=False, connect=False)

        
        await member.add_roles(muted_role, reason=reason)
        await inter.response.send_message(f"🔇 Пользователь {member.mention} был замьючен. Причина: {reason}", ephemeral=True)
    

    @commands.slash_command(description="Размьютить участника")
    async def unmute(self, inter: disnake.ApplicationCommandInteraction, member: disnake.Member, reason: str = "Причина не указана"):
        muted_role = disnake.utils.get(inter.guild.roles, name="Muted")
        
        await member.remove_roles(muted_role, reason=reason)
        await inter.response.send_message(f"🔈 Пользователь {member.mention} был размьючен. Причина: {reason}", ephemeral=True)
    

def setup(bot):
    bot.add_cog(Moderation(bot))