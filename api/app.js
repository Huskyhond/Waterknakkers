var app = require('express')()
var server = require('http').Server(app)
var io = require('socket.io')(server)
var endpoints = require('./endpoints')(app)
var api = require('./api')(io)

server.listen(3000, function() {
  console.log('Listening on port 3000')
})

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
