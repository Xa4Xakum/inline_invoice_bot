from aiogram.filters import BaseFilter
from aiogram.types import InlineQuery, Message

from operations import get_data
from config import Config


class NumericInput(BaseFilter):
    async def __call__(self, iq: InlineQuery) -> bool:
        try:
            text = iq.query.replace(',', '.')
            params = text.split()
            if len(params) == 0: params = [text]
            for i in params:
                num = float(i)
                num += 1
            return True
        except:
            return False


class NumericSecParam(BaseFilter):
    async def __call__(self, msg: Message) -> bool:
        try:
            text = msg.text.replace(',', '.')
            params = text.split()
            num = float(params[1])
            num += 1
            return True
        except Exception as e:
            await msg.answer(f'Не является числом({e})')
            return False


class AdminInline(BaseFilter):
    async def __call__(self, iq: InlineQuery) -> bool:
        data = get_data()
        conf = Config()
        if iq.from_user.id == conf.get_admin_id():
            return True
        if 'admins' in data:
            return iq.from_user.id in data['admins']
        return False


class Admin(BaseFilter):
    async def __call__(self, msg: Message) -> bool:
        data = get_data()
        conf = Config()
        if msg.from_user.id == conf.get_admin_id():
            return True
        if 'admins' in data:
            return msg.from_user.id in data['admins']
        return False


class WordsCount(BaseFilter):
    def __init__(self, count: int):
        self.count = count

    async def __call__(self, msg: Message) -> bool:
        words = msg.text.split()
        if len(words) != self.count:
            await msg.answer('Неверное количество параметров')
            return False
        return True


class Numeric(BaseFilter):
    async def __call__(self, msg: Message) -> bool:
        try:
            text = msg.text.replace(',', '.')
            num = float(text)
            num += 1
            return True
        except Exception as e:
            await msg.answer(f'Не является числом({e})')
            return False