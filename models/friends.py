from tortoise.models import Model
from tortoise import fields


class Friends(Model):
    friend_list_id = fields.IntField(default=1)
    sip_uri = fields.TextField()
    subscribe_policy = fields.IntField(default=1)
    send_subscribe = fields.IntField(default=0)
    ref_key = fields.TextField(default=None)
    vCard = fields.TextField(default='')
    vCard_etag = fields.TextField(default=None)
    vCard_url = fields.TextField(default=None)
    presence_received = fields.IntField(default=0)

    def __str__(self):
        return self.sip_uri
