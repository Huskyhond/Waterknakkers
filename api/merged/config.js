var fs = require('fs')

var address = '127.0.0.1'
var port = '80'
var privateKey = fs.readFileSync('cert/key.pem', 'utf8')
var certificate = fs.readFileSync('cert/cert.pem', 'utf8')

module.exports = {

    listenAddress : address,

    listenPort : port,

    httpsCredentials: {key: privateKey, cert: certificate, passphrase: "waterknakkers" }


    //var privateKey = fs.readFileSync('cert/key.pem', 'utf8')
    //var certificate = fs.readFileSync('cert/cert.pem', 'utf8')
    //var pass = fs.readFileSync('cert/passphrase.txt', 'utf8')
    //var credentials = {key: privateKey, cert: certificate, passphrase: pass}
}
