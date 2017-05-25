var config = require('./config')
var socket = require('socket.io-client')(config.host)

socket.on('connect', function(){
    console.log('connected')
    socket.emit('boatreq', {
        id: config.id,
        name: config.name
    })

    socket.on('controller', function(data) {
        //console.log(data)
	var now = Date.now()
	var delay = now - data.timestamp
	console.log("Delay in ms:", delay, data.timestamp, now)
	
    })
});

socket.on('disconnect', function(){
    console.log('disconnected')
})
