var five = require("johnny-five");
var Tessel = require("tessel-io");

var board = new five.Board({
  io: new Tessel()
});

board.on("ready", () => {
  var led = new five.Led("a5");
  led.blink(500);
});