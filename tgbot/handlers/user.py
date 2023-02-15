import logging
from aiogram import Dispatcher
from aiogram.dispatcher.storage import FSMContext
from aiogram.types import Message, CallbackQuery
from tgbot.config import Config
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from tgbot.filters.user import AddTimeFilter, DeleteTaskFilter, DetailTaskFilter, EditTaskFilter, MarkCanceledFilter, MarkReadyFilter, OffTimeFilter, OnTimeFilter, RestoreTaskFilter, DeleteTimeFilter, SetTimezoneFilter
from tgbot.keyboards import inline
from tgbot.misc import db_methods
from tgbot.misc.states import Tasks, History, Settings
from tgbot.services.planer import add_jobs


async def user_start(message: Message, state: FSMContext):  # START COMMAND
    await state.set_state(None)
    config: Config = message.bot['config']
    db_methods.add_user(config.db.FILE_PATH,
                        message.from_user.id, message.from_user.username)
    user_info = db_methods.read_user(config.db.FILE_PATH, message.from_user.id)
    text = "Hello, user!"
    if user_info['timezone'] == None:
        text = "Hello, user!\n❗️Please setup timezone in your settings"
    await message.answer(text, reply_markup=inline.main_menu())


async def home(callback: CallbackQuery, state: FSMContext):  # HOME BUTTON
    await state.set_state(None)
    await callback.message.edit_text('Hello user')
    await callback.message.edit_reply_markup(inline.main_menu())
    await callback.answer()


async def tasks(callback: CallbackQuery, state: FSMContext):  # TASKS BUTTON
    await state.set_state(Tasks.tasks_menu)
    config: Config = callback.bot['config']
    data = db_methods.read_tasks(config.db.FILE_PATH, callback.from_user.id)
    await callback.message.edit_text('Tasks')
    await callback.message.edit_reply_markup(inline.tasks_menu(data))
    await callback.answer()


async def add_task_init(callback: CallbackQuery, state: FSMContext):  # ADD TASK BUTTON
    await state.set_state(Tasks.add_task)
    await callback.message.edit_text('Input task description')
    await callback.message.edit_reply_markup(InlineKeyboardMarkup().add(InlineKeyboardButton('⬅️ Назад', callback_data='back')))
    await callback.answer()


async def add_task(message: Message, state: FSMContext):  # ADD TASK TEXT
    config: Config = message.bot['config']
    db_methods.add_task(config.db.FILE_PATH,
                        message.from_user.id, message.text)
    await state.set_state(Tasks.tasks_menu)
    data = db_methods.read_tasks(config.db.FILE_PATH, message.from_user.id)
    await message.answer('Tasks', reply_markup=inline.tasks_menu(data))


async def mark_ready(callback: CallbackQuery, state: FSMContext):  # READY TASK BUTTON
    config: Config = callback.bot['config']
    id = callback.data.split(' ')[0]
    db_methods.mark_ready(config.db.FILE_PATH, callback.from_user.id, id)
    await tasks(callback, state)


async def mark_cancel(callback: CallbackQuery, state: FSMContext):  # CANCEL TASK BUTTON
    config: Config = callback.bot['config']
    id = callback.data.split(' ')[0]
    db_methods.mark_canceled(config.db.FILE_PATH, callback.from_user.id, id)
    await tasks(callback, state)


async def edit_task_init(callback: CallbackQuery, state: FSMContext):  # EDIT TASK BUTTON
    await state.set_state(Tasks.edit)
    await state.update_data(edit_id=callback.data.split(' ')[0])
    await callback.message.edit_text('Input task description')
    await callback.message.edit_reply_markup(InlineKeyboardMarkup().add(InlineKeyboardButton('⬅️ Назад', callback_data='back')))
    await callback.answer()


async def edit_task(message: Message, state: FSMContext):  # EDIT TASK TEXT
    config: Config = message.bot['config']
    data = await state.get_data()
    db_methods.edit_task(config.db.FILE_PATH,
                         message.from_user.id, data['edit_id'], message.text)
    await state.set_state(Tasks.tasks_menu)
    await message.answer('Tasks', reply_markup=inline.tasks_menu(db_methods.read_tasks(config.db.FILE_PATH, message.from_user.id)))


