import codecs
from datetime import datetime

import bq_easy_zfullio as big_query
import pandas as pd
import xmltodict
from loguru import logger

from .ftp import FTP
from .sftp import SFTP


class Repository:

    def __init__(self, host: str, port: int, user: str, password: str, path: str, filename: str):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.path = path
        self.filename = filename
        self.df = pd.DataFrame()

    def push(self, bq_table: str, schema, start_date: str | datetime, finish_date: str | datetime, bq_token: str,
             bq_project: str, is_append: bool = False) -> None:
        if len(self.df) > 0:
            try:
                client = big_query.Client(bq_token, bq_project)
                logger.info(f"Обновление {bq_project}//{bq_table}")
                if not is_append:
                    logger.info("Режим: Перезапись")
                    client.delete_row(bq_table, "date", start_date, finish_date)
                else:
                    logger.info("Режим: Добавление")
                client.upload_table(self.df, bq_table, schema)
                logger.success(f"{bq_project}//{bq_table}: Данные успешно записаны")
            except Exception as err:
                logger.exception(err)
        else:
            logger.warning("Отсутствуют данные")


class FromSFTP(Repository):

    def __init__(self, host: str, port: int, user: str, password: str, path: str, filename: str):
        super().__init__(host, port, user, password, path, filename)
        self.repository = SFTP(self.host, self.user, self.password, port=self.port)

    def get(self) -> None:
        self.repository.connect()
        self.repository.get_file(self.path, self.filename)
        if self.filename.endswith(".xlsx"):
            self.df = pd.read_excel(f"data/{self.filename}", converters={"UA_Client_Id": str})
        else:
            logger.warning(f"Я не умею работать с типом файла: {self.filename}")

    def check_date_update(self) -> bool:
        self.repository.connect()
        files = self.repository.list(self.path)
        if not files:
            return False
        for file in files:
            if file.filename == self.filename:
                date = datetime.fromtimestamp(file.st_mtime)
                today = datetime.now()
                if date.month == today.month and date.day == today.day:
                    return True
        return False


class FromFTP(Repository):

    def __init__(self, host: str, port: int, user: str, password: str, path: str, filename: str):
        super().__init__(host, port, user, password, path, filename)
        self.repository = FTP(self.host, self.user, self.password, port=self.port)

    def check_file(self) -> str | None:
        today = datetime.now()
        self.repository.connect()
        files = self.repository.ls()
        f = next((file for file in files if self.filename in file), None)
        if not f:
            return None
        modified_time = datetime.strptime(self.repository.connection.sendcmd('MDTM ' + f)[4:], "%Y%m%d%H%M%S")
        return f if modified_time.day == today.day else None


def convert_xml(file: str) -> pd.DataFrame:
    raw_data = codecs.open(file, "utf_8_sig").read()
    dict_data = xmltodict.parse(raw_data, dict_constructor=dict)['CRM_Bitrix']['header']['Event']

    prepared_data = []
    for i in dict_data:
        k = {j[1:]: i[j] for j in i.keys()}
        prepared_data.append(k)
    return pd.DataFrame(prepared_data)
