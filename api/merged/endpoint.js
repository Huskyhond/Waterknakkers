var crypto = require('crypto')
var db = require('./database.js')

module.exports = {

    serveIndex: function (req, res, next) {
        res.sendFile(__dirname + '/client/index.html')
    },

    login: function (req, res, next) {

        db.authenticate(req.body.username, req.body.password, function (err, rows, fields) {
            if (rows[0].userExists) {
                var token = generateToken()
                db.putValidTokenInDatabase(token, req.body.username)

                res.setHeader('Content-Type', 'application/json')
                res.write(
                    JSON.stringify({
                        'token': token
                    }))

                res.end()
            }
            else {
                errorReceived(res, 1, 'invalid username or password')
            }
        })
    }, 
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