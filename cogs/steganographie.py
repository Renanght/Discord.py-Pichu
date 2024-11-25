import discord
from discord.ext import commands
from PIL import Image
from PIL.ExifTags import TAGS
import exifread
import os
import requests
from lxml import etree
from io import BytesIO


class Steganographie(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def fetch_image(self, ctx, link=None):
        if link:
            response = requests.get(link)
            if response.status_code == 200:
                file_path = "temp_image.jpg"
                with open(file_path, "wb") as file:
                    file.write(response.content)
                return file_path
        elif ctx.message.attachments:
            attachment = ctx.message.attachments[0]
            file_path = "temp_image.jpg"
            await attachment.save(file_path)
            return file_path
        return None

    def extract_exif(self, image_path):
        try:
            image = Image.open(image_path)
            exif_data = image._getexif()
            if exif_data:
                return {TAGS.get(tag, tag): value for tag, value in exif_data.items()}
            return None
        except Exception as e:
            return str(e)

    def extract_other_metadata(self, image_path):
        try:
            with open(image_path, "rb") as file:
                tags = exifread.process_file(file)
            return tags
        except Exception as e:
            return str(e)

    def extract_xmp(self, image_path):
        try:
            with open(image_path, "rb") as file:
                data = file.read()
                start = data.find(b"<x:xmpmeta")
                end = data.find(b"</x:xmpmeta>") + len(b"</x:xmpmeta>")
                if start != -1 and end != -1:
                    xmp_data = data[start:end]
                    xml_tree = etree.fromstring(xmp_data)
                    xmp_dict = {}
                    for element in xml_tree.xpath("//*"):
                        if element.text and element.text.strip():
                            xmp_dict[element.tag] = element.text.strip()
                    return xmp_dict
                return None
        except Exception as e:
            return str(e)

    @commands.command(name="exif", help="List all exif informations")
    async def exif(self, ctx, link=None):
        image_path = await self.fetch_image(ctx, link)
        if not image_path:
            await ctx.send("Aucune image trouvée. Fournis un lien ou une pièce jointe.")
            return

        exif_data = self.extract_exif(image_path)
        if not exif_data:
            await ctx.send("Aucune donnée EXIF trouvée.")
        else:
            exif_text = "\n".join(f"{key}: {value}" for key, value in exif_data.items())
            await ctx.send(f"Données EXIF extraites :\n```{exif_text[:2000]}```")

        os.remove(image_path)

    @commands.command(name="iptc", help="List all iptc informations")
    async def iptc(self, ctx, link=None):
        image_path = await self.fetch_image(ctx, link)
        if not image_path:
            await ctx.send("Aucune image trouvée. Fournis un lien ou une pièce jointe.")
            return

        iptc_data = self.extract_other_metadata(image_path)
        if not iptc_data:
            await ctx.send("Aucune donnée IPTC trouvée.")
        else:
            iptc_text = "\n".join(f"{key}: {value}" for key, value in iptc_data.items())
            await ctx.send(f"Données IPTC extraites :\n```{iptc_text[:2000]}```")

        os.remove(image_path)

    @commands.command(name="xmp", help="List all xmp informations")
    async def xmp(self, ctx, link=None):
        image_path = await self.fetch_image(ctx, link)
        if not image_path:
            await ctx.send("Aucune image trouvée. Fournis un lien ou une pièce jointe.")
            return

        xmp_data = self.extract_xmp(image_path)
        if not xmp_data:
            await ctx.send("Aucune donnée XMP trouvée.")
        else:
            xmp_text = "\n".join(f"{key}: {value}" for key, value in xmp_data.items())
            await ctx.send(f"Données XMP extraites :\n```{xmp_text[:2000]}```")

        os.remove(image_path)

    @commands.command(name="rmexif", help="Remove all Metadata of an image")
    async def rmexif(self, ctx, link=None):
        image_path = await self.fetch_image(ctx, link)
        if not image_path:
            await ctx.send("Aucune image trouvée. Fournis un lien ou une pièce jointe.")
            return

        try:
            image = Image.open(image_path)

            data = list(image.getdata())
            new_image = Image.new(image.mode, image.size)
            new_image.putdata(data)

            buffer = BytesIO()
            new_image.save(buffer, format="JPEG")
            buffer.seek(0)

            file = discord.File(buffer, filename="image_sans_exif.jpg")
            await ctx.send("Voici l'image sans métadonnées EXIF :", file=file)

        except Exception as e:
            await ctx.send(f"Une erreur s'est produite lors du traitement de l'image : {e}")

        finally:
            os.remove(image_path)


async def setup(bot):
    await bot.add_cog(Steganographie(bot))
