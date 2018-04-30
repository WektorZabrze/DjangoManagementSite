from django.contrib import admin
from .models import ChatRoom

admin.site.register(
    ChatRoom,
    list_display=["id", "room_name"],
    list_display_links=["id", "room_name"],
)