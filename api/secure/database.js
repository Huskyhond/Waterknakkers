var mysql = require('mysql')
var connection = mysql.createConnection({
    host: '127.0.0.1',
    user: 'root',
    password: '',
    database: 'waterknakker'
})

connection.connect()

module.exports = {

findUser : function(username){
    connection.query('SELECT * FROM users WHERE username = ?',[username], function(err, rows, fields){
        if(!err){
            console.log(rows)
        }else{
            console.log(err)
        }
    })
}


}