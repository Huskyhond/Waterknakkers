var express = require('express')
var app = express()
var server = require('http').Server(app)
var io = require('socket.io')(server)
var endpoints = require('./endpoints')(app)
var api = require('./api')(io)
var MongoClient = require('mongodb').MongoClient

console.log('Waiting for database to connect before starting server...')
MongoClient.connect('mongodb://localhost:27017/waterknakkers', function(err, db) {
  api.setDatabase(db)
  console.log('Database connected')
 
  server.listen(3000, function() {
    console.log('Listening on port 3000')
  })

})


app.use(express.static(__dirname + '/client'))
//app.get('/location', endpoints.getBoatCoordinates)

io.on('connection', function(socket) {
    api.addConnection(socket)
    console.log('Socket connected!')
    
    socket.on('controller', api.onMotion)

    socket.on('boatreq', api.joinBoat)

    socket.on('getBoats', api.getBoats)

    socket.on('disconnect', api.disconnect)

    socket.on('info', api.parseInformation)
})
