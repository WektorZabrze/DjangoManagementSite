from django.db import models
from django.utils.six import python_2_unicode_compatible
from channels import Group
import json


@python_2_unicode_compatible
class ChatRoom(models.Model):
    room_name = models.CharField(max_length=255)
    #add room for seletected users

    #it's responsible for identyfing the current room
    @property
    def websocket_group(self):
        return Group("room-%s" % self.id)

    #ADD TYPES OF MESSAGES
    def send_message(self, message, user):
        '''it sends a message from the user'''
        message_json = {"room": str(self.id), "message": message, "username": user.username}
        self.websocket_group.send(
            {"text": json.dumps(message_json)}
        )

    def __str__(self):
        return self.room_name