var app = require('express')()
var server = require('http').Server(app)
var io = require('socket.io')(server)
var endpoints = require('./endpoints')(app)
var api = require('./api')(io)
//var controller = require('./controller')

server.listen(3000, function() {
  console.log('Listening on port 3000')
})

/*
controller.change = function(xLeft, xRight, motorSpeed) {
    var leftEngine = (xLeft == 0 ? motorSpeed : xLeft * motorSpeed)
    var rightEngine = (xLeft == 0 ? motorSpeed : -xLeft * motorSpeed)

    io.sockets.emit('message', {
        motors: [leftEngine, rightEngine],
        rudder: xRight
    })
}
*/


app.get('/', endpoints.root)
app.get('/client/controller.js', endpoints.clientController)
app.get('/client/jquery.min.js', endpoints.jQuery)

io.on('connection', function(socket) {
    api.addConnection(socket)
    console.log('Socket connected!')
    
    socket.on('controller', api.onMotion)

    socket.on('boatreq', api.joinBoat)

    socket.on('getBoats', api.getBoats)

    socket.on('disconnect', api.disconnect)
})
