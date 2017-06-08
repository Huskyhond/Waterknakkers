/* REQUIRES */
var config = require('./config.js')
var endpoints = require('./endpoints')

var bodyParser = require('body-parser')
var express = require('express')
var app = express()
var server = require('http').createServer(app)
var io = require('socket.io').listen(server)
var api = require('./api')(io)
var MongoClient = require('mongodb').MongoClient

require('socketio-auth')(io, {
    authenticate: authenticate, // auth function
    postAuthenticate: postAuthenticate, // post auth function, what to do when connection is allowed
    disconnect: disconnect, // disconnect function
    timeout: 1000 // timeout in ms
})
/* REQUIRES */
app.use(bodyParser.json()) // support JSON-encoded post bodies
app.use(bodyParser.urlencoded({ // support x-www-form-url encoded post bodies
    extended: true
}))

MongoClient.connect('mongodb://localhost:27017/waterknakkers', function(err, db) {
  api.setDatabase(db)
  console.log('Database connected')

  server.listen(config.listenPort, function () {
    console.log('web server is running at http://' + config.listenAddress + ':' + config.listenPort)
  })
})

app.use(express.static(__dirname + '/client'))
app.post('/login', api.authenticate)

// authentication algorithm for websockets
function authenticate(socket, data, callback) {
    data = api.formatInput(data)
    api.isTokenValid(data.token, function(err, docs){
        if (err) return callback(new Error(err))
        else if(docs === null) return callback(new Error('Invalid token'))
        else return callback(null, true)
    })
}

function postAuthenticate(socket, data) {
    socket.sendBuffer = []
    if(socket.auth){
        api.addConnection(socket)
        console.log('Socket connected!')

        socket.on('controller', api.onMotion)

        socket.on('boatreq', api.joinBoat)

        socket.on('getBoats', api.getBoats)

        socket.on('disconnect', api.disconnect)

        socket.on('info', api.parseInformation)
    }
}

function disconnect(socket) {
    console.log('client with socket id: ' + socket.id + ' disconnected')
}