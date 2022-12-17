#
# (c) 2022, Yegor Yakubovich
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#


from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor

from app.models import Order
from app.telegram.form import Form
from app.telegram.handlers.menu import menu
from app.telegram.handlers.order import hdl_order
from app.telegram.handlers.settings import settings, settings_fullname
from app.telegram.handlers.start import start
from app.telegram.keyboards import kb_registration_complete, kb_menu
from config import TG_KEY

bot = Bot(token=TG_KEY)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
HANDLERS = [
    {'handler': start, 'state': None, 'content_types': ['text']},
    {'handler': menu, 'state': Form.menu, 'content_types': ['text']},
    {'handler': settings, 'state': Form.settings, 'content_types': ['text']},
    {'handler': settings_fullname, 'state': Form.settings_fullname, 'content_types': ['text', 'photo', 'document']},
    {'handler': hdl_order, 'state': Form.order, 'content_types': ['text']},
]


def handlers_create():
    [dp.register_message_handler(h['handler'], state=h['state'], content_types=h['content_types']) for h in HANDLERS]


def orders_close():
    for order in Order.select().where((Order.is_closed == False) & (Order.rate == 0)):
        order.is_closed = True
        order.save()


def start_bot():
    orders_close()
    handlers_create()
    executor.start_polling(dp)
