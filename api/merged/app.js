/* REQUIRES */
var config = require('./config.js')
var endpoint = require('./endpoint')
var endpoints = require('./endpoints')
var db = require('./database.js')

var bodyParser = require('body-parser')
var app = require('express')()
var server = require('https').createServer(config.httpsCredentials, app)
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
    console.log('secure web server is running at https://' + config.listenAddress + ':' + config.listenPort)
  })
})

app.use(exres.static(__dirname + '../client'))


// authentication algorithm for websockets
function authenticate(socket, data, callback) {
    db.isTokenValid(data.token, function (err, rows, fields) {
        if (err) return callback(new Error(err))
        else if(!rows[0].isValid) return callback(new Error('Invalid token'))
        else return callback(null, true)
    })
}

function postAuthenticate(socket, data) {
    socket.on('test', function (data) {
        console.log(data)
    })
}

function disconnect(socket) {
    console.log('client with socket id: ' + socket.id + ' disconnected')
}