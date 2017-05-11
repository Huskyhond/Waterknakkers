var app = require('express')()
var server = require('http').Server(app)
var io = require('socket.io')(server)

var controller = require('./controller')

server.listen(80)

controller.change = function(xLeft, xRight, motorSpeed) {
    var leftEngine = (xLeft == 0 ? motorSpeed : xLeft * motorSpeed)
    var rightEngine = (xLeft == 0 ? motorSpeed : -xLeft * motorSpeed)

    io.sockets.emit('message', {
        motors: [leftEngine, rightEngine],
        rudder: xRight
    })
}

app.get('/', function(req, res) {
    res.sendFile(__dirname + '/index.html')
})

io.on('connection', function(socket) {

})