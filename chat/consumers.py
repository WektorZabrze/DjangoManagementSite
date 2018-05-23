from channels.auth import channel_session_user_from_http, channel_session_user
from channels import Channel
import json
from .exceptions import ClientError
from .models import ChatRoom
from .utils import catch_client_error, get_room_or_error

from .message_type import MSG_TYPE_LEAVE, MSG_TYPE_ENTER


#Faplllosss 04.05.18
@channel_session_user_from_http
def ws_connect(message):
    message.reply_channel.send({"accept": True})
    message.channel_session["rooms"] = []

@channel_session_user
def ws_disconnect(message):
    # Unsubscribe from any connected rooms
    for room_id in message.channel_session.get("rooms", set()):
        try:
            room = ChatRoom.objects.get(pk=room_id)
            # Removes us from the room's send group. If this doesn't get run,
            # we'll get removed once our first reply message expires.
            room.websocket_group.discard(message.reply_channel)
        except ChatRoom.DoesNotExist:
            pass

def ws_receive(message):
    #some text encoding
    payload = json.loads(message["text"])
    payload['reply_channel'] = message.content['reply_channel']
    Channel("chat.receive").send(payload)

@channel_session_user
@catch_client_error
def chat_join(message):
    room = get_room_or_error(message["room"], message.user)

    #it sends message without content with information about joining the room
    room.send_message(None, message.user, MSG_TYPE_ENTER)

    room.websocket_group.add(message.reply_channel)
    #appends current room to the sessions list
    message.channel_session["rooms"] = list(set(message.channel_session['rooms']).union([room.id]))

    message.reply_channel.send({
        "text": json.dumps({
            "join": str(room.id),
            "title": room.room_name,
        }),
    })

@channel_session_user
@catch_client_error
def chat_leave(message):
    room = get_room_or_error(message["room"], message.user)

    #send message about leaving room
    room.send_message(None, message.user, MSG_TYPE_LEAVE)

    room.websocket_group.discard(message.reply_channel)
    #removes current room from the sessions list
    message.channel_session["rooms"] = list(set(message.channel_session['rooms']).difference([room.id]))



    message.reply_channel.send({
        "text": json.dumps({
            "leave": str(room.id),
        }),
    })

@channel_session_user
@catch_client_error
def chat_send(message):
    #user is not allowed to communicate within this room
    if int(message["room"]) not in message.channel_session["rooms"]:
        raise ClientError("ROOM_ACCESS_DENIED")
    room = get_room_or_error(message["room"], message.user)
    room.send_message(message["message"], message.user)