var fs = require('fs')
var express = require('express')
var http = require('http')
var https = require('https')
var app = express()

var privateKey = fs.readFileSync('cert/key.pem', 'utf8')
var certificate = fs.readFileSync('cert/cert.pem', 'utf8')
var pass = fs.readFileSync('cert/passphrase.txt', 'utf8')
var credentials = {key: privateKey, cert: certificate, passphrase: pass}



console.log(pass)

app.get('/', function(req, res){
    res.send('Hellow')
})

var httpsServer = https.createServer(credentials, app)

httpsServer.listen(8443, '127.0.0.1', function(){
    console.log('secure server is running at https://127.0.0.1:8443')
})