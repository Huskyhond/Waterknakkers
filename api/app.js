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

/**
 * Importing and initializing the authentication module
 * 
 * @param {Object} io - socket io server object
 * @param {Function} authenticate - the name of the authentication function in this app
 * @param {Function} postAuthenticate - the name of the postAuthenticate function in this app
 * @param {Function} disconnect - the name of the disconnect function in this app 
 */
require('./auth.js')(io, {
    authenticate: authenticate, // auth function
    postAuthenticate: postAuthenticate, // post auth function, what to do when connection is allowed
    disconnect: disconnect, // disconnect function
    timeout: 5000 // timeout in ms
})

// make the express server able to decode specific object formats
app.use(bodyParser.json()) // support JSON-encoded post bodies
app.use(bodyParser.urlencoded({ // support x-www-form-url encoded post bodies
    extended: true
}))

// setting up the MongoDB connection and start listening to a port
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

/**
 * listens to the authentication emits from the connecting party
 * and grants or denies connections accordingly
 * 
 * the first parameter of the callback is an error object if any, else null
 * the secont parameter of the callback is true for a successful connection and false for unsuccesful
 * 
 * @param {Object} socket - the conneting party's socket connection 
 * @param {Object} data - a payload to check wether the user should be allowed connection or not
 * @param {function} callback - this function
 */
function authenticate(socket, data, callback) {
    data = api.formatInput(data)
    api.isTokenValid(data.token, function (err, docs) {
        if (err) callback(err, false) // error while authing
        else if (docs === null) callback(null, false) // invalid auth credentials
        else callback(null, true) // successful
    })
}

/**
 * listens to the postAuthenticate emit to grand authenticated parties
 * access to the API functions
 * 
 * @param {Object} socket - the connecting party's socket connection 
 * @param {Object} data - data object send with the socket connection
 */
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

/**
 * listens to disconnect emit and notifies the server someone diconnected
 * if the disconnecting party is a boat we log it out
 * 
 * @param {Object} socket - the disconnecting party's socket connection
 */
function disconnect(socket) {
    if (socket.isBoat) {
        //api.logout(socket.username.toLowerCase())
        console.log('Boat disconnected: %s with id: %s', socket.name, socket.boatId)
    } else {
        console.log('client disconnected')
    }
}
