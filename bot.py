import discord
from discord.ext import commands
from discord import Embed
import asyncio
import datetime
import os
from time import sleep



PREFIX = "/"

client = commands.Bot(command_prefix = PREFIX)


@client.event
async def on_ready():
	print("BOT connected")
	await client.change_presence(status = discord.Status.online, activity = discord.Game("VALORANT"))










@client.command()
async def say(ctx, arg):
	await ctx.send(f"{arg}")

	
# Kick
@client.command()
@commands.has_permissions(administrator = True) 
async def kick(ctx, member: discord.Member, *, reason = None):
	await member.kick(reason = reason)
																										



# Ban
@client.command()
@commands.has_permissions(administrator = True)
																																															
async def ban(ctx, member: discord.Member, *, reason = None):
	await member.ban(reason = reason)

	await ctx.channel.purge(limit = 1)


@client.command()
@commands.has_permissions(administrator = True)
async def voice_create(ctx, *, arg): 
    guild = ctx.guild
    channel = await guild.create_voice_channel(f'{arg}')
    await ctx.send(embed = discord.Embed(description = f'**:microphone2: Голосовой канал "{arg}" успешно создан!**', color=0x0c0c0c))



@client.command()
@commands.has_permissions(administrator = True)
async def channel_create(ctx, *, arg): 
    guild = ctx.guild
    channel = await guild.create_text_channel(f'{arg}')
    await ctx.send(embed = discord.Embed(description = f'**:keyboard: Текстовый канал "{arg}" успешно создан!**', color=0x0c0c0c))


@client.command()
@commands.has_permissions(administrator = True)
async def add_role(ctx, user: discord.Member, role: discord.Role):

    await discord.Member.add_roles(user, role)
    await ctx.send(embed = discord.Embed(description = f'**Роль успешна выдана!**', color=0x0c0c0c))


@client.command()
@commands.has_permissions(administrator = True)
async def remove_role(ctx, user: discord.Member, role: discord.Role):

    await discord.Member.remove_roles(user, role)
    await ctx.send(embed = discord.Embed(description = f'**Роль была успешно забрана!**', color=0x0c0c0c))



    embed.set_thumbnail(url=ctx.guild.icon_url)
    embed.set_footer(text=f"ID: {guild.id}")

    embed.set_footer(text=f"ID Пользователя: {ctx.author.id}")
    await ctx.send(embed=embed)


@client.command()
async def avatar(ctx, member : discord.Member = None):

    user = ctx.message.author if (member == None) else member

    embed = discord.Embed(title=f'Аватар пользователя {user}', color= 0x0c0c0c)

    embed.set_image(url=user.avatar_url)

    await ctx.send(embed=embed)



@client.command(name = "changename", aliases = ["rename", "change"])
@commands.has_permissions(administrator = True)
async def changing_name(ctx, member: discord.Member = None, nickname: str = None):
    try:
        if member is None:
            await ctx.send(embed = discord.Embed(description = "Обязательно укажите **пользователя**!"))
        elif nickname is None:
            await ctx.send(embed = discord.Embed(description = "Обязательно укажите ник!"))
        else:
            await member.edit(nick = nickname)
            await ctx.send(embed = discord.Embed(description = f"У пользователя **{member.name}** был изменен ник на **{nickname}**"))
    except:
        await ctx.send(embed = discord.Embed(description = f"Я не могу изменить ник пользователя **{member.name}**!"))



@client.command()
async def userinfo(ctx, Member: discord.Member = None ):
    if not Member:
        Member = ctx.author
    roles = (role for role in Member.roles )
    emb = discord.Embed(title='Информация о пользователе.'.format(Member.name), description=f"Участник зашёл на сервер: {Member.joined_at.strftime('%b %#d, %Y')}\n\n "
                                                                                      f"Имя: {Member.name}\n\n"
                                                                                      f"Никнейм: {Member.nick}\n\n"
                                                                                      f"Статус: {Member.status}\n\n"
                                                                                      f"ID: {Member.id}\n\n"
                                                                                      f"Высшая роль: {Member.top_role}\n\n"
                                                                                      f"Аккаунт создан: {Member.created_at.strftime('%b %#d, %Y')}", 
                                                                                      color=0xff0000, timestamp=ctx.message.created_at)

    emb.set_thumbnail(url= Member.avatar_url)
    emb.set_footer(icon_url= Member.avatar_url)
    emb.set_footer(text='Команда вызвана: {}'.format(ctx.author.name), icon_url=ctx.author.avatar_url)
    await ctx.send(embed=emb)






@client.command()
@commands.has_permissions(administrator = True)
async def clear(ctx,amount : int):
    
    channel_log = client.get_channel(672701227817238559) 

    await ctx.channel.purge(limit = amount)
    await ctx.send(embed = discord.Embed(description = f'**:heavy_check_mark: Удалено {amount} сообщений.**', color=0x0c0c0c))
    await channel_log.send(embed = discord.Embed(description = f'**:wastebasket:  Удалено {amount} сообщений.**', color=0x0c0c0c))

