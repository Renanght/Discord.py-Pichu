from discord.ext import commands
from discord.ui import Select, View
import discord


class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        if "pichu" in message.content.lower() or "pitchu" in message.content.lower():
            await message.channel.send("Pitchuuuu ⚡️")

    @commands.command(name="ping", help="Check the bot's latency.")  
    async def ping(self, ctx):
        bot_latency = round(self.bot.latency * 1000)
        await ctx.send(f"Pong! Latency is `{bot_latency}ms`.")

    @commands.command(name="help", help="List all available commands")
    async def help(self, ctx):
        intro_embed = discord.Embed(
            title="The following categories are available :four_leaf_clover:",
            description="Select a category to see the corresponding commands.",
            color=discord.Color.green()
        )

        select_options = [
            discord.SelectOption(
                label=cog_name,
                description=f"{cog_name}'s Commands.",
                value=cog_name
            )
            for cog_name in self.bot.cogs
        ]

        select = Select(placeholder="Select a category", options=select_options)

        async def select_callback(interaction: discord.Interaction):
            if interaction.user != ctx.author:
                await interaction.response.send_message("You cannot use this menu.", ephemeral=True)
                return

            cog_name = interaction.data["values"][0]
            embed = discord.Embed(title=f"Help - {cog_name}", color=discord.Color.blue())

            cog = self.bot.get_cog(cog_name)
            if cog:
                commands_list = "\n".join(
                    f"**/{command.name}** - {command.help or 'No description available.'}"
                    for command in cog.get_commands()
                )
                embed.description = commands_list
            else:
                embed.description = "No commands available for this category."

            await interaction.response.edit_message(embed=embed, view=view)

        select.callback = select_callback 

        view = View()
        view.add_item(select)

        await ctx.send(embed=intro_embed, view=view)


async def setup(bot):
    await bot.add_cog(General(bot))