async def task_detail(callback: CallbackQuery, state: FSMContext):  # TASK DETAIL BUTTON
    config: Config = callback.bot['config']
    current_state = await state.get_state()
    id = int(callback.data.split(' ')[0])
    data = db_methods.read_tasks(config.db.FILE_PATH, callback.from_user.id)
    detail = inline.get_detail(data, id)
    if current_state == 'Tasks:tasks_menu':
        await state.set_state(Tasks.detail)
    elif current_state == 'History:history_menu':
        await state.set_state(History.detail)
    await callback.message.edit_text(detail[0])
    await callback.message.edit_reply_markup(detail[1])
    await callback.answer()


async def history(callback: CallbackQuery, state: FSMContext):  # HISTORY BUTTON
    await state.set_state(History.history_menu)
    config: Config = callback.bot['config']
    data = db_methods.read_history(config.db.FILE_PATH, callback.from_user.id)
    await callback.message.edit_text('History')
    await callback.message.edit_reply_markup(inline.history_menu(data))
    await callback.answer()


async def delete_task(callback: CallbackQuery, state: FSMContext):  # DELETE TASK BUTTON
    config: Config = callback.bot['config']
    id = callback.data.split(' ')[0]
    db_methods.delete_task(config.db.FILE_PATH, callback.from_user.id, id)
    await history(callback, state)


async def restore_task(callback: CallbackQuery, state: FSMContext):  # RESTORE TASK BUTTON
    config: Config = callback.bot['config']
    id = callback.data.split(' ')[0]
    db_methods.restore(config.db.FILE_PATH, callback.from_user.id, id)
    await history(callback, state)


async def settings(callback: CallbackQuery, state: FSMContext):  # SETTINGS BUTTON
    await state.set_state(Settings.settings_menu)
    await callback.message.edit_text('Settings')
    await callback.message.edit_reply_markup(inline.settings_menu())
    await callback.answer()


async def timezone_info(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Settings.timezone_info)
    config: Config = callback.bot['config']
    user_info = db_methods.read_user(
        config.db.FILE_PATH, callback.from_user.id)
    await callback.message.edit_text(f'Current timezone UTC{user_info["timezone"]}')
    await callback.message.edit_reply_markup(inline.timezone_info())
    await callback.answer()


async def timezone_set_init(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Settings.set_timezone)
    await callback.message.edit_text(f'Enter timezone in format UTC')
    await callback.message.edit_reply_markup(InlineKeyboardMarkup().add(InlineKeyboardButton('⬅️ Назад', callback_data='back')))
    await callback.answer()


async def timezone_set(message: Message, state: FSMContext):
    await state.set_state(Settings.timezone_info)
    timezone = message.text[3:]
    config: Config = message.bot['config']
    db_methods.set_timezone(config.db.FILE_PATH,
                            message.from_user.id, timezone)
    user_info = db_methods.read_user(
        config.db.FILE_PATH, message.from_user.id)
    await message.answer(f'Current timezone UTC{user_info["timezone"]}', reply_markup=inline.timezone_info())


async def times(callback: CallbackQuery, state: FSMContext):  # TIME MENU BUTTON
    await state.set_state(Settings.time_menu)
    config: Config = callback.bot['config']
    data = db_methods.read_times(config.db.FILE_PATH, callback.from_user.id)
    await callback.message.edit_text('Time')
    await callback.message.edit_reply_markup(inline.time_menu(data))
    await callback.answer()


async def add_time_init(callback: CallbackQuery, state: FSMContext):  # ADD TIME BUTTON
    await state.set_state(Settings.add_time)
    await callback.message.edit_text('Input time in format "HH:MM"')
    await callback.message.edit_reply_markup(InlineKeyboardMarkup().add(InlineKeyboardButton('⬅️ Назад', callback_data='back')))
    await callback.answer()


