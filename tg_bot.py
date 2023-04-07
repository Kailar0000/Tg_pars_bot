import asyncio
import datetime
import json
from aiogram import Bot, Dispatcher,executor, types
from tg_config import token, user_id, time_sleep
from main import check_news_update

bot = Bot(token=token)
dp = Dispatcher(bot)


async def news_every_minute():
    while True:
        fresh_news = check_news_update()
        if len(fresh_news) >= 1:
            for k, v in sorted(fresh_news.items()):
                news = f"{datetime.datetime.fromtimestamp(v['article_data_taimestamp'])}\n" \
                       f"{v['article_title']}\n" \
                       f"{v['article_desc']}\n" \
                       f"{v['article_url']}"
                await bot.send_message(user_id, news, disable_notification=True)

        await asyncio.sleep(time_sleep)



if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(news_every_minute())
    executor.start_polling(dp)
