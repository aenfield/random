var twilio = require("twilio");
var Tessel = require("tessel-io");
var five = require("johnny-five");
var board = new five.Board({
  io: new Tessel()
});

var accountSid = "AC019517cf46788835413f7d064dd0566e"; // SID copied from www.twilio.com/console
var authToken = "26d2000d9894a92eb4456e1073a67f7d"; // token copied from www.twilio.com/console

var sender = "206-516-6175"; // This is your Twilio phone number
var recipient = "206-306-3904"; // This is your own mobile phone number

var client = new twilio.RestClient(accountSid, authToken);

board.on("ready", () => {
  var door = new five.Switch({
    pin: "a2",
    invert: true,
  });

  door.on("open", () => {
    var details = {
      body: `Willie says hi at ${Date.now()}`,
      from: sender,
      to: recipient,
    };

    client.messages.create(details, error => {
      if (error) {
        console.error(error.message);
      }
      // Success! Nothing else to do
    });
  });
});