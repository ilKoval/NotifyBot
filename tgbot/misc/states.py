from aiogram.dispatcher.filters.state import State, StatesGroup


class Tasks(StatesGroup):  # TASKS MENU
    tasks_menu = State()
    detail = State()
    edit = State()
    add_task = State()


class History(StatesGroup):  # HISTORY MENU
    history_menu = State()
    detail = State()


class Settings(StatesGroup):  # SETTINGS MENU
    settings_menu = State()
    time_menu = State()
    add_time = State()
