var five = require("johnny-five");
var Tessel = require("tessel-io");

var board = new five.Board({
  io: new Tessel()
});

board.on("ready", function() {
  // 1
  var leds = new five.Leds(["a2", "a3", "a4", "a5", "a6", "a7"]);
  // 2
  leds.blink(500);
});