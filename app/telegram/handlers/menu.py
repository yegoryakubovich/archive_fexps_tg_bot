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


from aiogram import types

from app.models import Customer
from app.telegram import Form
from app.telegram.keyboards import kb_settings
from config import Texts, TextsKbs, TG_HELPER


async def menu(message: types.Message):
    user_id = message.from_user.id
    text = message.text
    customer = Customer.get(Customer.user_id == user_id)

    if text == TextsKbs.menu_transfer:
        pass
    elif text == TextsKbs.menu_orders:
        pass
    elif text == TextsKbs.menu_settings:
        await Form.settings.set()
        await message.reply(Texts.menu_settings.format(first_name=customer.first_name,
                                                       second_name=customer.second_name,
                                                       patronymic=customer.patronymic), reply_markup=kb_settings)
    elif text == TextsKbs.menu_help:
        await message.reply(Texts.menu_help.format(TG_HELPER))
    else:
        await message.reply(Texts.error)
