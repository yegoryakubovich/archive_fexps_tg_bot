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
from datetime import datetime

from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.exceptions import ChatNotFound

from app.ftp import ftp_upload
from app.models import Customer, Order, Rate, Doc, Direction, RequisiteReceived, RequisiteExchangeable
from app.models.models import db_manager, AdminMethodInput
from app.telegram import Form
from app.telegram.keyboards import kb_menu, kb_back, kb_order_back
from app.telegram.notifications import notification_send, Recipients
from config import TextsKbs, Texts, TG_HELPER, PATH_DOCS, PATH_ORDER, PATH_RATES_UPDATER, URL_DOC, URL_ORDER


@db_manager
async def handler_order(message: types.Message):
    user_id = message.from_user.id
    text = message.text
    customer = Customer.get(Customer.user_id == user_id)
    order = Order.get_or_none((Order.customer == customer) & (Order.is_closed == False))

    if not order:
        await Form.menu.set()
        await message.reply(Texts.menu)
        return

    # Go back
    if text == TextsKbs.back:
        # Close order & break menu
        order.is_closed = True
        order.save()

        await Form.menu.set()
        await message.reply(Texts.menu, reply_markup=kb_menu)

    elif text == TextsKbs.menu_help:
        await message.reply(Texts.menu_help.format(TG_HELPER))
        return

    # Enter order direction
    elif not order.direction:

        # Detect direction
        direction = None
        for d in Direction.select():
            d_text = Texts.order_direction_item.format(
                currency_exchangeable=d.currency_exchangeable.name,
                currency_exchangeable_icon=d.currency_exchangeable.icon,
                currency_received=d.currency_received.name,
                currency_received_icon=d.currency_received.icon,
            )
            if not text == d_text:
                continue
            direction = d

        # Errors if not detected direction with rates
        if not direction:
            await message.reply(Texts.error_direction)
            return
        if not Rate.get_or_none(Rate.direction == direction):
            await message.reply(Texts.error_direction)
            return

        # Save direction
        order.direction = direction
        order.save()

        img = 'rubusd'
        if order.direction.id == 2:
            img = 'usdrub'
        elif order.direction.id == 4:
            img = 'usdtusd'

        image = open('{}/images/{}.png'.format(PATH_RATES_UPDATER, img), 'rb')
        await message.answer_photo(photo=image)
        await message.reply(text='Введите сумму в {}, которую вы хотите ПОЛУЧИТЬ за {}.'.format(
            order.direction.currency_received.name,
            order.direction.currency_exchangeable.name,
        ), reply_markup=kb_order_back)

    # Enter currency exchangeable value
    elif not order.currency_exchangeable_value:
        if not text.isdigit():
            await message.reply(Texts.error_order_currency_value)
            return

        value = int(text)
        rate = Rate.get_or_none((Rate.direction == order.direction) &
                                (Rate.currency_exchangeable_from <= value) &
                                (Rate.currency_exchangeable_to >= value))

        if not rate:
            rate = Rate.get_or_none((Rate.direction == order.direction) &
                                    (Rate.currency_exchangeable_from <= value) &
                                    (Rate.currency_exchangeable_to == 0))

        # Errors
        if not rate:
            await message.reply(Texts.error_order_rate_not_exists)

            # Close order & back to menu
            order.is_closed = True
            order.save()

            await Form.menu.set()
            await message.answer(Texts.menu, reply_markup=kb_menu)
            return

        # Save changes
        order.currency_received_value = value
        order.save()

        if rate.only_admin:
            await message.reply(Texts.error_order_rate_only_admin.format(TG_HELPER))

            # Close order & back to menu
            order.is_closed = True
            order.save()

            await Form.menu.set()
            await message.answer(Texts.menu, reply_markup=kb_menu)
            return

        order.rate = rate.rate
        order.currency_exchangeable_value = round(order.currency_received_value * order.rate * 10000, 1)
        order.save()

        await message.reply(Texts.order_currency_received_value.format(
            currency_exchangeable=order.direction.currency_exchangeable.name,
            currency_exchangeable_value=order.currency_exchangeable_value,
            currency_received=order.direction.currency_received.name,
            currency_received_value=order.currency_received_value,
        ))

        kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
        for requisite_received in RequisiteReceived.select().where(
                RequisiteReceived.currency == order.direction.currency_exchangeable
        ):
            kb_btn = KeyboardButton(requisite_received.name)
            kb.add(kb_btn)
        kb.add(TextsKbs.menu_help)
        kb.add(TextsKbs.back)

        await message.answer(Texts.order_requisite_received, reply_markup=kb)

    # Enter received requisite
    elif not order.requisite_received:
        requisite_received = RequisiteReceived.get_or_none(
            (RequisiteReceived.name == text) &
            (RequisiteReceived.currency == order.direction.currency_exchangeable)
        )

        if not requisite_received:
            await message.reply(Texts.error_order_requisite)
            return

        order.requisite_received = requisite_received
        order.save()

        kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
        for requisite_exchangeable in RequisiteExchangeable.select().where(
                RequisiteExchangeable.direction == order.direction
        ):
            kb_btn = KeyboardButton(requisite_exchangeable.name)
            kb.add(kb_btn)
        kb.add(TextsKbs.menu_help)
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
            await message.reply(order.requisite_exchangeable.description, reply_markup=kb_order_back)
            return

        await message.reply(Texts.order_currency_exchangeable_requisite_payment.format(
            currency_exchangeable=order.direction.currency_exchangeable.name,
            currency_exchangeable_value=order.currency_exchangeable_value,
            requisite_received=order.requisite_received.requisite),
            reply_markup=kb_order_back)

    # Enter requisite description
    elif not order.requisite_exchangeable_value:
        order.requisite_exchangeable_value = text
        order.save()
        await message.reply(Texts.order_currency_exchangeable_requisite_payment.format(
            currency_exchangeable=order.direction.currency_exchangeable.name,
            currency_exchangeable_value=order.currency_exchangeable_value,
            requisite_received=order.requisite_received.requisite),
            reply_markup=kb_order_back)

    # Enter doc
    elif not order.doc:
        photo = message.photo
        document = message.document

        if photo:
            extension = 'jpg'
        elif document:
            extension = document.file_name.split('.')[-1]
        else:
            await message.reply(Texts.error_order_doc, reply_markup=kb_order_back)
            return

        doc = Doc(extension=extension)
        doc.save()

        destination_file = '{}/{}.{}'.format(PATH_DOCS, doc.id, doc.extension)
        if photo:
            await photo[-1].download(destination_file=destination_file)
        elif doc:
            await document.download(destination_file=destination_file)

        order.doc = doc
        order.save()

        # Upload to server
        ftp_upload(doc)

        # Admin notification
        order_doc_url = URL_DOC.format(
            id=doc.id,
            extension=doc.extension,
        )
        await notification_send(
            recipient=Recipients.group_logs,
            text='🟡 Создан <a href="{order_url}">заказ №{order_id}</a>:\n\n'
                 'Клиент: {customer_contact};\n'
                 'Сумма: {order_currency_exchangeable_value} {order_direction_currency_exchangeable_name} → '
                 '{order_currency_received_value} {order_direction_currency_received_name};\n'
                 'Метод оплаты: {method_input};\n'
                 'Метод получения: {method_output};\n'
                 'Значение метода получения: {method_output_value};\n'
                 'Документ: <a href="{order_doc_url}">url</a>.'
                 '\n\n#order_{order_id}'.format(
                order_url=URL_ORDER.format(order_id=order.id),
                order_id=order.id,
                customer_contact='@' + customer.username if customer.username else customer.contact,
                order_currency_exchangeable_value=order.currency_exchangeable_value,
                order_direction_currency_exchangeable_name=order.direction.currency_exchangeable.name,
                order_currency_received_value=order.currency_received_value,
                order_direction_currency_received_name=order.direction.currency_received.name,
                method_input=order.requisite_received.name,
                method_output=order.requisite_exchangeable.name,
                method_output_value=order.requisite_exchangeable_value,
                order_doc_url=order_doc_url,
            )
        )
        for admin_method_input in AdminMethodInput.select().where(
                AdminMethodInput.method_input == order.requisite_received
        ):
            await notification_send(
                recipient=Recipients.admin,
                admin=admin_method_input.admin,
                text='❗ Проверьте оплату <a href="{order_url}">заказа №{order_id}</a>:\n\n'
                     'Сумма: {order_currency_exchangeable_value} {order_direction_currency_exchangeable_name};\n'
                     'Метод оплаты: {method_input};\n'
                     'Документ: <a href="{order_doc_url}">url</a>.'
                     '\n\n#order_{order_id}'.format(
                    order_url=URL_ORDER.format(order_id=order.id),
                    order_id=order.id,
                    order_currency_exchangeable_value=order.currency_exchangeable_value,
                    order_direction_currency_exchangeable_name=order.direction.currency_exchangeable.name,
                    method_input=order.requisite_received.name,
                    order_doc_url=order_doc_url,
                )
            )

        await Form.menu.set()
        await message.reply(Texts.order_doc)
        await message.answer(Texts.menu, reply_markup=kb_menu)


@db_manager
async def handler_order_confirming(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    customer = Customer.get(Customer.user_id == user_id)
    order = Order.get_or_none((Order.customer == customer) & (Order.is_closed == False))

    if not order:
        await callback_query.message.delete()
        return

    order.is_completed = True
    order.datetime_completed = datetime.now()
    order.is_closed = True
    order.save()

    await callback_query.message.answer('💜 Спасибо за Ваш заказ! Будем рады Вам помочь еще. '
                                        'Пожалуйста, оставьте отзыв в нашей группе.\n\n'
                                        '👥 t.me/Obmen_USA/22\n\n'
                                        '❗ Также там в режиме реального времени публикуются актуальные курсы валют.')
    await callback_query.message.delete()

    await notification_send(
        recipient=Recipients.group_logs,
        text='🟢 <a href="{order_url}">Заказ №{order_id}</a> '
             'помечен пользователем ({customer_contact} как выполненный.'
             '\n\n#order_{order_id}'.format(
            order_url=URL_ORDER.format(order_id=order.id),
            order_id=order.id,
            customer_contact='@' + customer.username if customer.username else customer.contact,
        )
    )