async def add_time(message: Message, state: FSMContext):  # ADD TIME TEXT
    await state.set_state(Settings.time_menu)
    config: Config = message.bot['config']
    time = message.text
    db_methods.add_time(config.db.FILE_PATH, message.from_user.id, time)
    data = db_methods.read_times(config.db.FILE_PATH, message.from_user.id)
    add_jobs(message.bot)
    await message.answer('Times', reply_markup=inline.time_menu(data))


async def turn_on_time(callback: CallbackQuery, state: FSMContext):  # TURN ON TIME BUTTON
    config: Config = callback.bot['config']
    time = callback.data.split('_')[0]
    db_methods.turn_on_time(config.db.FILE_PATH, callback.from_user.id, time)
    add_jobs(callback.bot)
    await times(callback, state)
    await callback.answer()


async def turn_off_time(callback: CallbackQuery, state: FSMContext):  # TURN OFF TIME BUTTON
    config: Config = callback.bot['config']
    time = callback.data.split('_')[0]
    db_methods.turn_off_time(config.db.FILE_PATH, callback.from_user.id, time)
    add_jobs(callback.bot)
    await times(callback, state)
    await callback.answer()


async def delete_time(callback: CallbackQuery, state: FSMContext):  # DELETE TIME BUTTON
    config: Config = callback.bot['config']
    time = callback.data.split('_')[0]
    db_methods.delete_time(config.db.FILE_PATH, callback.from_user.id, time)
    add_jobs(callback.bot)
    await times(callback, state)
    await callback.answer()


async def clear_tasks(callback: CallbackQuery, state: FSMContext):  # CLEAR TASKS BUTTON
    config: Config = callback.bot['config']
    db_methods.clear_tasks(config.db.FILE_PATH, callback.from_user.id)
    await callback.answer('Tasks cleared')


async def clear_history(callback: CallbackQuery, state: FSMContext):  # CLEAR HISTORY BUTTON
    config: Config = callback.bot['config']
    db_methods.clear_history(config.db.FILE_PATH, callback.from_user.id)
    await callback.answer('History cleared')


async def clear_all(callback: CallbackQuery, state: FSMContext):  # CLEAR ALL BUTTON
    config: Config = callback.bot['config']
    db_methods.clear_all(config.db.FILE_PATH, callback.from_user.id, True)
    await callback.answer('All cleared')


async def back(callback: CallbackQuery, state: FSMContext):  # BACK BUTTON
    current_state = await state.get_state()
    config: Config = callback.bot['config']
    if current_state in ['Tasks:tasks_menu', 'History:history_menu', 'Settings:settings_menu']:
        await state.set_state(None)
        user_info = db_methods.read_user(
            config.db.FILE_PATH, callback.from_user.id)
        text = "Hello, user!"
        if user_info['timezone'] == None:
            text = "Hello, user!\n❗️Please setup timezone in your settings"
        await callback.message.edit_text(text)
        await callback.message.edit_reply_markup(inline.main_menu())
    elif current_state in ['Tasks:add_task', 'Tasks:detail']:
        await tasks(callback, state)
    elif current_state == 'Tasks:edit':
        config: Config = callback.bot['config']
        state_data = await state.get_data()
        data = db_methods.read_tasks(
            config.db.FILE_PATH, callback.from_user.id)
        detail = inline.get_detail(data, int(state_data['edit_id']))
        await state.set_state(Tasks.detail)
        await callback.message.edit_text(detail[0])
        await callback.message.edit_reply_markup(detail[1])
    elif current_state == 'History:detail':
        await history(callback, state)
    elif current_state == 'Settings:time_menu':
        await settings(callback, state)
    elif current_state == 'Settings:add_time':
        await times(callback, state)
    elif current_state == 'Settings:timezone_info':
        await settings(callback, state)
    elif current_state == 'Settings:set_timezone':
        await timezone_info(callback, state)
    await callback.answer()


