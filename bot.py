import asyncio
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher
from config import Config, load_config
import handler_admin
import handler_user
import handler_pd
# from concurrent.futures import ThreadPoolExecutor
# import time


async def main():
    # asyncio.create_task(regular_task())

    # Инициализация бота
    config: Config = load_config()
    storage: MemoryStorage = MemoryStorage()
    bot: Bot = Bot(token=config.tg_bot.token)
    dp: Dispatcher = Dispatcher(storage=storage)

    # Регистрируем роутеры в диспетчере
    dp.include_router(handler_pd.router)
    dp.include_router(handler_user.router)
    dp.include_router(handler_admin.router)
    # import test
    # dp.include_router(test.router)

    # Пропускаем накопившиеся апдейты и запускаем polling
    await bot.delete_webhook(drop_pending_updates=False)  # False > бот ответит на апдейты, присланные за время откл
    await dp.start_polling(bot)


# # Следующая функция исполняется раз в n часов
# async def regular_task(n=2):
#     from regular_tasks import fill_g_sheet
#     while True:
#         print('doing regular_task')
#         await fill_g_sheet()
#         await asyncio.sleep(n * 3600)
# _executor = ThreadPoolExecutor(1)
#
#
# def sync_blocking():
#     time.sleep(2)
#
#
# async def hello_world():
#     # run blocking function in another thread and wait for its result:
#     await loop.run_in_executor(_executor, sync_blocking)
#
#
# loop = asyncio.get_event_loop()
# loop.run_until_complete(hello_world())
# loop.close()


if __name__ == '__main__':
    asyncio.run(main())
