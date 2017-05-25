//import custom modules
var config = require('./config.js')
var endpoint = require('./endpoint')

//setup http webserver with socket.io
var app = require('express')()
var server = require('https').createServer(config.httpsCredentials, app)
var io = require('socket.io').listen(server)


//listen to ip address and port defined in the config.js file
server.listen(config.listenPort,  function(){
    console.log('secure web server is running at https://'+config.listenAddress+':'+config.listenPort)
})

//request paths to api calls
app.get('/', endpoint.serveIndex)
app.get('/auth', endpoint.auth)


require('socketio-auth')(io, function(socket, data, callback){

})

io.on('connection', function(socket){

    socket.on('disconnect', function(data){
        console.log("client disconnected")
    })
})



// broadcast to all sockets
//io.sockets.emit('hello', {});