def register_user_handlers(dp: Dispatcher):  # REGISTER HANDLERS
    dp.register_message_handler(
        user_start, commands=['start'], state='*')  # START COMMAND

    dp.register_callback_query_handler(
        home, text='home', state='*')  # HOME BUTTON

    dp.register_callback_query_handler(
        back, text='back', state='*')  # BACK BUTTON

    # ---------------------------------------------------------------TASKS MENU-------------------------------------------------------------------------
    dp.register_callback_query_handler(
        tasks, text='tasks', state=None)  # TASKS BUTTON

    dp.register_callback_query_handler(
        add_task_init, text='add_task', state=Tasks.tasks_menu)  # ADD TASK BUTTON

    dp.register_callback_query_handler(
        edit_task_init, EditTaskFilter(), state=Tasks.detail)  # EDIT TASK BUTTON

    dp.register_message_handler(add_task, content_types=[
                                'text'], state=Tasks.add_task)  # ADD TASK TEXT HANDLER

    dp.register_message_handler(edit_task, content_types=[
                                'text'], state=Tasks.edit)  # EDIT TASK TEXT HANDLER

    dp.register_callback_query_handler(mark_ready, MarkReadyFilter(), state=[
                                       Tasks.tasks_menu, Tasks.detail])  # READY TASK BUTTON

    dp.register_callback_query_handler(mark_cancel, MarkCanceledFilter(), state=[
                                       Tasks.tasks_menu, Tasks.detail])  # CANCEL TASK BUTTON

    dp.register_callback_query_handler(
        task_detail, DetailTaskFilter(), state=[Tasks.tasks_menu, History.history_menu])  # DETAIL TASK BUTTON

    # ---------------------------------------------------------------HISTORY MENU-------------------------------------------------------------------------
    dp.register_callback_query_handler(
        history, text='history', state=None)  # HISTORY BUTTON

    dp.register_callback_query_handler(delete_task, DeleteTaskFilter(), state=[
                                       History.history_menu, History.detail])  # DELETE TASK FROM HISTORY BUTTON

    dp.register_callback_query_handler(restore_task, RestoreTaskFilter(), state=[
                                       History.history_menu, History.detail])  # RESTORE TASK FROM HISTORY BUTTON

    # ---------------------------------------------------------------SETTINGS MENU-------------------------------------------------------------------------
    dp.register_callback_query_handler(
        settings, text='settings', state=None)  # SETTINGS BUTTON

    dp.register_callback_query_handler(
        timezone_info, text='timezone', state=Settings.settings_menu)  # TIMEZONE INFO BUTTON

    dp.register_callback_query_handler(
        timezone_set_init, text='set timezone', state=Settings.timezone_info)  # SET TIMEZONE BUTTON

    dp.register_message_handler(
        timezone_set, SetTimezoneFilter(), state=Settings.set_timezone)  # SET TIMEZONE HANDLER

    dp.register_callback_query_handler(
        times, text='times', state=Settings.settings_menu)  # TIMES MENU BUTTON

    dp.register_callback_query_handler(
        add_time_init, text='add_time', state=Settings.time_menu)  # ADD TIME BUTTON

    dp.register_message_handler(add_time, AddTimeFilter(), content_types=[
                                'text'], state=Settings.add_time)  # ADD TIME TEXT HANDLER

    dp.register_callback_query_handler(
        turn_on_time, OnTimeFilter(), state=Settings.time_menu)  # TURN ON TIME BUTTON

    dp.register_callback_query_handler(
        turn_off_time, OffTimeFilter(), state=Settings.time_menu)  # TURN OFF TIME BUTTON

    dp.register_callback_query_handler(
        delete_time, DeleteTimeFilter(), state=Settings.time_menu)  # DELETE TIME BUTTON

    dp.register_callback_query_handler(
        clear_tasks, text='clear_tasks', state=Settings.settings_menu)  # CLEAR TASKS BUTTON

    dp.register_callback_query_handler(
        clear_history, text='clear_history', state=Settings.settings_menu)  # CLEAR HISTORY BUTTON

    dp.register_callback_query_handler(
        clear_all, text='clear_all', state=Settings.settings_menu)  # CLEAR ALL BUTTON
