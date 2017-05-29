//import custom modules
var config = require('./config.js')
var endpoint = require('./endpoint')
var db = require('./database.js')

//setup https webserver with socket.io
var bodyParser = require('body-parser')
var app = require('express')()
var server = require('https').createServer(config.httpsCredentials, app)
var io = require('socket.io').listen(server)

app.use(bodyParser.json()) // support JSON-encoded post bodies
app.use(bodyParser.urlencoded({ // support x-www-form-url encoded post bodies
    extended : true
}))

//listen to ip address and port defined in the config.js file
server.listen(config.listenPort,  function(){
    console.log('secure web server is running at https://'+config.listenAddress+':'+config.listenPort)
})

//request paths to api calls
app.get('/', endpoint.serveIndex)
app.post('/login', endpoint.login)

// authentication algorithm for websockets
require('socketio-auth')(io, {
    authenticate : function(socket, data, callback){
        db.getValidToken(data.token, function(err, rows, fields){
            if(rows[0].tokenExists){
                 return callback(null, true)
            }
        })
    }
})

io.on('connection', function(socket){
    socket.on('disconnect', function(data){
        console.log("client disconnected")
    })
})



// broadcast to all sockets
//io.sockets.emit('hello', {});
