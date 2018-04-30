from django.db import models
from django.utils.six import python_2_unicode_compatible


@python_2_unicode_compatible
class ChatRoom(models.Model):
    room_name = models.CharField(max_length=255)

    def __str__(self):
        return self.room_name