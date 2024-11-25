from discord.ext import commands
from discord.ui import Select, View
import discord


class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        # Ignore les messages du bot
        if message.author.bot:
            return

        # Vérifie si "Pichu" ou "pitchu" est dans le contenu du message
        if "pichu" in message.content.lower() or "pitchu" in message.content.lower():
            await message.channel.send("Pitchuuuu ⚡️")

    @commands.command(name="ping", help="Check the bot's latency.")  
    async def ping(self, ctx):
        bot_latency = round(self.bot.latency * 1000)
        await ctx.send(f"Pong! Latency is `{bot_latency}ms`.")

    @commands.command(name="help", help="List all available commands")
    async def help(self, ctx):
        # Embed introductif
        intro_embed = discord.Embed(
            title="The following categories are available :four_leaf_clover:",
            description="Select a category to see the corresponding commands.",
            color=discord.Color.green()
        )

        # Créer les options dynamiquement à partir des cogs chargés
        select_options = [
            discord.SelectOption(
                label=cog_name,
                description=f"{cog_name}'s Commands.",
                value=cog_name
            )
            for cog_name in self.bot.cogs
        ]

        # Créer le menu déroulant
        select = Select(placeholder="Select a category", options=select_options)

        # Callback pour gérer l'interaction avec le menu
        async def select_callback(interaction: discord.Interaction):
            if interaction.user != ctx.author:
                await interaction.response.send_message("You cannot use this menu.", ephemeral=True)
                return

            # Récupérer la catégorie sélectionnée
            cog_name = interaction.data["values"][0]
            embed = discord.Embed(title=f"Help - {cog_name}", color=discord.Color.blue())

            # Récupérer les commandes du cog sélectionné
            cog = self.bot.get_cog(cog_name)
            if cog:
                # Ajouter les commandes sous forme de texte dans la description
                commands_list = "\n".join(
                    f"**/{command.name}** - {command.help or 'No description available.'}"
                    for command in cog.get_commands()
                )
                embed.description = commands_list
            else:
                embed.description = "No commands available for this category."

            # Mettre à jour le message avec les informations du cog
            await interaction.response.edit_message(embed=embed, view=view)

        select.callback = select_callback  # Associer le callback au menu déroulant

        # Créer la vue et y ajouter le menu déroulant
        view = View()
        view.add_item(select)

        # Envoyer le message avec le menu déroulant
        await ctx.send(embed=intro_embed, view=view)


async def setup(bot):
    await bot.add_cog(General(bot))
