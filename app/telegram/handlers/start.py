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
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

from app.models import Customer
from app.telegram.form import Form
from app.telegram.keyboards import kb_registration_complete, kb_menu
from config import Texts, TextsKbs


async def handler_start(message: types.Message):
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
        tg_name = message.from_user.first_name
        if tg_name:
            kb_btn = KeyboardButton(tg_name)
            kb.add(kb_btn)
        await message.answer(Texts.name, reply_markup=kb)

    # Enter  name
    elif not customer.name:
        customer.name = text
        customer.save()
        await message.reply(Texts.referral, reply_markup=ReplyKeyboardRemove())

    # Enter referral
    elif not customer.referral:
        customer.referral = text
        customer.save()
        await message.reply(Texts.contact)

    # Enter contact
    elif not customer.contact:
        customer.contact = text
        customer.save()
        await message.reply(Texts.city)

    # Enter city
    elif not customer.city:
        customer.city = text
        customer.save()
        await message.reply(Texts.registration_complete.format(customer.name,
                                                               customer.contact,
                                                               customer.city,),
                            reply_markup=kb_registration_complete)

    # Error registration, go to start
    elif text == TextsKbs.registration_complete_err:
        # Delete data
        customer.name = None
        customer.referral = None
        customer.contact = None
        customer.city = None
        customer.save()

        # Create keyboard & send message
        kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        tg_name = message.from_user.first_name
        if tg_name:
            kb_btn = KeyboardButton(tg_name)
            kb.add(kb_btn)
        await message.reply(Texts.registration_complete_err)
        await message.answer(Texts.name, reply_markup=kb)

    # Success registration, go to menu
    elif text == TextsKbs.registration_complete_suc:
        await Form.menu.set()
        await message.reply(Texts.registration_complete_suc, reply_markup=kb_menu)

    # Account exists, go to menu
    else:
        await Form.menu.set()
        await message.reply(Texts.menu, reply_markup=kb_menu)
