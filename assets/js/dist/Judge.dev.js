"use strict";

var textbox = document.querySelector(".chits_box"),
    Success = "",
    errorMessage = "",
    form = document.querySelector("form"),
    old_messages = [],
    result = [];
var reply_to_id,
    type = "send",
    url,
    inputField = document.querySelector('#sendTo'),
    sendButton = document.querySelector('.chit_send_button'),
    inputFieldDev = document.querySelector(".input_country"),
    csrf = document.querySelector(".csrf"),
    chit_div;

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
            var RatifyButton = document.createElement('button');
            var RejectButton = document.createElement('button');
            content.textContent = message.chit;
            header.textContent = "From: " + message.chit_from.name + " <" + message.chit_from.country_id + ">";

            if (message.reply_to_country) {
              var replyHeader = document.createElement('div');
              replyHeader.textContent = "Reply from " + message.chit_from.name + " to " + message.reply_to_country + "'s" + " message";
              wrapper.appendChild(replyHeader);
            }

            RatifyButton.textContent = "Ratify";
            RejectButton.textContent = "Reject";
            RatifyButton.addEventListener('click', function () {
              RatifyButton.disabled = true;
              RatifyButton.classList.add('clicked');
              fetch('/chits/judge/', {
                method: 'POST',
                body: JSON.stringify({
                  chit_id: message.id
                }),
                headers: {
                  'Content-Type': 'application/json',
                  'X-CSRFToken': csrf.value
                }
              }).then(function (response) {
                return response.json();
              }).then(function (data) {
                Success = data.message;
                chit_div = document.getElementById(message.id);
                chit_div.remove();
              })["catch"](function (error) {
                return errorMessage = error.message;
              });
              setTimeout(function () {
                RatifyButton.disabled = false;
                RatifyButton.classList.remove('clicked');
              }, 2000);
            });
            RejectButton.addEventListener('click', function () {
              RejectButton.disabled = true;
              RejectButton.classList.add('clicked');
              fetch('/chits/judge/reject/', {
                method: 'POST',
                body: JSON.stringify({
                  chit_id: message.id
                }),
                headers: {
                  'Content-Type': 'application/json',
                  'X-CSRFToken': csrf.value
                }
              }).then(function (response) {
                return response.json();
              }).then(function (data) {
                Success = data.message;
                chit_div = document.getElementById(message.id);
                chit_div.remove();
              })["catch"](function (error) {
                return errorMessage = error.message;
              });
              setTimeout(function () {
                RejectButton.disabled = false;
                RejectButton.classList.remove('clicked');
              }, 2000);
            });
            button_wrapper.appendChild(RejectButton);
            button_wrapper.appendChild(RatifyButton);
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

setInterval(SetMessages, 10000);