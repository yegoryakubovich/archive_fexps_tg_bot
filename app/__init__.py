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


from os import mkdir
from os.path import exists

from app.models import create_tables
from app.rates_updater import rates_updater_create
from app.telegram import start_bot
from config import PATH_DOCS


def create_app():
    create_tables()
    mkdir(PATH_DOCS) if not exists(PATH_DOCS) else None
    rates_updater_create()
    start_bot()
