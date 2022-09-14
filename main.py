import os
from io import BytesIO

import aiohttp
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())


@bot.event
async def on_ready():
    print("connected")


@bot.command()
async def copy(ctx, emoji, name):
    filterid = emoji.split(":")[2].replace(">", "")

    embed = discord.Embed(
        title="copying emoji..."
    )

    embed.set_image(url=f"https://cdn.discordapp.com/emojis/{filterid}")
    embedobject = await ctx.reply(embed=embed)

    guild = ctx.guild
    if ctx.author.guild_permissions.manage_emojis:
        async with aiohttp.ClientSession() as ses:
            async with ses.get(f"https://cdn.discordapp.com/emojis/{filterid}") as r:

                try:
                    img_or_gif = BytesIO(await r.read())
                    b_value = img_or_gif.getvalue()
                    if r.status in range(200, 299):
                        emoji = await guild.create_custom_emoji(image=b_value, name=name)
                        embed = discord.Embed(
                            title="EmojiGrabber",
                            description=f"✅ | I successfully stole the emoji and added it to this server.\n"
                                        f"\n"
                                        f"Emoji: <:{name}:{emoji.id}>\n"
                                        f'Emoji ID: {emoji.id}\n'
                                        f'ImageURL: [Click to open]({f"https://cdn.discordapp.com/emojis/{filterid}"})\n'
                                        f'Emoji Name: {name}'
                        )
                        await embedobject.edit(embed=embed)
                        await ses.close()
                    else:
                        embed = discord.Embed(
                            title="EmojiGrabber",
                            description="❌ | There was an Error while trying to copy the emoji.\n"
                                        "\n"
                                        "Make sure there are no numbers in the name of the emoji you want to copy."
                        )
                        await embedobject.edit(embed=embed)
                        await ses.close()

                except discord.HTTPException:
                    await ctx.send('File size is too big!')


bot.run(os.getenv("TOKEN"))
