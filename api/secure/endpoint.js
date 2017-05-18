module.exports = {

serveIndex : function(req, res, next){
    res.sendFile(__dirname + '/index.html')
},

auth : function(req, res, next){

}


}

