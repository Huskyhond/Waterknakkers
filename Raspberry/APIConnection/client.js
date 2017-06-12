var config = require('./config')
var request = require('request')
var socket = require('socket.io-client')(config.host)
var PythonShell = require('python-shell')
var gpspy = new PythonShell('../GPS/get_gps.py')
var controllerpy = new PythonShell('../boatController.py')

var controllable, followQuay
var coords = [] // hard coded -> RDM's location
var queue = []
var initialize = true
var tokenRequestOptions = {
    url: config.host + "/login",
    method: 'POST',
    headers: { 'User-Agent': 'Waterknakker/0.0.1', 'Content-Type': 'application/x-www-form-urlencoded' },
    form: { 'username': 'anna', 'password': 'waterknakker' }
}

var temperatureRequestOptions = {
    url: 'http://api.openweathermap.org/data/2.5/weather',
    method: 'GET',
    //headers: { 'User-Agent': 'Waterknakker/0.0.1', 'Content-Type': 'application/x-www-form-urlencoded' },
    qs: { 'lat': 0, 'lon': 1, 'units': 'metric', 'APPID': '9977c05ce186bfe3c57ee3dbba5ef581' }
}

var authenticatedOnly = function () {
    console.log("Boat authenticated")
    socket.emit('boatreq', {
        id: config.id,
        name: config.name
    })

    socket.on('controller', function (data) {
        //console.log(data)
        var now = Date.now()
        var delay = now - data.timestamp
        console.log("Delay in ms:", delay, data.timestamp, now)

        var boatData = [data.motion.leftEngine, data.motion.rightEngine, data.motion.rudder]
        // Dont bother the arduino if the delay between the sockets is too much.
        console.log('delay', delay, 'controllable', controllable)
        //if(delay > 200 && controllable) {
        controllerpy.send(JSON.stringify(boatData))
        //}
        //else {
        //    controllerpy.send('')
        //}
    })

    setInterval(function () {
        if (queue.length > 0) {
            var data = queue.shift()
            socket.emit('info', data)
        }
    }, 100)

}

socket.on('connect', function () {
    httpRequest(tokenRequestOptions, function (data) {
        console.log('Recieved auth token', data.token)
        socket.emit('authentication', { token: data.token })
    })
})

socket.on('authenticated', authenticatedOnly)

socket.on('unautherized', function (err) {
    console.log("unautherized")
    console.log(err)
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
    catch (e) {
        // Not a json object, ignore..
    }
    if (parse) {
        if (parse.controllable === true || parse.controllable === false) {
            controllable = parse.controllable
            console.log('setting controllable to', controllable)
        }
        if (parse.followQuay === true || parse.followQuay === false) {
            if (followQuay !== parse.followQuay) queue.push({ followQuay: parse.followQuay })
            followQuay = parse.followQuay
        }
    }
})


function httpRequest(options, callback) {
    request(options, function (err, res, body) {
        if (!err && res.statusCode == 200) {
            var paredBody = JSON.parse(body) // response is a string, so we parse it back to a JSON object
            console.log('Recieved http response')
            callback(paredBody)
        } else {
            callback(null)
        }
    })
}
var gpsIterations = 0
var latT = 0, lngT = 0
setInterval(function () {
    gpspy.send()
}, 1000 / 10)

gpspy.on('message', function (message) {
    var msgParsed = JSON.parse(message)
    gpsIterations++
    latT += msgParsed[0]
    lngT += msgParsed[1]

    // On rec of a coordinate.
    if (gpsIterations > 9) { // Send location every second (location is average of 10 calls)
        var lat = latT / gpsIterations
        var lng = lngT / gpsIterations

        if (initialize) {
            temperatureRequestOptions.qs.lat = lat
            temperatureRequestOptions.qs.lon = lng
            httpRequest(temperatureRequestOptions, function (data) {
                console.log(data)
                initialize = false
                console.log('Current temperature in ' + data.name + ' is ' + data.main.temp + ' °C')
            })


        }
        queue.push({ sensors: {}, location: [lat, lng] })
        latT = lngT = gpsIterations = 0
    }
})

gpspy.on('end', function (err) { console.log('ERROR OF GPS', err) })
