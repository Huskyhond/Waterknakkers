var instance;
class Api {
    constructor(io) {
        this.io = io
        this.that = this
        this.connections = []
    }

    addConnection(socket) {
        instance.connections.push(socket)
    }

    onMotion(motion) {
        instance.io.sockets.emit('controller', { timestamp: Date.now() , motion: motion })
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

}

module.exports = function(io) {
    instance = new Api(io)
    return instance;
}
