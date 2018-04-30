from channels import route

#Faplo 30.04
#responsible for handling messages - for now it prints message in the console
def message_handler(message):
    print(message['text'])

channel_routing = [
    route("websocket.receive", message_handler) #temporary message handler is registred
]