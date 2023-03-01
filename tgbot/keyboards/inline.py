from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def main_menu() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=2)
    show_all_btn = InlineKeyboardButton('Все задачи', callback_data='tasks')
    history_btn = InlineKeyboardButton('История', callback_data='history')
    settings_btn = InlineKeyboardButton(
        'Настройки', callback_data='settings')
    markup.add(show_all_btn, history_btn).add(settings_btn)
    return markup


def tasks_menu(data_list: list) -> InlineKeyboardMarkup:
    tasks = InlineKeyboardMarkup()
    for task in data_list:
        if task[2] == 0 and task[3] == 0:
            if task[4]:
                mark_important = InlineKeyboardButton(
                    '🔕', callback_data=f'{task[0]} unimportant')
                detail = InlineKeyboardButton(
                    f'{task[1]}', callback_data=f'{task[0]} detail')
            else:
                mark_important = InlineKeyboardButton(
                    '🔔', callback_data=f'{task[0]} important')
                detail = InlineKeyboardButton(
                    f'🔕{task[1]}', callback_data=f'{task[0]} detail')

            mark_ready = InlineKeyboardButton(
                '✅', callback_data=f'{task[0]} ready')
            mark_canceled = InlineKeyboardButton(
                '🚫', callback_data=f'{task[0]} cancel')

            tasks.add(detail).add(mark_ready, mark_canceled, mark_important)
        else:
            pass
    add_task = InlineKeyboardButton(
        '➕ Добавить задачу', callback_data='add_task')
    back = InlineKeyboardButton('⬅️ Назад', callback_data='back')
    tasks.add(add_task).add(back)
    return tasks


def history_menu(data_list: list) -> InlineKeyboardMarkup:
    history = InlineKeyboardMarkup()
    for task in data_list:
        if task[2] == 1 or task[3] == 1:
            text = task[1]
            if task[2] == 1:
                text = f'✅ {text}'
            elif task[3] == 1:
                text = f'🚫 {text}'
            detail = InlineKeyboardButton(
                text, callback_data=f'{task[0]} detail')
            restore = InlineKeyboardButton(
                '⬆️', callback_data=f'{task[0]} restore')
            delete = InlineKeyboardButton(
                '❌', callback_data=f'{task[0]} delete')
            history.add(detail).add(restore, delete)
        else:
            pass
    back = InlineKeyboardButton('⬅️ Назад', callback_data='back')
    history.add(back)
    return history


def settings_menu() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    timezone_btn = InlineKeyboardButton(
        'Часовой пояс', callback_data='timezone')
    time_btn = InlineKeyboardButton(
        'Время напоминаний', callback_data='times')
    clear_tasks = InlineKeyboardButton(
        'Удалить задачи', callback_data='clear_tasks')
    clear_history = InlineKeyboardButton(
        'Удалить историю', callback_data='clear_history')
    clear_all = InlineKeyboardButton(
        'Удалить всё', callback_data='clear_all')
    back = InlineKeyboardButton('⬅️ Назад', callback_data='back')
    markup.add(timezone_btn).add(time_btn).add(clear_tasks).add(
        clear_history).add(clear_all).add(back)
    return markup


def get_detail(data_list: list, id: int) -> tuple[str, InlineKeyboardMarkup]:
    text: str
    markup = InlineKeyboardMarkup()
    back = InlineKeyboardButton('⬅️ Назад', callback_data='back')
    for data in data_list:
        if data[0] == id:
            text = data[1]
            if data[2] == 0 and data[3] == 0:
                edit = InlineKeyboardButton(
                    '📝Редактировать', callback_data=f'{data[0]} edit')
                mark_ready = InlineKeyboardButton(
                    '✅', callback_data=f'{data[0]} ready')
                mark_canceled = InlineKeyboardButton(
                    '🚫', callback_data=f'{data[0]} cancel')
                markup.add(edit)
                markup.add(back, mark_ready, mark_canceled)
            elif data[2] == 1 or data[3] == 1:
                if data[2] == 1:
                    text = f'✅ {text}'
                elif data[3] == 1:
                    text = f'🚫 {text}'
                restore = InlineKeyboardButton(
                    '⬆️', callback_data=f'{data[0]} restore')
                delete = InlineKeyboardButton(
                    '❌', callback_data=f'{data[0]} delete')
                markup.add(back, restore, delete)
            return text, markup
    text = 'Not Found'
    markup.add(back)
    return text, markup


def timezone_info() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    set_btn = InlineKeyboardButton(
        'Установить часовой пояс', callback_data='set timezone')
    back = InlineKeyboardButton('⬅️ Назад', callback_data='back')
    markup.add(set_btn).add(back)
    return markup


def time_menu(data_list: list) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    for data in data_list:
        if data[1] == 1:
            turn_status = InlineKeyboardButton(
                f'🟢{data[0]}', callback_data=f'{data[0]}_off')
        elif data[1] == 0:
            turn_status = InlineKeyboardButton(
                f'🔴{data[0]}', callback_data=f'{data[0]}_on')
        delete = InlineKeyboardButton('❌', callback_data=f'{data[0]}_delete')
        markup.add(turn_status, delete)

    add = InlineKeyboardButton('➕', callback_data='add_time')
    back = InlineKeyboardButton('⬅️', callback_data='back')
    markup.add(add, back)
    return markup
