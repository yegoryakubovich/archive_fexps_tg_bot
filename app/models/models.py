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


from peewee import MySQLDatabase, Model, PrimaryKeyField, CharField, BigIntegerField, DateTimeField, ForeignKeyField, \
    FloatField, BooleanField

from config import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT


db = MySQLDatabase(DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT, charset='utf8mb4')


class BaseModel(Model):
    class Meta:
        database = db


class Customer(BaseModel):
    id = PrimaryKeyField()
    user_id = BigIntegerField()
    username = CharField(max_length=64, null=True)
    first_name = CharField(max_length=128, null=True, default=None)
    second_name = CharField(max_length=128, null=True, default=None)
    datetime = DateTimeField()

    class Meta:
        db_table = "customers"


class Currency(BaseModel):
    id = PrimaryKeyField()
    name = CharField(max_length=16)

    class Meta:
        db_table = "currencies"


class CurrencyMethod(BaseModel):
    id = PrimaryKeyField()
    currency = ForeignKeyField(Currency, to_field='id', on_delete='cascade')
    name = CharField(max_length=64)
    description = CharField(max_length=1024)
    active = BooleanField(default=True)

    class Meta:
        db_table = "currencies_methods"


class Rate(BaseModel):
    id = PrimaryKeyField()
    currency_exchangeable = ForeignKeyField(Currency, to_field='id', on_delete='cascade')
    currency_received = ForeignKeyField(Currency, to_field='id', on_delete='cascade')
    currency_exchangeable_from = FloatField()
    currency_exchangeable_to = FloatField()
    rate = FloatField()
    only_admin = BooleanField(default=False)

    class Meta:
        db_table = "rates"


class Order(BaseModel):
    id = PrimaryKeyField()
    customer = ForeignKeyField(Customer, to_field='id', on_delete='cascade')
    currency_exchangeable = ForeignKeyField(Currency, to_field='id', on_delete='cascade', null=True, default=None)
    currency_received = ForeignKeyField(Currency, to_field='id', on_delete='cascade', null=True, default=None)
    currency_exchangeable_value = FloatField(null=True, default=None)
    currency_received_value = FloatField(null=True, default=None)
    rate = FloatField(default=0)
    currency_method = ForeignKeyField(CurrencyMethod, to_field='id', on_delete='cascade', null=True, default=None)
    is_paid = BooleanField(default=False)
    is_completed = BooleanField(default=False)
    datetime = DateTimeField()
    datetime_paid = DateTimeField(null=True, default=None)
    datetime_complete = DateTimeField(null=True, default=None)
    is_closed = BooleanField(default=False)

    class Meta:
        db_table = "orders"
