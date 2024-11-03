import disnake
from disnake.ext import commands
import os
import json
import sqlite3
import asyncio

bot = commands.InteractionBot(intents=disnake.Intents.all())

conn = sqlite3.connect("main.db")
cursor = conn.cursor()


    

with open("config.json", "r") as f:
    data = json.load(f)




@bot.event
async def on_ready():
    cursor.execute("CREATE TABLE IF NOT EXISTS vouches (user INTEGER, seller INTEGER, stars INTEGER, message TEXT, timestamp TEXT)")
    conn.commit()
    print(f"{bot.user} is ready and online")
    print(f"-" * 24)
    print(f"Bot was made and developed by: @userxx77")
    print(f"Support Discord: https://discord.gg/uxdevelopment")
    print(f"-" * 24)

@bot.slash_command(name="vouch")
async def vouch(inter:disnake.ApplicationCommandInteraction):
    pass

@vouch.sub_command(name="add", description="Leave a review for the server")
async def add(inter:disnake.ApplicationCommandInteraction,
              *,
              stars:int=commands.Param(choices=[1, 2, 3, 4, 5]),
              message: str = commands.Param(description="Leave a custom message for your review", max_length=128),
              seller: disnake.Member,
              image:disnake.Attachment = commands.Param(default=None)):
    
    role = disnake.utils.get(inter.guild.roles, id=data['role'])
    if role not in inter.user.roles:
        embed = disnake.Embed(description="You do not have the required role to run this command", color=0xff0000)
        await inter.response.send_message(embed=embed, ephemeral=True, delete_after=15)
        return
    if inter.guild is None:
        return
    emoj = "⭐" * stars
    timestampa = f"<t:{int(inter.created_at.timestamp())}:R>"
    embed = disnake.Embed(title="New Vouch", url="https://discord.gg/uxdevelopment", description=emoj, color=0x2b2d31)
    embed.add_field(name="Vouch", value=message, inline=False)
    embed.add_field(name="Seller", value=seller.mention, inline=True)
    embed.add_field(name="Timestamp", value=timestampa)
    if image:
        embed.set_image(url=image.url)
    embed.set_thumbnail(url=inter.user.avatar.url if inter.user.avatar else inter.user.default_avatar.url)
    embed.set_author(name=inter.user.name, icon_url=inter.user.avatar.url if inter.user.avatar else inter.user.default_avatar.url)
    embed.set_footer(text="discord.gg/uxdevelopment")
    t = inter.guild.get_channel(data['channel'])
    if t:
        await t.send(embed=embed)
    try:
        cursor.execute("INSERT INTO VOUCHES (user, seller, stars, message, timestamp) VALUES (?, ?, ?, ?, ?)", (inter.user.id, seller.id, stars, message, timestampa))
    except Exception as e:
        print(e)

    conn.commit()


@vouch.sub_command(name="reload", description="Reload the vouches")
@commands.is_owner()
async def reload(inter:disnake.ApplicationCommandInteraction):
    t = inter.guild.get_channel(data['channel'])
    if not t:
        await inter.response.send_message(f"The channel with the id {data['channel']} does not exist", ephemeral=True, delete_after=15)
        return
    await inter.response.send_message("The stored vouches will now start to be reloaded")
    cursor.execute("SELECT * FROM vouches")
    result = cursor.fetchall()
    for row in result:
        emoj = "⭐" * row[2]
        embed = disnake.Embed(title="New Vouch", description=f"{emoj}", url="https://discord.gg/uxdevelopment", color=0x2b2d31)
        embed.add_field(name="Vouch", value=row[3], inline=False)
        embed.add_field(name="Seller", value=f"<@{row[1]}>", inline=True)
        embed.add_field(name="Timestamp", value=row[4], inline=True)
        user = await inter.guild.fetch_member(row[0])
        embed.set_author(name=user.name, icon_url=user.avatar.url if user.avatar else user.default_avatar.url)
        embed.set_footer(text="discord.gg/uxdevelopment")
        await t.send(embed=embed)
        await asyncio.sleep(3)
        


    


if data['token'] != "":
    bot.run(data['token'])
else:
    print("Please check your config.json file and enter a discord token")