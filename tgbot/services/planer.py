from types import NoneType
from aiogram import Bot, Dispatcher
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from tgbot.config import Config
from tgbot.config import load_config
from tgbot.keyboards import inline
from tgbot.misc import db_methods
from tgbot.misc.states import Tasks
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def send(bot: Bot, user_id: int):
    config: Config = bot['config']
    text = 'Tasks:\n'
    data = db_methods.send_tasks(config.db.FILE_PATH, user_id)
    if len(data) != 0:
        for task in data:
            text += f'{task[1]}\n'
        await bot.send_message(user_id, text, reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton('Главное меню', callback_data='home')))


def add_jobs(bot: Bot):
    scheduler: AsyncIOScheduler = bot['scheduler']
    scheduler.remove_all_jobs()
    config: Config = bot['config']
    users = db_methods.read_users(config.db.FILE_PATH)
    for user in users:
        timezone = db_methods.read_user(config.db.FILE_PATH, user)['timezone']
        if timezone == NoneType:
            timezone = 0
        times = db_methods.read_times(load_config('.env').db.FILE_PATH, user)
        for time in times:
            if bool(time[1]):
                h = int(time[0].split(':')[0]) + timezone
                m = time[0].split(':')[1]
                scheduler.add_job(send, 'cron', hour=int(h),
                                  minute=int(m), args=(bot, user))
