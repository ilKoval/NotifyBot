import logging
from background import keep_alive

from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from tgbot.config import load_config
from tgbot.filters.admin import register_admin_filters
from tgbot.filters.user import register_user_filters
from tgbot.handlers.admin import register_admin
from tgbot.handlers.user import register_user_handlers
from tgbot.middlewares.environment import EnvironmentMiddleware
from tgbot.misc import db_methods
from tgbot.services.planer import add_jobs

logger = logging.getLogger(__name__)


async def on_startup(_):
    with open('info.log', 'w') as file:
        file.write('')
    db_methods.create_db(load_config('.env').db.FILE_PATH)
    register_all_middlewares(dp, config)
    register_all_filters(dp)
    register_all_handlers(dp)
    add_jobs(bot)
    logging.info('Bot started')


async def on_shutdown(_):
    logger.error("Bot stopped!")
    await dp.storage.close()
    await dp.storage.wait_closed()
    await dp.bot.send_message(config.tg_bot.admin_ids[0], 'Bot stopped')
    # await bot.close()


def register_all_middlewares(dp: Dispatcher, config):
    dp.setup_middleware(EnvironmentMiddleware(config=config))


def register_all_filters(dp: Dispatcher):
    register_admin_filters(dp)
    register_user_filters(dp)


def register_all_handlers(dp: Dispatcher):
    register_admin(dp)
    register_user_handlers(dp)


logging.basicConfig(
    level=logging.INFO,
    format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    # filename='info.log'
)
config = load_config(".env")
storage = RedisStorage2() if config.tg_bot.use_redis else MemoryStorage()
bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
dp = Dispatcher(bot, storage=storage)

scheduler = AsyncIOScheduler()

bot['config'] = config
bot['scheduler'] = scheduler

if __name__ == '__main__':
    scheduler.start()
    keep_alive()
    executor.start_polling(dp,
                           on_startup=on_startup,
                           on_shutdown=on_shutdown,
                           skip_updates=True)
