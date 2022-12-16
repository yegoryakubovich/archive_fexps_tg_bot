from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from app.models import Customer
from app.telegram import Form
from app.telegram.keyboards import kb_menu, kb_settings
from config import TextsKbs, Texts


async def settings(message: types.Message):
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
        customer.patronymic = None
        customer.save()

        await Form.settings_fullname.set()

        # Create keyboard & send message
        kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        tg_first_name = message.from_user.first_name
        if tg_first_name:
            kb_btn = KeyboardButton(tg_first_name)
            kb.add(kb_btn)
        await message.reply(Texts.settings_fullname_first_name, reply_markup=kb)
    else:
        await message.reply(Texts.error)


async def settings_fullname(message: types.Message):
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

        await message.reply(Texts.settings_fullname_patronymic)

    # Enter patronymic
    elif not customer.patronymic:
        customer.patronymic = text
        customer.save()

        await Form.settings.set()
        await message.reply(Texts.settings_fullname, reply_markup=kb_settings)
