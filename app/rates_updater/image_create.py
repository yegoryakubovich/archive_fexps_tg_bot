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


from datetime import datetime, timezone

from PIL import Image, ImageDraw, ImageFont

from config import PATH_RATES_UPDATER


def image_create(filename: str, text: str):
    image = Image.open('{path}/images_source/{filename}.png'.format(path=PATH_RATES_UPDATER, filename=filename))
    draw_text = ImageDraw.Draw(image)
    draw_text.text(
        (228, 377),
        font=ImageFont.truetype('{}/fonts/Montserrat-Medium.ttf'.format(PATH_RATES_UPDATER), size=70),
        text=text,
        fill='#333'
    )
    draw_text.text(
        (1409, 62),
        font=ImageFont.truetype('{}/fonts/Montserrat-Regular.ttf'.format(PATH_RATES_UPDATER), size=24),
        text='{}'.format(datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')),
        fill='#333',
    )
    image.save('{path}/images/{filename}.png'.format(path=PATH_RATES_UPDATER, filename=filename))
