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


from aiogram import Bot
from aiogram.utils.exceptions import ChatNotFound
from telebot import TeleBot

from app.models import Customer, Admin, Doc
from config import TG_GROUP_LOGS_ID, TG_BOT_ADMIN_KEY, URL_DOC, TG_BOT_KEY


bot_customer = TeleBot(token=TG_BOT_KEY)
bot_admin = Bot(token=TG_BOT_ADMIN_KEY)


class Recipients:
    group_logs = 'group_logs'
    admin = 'admin'
    customer = 'customer'
    customers_all = 'customers_all'


async def notification_send(
        recipient: str,
        text: str = None,
        doc: Doc = None, customer:
        Customer = None,
        admin: Admin = None,
        markup=None,
):
    chat_id = None
    bot = bot_customer
    if recipient == Recipients.customer:
        chat_id = customer.user_id
    elif recipient == Recipients.admin:
        chat_id = admin.customer.user_id
        bot = bot_admin
    elif recipient == Recipients.group_logs:
        chat_id = TG_GROUP_LOGS_ID
        bot = bot_admin
    try:
        if doc:
            doc_url = URL_DOC.format(
                id=doc.id,
                extension=doc.extension,
            )
            await bot.send_document(chat_id=chat_id, document=doc_url)

        if text:
            await bot.send_message(
                chat_id=chat_id,
                text=text,
                reply_markup=markup,
                parse_mode='html',
                disable_web_page_preview=True,
            )
    except ChatNotFound:
        await notification_send(
            recipient=Recipients.group_logs,
            text='❗ Администратор {admin_contact} не написал в @fexps_admin_bot. '
                 'Он не получает уведолмение.\n\nНедоставленное уведомление продублированно ниже.'.format(
                admin_contact=admin.customer.username if admin.customer.username else admin.customer.username,
            )
        )
        await notification_send(
            recipient=Recipients.group_logs,
            text=text,
            doc=doc,
        )
