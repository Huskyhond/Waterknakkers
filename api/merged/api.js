"use strict";
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
	for(var i = 0; i < instance.connections.length; i++) {
		if(instance.connections[i].boatId == id) {
			return instance.connections[i]
		}
	}
	return false;
    }

    onMotion(data) {
	console.log('Sending data to boat: ' + data.boat)
	var socket = instance.getConnection(data.boat)
	if(socket) {
            socket.emit('controller', { timestamp: Date.now() , motion: data.motion })
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
        if(this.isBoat) {
            console.log('Disconnected boat')
            instance.io.sockets.emit('boatDisconnected', { boat: { id: this.boatId, name: this.name }})
        }
        var index = instance.connections.indexOf(this)
        instance.connections.splice(index, 1)
    }

    getBoats() {
        var boats = []
        for(var i in instance.connections) {
            var socket = instance.connections[i]
            if(socket.rooms.boats) {
                boats.push({ id: socket.boatId,  name: socket.name })
            }
        }
        this.emit('getBoats', { boats: boats })  
    }

    parseInformation(data) {
        if(typeof(data) !== 'object' || !data.sensors || !data.location)
            return
        var collection = this.db.collection('boatData')
        var _this = this; // Socket this.
        collection.insert(data, function(err, result) {
            if(result.result.n == 1) {
                _this.emit('info', data)
            }
        })
    }

}

module.exports = function(io) {
    instance = new Api(io)
    return instance
}
