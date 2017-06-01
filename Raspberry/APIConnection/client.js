var config = require('./config')
var socket = require('socket.io-client')(config.host)
var PythonShell = require('python-shell')
//var gpspy = new PythonShell('../GPS/gps_callback.py')
var controllerpy = new PythonShell('../boatController.py');
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

        var boatData = [data.motion.leftEngine, data.motion.rightEngine, data.motion.rudder]
        controllerpy.send(JSON.stringify(boatData))	
    })

    setInterval(function() {
        if(queue.length > 0) {
            var data = queue.splice()
            socket.emit('info', data)
        }
    }, 100)

})

socket.on('disconnect', function(){
    console.log('disconnected')
})

controllerpy.on('message', function(message){
    console.log(message)
})

/*
gpspy.on('message', function (message) {
  // On rec of a coordinate.
  queue.append({ sensors: {}, location: message })
})

gpspy.end(function (err) {
  //if (err) throw err
  //console.log(err)
})
*/
