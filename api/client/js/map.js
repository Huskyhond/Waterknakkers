var markers = [];
function addToMap(latLngArr) {
	console.log('Adding marker', latLngArr)
	if(markers.length > 0) {
		var oldMarker = markers.pop();
		var oldLatLng = oldMarker._latlng;
		map.removeLayer(oldMarker);
		markers.push(L.circle(latLngArr, 0.1).addTo(map));
	}
	else {
		map.setView(new L.LatLng(latLngArr[0], latLngArr[1]), 16);
	}
	markers.push(L.marker(latLngArr).addTo(map));
}
L.mapbox.accessToken = 'pk.eyJ1IjoiaHVza3lob25kIiwiYSI6ImNqMmFibjd3cDAwMDkzM21laXBncDN0bGgifQ.bBUvToPnn5_wAP12kmwJyw';
var markers = [];
var map = L.mapbox.map('map', 'mapbox.light')
    .setView([51.8980995, 4.4171458], 16);

var xmlhttp = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject("Microsoft.XMLHTTP");

setInterval(function() {
    //readFile(map);
}, 1000);

