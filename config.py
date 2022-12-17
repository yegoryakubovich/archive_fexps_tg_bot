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

DOCS_PATH = getenv('DOCS_PATH')


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

    order_currency_exchangeable = 'Какую валюту Вы хотите обменять?'
    order_currency_received = 'Какую валюту Вы хотите получить?'
    order_rates = 'Актуальный курс по переводу {currency_exchangeable} => {currency_received}:\n\n{}'
    order_rate = '{num}. {currency_exchangeable_from} {currency_exchangeable} - {currency_exchangeable_to} ' \
                 '{currency_exchangeable} - {currency_received_rate} {currency_received};\n'
    order_currency_exchangeable_value = 'Введите сумму в {currency_exchangeable}, которую вы хотите обменять в {' \
                                        'currency_received}. '
    order_currency_received_value = 'За {currency_exchangeable_value} {currency_exchangeable} вы получите {' \
                                    'currency_received_value} {currency_received} '
    order_currency_method = 'Выберите способ оплаты из списка.'
    order_currency_description = 'Пожалуйста, произведите оплату по следующим реквизитам:\n\n{}\n\n' \
                                 'После оплаты обязательно пришлите чек (pdf/скриншот).'
    order_doc = 'Заказ исполняется!\n\nДокумент отправлен на проверку. Как только мы убедимся, что оплата прошла, ' \
                'мы отправим Вам денежные средства на указанные реквизиты.\n\nЕсли возникнут вопросы - обращайтесь ' \
                'в поддержку!'

    error = '❌ Возникла ошибка, пожалуйста, повторите попытку.'
    error_menu_order = '❌ У Вас уже есть активный заказ. Пожалуйста, дождитесь его исполнения.\n\n' \
                       'Если у Вас появились проблемы - обратитесь в поддержку.'
    error_order_currency = '❌ Возникла ошибка, пожалуйста, выберите верную валюту.'
    error_order_currency_value = '❌ Возникла ошибка, пожалуйста, введите верное число.'
    error_order_rate_not_exists = '❌ В данный момент мы не можем предложить Вам обмен. Остались вопросы? Напишите ' \
                                  'в нашу поддержку! '
    error_order_rate_only_admin = '❌ Для обмена такой суммы, пожалуйста, обращайтесь к @{}.'
    error_order_currency_method = '❌ Пожалуйста, выберите способ оплаты из списка!'
    error_order_doc = '❌ В качестве доказательств, пожалуйста, пришлите чек pdf или скриншот.!'
    error_dev = '❌ 👨‍💻 В разработке.'


class TextsKbs:
    registration_complete_suc = '✔ Данные верны'
    registration_complete_err = '❌ Начать ввод заново'

    menu_order = '💸 Обменять (перевести) деньги'
    menu_orders = '📦 Мои заказы'
    menu_help = '🙋 Поддержка'
    menu_settings = '⚙ Настройки'

    settings_fullname = '📁 Изменить ИФ'

    back = '◀ Вернуться назад'
