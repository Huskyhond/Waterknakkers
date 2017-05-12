//import custom modules
var config = require('./config.js')
var endpoint = require('./endpoint')

//setup http webserver with socket.io
var app = require('express')()
var server = require('https').Server(config.httpsCredentials, app)
var io = require('socket.io')(server)
//listen to ip address and port defined in the config.js file
server.listen(config.listenPort, config.listenAddress, function(){
    console.log('secure web server is running at https://'+config.listenAddress+':'+config.listenPort)
})


//request paths to api calls
app.get('/', endpoint.test)

