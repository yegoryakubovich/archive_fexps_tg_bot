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


from peewee import MySQLDatabase, Model, PrimaryKeyField, CharField, BigIntegerField, DateTimeField

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
    patronymic = CharField(max_length=128, null=True, default=None)
    datetime = DateTimeField()

    class Meta:
        db_table = "customers"
