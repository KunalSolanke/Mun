"use strict";

var textbox = document.querySelector(".chits_box"),
    Success = "",
    errorMessage = "",
    form = document.querySelector("form"),
    old_messages = [],
    result = [],
    text;
var reply_to_id,
    type = "send",
    url,
    inputField = document.querySelector('#sendTo'),
    sendButton = document.querySelector('.chit_send_button'),
    inputFieldDev = document.querySelector(".input_country");
text = document.querySelector(".message textarea");

var SetMessages = function SetMessages() {
  return regeneratorRuntime.async(function SetMessages$(_context) {
    while (1) {
      switch (_context.prev = _context.next) {
        case 0:
          _context.next = 2;
          return regeneratorRuntime.awrap(Messages());

        case 2:
          new_messages = _context.sent;
          result = new_messages.filter(function (message) {
            return !old_messages.some(function (message2) {
              return message.id === message2.id;
            });
          });
          result.forEach(function (message) {
            var wrapper = document.createElement('div');
            wrapper.classList.add("single_chit");
            var header = document.createElement('div');
            header.classList.add("from");
            var content = document.createElement('div');
            content.classList.add("content");
            var button_wrapper = document.createElement('div');
            button_wrapper.classList.add('reply_button');
            var replyButton = document.createElement('button');
            var replyHeader = document.createElement('div');
            replyHeader.classList.add('reply');
            content.textContent = message.chit;
            header.textContent = "From: " + message.chit_from.name + " <" + message.chit_from.country_id + ">";

            if (message.reply_to_country) {
              replyHeader.textContent = "Reply from " + message.chit_from.name + " to " + message.reply_to_country + "'s " + " message";
              wrapper.appendChild(replyHeader);
            }

            replyButton.textContent = "Reply";
            replyButton.addEventListener('click', function () {
              replyButton.classList.add('clicked');
              inputFieldDev.classList.add('clicked');
              inputField.classList.add('clicked');
              inputField.value = message.chit_from.country_id;
              type = "reply";
              reply_to_id = message.id;
              setTimeout(function () {
                replyButton.classList.remove('clicked');
                inputFieldDev.classList.remove('clicked');
                inputField.classList.remove('clicked');
              }, 500);
            });
            button_wrapper.appendChild(replyButton);
            wrapper.appendChild(header);
            wrapper.appendChild(content);
            wrapper.setAttribute("id", "".concat(message.id));
            wrapper.appendChild(button_wrapper);
            textbox.appendChild(wrapper);
          });
          old_messages = new_messages;

        case 6:
        case "end":
          return _context.stop();
      }
    }
  });
};

form.addEventListener('submit', function (e) {
  e.preventDefault();
  sendButton.disabled = true;
  var formData = new FormData(form);
  sendButton.classList.add('clicked');

  if (type == "send") {
    url = '/chits/deligate';
    send_data = JSON.stringify({
      "chit_to": formData.getAll("country_name")[0],
      "content": formData.getAll("chit")[0]
    });
  } else {
    url = '/chits/deligate/reply';
    send_data = JSON.stringify({
      "chit_to": formData.getAll("country_name")[0],
      "content": formData.getAll("chit")[0],
      "reply_to": reply_to_id
    });
  }

  fetch(url, {
    method: 'POST',
    body: send_data,
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': formData.getAll('csrfmiddlewaretoken')
    }
  }).then(function (response) {
    return response.json();
  }).then(function (data) {
    Success = data.message;
    type = "send";
  })["catch"](function (error) {
    return errorMessage = error.message;
  });
  setTimeout(function () {
    sendButton.disabled = false;
    text.disabled = false;
    sendButton.classList.remove('clicked');
    console.log(text);
    text.value = "";
  }, 1000);
});
setInterval(SetMessages, 5000);