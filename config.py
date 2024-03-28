
from enum import Enum

import os

from dotenv import load_dotenv


class Modes(Enum):
    '''Список режимов, в которых можно запустить бота'''

    test = 'TEST'
    relise = 'RELISE'


class Config():
    '''Параметры бота'''

    def __init__(self, mode=Modes.test.value):
        load_dotenv()

        self.mode: str = mode


    def get_token(self):
        '''Токен бота в соответствии с режимом'''

        if self.mode == Modes.test.value:
            return os.getenv('TOKEN_TEST')
        if self.mode == Modes.relise.value:
            return os.getenv('TOKEN')


    def get_admin_id(self):
        return int(os.getenv('ADMIN_ID'))
