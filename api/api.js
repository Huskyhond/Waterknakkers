"use strict";
var crypto = require('crypto')
var instance;
class Api {
    constructor(io) {
        this.io = io
        this.that = this
        this.connections = []
	this.boatPings = {}
	this.pingBoats()
    }

    setDatabase(db) {
        this.db = db
    }

    addConnection(socket) {
        instance.connections.push(socket)
    }

    pingBoats() {
	setInterval(function() {
		var boats = instance.getBoatConnections()
		for(var i = 0; i < boats.length; i++) {
			instance.boatPings[boats[i].boatId] = Date.now()
			boats[i].emit('pingBoat')
		}
	}, 2000)
    }
	
    boatPingsBack() {
	var ping = Date.now() - instance.boatPings[this.boatId] 
	instance.io.sockets.emit('pong', { boat: this.boatId, ping: ping })
    }

    getBoatConnections() {
	var boats = []
	for(var i = 0; i < instance.connections.length; i++) {
		if(instance.connections[i].isBoat) {
			boats.push(instance.connections[i])
		}
	}
	return boats;
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
        console.log('Sending data to boat', data)
        var socket = instance.getConnection(data.boat)
        if (socket) {
            data.timestamp = Date.now()
	    instance.io.sockets.emit('controlledBoat', data)
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
                boats.push({ id: socket.boatId, name: socket.name, followQuay: socket.followQuay, followCoords: socket.followCoords, controllable: socket.controllable })
            }
        }
        this.emit('getBoats', { boats: boats })
    }

    /**
     * Receives and handles information from the boat.
     * @param {Object} data Data send by boat
     */
    parseInformation(data) {
        data = instance.formatInput(data)
        if (typeof (data) !== 'object' || Array.isArray(data))
            return
        var collection = instance.db.collection('boatData')
        var _this = this; // Socket this.
        
        if(data.followQuay !== undefined)
            _this.followQuay = data.followQuay
        if(data.followCoords !== undefined)
            _this.followCoords = data.followCoords
        if(data.controllable !== undefined)
            _this.controllable = data.controllable
        
        collection.insert(data, function (err, result) {
            if (result.result.n == 1) {
		console.log('Boat sending data', data)
                instance.io.sockets.emit('info', { id: _this.boatId, name: _this.name, info: data })
            }
        })
    }


    /**
     * Listening on the https://example.org/login for login requests
     * If successful return a JSON object conainting a valid token for the WebSocket authentication and store it in the database
     * If successful return a JSON object containing a error message
     * 
     * @param {Object} req - request object from the user via HTTP POST 
     * @param {Object} res - response object to the user with a JSON payload
     * @param {Function} next - function to execute after this one. CAN BE NONE
     */
    login(req, res, next) {
        var collection = instance.db.collection('users') // tell mongodb we want to look in the users table
        var sha = crypto.createHash('sha256')

        var _username = req.body.username
        var _password = sha.update(req.body.password).digest('hex') // sha256 hash the incoming password. Because they are stored as sha256 hashes in the databae

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


    /**
     * Called by the authenticate function in app.js
     * Check wether the given token exists in the database and is valid
     * 
     * @param {String} token - authentication token from connecting WebSocket user. Obtained from the login function 
     * @param {Function} callback - returning the collection.findOne function. So the results can be used everywhere.
     */
    isTokenValid(token, callback) {
        var collection = instance.db.collection('users')
        collection.findOne({ token: token, isValid: 1 }, callback)
    }


    /**
     * Called by dissconnect function in app.js
     * Set the token of the corresponding username to inValid. This forces the user to reauthenticate 
     * 
     * @param {String} username - username of the disconnecting user 
     */
    logout(username) {
        var collection = instance.db.collection('users')
        collection.update({ username: username }, {
            $set: {
                isValid: 0
            }
        })
    }


    /**
     * 
     * Format given input to a JSON object if possible
     * 
     * @param {Any} input 
     */
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



/**
 * Generates a preudo-random 40 character string when called and returns it
 */
var generateToken = function () {
    return crypto.randomBytes(20).toString('hex')
}

/**
 * Sends a customizable HTTP reponse to the requesting user if called
 * 
 * @param {Object} res - reponse object to a user 
 * @param {JSON} payload - JSON payload to send to the user
 * @param {Any} err - error message or object to send to the user. If any
 */
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
