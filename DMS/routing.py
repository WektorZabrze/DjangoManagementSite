from channels import include

#Faplo 30.04
#responsible for handling messages - for now it prints message in the console
def message_handler(message):
    print(message['text'])

channel_routing = [
    include("chat.routing.websocket_routing", path=r"^/chat/stream"),
    include("chat.routing.custom_routing"),
    #route("websocket.receive", message_handler) #temporary message handler is registred
]