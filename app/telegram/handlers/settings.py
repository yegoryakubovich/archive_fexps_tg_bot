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
from aiogram.types import ReplyKeyboardRemove

from app.models import Customer
from app.models.models import db_manager
from app.telegram import Form
from app.telegram.keyboards import kb_menu, kb_settings
from config import TextsKbs, Texts


@db_manager
async def handler_settings(message: types.Message):
    user_id = message.from_user.id
    text = message.text
    customer = Customer.get(Customer.user_id == user_id)

    if text == TextsKbs.back:
        await Form.menu.set()
        await message.reply(Texts.menu, reply_markup=kb_menu)

    elif text == TextsKbs.setting_contact:
        # Delete data
        customer.contact = None
        customer.save()

        await Form.settings_name.set()
        await message.reply(Texts.setting_contact, reply_markup=ReplyKeyboardRemove())

    else:
        await message.reply(Texts.error)


@db_manager
async def handler_settings_name(message: types.Message):
    user_id = message.from_user.id
    text = message.text
    customer = Customer.get(Customer.user_id == user_id)

    # Enter first name
    if not customer.contact:
        customer.contact = text
        customer.save()

        await Form.settings.set()
        await message.reply(Texts.setting_contact_success)
        await message.answer(Texts.menu_settings, reply_markup=kb_settings)
