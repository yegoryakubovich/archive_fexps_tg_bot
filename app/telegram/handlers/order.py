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

from app.ftp import ftp_upload
from app.models import Customer, Order, Rate, Doc, Direction, RequisiteReceived, RequisiteExchangeable
from app.telegram import Form
from app.telegram.keyboards import kb_menu, kb_back
from app.telegram.notifications import notification_send
from config import TextsKbs, Texts, TG_HELPER, DOCS_PATH, SITE_ORDER


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

    # Enter order direction
    elif not order.direction:
        # Detect currency
        direction = None
        for d in Direction.select():
            d_text = Texts.order_direction_item.format(
                currency_exchangeable=d.currency_exchangeable.name,
                currency_received=d.currency_received.name
            )
            if not text == d_text:
                continue
            direction = d

        if not direction:
            await message.reply(Texts.error_direction)
            return
        if not Rate.get_or_none(Rate.direction == direction):
            await message.reply(Texts.error_direction)
            return
        order.direction = direction
        order.save()

        text_reply = ''
        for num, rate in enumerate(Rate.select().where(Rate.direction == order.direction), 1):
            text_reply += Texts.order_rate.format(
                num=num, currency_exchangeable_from=int(rate.currency_exchangeable_from),
                currency_exchangeable_to=int(rate.currency_exchangeable_to),
                currency_exchangeable=order.direction.currency_exchangeable.name,
                currency_received_rate=round(rate.rate*10000, 1),
                currency_received=order.direction.currency_received.name
            )

        await message.reply(text_reply)
        await message.answer(Texts.order_currency_exchangeable_value.format(
            currency_exchangeable=order.direction.currency_exchangeable.name,
            currency_received=order.direction.currency_received.name
        ), reply_markup=kb_back)

    # Enter currency exchangeable value
    elif not order.currency_exchangeable_value:
        if not text.isdigit():
            await message.reply(Texts.error_order_currency_value)
            return

        value = int(text)
        rate = Rate.get_or_none((Rate.direction == order.direction) &
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
            currency_exchangeable=order.direction.currency_exchangeable.name,
            currency_exchangeable_value=order.currency_exchangeable_value,
            currency_received=order.direction.currency_received.name,
            currency_received_value=order.currency_received_value,
        ))

        kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
        for requisite_received in RequisiteReceived.select():
            kb_btn = KeyboardButton(requisite_received.name)
            kb.add(kb_btn)
        kb.add(TextsKbs.back)

        await message.answer(Texts.order_requisite_received, reply_markup=kb)

    # Enter exchangeable requisite
    elif not order.requisite_received:
        requisite_received = RequisiteReceived.get_or_none(RequisiteReceived.name == text)

        if not requisite_received:
            await message.reply(Texts.error_order_requisite)
            return

        order.requisite_received = requisite_received
        order.save()

        kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
        for requisite_exchangeable in RequisiteExchangeable.select():
            kb_btn = KeyboardButton(requisite_exchangeable.name)
            kb.add(kb_btn)
        kb.add(TextsKbs.back)

        await message.answer(Texts.order_requisite_exchangeable, reply_markup=kb)

    # Enter exchangeable requisite
    elif not order.requisite_exchangeable:
        requisite_exchangeable = RequisiteExchangeable.get_or_none(RequisiteExchangeable.name == text)

        if not requisite_exchangeable:
            await message.reply(Texts.error_order_requisite)
            return
        requisite_exchangeable: RequisiteExchangeable

        order.requisite_exchangeable = requisite_exchangeable
        if requisite_exchangeable.description == 'null':
            order.requisite_exchangeable_value = 'Not required'
        order.save()

        if not order.requisite_exchangeable_value:
            await message.reply(order.requisite_exchangeable.description, reply_markup=kb_back)
            return

        await message.reply(Texts.order_currency_exchangeable_requisite_payment.format(
            currency_exchangeable=order.direction.currency_exchangeable.name,
            currency_exchangeable_value=order.currency_exchangeable_value,
            requisite_received=order.requisite_received.requisite),
            reply_markup=kb_back)

    # Enter requisite description
    elif not order.requisite_exchangeable_value:
        order.requisite_exchangeable_value = text
        order.save()
        await message.reply(Texts.order_currency_exchangeable_requisite_payment.format(
            currency_exchangeable=order.direction.currency_exchangeable.name,
            currency_exchangeable_value=order.currency_exchangeable_value,
            requisite_received=order.requisite_received.requisite),
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

        # Upload to server
        ftp_upload(doc)

        # Admin notification
        notification_send(text=Texts.admin_new_order.format(SITE_ORDER.format(order.id)))

        await Form.menu.set()
        await message.reply(Texts.order_doc)
        await message.answer(Texts.menu, reply_markup=kb_menu)
