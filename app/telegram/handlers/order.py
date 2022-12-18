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

from app.models import Customer, Order, Currency, Rate, CurrencyRequisite
from app.models.models import Doc, CustomerRequisite
from app.telegram import Form
from app.telegram.keyboards import kb_menu, kb_back
from config import TextsKbs, Texts, TG_HELPER, DOCS_PATH


async def handler_order(message: types.Message):
    user_id = message.from_user.id
    text = message.text
    customer = Customer.get(Customer.user_id == user_id)
    order = Order.get((Order.customer == customer) & (Order.is_closed == False))

    # Go back
    if text == TextsKbs.back:
        # Close order & break menu
        order.is_closed = True
        order.save()

        await Form.menu.set()
        await message.reply(Texts.menu, reply_markup=kb_menu)

    # Enter currency exchangeable
    elif not order.currency_exchangeable:
        # Detect currency
        currency_exchangeable = Currency.get_or_none(Currency.name == text)
        if not currency_exchangeable:
            await message.reply(Texts.error_currency)
            return
        order.currency_exchangeable = currency_exchangeable
        order.save()

        # Create keyboard & send message
        kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
        for currency in Currency.select():
            if currency == currency_exchangeable:
                continue
            kb_btn = KeyboardButton(currency.name)
            kb.add(kb_btn)
        kb.add(TextsKbs.back)
        await message.reply(Texts.order_currency_received, reply_markup=kb)

    # Enter currency received
    elif not order.currency_received:
        # Detect currency
        currency_received = Currency.get_or_none(Currency.name == text)
        if not currency_received or currency_received == order.currency_exchangeable:
            await message.reply(Texts.error_currency)
            return

        order.currency_received = currency_received
        order.save()

        # Not requisite
        if not CustomerRequisite.get_or_none((CustomerRequisite.customer == customer) &
                                             (CustomerRequisite.currency == order.currency_received)):
            order.is_closed = True
            order.save()

            await Form.menu.set()
            await message.reply(Texts.error_order_currency_received_requisite)
            await message.answer(Texts.menu, reply_markup=kb_menu)
            return

        text_reply = ''
        for num, rate in enumerate(Rate.select().where((Rate.currency_exchangeable == order.currency_exchangeable) &
                                                       (Rate.currency_received == order.currency_received)), 1):
            text_reply += Texts.order_rate.format(
                num=num, currency_exchangeable_from=rate.currency_exchangeable_from,
                currency_exchangeable_to=rate.currency_exchangeable_to,
                currency_exchangeable=order.currency_exchangeable.name,
                currency_received_rate=rate.rate,
                currency_received=order.currency_received.name
            )

        await message.reply(text_reply)
        await message.answer(Texts.order_currency_exchangeable_value.format(
            currency_exchangeable=order.currency_exchangeable.name,
            currency_received=order.currency_received.name
        ), reply_markup=kb_back)

    # Enter currency exchangeable value
    elif not order.currency_exchangeable_value:
        if not text.isdigit():
            await message.reply(Texts.error_order_currency_value)
            return

        value = int(text)
        rate = Rate.get_or_none((Rate.currency_exchangeable == order.currency_exchangeable) &
                                (Rate.currency_received == order.currency_received) &
                                (Rate.currency_exchangeable_from <= value) &
                                (Rate.currency_exchangeable_to >= value))

        # Save changes
        order.currency_exchangeable_value = value
        order.save()

        # Errors
        if not rate:
            await message.reply(Texts.error_order_rate_not_exists)

            # Close order & back to menu
            order.is_closed = True
            order.save()

            await Form.menu.set()
            await message.answer(Texts.menu, reply_markup=kb_menu)
            return

        elif rate.only_admin:
            await message.reply(Texts.error_order_rate_only_admin.format(TG_HELPER))

            # Close order & back to menu
            order.is_closed = True
            order.save()

            await Form.menu.set()
            await message.answer(Texts.menu, reply_markup=kb_menu)
            return

        order.rate = rate.rate
        order.currency_received_value = order.currency_exchangeable_value * order.rate
        order.save()

        await message.reply(Texts.order_currency_received_value.format(
            currency_exchangeable=order.currency_exchangeable.name,
            currency_exchangeable_value=order.currency_exchangeable_value,
            currency_received=order.currency_received.name,
            currency_received_value=order.currency_received_value,
        ), reply_markup=kb_back)

        kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
        for currency_requisite in CurrencyRequisite \
                .select().where((CurrencyRequisite.active == True) &
                                (CurrencyRequisite.currency == order.currency_exchangeable)):
            kb.add(KeyboardButton(currency_requisite.name))
        kb.add(KeyboardButton(TextsKbs.back))
        await message.answer(Texts.order_currency_requisites, reply_markup=kb)

    # Enter payment requisite
    elif not order.currency_requisite:
        currency_requisite = CurrencyRequisite.get_or_none((CurrencyRequisite.active == True) &
                                                           (CurrencyRequisite.name == text))
        if not currency_requisite:
            await message.reply(Texts.error_order_currency_exchangeable_requisite)
            return

        order.currency_requisite = currency_requisite
        order.save()

        await message.reply(Texts.order_currency_requisite.format(
            currency_exchangeable=order.currency_exchangeable.name,
            currency_exchangeable_value=order.currency_exchangeable_value,
            order_currency_requisite=order.currency_requisite.requisite),
            reply_markup=kb_back)

    # Enter doc
    elif not order.doc:
        photo = message.photo
        document = message.document

        if photo:
            extension = 'jpg'
        elif document:
            extension = document.file_name.split('.')[-1]
        else:
            await message.reply(Texts.error_order_doc, reply_markup=kb_back)
            return

        doc = Doc(extension=extension)
        doc.save()

        destination_file = '{}/{}.{}'.format(DOCS_PATH, doc.id, doc.extension)
        if photo:
            await photo[-1].download(destination_file=destination_file)
        elif doc:
            await document.download(destination_file=destination_file)

        order.doc = doc
        order.save()

        await Form.menu.set()
        await message.reply(Texts.order_doc)
        await message.answer(Texts.menu, reply_markup=kb_menu)
