var config = require('./config')
var request = require('request')
var socket = require('socket.io-client')(config.host)
var PythonShell = require('python-shell')
//var gpspy = new PythonShell('../GPS/gps_callback.py')
var controllerpy = new PythonShell('../boatController.py')

var controllable
var queue = []

var options = {
    url: config.host + "/login",
    method: 'POST',
    headers: { 'User-Agent': 'Waterknakker/0.0.1', 'Content-Type': 'application/x-www-form-urlencoded' },
    form: { 'username': 'anna', 'password': 'waterknakkers' }
}


socket.on('connect', function () {
    requestToken(function (token) {
        socket.emit('authentication', { token: token })
        socket.on('authenticated', function () {
            console.log('boat authenticated!')
        })

        socket.on('unautherized', function (err) {
            console.log(err)
        })
    })

    socket.emit('boatreq', {
        id: config.id,
        name: config.name
    })
    console.log('boats')
    socket.on('controller', function (data) {
        //console.log(data)
        var now = Date.now()
        var delay = now - data.timestamp
        console.log("Delay in ms:", delay, data.timestamp, now)

        var boatData = [data.motion.leftEngine, data.motion.rightEngine, data.motion.rudder]
        controllerpy.send(JSON.stringify(boatData))
        // Dont bother the arduino if the delay between the sockets is too much.
        if(delay > 200 && controllable) {
            controllerpy.send(JSON.stringify(boatData))	
        }
    })

    setInterval(function () {
        if (queue.length > 0) {
            var data = queue.splice()
            socket.emit('info', data)
        }
    }, 100)

})

socket.on('disconnect', function () {
    console.log('disconnected')
})

controllerpy.on('message', function (message) {
    console.log(message)
    var parse = undefined;
    try {
        parse = JSON.parse(message);
    }
    catch(e) {
        // Not a json object, ignore..
    }
    if(parse) {
        if(parse.controllable === true || parse.controllable === false) {
            controllable = parse.controllable
        }
    }
})


function requestToken(callback) {
    request(options, function (err, res, body) {
        if (!err && res.statusCode == 200) {
            var token = JSON.parse(body).token // response token is a string, so we parse it back to a JSON object
            callback(token)
        } else {
            callback(null)
        }
    })
}
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
