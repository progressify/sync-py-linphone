import csv
from tqdm import tqdm
from os import path

from utils.contact import Contact
from utils.exceptions.csv_exception import CsvException


class CsvManager:
    def __init__(self, csv_path: str):
        if not path.exists(csv_path):
            raise CsvException("Please specify the path where I can read your contacts.\nBye.\n\n")
        if not path.isfile(csv_path):
            if not path.exists(path.join(csv_path, "contacts.csv")):
                raise CsvException("Please specify the path where I can read your contacts.\nBye.\n\n")
        self.csv_path = csv_path
        self.array_contacts = []

    def parse(self):
        with open(self.csv_path, newline='') as csv_file:
            contacts_reader = csv.DictReader(csv_file, delimiter=',', )
            for row in tqdm(contacts_reader):
                self.array_contacts.append(Contact(row))
