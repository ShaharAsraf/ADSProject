let username = null;
let openChats = {}

function get_JSON(yourUrl){
    var Httpreq = new XMLHttpRequest(); // a new request
    Httpreq.open("GET",yourUrl,false);
    Httpreq.send(null);
    return Httpreq.responseText;
}

function displayChat() {
    document.getElementById("chat-list-window").style.display = "block";
    document.getElementById("chat-list-button").style.display = "none";
}

function hideChat() {
    document.getElementById("chat-list-window").style.display = "none";
    document.getElementById("chat-list-button").style.display = "block";
}

function findPersonOnList() {
    var text = $("#search-input").val();

}

window.onload = function () {
    username = JSON.parse(document.getElementById('username').textContent);
}

window.onclose = function () {
    for (var id in openChats) {
        send("LEAVE", "", id);
    }
}

function send(command, content, chatID) {
    if (chatID in openChats) {
        let chatSocket = openChats[chatID];
        chatSocket.send(JSON.stringify({
            "type": command,
            "chat_id": chatID,
            "message": content
        }));
    }
}


function openChat(chatID, user) {
    if (!(chatID in openChats)) {
        let chatSocket = new WebSocket(
            "ws://"
            + window.location.host
            + '/ws/chat/'
            + chatID
            + '/'
        );
        chatSocket.onopen = function () {
            send("JOIN", "", chatID)
        }
        chatSocket.onmessage = function (mes) {
            addMessage(JSON.parse(mes.data), chatID)
        }
        openChats[chatID] = chatSocket;
        showNewChatPopup(chatID, user);


        var json_obj = JSON.parse(get_JSON('/chat/messages/' + chatID));
        for (var i = 0; i < json_obj.messages.length; i++) {
            addMessage(json_obj.messages[i], chatID);
        }
    }
}

function showNewChatPopup(chatID, user) {
    if (Object.keys(openChats).length >= 3) {
        closeChat(Object.keys(openChats)[2]);
    }
    var chatPopup = '<div id="' + chatID + '" class="chat-popup">' +
        '            <div class="chat-popup-header">' +
        '                <div class="chat-popup-header-name">' + user + '</div>' +
        '                <div class="chat-popup-header-close">x</div>' +
        '            </div>' +
        '            <div class="chat-popup-body ">' +
        '                <ul class="messages justify-content">' +
        '                </ul>' +
        '            </div>' +
        '            <div class="chat-popup-input">' +
        '                <textarea id="IN' + chatID + '" type="text" placeholder="Message..."></textarea>' +
        '                <button>Send</button>' +
        '            </div>' +
        '        </div>'
    chatPopup = $(chatPopup);
    chatPopup.find("button").click(function () {
        let element = $("#IN" + chatID);
        let text = element.val();
        if (text !== "") {
            send("MESSAGE", text, chatID);
        }
        element.val("");
    });
    chatPopup.find(".chat-popup-header-close").click(function () {
        closeChat(chatID);
    });
    chatPopup.find(".chat-popup-header").click(function () {
        minimize(chatID);
    })
    $("#popup-chat-list").append(chatPopup);
}

function addMessage(message, chatID) {
    let control = null;
    if (message.username === username) {
        control = '<li class="message-right float-right">' +
            message.message +
            '     </li>'
    } else {
        control = '<li class="message-left float-left">' +
            message.message +
            '     </li>'
    }

    $("#" + chatID + " ul").append($(control));
}

function closeChat(chatID) {
    if (chatID in openChats) {
        send("LEAVE", "", chatID);
        $("#" + chatID).remove();
        delete openChats[chatID];
    }
}

function minimize(chatID) {
    if (chatID in openChats) {
        let element = $("#" + chatID);
        if (element.find(".chat-popup-body").is(":visible")) {
            element.find(".chat-popup-body").hide();
            element.find(".chat-popup-input").hide();
        } else {
            element.find(".chat-popup-body").show();
            element.find(".chat-popup-input").show();
        }
    }
}
