import sys

import click
from tqdm import tqdm

from utils.csv_manager import CsvManager
from utils.db_manager import DbManager
from utils.exceptions.csv_exception import CsvException
from utils.exceptions.database_exception import DatabaseException


# TODO init


@click.command()
@click.option("--csvpath", default='./contacts.csv', help="Google Contacts CSV path.")
@click.option("--dbpath", default=None, help="friends.db path of your Linphone installation.")
def sync(csvpath: str, dbpath: str):
    print("Welcome to Sync Py Linphone (Syncronize my Linphone)\n")

    try:
        csv_manager = CsvManager(csvpath)
        db_manager = DbManager(dbpath)
    except DatabaseException as e:
        print(e.message)
        sys.exit(e.exit_code)
    except CsvException as e:
        print(e.message)
        sys.exit(e.exit_code)
    except Exception as e:
        print(e)
        sys.exit(-1)

    print("Reading contacts from csv:")
    csv_manager.parse()
    if csv_manager.array_contacts:
        print(f'\n-> {len(csv_manager.array_contacts)} contacts parsed!')
        print("\nSyncing..")
        for a_contact in tqdm(csv_manager.array_contacts):  # TODO syncing login
            db_manager.insert_contact(a_contact)
    db_manager.close()


if __name__ == '__main__':
    sync()
