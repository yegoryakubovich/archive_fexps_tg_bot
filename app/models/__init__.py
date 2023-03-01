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


from app.models.models import Currency, Direction, RequisiteExchangeable, RequisiteReceived, Customer, Rate, Doc, \
    Order, db_manager, db, MailingRate


models = [
    Currency, Direction, RequisiteExchangeable, RequisiteReceived, Customer, Rate, Doc, Order, MailingRate
]


def create_tables():
    db.connect()
    for model in models:
        exec('{}.create_table()'.format(model.__name__))
    db.close()
