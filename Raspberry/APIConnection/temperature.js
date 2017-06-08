var request = require('request')

var apiUrl = 'http://api.openweathermap.org/data/2.5/weather'
var apiKey = '9977c05ce186bfe3c57ee3dbba5ef581'
var coords = [51.897184, 4.4178663]


var options = {
    url: apiUrl,
    method: 'GET',
    headers: { 'User-Agent': 'Waterknakker/0.0.1', 'Content-Type': 'application/x-www-form-urlencoded' },
    qs: {'lat': coords[0], 'lon': coords[1], 'units': 'metric','APPID': apiKey}
}

request(options, function(err, res, body){
    if(!err || res.statusCode == 200){
        parsedBody = JSON.parse(body)
        temperature = parsedBody.main.temp
        console.log(temperature)

    }
})