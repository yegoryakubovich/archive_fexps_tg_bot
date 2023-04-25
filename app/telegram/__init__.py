#
# (c) 2023, Yegor Yakubovich
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
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiogram.utils import executor
from telebot import types

from app.models import Order
from app.models.models import db
from app.telegram.form import Form
from app.telegram.handlers.menu import handler_menu
from app.telegram.handlers.order import handler_order, handler_order_confirming
from app.telegram.handlers.orders import handler_orders
from app.telegram.handlers.settings import handler_settings, handler_settings_name
from app.telegram.handlers.start import handler_start
from app.telegram.keyboards import kb_registration_complete, kb_menu
from config import TG_BOT_KEY, REDIS_HOST, REDIS_PORT, REDIS_PASSWORD, REDIS_DB, REDIS_PREFIX


bot = Bot(token=TG_BOT_KEY)
storage = RedisStorage2(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD,
                        db=REDIS_DB, pool_size=10, prefix=REDIS_PREFIX)
dp = Dispatcher(bot, storage=storage)
HANDLERS = [
    {'handler': handler_start, 'state': None, 'content_types': ['text']},
    {'handler': handler_menu, 'state': Form.menu, 'content_types': ['text']},
    {'handler': handler_order, 'state': Form.order, 'content_types': ['text', 'photo', 'document']},
    {'handler': handler_orders, 'state': Form.orders, 'content_types': ['text']},
    {'handler': handler_settings, 'state': Form.settings, 'content_types': ['text']},
    {'handler': handler_settings_name, 'state': Form.settings_name, 'content_types': ['text']},
]


def handlers_create():
    [dp.register_message_handler(h['handler'], state=h['state'], content_types=h['content_types']) for h in HANDLERS]
    dp.register_callback_query_handler(
        handler_order_confirming,
        lambda c: c.data == 'order_confirm',
        state=Form.all_states,
    )


def start_bot():
    handlers_create()
    executor.start_polling(dp)
