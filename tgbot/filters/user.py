import typing
import re
from aiogram import Dispatcher
from aiogram.types import CallbackQuery, Message
from aiogram.dispatcher.filters import BoundFilter
from aiogram.dispatcher.storage import FSMContext

from tgbot.misc.states import Tasks, History, Settings


class DetailTaskFilter(BoundFilter):
    async def check(self, callback: CallbackQuery):
        return re.fullmatch('^\d+ detail$', callback.data)


class MarkReadyFilter(BoundFilter):
    async def check(self, callback: CallbackQuery):
        return re.fullmatch('^\d+ ready$', callback.data)


class MarkCanceledFilter(BoundFilter):
    async def check(self, callback: CallbackQuery):
        return re.fullmatch('^\d+ cancel$', callback.data)


class DeleteTaskFilter(BoundFilter):
    async def check(self, callback: CallbackQuery):
        return re.fullmatch('^\d+ delete$', callback.data)


class RestoreTaskFilter(BoundFilter):
    async def check(self, callback: CallbackQuery):
        return re.fullmatch('^\d+ restore$', callback.data)


class EditTaskFilter(BoundFilter):
    async def check(self, callback: CallbackQuery):
        return re.fullmatch('^\d+ edit$', callback.data)


class DeleteTimeFilter(BoundFilter):
    async def check(self, callback: CallbackQuery):
        return re.fullmatch('^\d\d:\d\d_delete$', callback.data)


class OnTimeFilter(BoundFilter):
    async def check(self, callback: CallbackQuery):
        return re.fullmatch('^\d\d:\d\d_on$', callback.data)


class OffTimeFilter(BoundFilter):
    async def check(self, callback: CallbackQuery):
        return re.fullmatch('^\d\d:\d\d_off$', callback.data)


class AddTimeFilter(BoundFilter):
    async def check(self, message: Message):
        return re.fullmatch('^\d\d:\d\d$', message.text)


def register_user_filters(dp: Dispatcher):
    dp.filters_factory.bind(DeleteTimeFilter)
    dp.filters_factory.bind(AddTimeFilter)
    dp.filters_factory.bind(OnTimeFilter)
    dp.filters_factory.bind(OffTimeFilter)
    dp.filters_factory.bind(DetailTaskFilter)
    dp.filters_factory.bind(MarkReadyFilter)
    dp.filters_factory.bind(MarkCanceledFilter)
    dp.filters_factory.bind(DeleteTaskFilter)
    dp.filters_factory.bind(RestoreTaskFilter)
    dp.filters_factory.bind(EditTaskFilter)