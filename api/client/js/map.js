var markers = [];
var navigationPath = [];
var oldNavigationPath = [];
var followingCoords = false;

function setFollowStates(boat) {
  if(boat.followQuay !== undefined) {
	var color = (boat.followQuay) ? 'green' : 'white';
	$('.followQuay').css('background-color', color);
	followQuay = boats.followQuay;
  }
  if(boat.followCoords !== undefined) {
	var color = (boat.followCoords) ? 'green' : 'white';
	$('.followCoords').css('background-color', color);
	followCoords = boats.followCoords;
  }
}

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
var map = L.mapbox.map('map', 'mapbox.streets')
    .setView([51.8980995, 4.4171458], 16);

function setStartPosition(marker, boatName) {
	var latlng = Array.isArray(marker) ? marker : marker.latlng;
	if(navigationPath[0]) map.removeLayer(navigationPath[0]);
	var newMarker = new L.marker(latlng).bindPopup('<h4>' + boatName + '</h4>').addTo(map).openPopup();
	navigationPath[0] = newMarker;
};

var addMarker = function(event) {
	// If it is already navigating to a different marker, remove that one first.
	for(var i =0 ; i < oldNavigationPath.length; i++) {
		map.removeLayer(oldNavigationPath[i]);
	}
	oldNavigationPath = [];

	if(navigationPath.length < 1) {
    	setStartPosition(event);
	}
	else {
		if(navigationPath.length > 1) {
			var lastMarker = navigationPath.pop();

			var latLng = lastMarker._latlng;
			map.removeLayer(lastMarker);
			navigationPath.push(L.circle(latLng, 0,1).addTo(map));
		}
		var newMarker = new L.marker(event.latlng).bindPopup('<h4>End</h4>').addTo(map).openPopup();
		navigationPath.push(newMarker);
	}
	var navCoords = navigationPath.map(function(marker) { return [marker._latlng.lat, marker._latlng.lng] });
	L.polyline(navCoords, { color: 'red'}).addTo(map);
};

map.on('click', addMarker);


var sendCoordinatesButton = L.Control.extend({

  options: {
    position: 'topleft' 
    //control position - allowed: 'topleft', 'topright', 'bottomleft', 'bottomright'
  },

  onAdd: function (map) {
	var container = L.DomUtil.create('div', 'leaflet-bar leaflet-control leaflet-control-custom arrownav-container followCoords');
	var i = document.createElement('i');
	i.className = 'fa fa-location-arrow arrownav';
	container.appendChild(i);
	container.setAttribute('title', 'Navigate path');
	container.style.width = '30px';
	container.style.height = '30px';
	
	container.onclick = function(event) {
		event.preventDefault();
		followingCoords = !followingCoords;
		var navCoords = navigationPath.map(function(marker) { return [marker._latlng.lat, marker._latlng.lng] });
		if(followingCoords) {
		    container.style['background-color'] = 'green';
		    console.log('Emitting the following:',  { boat: boatSelected, motion: { followCoords: true, goalLocation: navCoords } })
		    socket.emit('controller', { boat: boatSelected, maxPower: 50, motion: { followCoords: true, goalLocation: navCoords } });
		}
		else {
		    container.style['background-color'] = 'white';
		    socket.emit('controller', { boat: boatSelected, maxPower: 50, motion: { followCoords: false, goalLocation: [] } });
		}
		oldNavigationPath = navigationPath;
		navigationPath = [];
		event.stopPropagation();
		return false;
	}

    return container;
  }

});

var followQuayButton = L.Control.extend({

  options: {
    position: 'topleft' 
    //control position - allowed: 'topleft', 'topright', 'bottomleft', 'bottomright'
  },

  onAdd: function (map) {
	var container = L.DomUtil.create('div', 'leaflet-bar leaflet-control leaflet-control-custom arrownav-container followQuay');
	var i = document.createElement('i');
	i.className = 'fa fa-ship arrownav';
	container.appendChild(i);
	container.setAttribute('title', 'Follow quay');
	container.style.width = '30px';
	container.style.height = '30px';
	
	container.onclick = function(event) {
		event.preventDefault();
		followQuay = !followQuay
		if(followQuay) {
			container.style['background-color'] = 'green';
		}
		else {
			container.style['background-color'] = 'white';
		}
		
		socket.emit('controller', { boat: boatSelected, maxPower: 50, motion: { leftEngine: 0, rightEngine: 0, rudder: 0 }, followQuay: followQuay})
		event.stopPropagation();
		return false;
	}

    return container;
  }

});


map.addControl(new sendCoordinatesButton());
map.addControl(new followQuayButton());
