var crypto = require('crypto')
var db = require('./database.js')

module.exports = {

    serveIndex : function(req, res, next){
        res.sendFile(__dirname + '/index.html')
    },

    login : function(req, res, next){

        console.log(req.body)

        db.authenticate(req.body.username, req.body.password)

        res.setHeader('Content-Type', 'application/json');
        res.write(
            JSON.stringify({
                'token': generateToken()
        }))

        res.end()
    }
}

// generate a pseudo-random 40 character string
var generateToken = function(){
    return crypto.randomBytes(20).toString('hex')
}

// return any error that occured to the user as a JSON response
var errorReceived = function (errnum, err, res){
	res.write(
		JSON.stringify({
			'code' : errnum,
			'error' : err
		}));
	res.end();  
};