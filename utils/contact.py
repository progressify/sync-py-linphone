
NAME_FIELD = 'Name'
PHONE_VALUE = 'Phone {number} - Value'


class Contact:
    def __init__(self, row):
        self.name = row[NAME_FIELD]
        print(self.name)
        self.phones = []
        for i in range(1, 6):
            self.phones.append(row[PHONE_VALUE.format(number=i)].replace(' ', ''))
        print(f'{row}\n\n')
