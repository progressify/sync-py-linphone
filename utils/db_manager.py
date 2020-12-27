import sqlite3
import sys
from os import path

from syncasync import AsyncToSync
from tortoise import Tortoise

from utils.contact import Contact
from utils.exceptions.database_exception import DatabaseException

LINPHONE_MACOS_DB_PATH = '~/Library/Application Support/linphone/friends.db'
LINPHONE_LINUX_DB_PATH_1 = '~/.var/app/com.belledonnecommunications.linphone/data/linphone/friends.db'  # flatpack?
LINPHONE_LINUX_DB_PATH_2 = '~/.local/linphone/friends.db'  # TODO verifica
LINPHONE_LINUX_DB_PATH_3 = '~/.config/linphone/friends.db'  # TODO verifica
LINPHONE_WINDOWS_DB_PATH = ''  # TODO


class DbManager:

    def __init__(self, db_path):
        self.with_tortoise = True
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

        if self.with_tortoise:
            self.create_tortoise_instance()
        else:
            self.connection = sqlite3.connect(self.db_filename)
            self.cursor = self.connection.cursor()

    @AsyncToSync
    async def create_tortoise_instance(self):
        await Tortoise.init(
            db_url=f'sqlite://{self.db_filename}',
            modules={'models': ['models.friends']}
        )
        await Tortoise.generate_schemas()

    @AsyncToSync
    async def insert_contact(self, a_contact: Contact):  # TODO
        if self.with_tortoise:
            friend = a_contact.friends_obj()
            await friend.save()
        else:
            sql = ("INSERT INTO friends"
                   "(friend_list_id, sip_uri, subscribe_policy, send_subscribe, ref_key, vCard, "
                   "vCard_etag, vCard_url, presence_received) "
                   "VALUES (1, ?, 1, 0, NULL, ?, NULL, NULL, 0)")
            self.cursor.execute(sql, (a_contact.sip_uri, a_contact.create_vcard()))
            self.connection.commit()

    @AsyncToSync
    async def close(self):
        if self.with_tortoise:
            await Tortoise.close_connections()
        else:
            self.cursor.close()
            self.connection.close()
