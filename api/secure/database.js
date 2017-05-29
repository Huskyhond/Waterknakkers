var mysql = require('mysql')
var db = mysql.createConnection({
    host: '127.0.0.1',
    user: 'root',
    password: '',
    database: 'waterknakker'
})

db.connect()

module.exports = {

authenticate : function(username, password){
    db.query('SELECT count(*) AS userExists FROM users WHERE username = ? AND password = SHA2(?, 256)', [username, password], function(err, rows, fields){
        if(!err){
            return rows
        }else{
            return err
        }
    })
}


}