#-*- coding:utf-8 -*-
import asyncio
import discord
import os
import datetime


token = "NjA3ODc5NTIzMzIwNTk0NDYy.XUhNbQ.xwQbfU7beremQO_tCiu-mH_Uyxc"
app = discord.Client()
dict_interval_reminder = dict()
dict_remind_channel = dict()
dict_status_reminder = dict()
COMMAND_DESCRIPTION = "**!start_pose_reminder**\n" \
                      "- 해당 서버의 자세 알리미를 현재 채널로 설정하고 작동시킵니다.\n" \
                      "- 기본 알림 주기는 60분입니다.\n**" \
                      "!stop_pose_reminder**\n" \
                      "- 현재 서버의 자세 알리미를 중단합니다.\n" \
                      "**!set_pose_reminder_interval**\n" \
                      "- 현재 서버의 알림 주기를 설정합니다. (분 단위)"


# generator for sending notification
async def send_pose_remind(guild_id):
    while True:
        embed = discord.Embed(title="자세를 바로잡을 시간입니다!",
                              description="라운드 숄더와 거북목을 퇴치합시다",
                              color=0xe5c41e)
        embed.set_image(url="https://i.imgur.com/ZnsjPNi.png")

        # get current time for footer
        now_time = str(datetime.datetime.now())
        embed.set_footer(text=now_time)

        # REMIND!
        channel = dict_remind_channel[guild_id]
        await channel.send(embed=embed)
        print("Remind message has been sent to guild_id: %s, channel: %s(%s)" % (guild_id, channel.name, channel.id))
        yield True


# work as timer
async def auto_reminder(guild_id):
    async for _ in send_pose_remind(guild_id):
        await asyncio.sleep(dict_interval_reminder[guild_id] * 60)
        flag = dict_status_reminder[guild_id]
        if not flag:
            return

햐소
@app.event
async def on_ready():
    print("Now log in as {nickname: %s, id: %s}" % (app.user.name, app.user.id))
    # set gaming status
    activity = discord.Game(name="거북목 퇴치!", type=1)
    await app.change_presence(status=discord.Status.idle, activity=activity)

    # set default intervals
    for guild in app.guilds:
        dict_interval_reminder[guild.id] = 60
        dict_status_reminder[guild.id] = False


@app.event
async def on_message(message):
    # Start reminder
    if message.content.startswith("!start_pose_reminder"):
        dict_remind_channel[message.guild.id] = message.channel
        await message.channel.send("자세 알리미가 채널 %s에 설정되었습니다." % message.channel.name)
        loop = asyncio.get_event_loop()
        loop.create_task(auto_reminder(message.guild.id))
        dict_status_reminder[message.guild.id] = True
        print("Start on guild: %s(%d), channel: %s(%s)" % (message.guild.name, message.guild.id,
                                                    message.channel.name, message.channel.id))
    # Stop reminder
    elif message.content.startswith("!stop_pose_reminder"):
        if message.guild.id in dict_remind_channel:
            del dict_remind_channel[message.guild.id]
            await message.channel.send("자세 알리미가 해제되었습니다.")
            dict_status_reminder[message.guild.id] = False
            print("Stopped on guild: %s(%d)" % (message.guild.name, message.guild.id))
    # Set interval of reminder
    elif message.content.startswith("!set_pose_reminder_interval"):
        interval = int(message.content.replace("!set_pose_reminder_interval ", ""))
        # input interval is valid
        if 0 < interval:
            dict_interval_reminder[message.guild.id] = interval
            await message.channel.send("주기가 %d분으로 변경되었습니다."% interval)
            print("Interval has been changed on guild: %s(%s), channel: %s(%s)" % (message.guild.name, message.guild.id,
                                                                                   message.channel.name, message.channel.id))
        # input interval is not valid
        else:
            await message.channel.send("입력하신 주기가 올바르지 않습니다. 1분 이상의 정수를 입력해주세요.")
    elif message.content == "!help_pose_reminder":
        embed = discord.Embed(title="명령어 목록",
                              description=COMMAND_DESCRIPTION,
                              color=0x49eaf2)
        await message.channel.send(embed=embed)


app.run(token)