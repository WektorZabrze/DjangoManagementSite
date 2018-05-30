$(function () {
    // provide the secured transmission whenever it's possible
    var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
    var ws_path = ws_scheme + '://' + window.location.host + "/chat/stream/";
    console.log("Connecting to " + ws_path);
    var socket = new ReconnectingWebSocket(ws_path);

    //closses connection send message about it and redirect to the chat list
    function leaveRoom()
    {
                // Leave room
                $(this).removeClass("joined");
                socket.send(JSON.stringify({
                    "command": "leave",  // determines which handler will be used (see chat/routing.py)
                    "room": room_id
                    }));
    }

    //Socket connection estabilished
    socket.onopen = function () {
        console.log("Connected to the chat socket");

        $(this).addClass("joined");

        //it has to wait until the end of estabilishing socket connection
         socket.send(JSON.stringify({
            "command": "join",
            "room": room_id
        }));
    };

    socket.onclose = function () {
        console.log("Disconnected from the chat socket");
    };

    socket.onmessage = function (message) {
    // Decode the JSON
    console.log("Got websocket message " + message.data);
    var data = JSON.parse(message.data);
    // Handle errors
        if (data.error) {
            alert(data.error);
            return;
        }
        // Handle joining
        if (data.join) {
            //it has to be made here to ensure that connection is estabilished
            //it sets action which is resposnsible for sending message on button click
            $("#btn-chat").on("click", function(){
                const message = $("#message").val();
                $("#message").val(""); //clear text input

                socket.send(JSON.stringify({
                    "command": "send", //uses send handler
                    "room": data.join, //it stores the room id
                    "message": message
                }));
            });

            //enter button sends the message
            var message_input = document.getElementById("message");
            message_input.addEventListener("keyup", function(event){
                event.preventDefault();

                if(event.keyCode === 13)
                    $("#btn-chat").click();
            });

             //action for the button responsible for leaving the room
            $("button.btn.btn-info").click(function () {
                //redirect back to the chat list
                window.location.href = "/chat/";
            });

            //disconnecting after closing window or reloading page
            window.onbeforeunload = function(){
                leaveRoom();
            }

            // Handle leaving
        } else if (data.leave) {
            console.log("Leaving room " + data.leave);
        } else if (data.message || data.msg_type != 0) {
            var msg_div = $(".chat");

            var msg_content = ""

            switch (data.msg_type) {
            case 0://normal message
                if (username == data.username)
                    msg_content =  "<li class='right clearfix'><div class='chat-body clearfix'><p><span class='username'>" +
                                    data.username + ": </span><span class='body'>" + data.message + "</span> </p></div></li>";
                else
                    msg_content =  "<li class='left clearfix'><div class='chat-body clearfix'><p><span class='username'>" +
                                    data.username + ": </span><span class='body'>" + data.message + "</span> </p></div></li>";
                break;
            case 1://user join
                    msg_content = "<li class='right clearfix'><div class='chat-body clearfix'><p class='leave-join'><span class='username'>" +
                                    data.username + " </span><span class='body'>joins the room!</span> </p></div></li>";
                break;
            case 2://user left
                msg_content = "<li class='right clearfix'><div class='chat-body clearfix'><p class='leave-join'><span class='username'>" +
                                    data.username + " </span><span class='body'>left the room!</span> </p></div></li>";
                break;
             }
            msg_div.append(msg_content);

            var chat_div = $('div.panel-body.body-panel');
            //it;s responsible for automatic scrolling down
            chat_div.scrollTop(chat_div[0].scrollHeight);
        }
        else {
            console.log("Cannot handle message!");
        }
    }

});