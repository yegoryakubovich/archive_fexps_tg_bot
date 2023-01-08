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

FTP_HOST = getenv('FTP_HOST')
FTP_USER = getenv('FTP_USER')
FTP_PASSWORD = getenv('FTP_PASSWORD')
FTP_PATH = getenv('FTP_PATH')

TG_KEY = getenv('TG_KEY')
TG_HELPER = getenv('TG_HELPER')
TG_GROUP = getenv('TG_GROUP')

SITE_ORDER = getenv('SITE_ORDER')
ORDERS_COUNT = int(getenv('ORDERS_COUNT'))
DOCS_PATH = getenv('DOCS_PATH')


class Texts:
    welcome = '🟡 Вас приветствует ФИНАНС EXPRESS Проверенный обмен денег №1 В АМЕРИКЕ\n\n' \
              'RUB USD UAH USDT (кэш, онлайн перевод)\n\n'
    name = 'Для продолжения, введите свое имя и фамилию.'
    referral = 'Откуда вы о нас узнали?'
    contact = 'Напишите контактный номер телефона или телеграм.' \
              'номер телефона или адрес электронной почты.'
    city = 'В каком городе вы находитесь?'
    registration_complete = 'Пожалуйста, проверьте свои данные:\n\n' \
                            'Имя: {}\n' \
                            'Контакт для связи: {}\n' \
                            'Город: {}'
    registration_complete_suc = 'Спасибо за регистрацию! Если потребуется помощь - нажмите на соответствующую ' \
                                'кнопку.\n\n' \
                                'Ваш Finance Express.'
    registration_complete_err = 'Вы начали регистрацию заново.'

    menu = 'Вы перенаправлены в главное меню.'
    menu_orders = '📦 Показаны последние 10 заказов:\n\n{}\nДля детализации конкретного заказа, введите его ID.'
    menu_order = '[{datetime}] [ID {order_id}] {currency_exchangeable_value} {currency_exchangeable} => ' \
                 '{currency_received_value} {currency_received};\n'
    menu_order_details = '<code>======= [ID {order_id}] =======\n\n' \
                         '1. Клиент: {customer_name};\n' \
                         '2. Меняемая валюта: {currency_exchangeable};\n' \
                         '3. Меняемая сумма: {currency_exchangeable_value};\n' \
                         '4. Обмен в: {currency_received};\n' \
                         '5. Курс обмена: {rate} {currency_received} за 1 {currency_exchangeable};\n' \
                         '6. Получаемая сумма: {currency_received_value};\n' \
                         '7. Подтверждение оплаты в {currency_exchangeable} от клиента: ✅ FILE {doc};\n' \
                         '8. Подтверждение оплаты в {currency_exchangeable} от администратора: {is_paid};\n' \
                         '9. Статус исполнения: {is_completed};\n' \
                         '10. Дата заказа: {datetime};\n' \
                         '11. Дата подтверждения оплаты в {currency_exchangeable}: {datetime_paid};\n' \
                         '12. Дата исполнения: {datetime_completed};\n' \
                         '13. Статус заказа: {is_closed}.\n\n' \
                         '===========================</code>'
    menu_order_statuses = {
        'is_paid': {True: '✅ ПОДТВЕРЖДЕНО', False: '🚫 ОТКЛОНЕНО', 'WAITING': '🕒 ОЖИДАНИЕ'},
        'is_completed': {True: '✅ ИСПОЛНЕН', False: '🚫 НЕ ИСПОЛНЕН'},
        'is_closed': {True: '✅ ЗАКРЫТ', False: '🕒 В РАБОТЕ'},
        'datetime': {False: '-'}
    }
    menu_help = '🙋 Для обращения к службе поддержки, пожалуйста, напишите на аккаунт: @{}'
    menu_settings = '⚙ Вы перенаправлены в меню настроек.'

    settings_name = 'Введите свое имя и фамилию.'
    settings_name_success = 'Данные успешно изменены!'

    order_direction_item = '{currency_exchangeable_icon}{currency_exchangeable} ➡ ' \
                           '{currency_received_icon}{currency_received}'
    order_direction = 'Выберите направление, по которому Вы бы хотели осуществить перевод.'
    order_range_infinity = 'от {currency_exchangeable_from} {currency_exchangeable}'
    order_range_column = 'Диапазон'
    order_rate_column = 'за 1 {currency_received}'
    order_range = '{currency_exchangeable_from}-{currency_exchangeable_to} {currency_exchangeable}'
    order_rate = '{rate} {currency_exchangeable}'
    order_rates = '<b>Актуальный КУРС {currency_exchangeable_icon}{currency_exchangeable}➡' \
                  '{currency_received_icon}{currency_received}</b>\n\n' \
                  '<code>{table_rates}</code>\n\n' \
                  '✅ Введите сумму в {currency_exchangeable_icon}{currency_exchangeable}, ' \
                  'которую вы хотите обменять в {currency_received_icon}{currency_received}.'
    order_currency_received_value = 'За {currency_exchangeable_value} {currency_exchangeable} вы получите {' \
                                    'currency_received_value} {currency_received} '
    order_requisite_exchangeable = 'Как вы хотите ПОЛУЧИТЬ деньги?'
    order_requisite_received = 'Как вы хотите ОТПРАВИТЬ деньги?'
    order_currency_exchangeable_requisite_payment = 'Пожалуйста, произведите оплату {currency_exchangeable_value} ' \
                                                    '{currency_exchangeable} по следующим реквизитам:\n\n' \
                                                    '{requisite_received}\n\n' \
                                                    'После оплаты обязательно пришлите чек (pdf/скриншот).'
    order_doc = 'Заказ исполняется!\n\nДокумент отправлен на проверку. Как только мы убедимся, что оплата прошла, ' \
                'мы отправим Вам денежные средства на указанные реквизиты.\n\nЕсли возникнут вопросы - обращайтесь ' \
                'в поддержку!'

    admin_new_order = 'Новый заказ! Обработайте его, перейдя по ссылке:\n\n{}'

    error = '❌ Возникла ошибка, пожалуйста, повторите попытку.'
    error_direction = '❌ Возникла ошибка, пожалуйста, выберите верное направление перевода.'
    error_dev = '❌ 👨‍💻 В разработке.'

    error_menu_order = '❌ У Вас уже есть активный заказ. Пожалуйста, дождитесь его исполнения.\n\n' \
                       'Если у Вас появились проблемы - обратитесь в поддержку.'
    error_order_direction = '❌ Нету валют, по которым мы могли бы предложить Вам обмен.'
    error_order_currency_value = '❌ Возникла ошибка, пожалуйста, введите верное число.'
    error_order_rate_not_exists = '❌ В данный момент мы не можем предложить Вам обмен. Остались вопросы? Напишите ' \
                                  'в нашу поддержку! '
    error_order_rate_only_admin = '❌ Для обмена такой суммы, пожалуйста, обращайтесь к @{}.'
    error_order_requisite = '❌ Пожалуйста, выберите способ оплаты из списка!'
    error_order_doc = '❌ В качестве доказательств, пожалуйста, пришлите чек pdf или скриншот.!'

    error_orders = '❌ Список заказов пуст.'
    error_order = '❌ Введите номер существующего заказа.'


class TextsKbs:
    registration_complete_suc = '✔ Данные верны'
    registration_complete_err = '❌ Начать ввод заново'

    menu_order = '💰 Обменять (перевести) ДЕНЬГИ'
    menu_orders = '📦 Мои заказы'
    menu_help = '🙋 Поддержка'
    menu_settings = '⚙ Настройки'

    settings_name = '📁 Изменить имя и фамилию'

    back = '◀ Вернуться назад'
