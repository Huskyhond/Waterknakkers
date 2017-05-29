var mysql = require('mysql')
var db = mysql.createConnection({
    host: '127.0.0.1',
    user: 'root',
    password: '',
    database: 'waterknakker'
})

db.connect()

module.exports = {

    authenticate : function(username, password, callback){
        db.query('SELECT count(*) AS userExists FROM users WHERE username = ? AND password = SHA2(?, 256)', [username, password], callback)
    },

    putValidTokenInDatabase : function(token, username, callback){
        db.query('UPDATE users SET token = ?, isValid = 1, lastLogin = NOW()  WHERE username = ?', [token, username], callback)
    },

    getValidToken : function(token, callback){
        db.query('SELECT count(*) AS tokenExists FROM users WHERE token = ? AND isValid = 1', [token], callback)
    }
}