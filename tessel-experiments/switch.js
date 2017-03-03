var Tessel = require("tessel-io");
var five = require("johnny-five");

var board = new five.Board({
  io: new Tessel()
});

board.on("ready", function() {
  var led = new five.Led("b5");
  var spdt = new five.Switch("a5");
  spdt.on("close", () => led.on());
  spdt.on("open", () => led.off());
});