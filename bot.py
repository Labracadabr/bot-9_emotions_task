import asyncio
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher
# from config import Config, load_config
from handlers import handler_admin, handler_small_commands, handler_user, handler_pd
from config import config

async def main():
    # Инициализация бота
    storage: MemoryStorage = MemoryStorage()
    bot: Bot = Bot(token=config.BOT_TOKEN)
    dp: Dispatcher = Dispatcher(storage=storage)

    # Регистрируем роутеры в диспетчере
    dp.include_router(handler_pd.router)
    dp.include_router(handler_small_commands.router)
    dp.include_router(handler_user.router)
    dp.include_router(handler_admin.router)
    # import test
    # dp.include_router(test.router)

    # Пропускаем накопившиеся апдейты и запускаем polling
    await bot.delete_webhook(drop_pending_updates=False)  # False > бот ответит на апдейты, присланные за время откл
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
