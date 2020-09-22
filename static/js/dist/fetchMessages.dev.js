"use strict";

var new_messages = [];

var Messages = function Messages(url) {
  var response, json;
  return regeneratorRuntime.async(function Messages$(_context) {
    while (1) {
      switch (_context.prev = _context.next) {
        case 0:
          _context.next = 2;
          return regeneratorRuntime.awrap(fetch("/chits/api/messages/".concat(url), {
            method: 'GET',
            mode: 'cors',
            cache: 'no-cache',
            headers: {
              'Content-Type': 'application/json'
            }
          }));

        case 2:
          response = _context.sent;
          _context.next = 5;
          return regeneratorRuntime.awrap(response.json());

        case 5:
          json = _context.sent;

          if (json.detail && json.detail == "Authentication credentials were not provided.") {
            window.location = "/accounts/login";
          } else {
            new_messages = json;
          }

          return _context.abrupt("return", new_messages);

        case 8:
        case "end":
          return _context.stop();
      }
    }
  });
};