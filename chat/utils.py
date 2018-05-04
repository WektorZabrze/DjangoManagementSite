from functools import wraps

from .exceptions import ClientError
from .models import ChatRoom

def catch_client_error(func):
    '''It catches the ClientError and translates it to the reply'''
    @wraps(func)
    def check_errors(message, *args, **kwargs):
        try:
            return func(message, *args, **kwargs)
        except ClientError as e:
            e.send_to(message.reply_channel)#send the error back to the client
    return check_errors

#Faplo 04.05.18
def get_room_or_error(room_id, user):
    '''checks whether user is authorized to get into the room'''
    if not user.is_authenticated:
        raise ClientError("USER_HAS_TO_LOGIN")
    try:
        room = ChatRoom.objects.get(pk=room_id)
    except ChatRoom.DoesNotExist:
        raise ClientError("INVALID_ROOM")
    #add options for checking permsions

    return room