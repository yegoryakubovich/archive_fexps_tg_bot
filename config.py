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


from os import getenv

DB_HOST = getenv('DB_HOST')
DB_PORT = int(getenv('DB_PORT'))
DB_USER = getenv('DB_USER')
DB_PASSWORD = getenv('DB_PASSWORD')
DB_NAME = getenv('DB_NAME')

TG_KEY = getenv('TG_KEY')
TG_HELPER = getenv('TG_HELPER')


class Texts:
    welcome = '🟡 Вас приветствует ФИНАНС EXPRESS Проверенный обмен денег №1 В АМЕРИКЕ\n\n' \
              'RUB USD UAH USDT (кэш, онлайн перевод)\n\n'
    first_name = 'Для продолжения, пожалуйста, введите свое имя.'
    second_name = '{}, спасибо. Теперь введите свою фамилию.'
    registration_complete = 'Пожалуйста, проверьте свои данные:\n\n' \
                            'Имя: {}\n' \
                            'Фамилия: {}.'
    registration_complete_suc = 'Спасибо за регистрацию! Если потребуется помощь - нажмите на соответствующую ' \
                                'кнопку.\n\n' \
                                'Ваш Finance Express.'
    registration_complete_err = 'Вы начали регистрацию заново.'

    menu = 'Вы перенаправлены в главное меню.'
    menu_transfer = '💸 Обменять (перевести) деньги'
    menu_orders = '📦 Мои заказы'
    menu_help = '🙋 Для обращения к службе поддержки, пожалуйста, напишите на аккаунт: @{}'
    menu_settings = '⚙ Настройки\n\n' \
                    '1. ИФ: {second_name} {first_name};\n' \
                    '2. Количество заказов: 0 (~0$).'

    settings_fullname_first_name = 'Введите свое имя.'
    settings_fullname_second_name = 'Введите свою фамилию.'
    settings_fullname = 'Данные успешно изменены!'

    transfer_currency_exchangeable = 'Какую валюту Вы хотите обменять?'
    transfer_currency_received = 'Какую валюту Вы хотите получить?'
    transfer_rate = 'Актуальный курс по переводу {currency_exchangeable} => {currency_received}:\n\n{}'

    error = '❌ Возникла ошибка, пожалуйста, повторите попытку.'
    error_currency = '❌ Возникла ошибка, пожалуйста, выберите верную валюту.'
    dev = '👨‍💻 В разработке.'


class TextsKbs:
    registration_complete_suc = '✔ Данные верны'
    registration_complete_err = '❌ Начать ввод заново'

    menu_transfer = '💸 Обменять (перевести) деньги'
    menu_orders = '📦 Мои заказы'
    menu_help = '🙋 Поддержка'
    menu_settings = '⚙ Настройки'

    settings_fullname = '📁 Изменить ИФ'

    back = '◀ Вернуться назад'
