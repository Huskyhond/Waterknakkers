function readFile(map) {
    xmlhttp.onreadystatechange = function () {
        if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
            var arr = xmlhttp.responseText.match(/[^\r\n]+/g);
            for(var i = 0; i < arr.length; i++) {
                var splitted = arr[i].split(',');
                var isDuplicate = false;
                for(var j = 0; j < markers.length; j++) {
                    var marker = markers[j];
                    if(marker[0] == splitted[0] && marker[1] == splitted[1]) {
                        isDuplicate = true;
                    }
                }
                if(!isDuplicate) {
                    if(i < arr.length-2)
                        L.circle(splitted, 1).addTo(map);
                    else
                        L.marker(splitted).addTo(map);
                    markers.push(splitted);
                }
            }
        }
    }

    xmlhttp.open("GET", "coords.txt", true);
    xmlhttp.send();
}

L.mapbox.accessToken = 'pk.eyJ1IjoiaHVza3lob25kIiwiYSI6ImNqMmFibjd3cDAwMDkzM21laXBncDN0bGgifQ.bBUvToPnn5_wAP12kmwJyw';
var markers = [];
var map = L.mapbox.map('map', 'mapbox.light')
    .setView([51.8980995, 4.4171458], 16);

var xmlhttp = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject("Microsoft.XMLHTTP");

setInterval(function() {
    readFile(map);
}, 1000);


var marker = new mapboxgl.Marker()
    .setLngLat([30.5, 50.5])
    .addTo(map);