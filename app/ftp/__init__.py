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


from ftplib import FTP

from app.models import Doc
from config import FTP_HOST, FTP_USER, FTP_PASSWORD, DOCS_PATH, FTP_PATH


ftp = FTP()


def ftp_upload(doc: Doc):
    ftp.connect(FTP_HOST)
    ftp.login(user=FTP_USER, passwd=FTP_PASSWORD)

    local_doc_path = '{}/{}.{}'.format(DOCS_PATH, doc.id, doc.extension)
    ftp_doc_path = '{}/{}.{}'.format(FTP_PATH, doc.id, doc.extension)
    with open(local_doc_path, 'rb') as file:
        ftp.storbinary('STOR ' + ftp_doc_path, file, 1024)
    ftp.quit()
