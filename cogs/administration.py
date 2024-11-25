import discord
from discord.ext import commands

class Administration(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print("Cog 'Administration' chargé avec succès !")

    @commands.command(name="clear", help="Deletes a specific number of messages in this channel.")
    async def clear(self, ctx, amount: int):

        if amount < 1:
            await ctx.send("❌ Vous devez supprimer au moins un message.")
            return

        deleted = await ctx.channel.purge(limit=amount)
        await ctx.send(f"✅ {len(deleted)} messages ont été supprimés.")

async def setup(bot):
    await bot.add_cog(Administration(bot))
