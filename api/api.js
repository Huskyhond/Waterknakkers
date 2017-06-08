"use strict";
var crypto = require('crypto')
var instance;
class Api {
    constructor(io) {
        this.io = io
        this.that = this
        this.connections = []
    }

    setDatabase(db) {
        this.db = db
    }

    addConnection(socket) {
        instance.connections.push(socket)
    }

    getConnection(id) {
        for (var i = 0; i < instance.connections.length; i++) {
            if (instance.connections[i].boatId == id) {
                return instance.connections[i]
            }
        }
        return false;
    }

    onMotion(data) {
        console.log('Sending data to boat: ' + data.boat)
        var socket = instance.getConnection(data.boat)
        if (socket) {
            socket.emit('controller', { timestamp: Date.now(), motion: data.motion })
        }
    }

    joinBoat(options) {
        console.log("Boat connected")
        this.name = options.name
        this.boatId = options.id
        this.isBoat = true
        this.join('boats')
        instance.io.sockets.emit('boatConnected', { boat: { id: this.boatId, name: this.name } })
    }

    disconnect() {
        console.log('disconnected')
        if (this.isBoat) {
            console.log('Disconnected boat')
            instance.io.sockets.emit('boatDisconnected', { boat: { id: this.boatId, name: this.name } })
        }
        var index = instance.connections.indexOf(this)
        instance.connections.splice(index, 1)
    }

    getBoats() {
        var boats = []
        for (var i in instance.connections) {
            var socket = instance.connections[i]
            if (socket.rooms.boats) {
                boats.push({ id: socket.boatId, name: socket.name })
            }
        }
        this.emit('getBoats', { boats: boats })
    }

    parseInformation(data) {
        if (typeof (data) !== 'object')
            return
        var collection = this.db.collection('boatData')
        var _this = this; // Socket this.
        collection.insert(data, function (err, result) {
            if (result.result.n == 1) {
                _this.emit('info', data)
            }
        })
    }

    authenticate(req, res, next) {
        var collection = instance.db.collection('users') // tell mongodb we want to look in the users table
        var sha = crypto.createHash('sha256')

        var _username = req.body.username
        var _password = sha.update(req.body.password).digest('hex') // sha256 hash the incoming password

        collection.findOne({ username: _username, password: _password }, function (err, docs) {
            if (!err && docs != null) { // if there are no errors and the username / passwords exists proceed to generate a token and put it with the corresponding user
                var _token = generateToken()
                collection.update({ username: _username }, {
                    $set: {
                        token: _token,
                        isValid: 1
                    }
                }) // put a valid token into the database

                res.setHeader('Content-Type', 'application/json') // give the valid token as a http(s) response
                res.write(
                    JSON.stringify({
                        'token': _token
                    }))
                res.end()
            } else {
                if (err) errorReceived(res, 1, err) // send the error in a json response if occured
            }
        })
    }

    isTokenValid(token, callback) {
        var collection = instance.db.collection('users')
        collection.findOne({ token: token, isValid: 1 }, callback)
    }

}

// generate a pseudo-random 40 character string
var generateToken = function () {
    return crypto.randomBytes(20).toString('hex')
}

// return any error that occured to the user as a JSON response
var errorReceived = function (res, errnum, err) {
    res.setHeader('Content-Type', 'application/json')
    res.write(
        JSON.stringify({
            'code': errnum,
            'error': err
        }));
    res.end();
}

module.exports = function (io) {
    instance = new Api(io)
    return instance
}
