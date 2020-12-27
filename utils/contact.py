import vobject

from models.friends import Friends

NAME_FIELD = 'Name'
PHONE_VALUE = 'Phone {number} - Value'


class Contact:
    sip = 'sip.messagenet.it'  # TODO metti in un file di configurazione

    def __init__(self, row):
        self.name = row[NAME_FIELD]
        self.phones = []
        for i in range(1, 6):
            if row[PHONE_VALUE.format(number=i)]:
                self.phones.append(row[PHONE_VALUE.format(number=i)].replace(' ', ''))
        self.sip_uri = ''
        if len(self.phones) > 0:
            self.sip_uri = f'sip:{self.phones[0]}@{self.sip}'

    def create_vcard(self):
        person = {
            'VERSION': '4.0',
            'FN': self.name,
            'ROLE': self.name
        }

        vcard = vobject.readOne('\n'.join([f'{k}:{person[k]}' for k in person.keys()]))
        vcard.name = 'VCARD'
        for num in self.phones:
            impp = vcard.add('IMPP')
            impp.value = f'sip:{num}@{self.sip}'

        vcard.useBegin = True
        return vcard.serialize()

    def friends_obj(self):
        return Friends(sip_uri=self.sip_uri, vCard=self.create_vcard())
