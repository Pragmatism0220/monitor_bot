import nonebot
from aiocqhttp.exceptions import Error as CQHttpError
from awesome.plugins.crawlers import *


@nonebot.scheduler.scheduled_job('interval', minutes=10)
async def top_main():
    '''
    Explain the at(@) statement:
    The first parameter we can choose: date, interval, cron
    The second parameter we can choose: seconds, minutes, hour
    More information:
    https://apscheduler.readthedocs.io/en/latest/userguide.html
    https://nonebot.cqp.moe/
    '''
    try:
        bot = nonebot.get_bot()
        # If you wanna send a group message, you can use this code:
        # await bot.send_group_msg(group_id=xxx, message='')
        # Instagram
        for msg in instagram.instagram_main():
            print(msg)
            try:
                await bot.send_private_msg(user_id=849689336, message=msg)
            except CQHttpError:
                pass
        # Twitter
        for msg in twitter.twitter_main():
            print(msg)
            try:
                await bot.send_private_msg(user_id=849689336, message=msg)
            except CQHttpError:
                pass
        # Weibo
        for msg in weibo.weibo_main():
            print(msg)
            try:
                await bot.send_private_msg(user_id=849689336, message=msg)
            except CQHttpError:
                pass
        # If you want, you can implement more functions and add them in this code in this top file.

        print('\n' + '*' * 100 + u'\n一轮爬取完成！\n' + '*' * 100)
    except Exception as e:
        print(e)