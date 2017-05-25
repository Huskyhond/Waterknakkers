var db = require('./database.js')

module.exports = {

    serveIndex : function(req, res, next){
        res.sendFile(__dirname + '/index.html')
    },

    auth : function(req, res, next){

        console.log(req.body.usernam)

        res.write(
            JSON.stringify({
            token: generateToken()
        }))
        res.end()
    }

}

var generateToken = function(){
    return Math.random().toString(36).substr(2)
}

var errorReceived = function (errnum, err, res) {
	res.write(
		JSON.stringify({
			'code' : errnum,
			'error' : err
		}));
	res.end();
};