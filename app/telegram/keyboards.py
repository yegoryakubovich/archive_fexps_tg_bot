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


from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from config import TextsKbs


kb_registration_complete = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
kb_registration_complete.add(KeyboardButton(TextsKbs.registration_complete_suc))
kb_registration_complete.add(KeyboardButton(TextsKbs.registration_complete_err))

kb_menu = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
kb_menu.add(KeyboardButton(TextsKbs.menu_order))
kb_menu.add(KeyboardButton(TextsKbs.menu_orders), KeyboardButton(TextsKbs.menu_settings))
kb_menu.add(KeyboardButton(TextsKbs.menu_help))

kb_settings = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
kb_settings.add(KeyboardButton(TextsKbs.setting_contact))
kb_settings.add(KeyboardButton(TextsKbs.back))

kb_back = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
kb_back.add(KeyboardButton(TextsKbs.back))

kb_order_back = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
kb_order_back.add(KeyboardButton(TextsKbs.menu_help))
kb_order_back.add(KeyboardButton(TextsKbs.back))
