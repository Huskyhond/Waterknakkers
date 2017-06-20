/* REQUIRES */
var config = require('./config')
var endpoints = require('./endpoints')
var bodyParser = require('body-parser')
var express = require('express')
var app = express()
var server = require('http').createServer(app)
var io = require('socket.io').listen(server)
var api = require('./api')(io)
var MongoClient = require('mongodb').MongoClient

require('./auth.js')(io, {
    authenticate: authenticate, // auth function
    postAuthenticate: postAuthenticate, // post auth function, what to do when connection is allowed
    disconnect: disconnect, // disconnect function
    timeout: 5000 // timeout in ms
})
/* REQUIRES */
app.use(bodyParser.json()) // support JSON-encoded post bodies
app.use(bodyParser.urlencoded({ // support x-www-form-url encoded post bodies
    extended: true
}))

MongoClient.connect('mongodb://localhost:27017/waterknakkers', function (err, db) {
    api.setDatabase(db)
    console.log('Database connected')

    server.listen(config.listenPort, function () {
        console.log('web server is running at http://localhost')
    })
})

app.use(express.static(__dirname + '/client'))
app.post('/login', api.login)

// authentication algorithm for websockets
// fist parameter is error if any, else null. second parameter is true for succesful or false for unsuccesful
function authenticate(socket, data, callback) {
    data = api.formatInput(data)
    api.isTokenValid(data.token, function (err, docs) {
        if (err) callback(err, false) // error while authing
        else if (docs === null) callback(null, false) // invalid auth credentials
        else callback(null, true) // successful
    })
}

function postAuthenticate(socket, data) {
    socket.sendBuffer = []
    if (socket.auth) {
        api.addConnection(socket)
        //console.log('Socket connected!')
        socket.on('controller', api.onMotion)

        socket.on('boatreq', api.joinBoat)

        socket.on('getBoats', api.getBoats)

        socket.on('disconnect', api.disconnect)

        socket.on('info', api.parseInformation)
	
	    socket.on('pongBoat', api.boatPingsBack)
    }
}

function disconnect(socket) {
    if (socket.isBoat) {
        //api.logout(socket.username.toLowerCase())
        console.log('Boat disconnected: %s with id: %s', socket.name, socket.boatId)
    } else {
        console.log('client disconnected')
    }
}
