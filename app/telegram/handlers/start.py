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


from datetime import datetime

from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from app.models import Customer
from app.telegram.form import Form
from app.telegram.keyboards import kb_registration_complete, kb_menu
from config import Texts, TextsKbs


async def start(message: types.Message):
    user_id = message.from_user.id
    text = message.text
    customer = Customer.get_or_none(Customer.user_id == user_id)

    # Start registration
    if not customer:
        username = message.from_user.username

        customer = Customer(user_id=user_id, username=username, datetime=datetime.now())
        customer.save()

        await message.reply(Texts.welcome)

        # Create keyboard & send message
        kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        tg_first_name = message.from_user.first_name
        if tg_first_name:
            kb_btn = KeyboardButton(tg_first_name)
            kb.add(kb_btn)
        await message.answer(Texts.first_name, reply_markup=kb)

    # Enter first name
    elif not customer.first_name:
        customer.first_name = text
        customer.save()

        # Create keyboard & send message
        kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        tg_second_name = message.from_user.last_name
        if tg_second_name:
            kb_btn = KeyboardButton(tg_second_name)
            kb.add(kb_btn)
        await message.reply(Texts.second_name.format(customer.first_name), reply_markup=kb)

    # Enter second name
    elif not customer.second_name:
        customer.second_name = text
        customer.save()

        await message.reply(Texts.registration_complete.format(customer.first_name,
                                                               customer.second_name),
                            reply_markup=kb_registration_complete)

    # Error registration, go to start
    elif text == TextsKbs.registration_complete_err:
        # Delete data
        customer.first_name = None
        customer.second_name = None
        customer.save()
        await message.reply(Texts.registration_complete_err, reply_markup=kb_menu)

        # Create keyboard & send message
        kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        tg_first_name = message.from_user.first_name
        if tg_first_name:
            kb_btn = KeyboardButton(tg_first_name)
            kb.add(kb_btn)
        await message.answer(Texts.first_name, reply_markup=kb)

    # Success registration, go to menu
    elif text == TextsKbs.registration_complete_suc:
        await Form.menu.set()
        await message.reply(Texts.registration_complete_suc, reply_markup=kb_menu)

    # Account exists, go to menu
    else:
        await Form.menu.set()
        await message.reply(Texts.menu, reply_markup=kb_menu)
