//import custom modules
var config = require('./config.js')
var endpoint = require('./endpoint')
var db = require('./database.js')

//setup https webserver with socket.io
var bodyParser = require('body-parser')
var app = require('express')()
var server = require('https').createServer(config.httpsCredentials, app)
var io = require('socket.io').listen(server)

require('socketio-auth')(io, {
    authenticate: authenticate, // auth function
    postAuthenticate: postAuthenticate, // post auth function, what to do when connection is allowed
    disconnect: disconnect, // disconnect function
    timeout: 1000 // timeout in ms
})

app.use(bodyParser.json()) // support JSON-encoded post bodies
app.use(bodyParser.urlencoded({ // support x-www-form-url encoded post bodies
    extended: true
}))

//listen to ip address and port defined in the config.js file
server.listen(config.listenPort, function () {
    console.log('secure web server is running at https://' + config.listenAddress + ':' + config.listenPort)
})

//request paths
app.get('/', endpoint.serveIndex)
app.post('/login', endpoint.login)

// authentication algorithm for websockets
function authenticate(socket, data, callback) {
    db.isTokenValid(data.token, function (err, rows, fields) {
        if(err || !rows[0].isValid){
            return callback(new Error('Invalid token'))
        }else{
            return callback(null, true) // null is error msg and true is authenticated
        }
    })
}


function postAuthenticate(socket, data){
    socket.on('test', function(data){
        console.log(data)
    })
}

function disconnect(socket) {
    console.log('client with socket id: ' + socket.id + ' disconnected')
}



// broadcast to all sockets
//io.sockets.emit('hello', {});
