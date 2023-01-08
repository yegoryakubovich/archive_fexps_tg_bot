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
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from app.models import Customer, Currency
from app.telegram import Form
from app.telegram.keyboards import kb_menu, kb_settings
from config import TextsKbs, Texts


async def handler_settings(message: types.Message):
    user_id = message.from_user.id
    text = message.text
    customer = Customer.get(Customer.user_id == user_id)

    if text == TextsKbs.back:
        await Form.menu.set()
        await message.reply(Texts.menu, reply_markup=kb_menu)

    elif text == TextsKbs.settings_fullname:
        # Delete data
        customer.first_name = None
        customer.second_name = None
        customer.save()

        await Form.settings_fullname.set()

        # Create keyboard & send message
        kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        tg_first_name = message.from_user.first_name
        if tg_first_name:
            kb_btn = KeyboardButton(tg_first_name)
            kb.add(kb_btn)
        await message.reply(Texts.settings_fullname_first_name, reply_markup=kb)

    elif text == TextsKbs.settings_requisites:
        await Form.settings_requisites.set()

        # Create keyboard & send message
        kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        for currency in Currency.select():
            kb.add(KeyboardButton(currency.name))
        kb.add(KeyboardButton(TextsKbs.back))
        await message.reply(Texts.settings_requisites, reply_markup=kb)

    else:
        await message.reply(Texts.error)


async def handler_settings_fullname(message: types.Message):
    user_id = message.from_user.id
    text = message.text
    customer = Customer.get(Customer.user_id == user_id)

    # Enter first name
    if not customer.first_name:
        customer.first_name = text
        customer.save()

        # Create keyboard & send message
        kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        tg_second_name = message.from_user.last_name
        if tg_second_name:
            kb_btn = KeyboardButton(tg_second_name)
            kb.add(kb_btn)
        await message.reply(Texts.settings_fullname_second_name, reply_markup=kb)

    # Enter second name
    elif not customer.second_name:
        customer.second_name = text
        customer.save()

        await Form.settings.set()
        await message.reply(Texts.settings_name_success)
        await message.answer(Texts.menu_settings, reply_markup=kb_settings)
