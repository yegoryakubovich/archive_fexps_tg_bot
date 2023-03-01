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

from config import MYSQL_NAME, MYSQL_USER, MYSQL_PASSWORD, MYSQL_HOST, MYSQL_PORT


db = MySQLDatabase(MYSQL_NAME, user=MYSQL_USER, password=MYSQL_PASSWORD, host=MYSQL_HOST, port=MYSQL_PORT, charset='utf8mb4',
                   autoconnect=False)


def db_manager(function):
    async def wrapper(message):
        print(function.__name__)
        print(db.is_closed())
        if db.is_closed():
            db.connect()
        print(db.is_closed())
        await function(message)
        if not db.is_closed():
            db.close()
        print(db.is_closed())
        print('----------------')

    return wrapper


class BaseModel(Model):
    class Meta:
        database = db


class Admin(BaseModel):
    id = PrimaryKeyField()
    login = CharField(max_length=32)
    password = CharField(max_length=64)
    permission_orders = BooleanField(default=False)
    permission_requisites = BooleanField(default=False)

    class Meta:
        db_table = 'admins'


class MailingRate(BaseModel):
    id = PrimaryKeyField()
    datetime = DateTimeField()


class Currency(BaseModel):
    id = PrimaryKeyField()
    name = CharField(max_length=16)
    icon = CharField(max_length=4)

    class Meta:
        db_table = 'currencies'


class Direction(BaseModel):
    id = PrimaryKeyField()
    currency_exchangeable = ForeignKeyField(Currency, to_field='id', on_delete='cascade', null=True, default=None)
    currency_received = ForeignKeyField(Currency, to_field='id', on_delete='cascade', null=True, default=None)
    message_id = BigIntegerField(default=None, null=True)

    class Meta:
        db_table = 'directions'


class RequisiteExchangeable(BaseModel):
    id = PrimaryKeyField()
    direction = ForeignKeyField(Direction, to_field='id', on_delete='cascade')
    name = CharField(max_length=64)
    description = CharField(max_length=1024)

    class Meta:
        db_table = 'requisites_exchangeable'


class RequisiteReceived(BaseModel):
    id = PrimaryKeyField()
    currency = ForeignKeyField(Currency, to_field='id', on_delete='cascade', null=True, default=None)
    admin = ForeignKeyField(Admin, to_field='id', on_delete='cascade')
    name = CharField(max_length=64)
    requisite = CharField(max_length=1024)

    class Meta:
        db_table = 'requisites_received'


class Customer(BaseModel):
    id = PrimaryKeyField()
    user_id = BigIntegerField()
    username = CharField(max_length=64, null=True)
    name = CharField(max_length=128, null=True, default=None)
    referral = CharField(max_length=128, null=True, default=None)
    contact = CharField(max_length=128, null=True, default=None)
    city = CharField(max_length=128, null=True, default=None)
    datetime = DateTimeField()

    class Meta:
        db_table = 'customers'


class Rate(BaseModel):
    id = PrimaryKeyField()
    direction = ForeignKeyField(Direction, to_field='id', on_delete='cascade', null=True, default=None)
    currency_exchangeable_from = FloatField()
    currency_exchangeable_to = FloatField()
    rate = FloatField()
    datetime_update = DateTimeField(null=True, default=None)
    only_admin = BooleanField(default=False)

    class Meta:
        db_table = 'rates'


class Doc(BaseModel):
    id = PrimaryKeyField()
    extension = CharField(max_length=8)

    class Meta:
        db_table = 'docs'


class Order(BaseModel):
    id = PrimaryKeyField()
    customer = ForeignKeyField(Customer, to_field='id', on_delete='cascade')
    direction = ForeignKeyField(Direction, to_field='id', on_delete='cascade', null=True, default=None)
    currency_exchangeable_value = FloatField(null=True, default=None)
    currency_received_value = FloatField(null=True, default=None)
    rate = FloatField(default=0)
    requisite_exchangeable = ForeignKeyField(RequisiteExchangeable, to_field='id', on_delete='cascade',
                                             null=True, default=None)
    requisite_exchangeable_value = CharField(max_length=1024, null=True, default=None)
    requisite_received = ForeignKeyField(RequisiteReceived, to_field='id', on_delete='cascade',
                                         null=True, default=None)
    doc = ForeignKeyField(Doc, to_field='id', on_delete='cascade', null=True, default=None)
    is_paid = BooleanField(default=False)
    is_completed = BooleanField(default=False)
    commission_rub = CharField(max_length=64, null=True, default=None)
    received_usdt = CharField(max_length=64, null=True, default=None)
    datetime = DateTimeField()
    datetime_paid = DateTimeField(null=True, default=None)
    datetime_completed = DateTimeField(null=True, default=None)
    is_closed = BooleanField(default=False)

    class Meta:
        db_table = 'orders'


class AdminDoc(BaseModel):
    id = PrimaryKeyField()
    admin = ForeignKeyField(Admin, to_field='id', on_delete='cascade')
    order = ForeignKeyField(Order, to_field='id', on_delete='cascade')
    extension = CharField(max_length=8)

    class Meta:
        db_table = 'admins_docs'
