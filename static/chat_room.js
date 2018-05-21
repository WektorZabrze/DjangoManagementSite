$(function () {
    // provide the secured transmission whenever it's possible
    var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
    var ws_path = ws_scheme + '://' + window.location.host + "/chat/stream/";
    console.log("Connecting to " + ws_path);
    var socket = new ReconnectingWebSocket(ws_path);

    //For debugging purposes
    socket.onopen = function () {
        console.log("Connected to the chat socket");

        //it has to wait until the end of estabilishing socket connection
         socket.send(JSON.stringify({
            "command": "join",
            "room": room_id
        }));
    };

    socket.onclose = function () {
        console.log("Disconnected from the chat socket");
    };

    console.log( "To jest id pokoju" +  room_id )



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
            console.log("Joining room " + data.join);
            var roomdiv = $(
                "<div class='room' id='room-" + data.join + "'>" +
                "<h2>" + data.title + "</h2>" +
                "<div class='messages'></div>" +
                "<input><button>Send</button>" +
                "</div>"
            );
            $("#chats").append(roomdiv);
            roomdiv.find("button").on("click", function(){
                socket.send(JSON.stringify({
                    "command": "send", //uses send handler
                    "room": data.join, //it stores the room id
                    "message": roomdiv.find("input").val()
                }));
            });

            //NEW FRONTEND

            $("#btn-chat").on("click", function(){
                const message = $("#message").val();
                $("#message").val(""); //clear text input

                socket.send(JSON.stringify({
                    "command": "send", //uses send handler
                    "room": data.join, //it stores the room id
                    "message": message
                }));
            });

            // Handle leaving
        } else if (data.leave) {
            //IT SHOULD BE SOMEHOW MODIFIED
            console.log("Leaving room " + data.leave);
            $("#room-" + data.leave).remove();
        } else if (data.message) { //in future it may also handle different types of messages!
            var msg_div = $(".chat");

            if (username == data.username)
            {
                var msg_content =  "<li class='right clearfix'><div class='chat-body clearfix'><p><span class='username'>" +
                                    data.username + ": </span><span class='body'>" + data.message + "</span> </p></div></li>";
            }
            else
            {
                var msg_content =  "<li class='left clearfix'><div class='chat-body clearfix'><p><span class='username'>" +
                                    data.username + ": </span><span class='body'>" + data.message + "</span> </p></div></li>";
            }

            msg_div.append(msg_content);
            msg_div.scrollTop(msg_div.prop("scrollHeight"));
        }
        else {
            console.log("Cannot handle message!");
        }
    }

    // checks whether user joined a room
    //if it doesn't found a room with our id within div id="chats"
    //then the length of text equals 0
    /*
    inRoom = function(roomId){
           return $("#room-" + roomId).length > 0;
    };

    $("li.room-link").click(function () {
        console.log("Clicked");
        roomId = $(this).attr("data-room-id");
        if (inRoom(roomId)) {
            console.log("Leaving room");
            // Leave room
            $(this).removeClass("joined");
            socket.send(JSON.stringify({
                "command": "leave",  // determines which handler will be used (see chat/routing.py)
                "room": roomId
            }));
        } else {
            // Join room
            //window.open('/templates/chat/chat_popup.html', 'dummyname', 'height=undefined,width=undefined', false);            $(this).addClass("joined");
            socket.send(JSON.stringify({
                "command": "join",
                "room": roomId
            }));
        }
});*/

});