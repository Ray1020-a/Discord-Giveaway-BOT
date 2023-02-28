import discord
from discord.ext import commands
import asyncio
import random
import datetime

bot = commands.Bot(command_prefix="!",intents=discord.Intents.all(), help_command=None)

@bot.command(aliases= ['g'])
async def gift(ctx):
    if ctx.author.guild_permissions.administrator:
        await ctx.message.delete()
        await ctx.send('你想要抽獎的獎品是什麼？')
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel
        try:
            message = await bot.wait_for('message', check=check, timeout=30)
        except asyncio.TimeoutError:
            await ctx.send('請您確保在30秒內回答問題，已超出時間請重試')
        else:
            giveaway_gift = (message.content)
            await ctx.send('你想要在什麼時候公布中獎者？ 格式YYYY/MM/DD HH:MM:SS')
            def check(m):
                return m.author == ctx.author and m.channel == ctx.channel
            try:
                message = await bot.wait_for('message', check=check, timeout=30)
            except asyncio.TimeoutError:
                await ctx.send('請您確保在30秒內回答問題，已超出時間請重試')
            else:
                giveaway_time = (message.content)
            try:
                giveaway_END_time = datetime.datetime.strptime(giveaway_time, '%Y/%m/%d %H:%M:%S')
            except ValueError:
                await ctx.send('抽獎截止日期格式不正確，請重試')
                return
        gift = str(giveaway_gift)
        participants = []
        remaining_time = (giveaway_END_time - datetime.datetime.now()).total_seconds()
        await message.channel.send(f'獎品：`{gift}`將在`{giveaway_END_time.strftime("%Y/%m/%d %H:%M:%S")}`抽出')
        embed = discord.Embed(title="🎉抽獎囉🎉", color=discord.Colour.random())
        embed.set_footer(text=f"說明：按下🎉進行登記抽獎")
        message = await ctx.send(embed=embed)
        await message.add_reaction('🎉')
        def cc(reaction, user):
            return user != ctx.user and str(reaction.emoji) == '🎉'
        await asyncio.sleep(remaining_time)
        new_message = await ctx.fetch_message(message.id)
        users = await new_message.reactions[0].users().flatten()
        for user in users:
                if user != bot.user:
                    participants.append(user)
        if len(participants) > 0:
            winner = random.choice(participants)
            embed = discord.Embed(title="🎉抽獎結果🎉", description=f"中獎者是 {winner.mention}，恭喜你！", color=discord.Colour.random())
            message = await ctx.send(embed=embed)
            winnerr = message.guild.get_member(winner.id)
            embed = discord.Embed(title="🎉抽獎結果🎉", description=f"{winner.mention}你在`{ctx.guild}`抽中了`{gift}`，恭喜你！", color=discord.Colour.random())
            message = await winnerr.send(embed=embed)
        else:
            embed = discord.Embed(title="🎉抽獎結果🎉", description=f"很遺憾，沒有人參加此抽獎。", color=discord.Colour.random())
            message = await ctx.send(embed=embed)
    else:
        await ctx.message.delete()
        a = await ctx.channel.send('抱歉，您沒有權限開始抽獎。')
        await asyncio.sleep(5)
        await a.delete()

bot.run('YOUR_DISCORD_BOT_TOKEN')#將YOUR_DISCORD_BOT_TOKEN替換成你的機器人TOKEN
