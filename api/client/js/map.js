var markers = [];
var navigationPath = [];
var oldNavigationPath = [];
var followingCoords = false;

/**
 * Update the html based on the current boats state.
 * @param {Object} boat A single boat. 
 */
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

/**
 * Add's a lat,lng marker.
 * @param {Array} latLngArr A single lat,lng array.
 */
function addToMap(latLngArr) {
	console.log('Adding marker', latLngArr)
	if(markers.length > 0) {
		var oldMarker = markers.pop();
		var oldLatLng = oldMarker._latlng;
		// Remove last marker
		map.removeLayer(oldMarker);
		// Make the last marker a circle.
		markers.push(L.circle(latLngArr, 0.1).addTo(map));
	}
	else {
		// Center towards the first location. 16 is the zoom rate.
		map.setView(new L.LatLng(latLngArr[0], latLngArr[1]), 16);
	}
	// Create new marker.
	markers.push(L.marker(latLngArr).addTo(map));
}
// MapBox accessToken.
L.mapbox.accessToken = 'pk.eyJ1IjoiaHVza3lob25kIiwiYSI6ImNqMmFibjd3cDAwMDkzM21laXBncDN0bGgifQ.bBUvToPnn5_wAP12kmwJyw';
var markers = [];
// Hardcode initial position of the map, will be updated upon getting the first location from the boat.
var map = L.mapbox.map('map', 'mapbox.streets')
    .setView([51.8980995, 4.4171458], 16);

/**
 * Update the startlocation of the boat.
 * @param {Array||Object} marker Location of the boat.
 * @param {String} boatName Name of the boat (for visual)
 */
function setStartPosition(marker, boatName) {
	var latlng = Array.isArray(marker) ? marker : marker.latlng;
	if(navigationPath[0]) map.removeLayer(navigationPath[0]);
	var newMarker = new L.marker(latlng).bindPopup('<h4>' + boatName + '</h4>').addTo(map).openPopup();
	navigationPath[0] = newMarker;
};

/**
 * Add marker upon clicking on the map and draw a line between the points.
 * @param {*} event Event Of onclick on the map.
 */
var addMarker = function(event) {
	// If it is already navigating to a different marker, remove that one first.
	for(var i =0 ; i < oldNavigationPath.length; i++) {
		map.removeLayer(oldNavigationPath[i]);
		// Remove polyline path.
		for(i in map._layers) {
        if(map._layers[i]._path != undefined) {
            try {
                map.removeLayer(map._layers[i]);
            }
            catch(e) {
                console.log("problem with " + e + map._layers[i]);
            }
        }
    }
	}
	oldNavigationPath = [];
	// If it is the first marker (if the boat has no Position) add it anyway, this is only for debugging.
	if(navigationPath.length < 1) {
    	setStartPosition(event);
	}
	else {
		// If aready 2 points, we remove the marker from the last and make it a dot.
		if(navigationPath.length > 1) {
			var lastMarker = navigationPath.pop();

			var latLng = lastMarker._latlng;
			map.removeLayer(lastMarker);
			navigationPath.push(L.circle(latLng, 0,1).addTo(map));
		}
		// Add new marker to the map.
		var newMarker = new L.marker(event.latlng).bindPopup('<h4>End</h4>').addTo(map).openPopup();
		navigationPath.push(newMarker);
	}
	// Map Marker objects to aray of coordinates.
	var navCoords = navigationPath.map(function(marker) { return [marker._latlng.lat, marker._latlng.lng] });
	//Draw a line between all coords.
	L.polyline(navCoords, { color: 'red'}).addTo(map);
};

// On click run addMarker function.
map.on('click', addMarker);

/**
 * Add a Navigate to button to the map.
 */
var sendCoordinatesButton = L.Control.extend({

  options: {
    position: 'topright' 
    //control position - allowed: 'topleft', 'topright', 'bottomleft', 'bottomright'
  },

  onAdd: function (map) {
	var container = L.DomUtil.create('div', 'leaflet-bar leaflet-control leaflet-control-custom arrownav-container followCoords');
	var i = document.createElement('i');
	i.className = 'fa fa-location-arrow arrownav';
	container.appendChild(i);
	container.setAttribute('title', 'Navigate path');
	container.style.width = '60px';
	container.style.height = '60px';
	
	container.onclick = function(event) {
		event.preventDefault();
		followingCoords = !followingCoords;
		var navCoords = navigationPath.map(function(marker) { return [marker._latlng.lat, marker._latlng.lng] });
		if(followingCoords) {
		    container.style['background-color'] = 'green';
		    console.log('Emitting the following:',  { boat: boatSelected, motion: { followCoords: true, goalLocation: navCoords } })
		    // tell the boat to follow the coordinations and send the list that was created here.
				socket.emit('controller', { boat: boatSelected, maxPower: 50, motion: { followCoords: true, goalLocation: navCoords } });
		}
		else {
		    container.style['background-color'] = 'white';
				// Tell the boat to stop following coords.
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

/**
 * Same as followCoords but with quay.
 */
var followQuayButton = L.Control.extend({

  options: {
    position: 'topright' 
    //control position - allowed: 'topleft', 'topright', 'bottomleft', 'bottomright'
  },

  onAdd: function (map) {
	var container = L.DomUtil.create('div', 'leaflet-bar leaflet-control leaflet-control-custom arrownav-container followQuay');
	var i = document.createElement('i');
	i.className = 'fa fa-ship arrownav';
	container.appendChild(i);
	container.setAttribute('title', 'Follow quay');
	container.style.width = '60px';
	container.style.height = '60px';
	
	container.onclick = function(event) {
		event.preventDefault();
		followQuay = !followQuay
		if(followQuay) {
			container.style['background-color'] = 'green';
		}
		else {
			container.style['background-color'] = 'white';
		}
		// Emit following or not following based on the local bool.
		socket.emit('controller', { boat: boatSelected, maxPower: 50, motion: { leftEngine: 0, rightEngine: 0, rudder: 0 }, followQuay: followQuay})
		event.stopPropagation();
		return false;
	}

    return container;
  }

});


map.addControl(new sendCoordinatesButton());
map.addControl(new followQuayButton());
