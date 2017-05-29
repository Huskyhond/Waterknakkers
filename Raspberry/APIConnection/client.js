var config = require('./config')
var socket = require('socket.io-client')(config.host)
var PythonShell = require('python-shell')
var pyshell = new PythonShell('../GPS/gps_callback.py')
var queue = []
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

    setInterval(function() {
        if(queue.length > 0) {
            var data = queue.splice()
            socket.emit('info', data)
        }
    }, 100)

});

socket.on('disconnect', function(){
    console.log('disconnected')
})

pyshell.on('message', function (message) {
  // On rec of a coordinate.
  queue.append({ sensors: {}, location: message })
});

pyshell.end(function (err) {
  if (err) throw err;
  console.log('finished');
});
