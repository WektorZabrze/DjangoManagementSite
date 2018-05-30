from django.conf import settings

MSG_TYPE_MESSAGE = 0  # For standard messages
MSG_TYPE_ENTER = 1  # For just OK information that doesn't bother users
MSG_TYPE_LEAVE = 2 # For just OK information that doesn't bother users

MESSAGE_TYPES_CHOICES = getattr(settings, 'MESSAGE_TYPES_CHOICES', (
    (MSG_TYPE_MESSAGE, 'MESSAGE'),
    (MSG_TYPE_ENTER, 'ENTER'),
    (MSG_TYPE_LEAVE, 'LEAVE')))

MESSAGE_TYPES_LIST = getattr(settings, 'MESSAGE_TYPES_LIST',
                             [MSG_TYPE_MESSAGE,
                              MSG_TYPE_ENTER,
                              MSG_TYPE_LEAVE])