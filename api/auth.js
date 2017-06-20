'use strict';

var _ = require('lodash')
/**
 * Force incoming WebSocket connections to authenticate before allowing them
 * 
 * @param {Object} - a socket.io server object
 * @param {Object} - config parameters
 */
module.exports = function socketAuth(io, config) {
    config = config || {}
    var timeout = config.timeout || 1000
    var postAuthenticate = config.postAuthenticate || undefined
    var disconnect = config.disconnect || undefined

    _.forEach(io.nsps, forbidConnections) // unauthorized sockets don't recieve global events
    io.on('connection', function (socket) {

        socket.auth = false
        socket.on('authentication', function (data) {

            config.authenticate(socket, data, function (err, success) {
                if (success) {
                    socket.auth = true

                    _.forEach(io.nsps, function (nsp) {
                        restoreConnection(nsp, socket)
                    })

                    socket.emit('authenticated', success) // authentication success
                    return postAuthenticate(socket, data) // return the socket with payload to the postAuthenticate function to use the protected functions

                } else if (err) {
                    socket.emit('unauthorized', { error: err }, function () {
                        socket.disconnect('unauthorized') // authentication failure because of or with a error. So we dissconnect the socket
                    })
                } else {
                    socket.emit('unauthorized', { error: 'Authentication failure' }, function () {
                        socket.disconnect('unauthorized') // authentication failure (invalid auth credentials)
                    })
                }
            })
        })

        socket.on('disconnect', function () {
            return disconnect(socket)
        });

        if (timeout !== 'none') {
            setTimeout(function () {
                // if the socket didn't authenticate after connecting, disconnect it after timeout seconds
                if (!socket.auth) {
                    socket.disconnect('timeout')
                }
            }, timeout)
        }
    })
}

// connections from unauthenticated sockets are not considered when emitting to the namespace. (Global emits)
function forbidConnections(nsp) {
    nsp.on('connect', function (socket) {
        if (!socket.auth) {
            delete nsp.connected[socket.id]
        }
    })
}

// If the socket attempted a connection before authentication, restore it.
function restoreConnection(nsp, socket) {
    if (_.findWhere(nsp.sockets, { id: socket.id })) {
        nsp.connected[socket.id] = socket
    }
}
