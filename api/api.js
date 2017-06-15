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
        data = instance.formatInput(data)
        console.log('Sending data to boat: ' + data.boat)
        var socket = instance.getConnection(data.boat)
        if (socket) {
            data.timestamp = Date.now()
            socket.emit('controller', data)
        }
    }

    joinBoat(options) {
        options = instance.formatInput(options)
        console.log("Boat connected")
        this.name = options.name
        this.boatId = options.id
        this.isBoat = true
        this.join('boats')
        instance.io.sockets.emit('boatConnected', { boat: { id: this.boatId, name: this.name } })
    }

    disconnect() {
        if (this.isBoat) {
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
        data = instance.formatInput(data)
        if (typeof (data) !== 'object' || Array.isArray(data))
            return
        var collection = instance.db.collection('boatData')
        var _this = this; // Socket this.
        collection.insert(data, function (err, result) {
            if (result.result.n == 1) {
                instance.io.sockets.emit('info', { id: _this.boatId, name: _this.name, info: data })
            }
        })
    }

    login(req, res, next) {
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
                httpReponse(res, { token: _token }, 0) //send HTTP reponse to user with custom payload. 
            } else {
                if (err) httpReponse(res, { token: 0 }, err) // send the error in a json response if occured
                httpReponse(res, { token: 0 }, 'Invalid username or password')
            }
        })
    }

    isTokenValid(token, callback) {
        var collection = instance.db.collection('users')
        collection.findOne({ token: token, isValid: 1 }, callback)
    }

    logout(username) {
        var collection = instance.db.collection('users')
        collection.update({ username: username }, {
            $set: {
                isValid: 0
            }
        })
    }

    formatInput(input) { // format JSON string to JSON objects
        if (typeof (input) === 'object') return input
        var output = {}
        try {
            output = JSON.parse(input)
        }
        catch (e) {
            // No object. Ignore
        }
        return output
    }
}

// generate a pseudo-random 40 character string
var generateToken = function () {
    return crypto.randomBytes(20).toString('hex')
}

// send a http reponse to the user
var httpReponse = function (res, payload, err) {
    res.setHeader('Content-Type', 'application/json')
    res.write(
        JSON.stringify({
            'error': err,
            payload
        }));
    res.end();
}

module.exports = function (io) {
    instance = new Api(io)
    return instance
}
