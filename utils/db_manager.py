import sqlite3
import sys
from os import path

from utils.contact import Contact
from utils.exceptions.database_exception import DatabaseException

LINPHONE_MACOS_DB_PATH = '~/Library/Application Support/linphone/friends.db'
LINPHONE_LINUX_DB_PATH_1 = '~/.var/app/com.belledonnecommunications.linphone/data/linphone/friends.db'  # flatpack?
LINPHONE_LINUX_DB_PATH_2 = '~/.local/linphone/friends.db'  # TODO verifica
LINPHONE_LINUX_DB_PATH_3 = '~/.config/linphone/friends.db'  # TODO verifica
LINPHONE_WINDOWS_DB_PATH = ''  # TODO


class DbManager:

    def __init__(self, db_path):
        if db_path:
            self.db_filename = db_path
        elif sys.platform == "linux" or sys.platform == "linux2":
            if path.exists(LINPHONE_LINUX_DB_PATH_1):
                self.db_filename = LINPHONE_LINUX_DB_PATH_1
            elif path.exists(LINPHONE_LINUX_DB_PATH_2):
                self.db_filename = LINPHONE_LINUX_DB_PATH_2
            elif path.exists(LINPHONE_LINUX_DB_PATH_3):
                self.db_filename = LINPHONE_LINUX_DB_PATH_3
        elif sys.platform == "darwin":
            self.db_filename = LINPHONE_MACOS_DB_PATH
        elif sys.platform == "win32":
            self.db_filename = LINPHONE_WINDOWS_DB_PATH

        self.db_filename = path.expanduser(self.db_filename)
        if not path.exists(self.db_filename):
            raise DatabaseException()

        self.connection = sqlite3.connect(self.db_filename)
        self.cursor = self.connection.cursor()

    def insert_contact(self, a_contact: Contact):  # TODO
        sql = ("INSERT INTO compito (dettagli, priorita)"
               "                 VALUES (:nome1, :nome2)"
               "              ")
        self.cursor.execute(sql, {'nome1': 'status', 'nome2': 'id'})