# Работа с ошибками очистки чата
@clear.error 
async def clear_error(ctx, error):

    if isinstance( error, commands.MissingPermissions ):
        await ctx.send(embed = discord.Embed(description = f'**:exclamation: {ctx.author.name},у вас нет прав для использования данной команды.**', color=0x0c0c0c))

    if isinstance( error, commands.MissingRequiredArgument  ): 
        await ctx.send(embed = discord.Embed(description = f'**:grey_exclamation: {ctx.author.name},обязательно укажите количество сообщений.**', color=0x0c0c0c))


@client.command( pass_context = True, aliases=[ "Мут", "мут", "мьют", "Мьют", "mute" ] )
async def tempmute(ctx, member : discord.Member, time:int, arg:str, *, reason=None):
    Переменная_размут = f'**Вы были размучены на сервере {ctx.guild.name}**'
    Переменная_мут = f'**Вы были замучены на сервере {ctx.guild.name} на {time}{arg} по причине: {reason}**'
    mute_role = discord.utils.get( ctx.message.guild.roles, id = 690963128300601426 )

    await member.add_roles(mute_role, reason=None, atomic=True)
    await ctx.send(embed = discord.Embed(description = f'**:shield:Мут пользователю {member.mention} успешно выдан на {time}{arg} по причине {reason} :shield:**', color=0x0000FF))
    await member.send(embed = discord.Embed(description = f'{Переменная_мут}', color=0x0c0c0c))

    if arg == "s":
        await asyncio.sleep(time)          
    elif arg == "m":
        await asyncio.sleep(time * 60)
    elif arg == "h":
        await asyncio.sleep(time * 60 * 60)
    elif arg == "d":
        await asyncio.sleep(time * 60 * 60 * 24)

    await member.remove_roles( mute_role )
    await ctx.send(embed = discord.Embed(description = f'**:white_check_mark:Мут у пользователя {member.mention} успешно снят!:white_check_mark:**', color=0x800080))
    await member.send(embed = discord.Embed(description = f'{Переменная_размут}', color=0x800080))  






@client.command()
async def serverinfo(ctx):
    members = ctx.guild.members
    online = len(list(filter(lambda x: x.status == discord.Status.online, members)))
    offline = len(list(filter(lambda x: x.status == discord.Status.offline, members)))
    idle = len(list(filter(lambda x: x.status == discord.Status.idle, members)))
    dnd = len(list(filter(lambda x: x.status == discord.Status.dnd, members)))
    allchannels = len(ctx.guild.channels)
    allvoice = len(ctx.guild.voice_channels)
    alltext = len(ctx.guild.text_channels)
    allroles = len(ctx.guild.roles)
    embed = discord.Embed(title=f"{ctx.guild.name}", color=0xff0000, timestamp=ctx.message.created_at)
    embed.description=(
        f":timer: Сервер создали **{ctx.guild.created_at.strftime('%A, %b %#d %Y')}**\n\n"
        f":flag_white: Регион **{ctx.guild.region}\n\nГлава сервера **{ctx.guild.owner}**\n\n"
        f":tools: Ботов на сервере: **{len([m for m in members if m.bot])}**\n\n"
        f":green_circle: Онлайн: **{online}**\n\n"
        f":black_circle: Оффлайн: **{offline}**\n\n"
        f":yellow_circle: Отошли: **{idle}**\n\n"
        f":red_circle: Не трогать: **{dnd}**\n\n"
        f":shield: Уровень верификации: **{ctx.guild.verification_level}**\n\n"
        f":musical_keyboard: Всего каналов: **{allchannels}**\n\n"
        f":loud_sound: Голосовых каналов: **{allvoice}**\n\n"
        f":keyboard: Текстовых каналов: **{alltext}**\n\n"
        f":briefcase: Всего ролей: **{allroles}**\n\n"
        f":slight_smile: Людей на сервере **{ctx.guild.member_count}\n\n"
    )

    embed.set_thumbnail(url=ctx.guild.icon_url)
    embed.set_footer(text=f"ID: {ctx.guild.id}")
    embed.set_footer(text=f"ID Пользователя: {ctx.author.id}")
    await ctx.send(embed=embed)








@client.command(aliases = ['count', 'calc', 'вычисли', 'math'])
async def __count(ctx,*,arg = None):
    text = ctx.message.content

    if args == None:
        await ctx.send(embed = discord.Embed(description = 'Напишите пример чтобы вычислить.', color = 0x39d0d6))
    else:
        result = eval(args)
        await ctx.send(embed = discord.Embed(description = f'Результат вычисления `{args}`: \n`{result}`', color = 0x39d0d6))













@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(embed = discord.Embed(description = f'**:exclamation:{ctx.author.name},данной команды не существует.**', color=0x0c0c0c)) 


# Connect
token = open ("token.txt","r").readline()		
client.run (token)																																																																																																																																																											