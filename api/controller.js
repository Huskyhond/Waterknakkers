var XboxController = require('xbox-controller')
var xbox = new XboxController
var xLeft = 0, xRight = 0, motorSpeed = 0;

xbox.on('lefttrigger', function(position){
  console.log('lefttrigger', position);
  var normalisedTrigger = Math.min(position/255, 1)
  normalisedTrigger = Math.max(normalisedTrigger, -1)
  motorSpeed = -normalisedTrigger
  module.exports.change(xLeft, xRight, motorSpeed)
});

xbox.on('righttrigger', function(position){
  console.log('righttrigger', position);
  var normalisedTrigger = Math.min(position/255, 1)
  normalisedTrigger = Math.max(normalisedTrigger, -1)
  motorSpeed = normalisedTrigger
  module.exports.change(xLeft, xRight, motorSpeed)
});

xbox.on('left:move', function(position){
  var normalisedPosX = position.x/31000
  if(position.x == 32767)
    normalisedPosX = 1
  normalisedPosX = Math.min(normalisedPosX, 1)
  normalisedPosX = Math.max(normalisedPosX, -1)
  xLeft = normalisedPosX
  module.exports.change(xLeft, xRight, motorSpeed)
});

xbox.on('right:move', function(position){
  var normalisedPosX = position.x/31000
  if(position.x == 32767)
    normalisedPosX = 1
  normalisedPosX = Math.min(normalisedPosX, 1)
  normalisedPosX = Math.max(normalisedPosX, -1)
  xRight = normalisedPosX
  module.exports.change(xLeft, xRight, motorSpeed)
});

module.exports = {
    change: function() {}
}