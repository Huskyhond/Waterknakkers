var boats = [];
var boatSelected = '';
var socket = io();


/**
 * Connect to the server and authenticate as a client.
 * The token is from the database and will be checked.
 */
socket.on('connect', function(){
   socket.emit('authentication', {token : '918d87a8171860a8e5181a0f249bccff98378278'});
});

/**
 * If another client controls the boat, this will be called.
 * @param {Object} data Data received from the server.
 */
socket.on('controlledBoat', function(data) {
    // Only show this data if this boat is selected.
    if(data.boat != boatSelected) return;
    // Update html.
    $('#motor_one').html(data.motion.leftEngine.toFixed(2));
    $('#motor_two').html(data.motion.rightEngine.toFixed(2));
    $('#rudder').html(data.motion.rudder.toFixed(2));
})

/**
 * This is called after the authentication succeeded, after we know it succeeded we can stat emitting.
 */
socket.on('authenticated', function (){
    console.log('client authenticated!');
    // Ask which boats are connected.
    socket.emit('getBoats');
})

/**
 * Authentication failed, we do no more here but log it in the console to know what went wrong.
 * @param {Object} err Error received from the server.
 */
socket.on('unauthorized', function (err) {
    console.log(err)
})

var dt = Date.now();

/**
 * The server gives the reaction time between a boat and the server.
 * Note! The ping is the delay from server to boat, not from server to client.
 * @param {Object} data Data received from the server.
 */
socket.on('pong', function(data) {
	console.log("received Pong:", data)
    // Set this ping next to boat's name.
	setUiPing(data.boat, data.ping);
});

/**
 * All the info a boat gives to the server will be forwarded to all listening clients.
 * Here we can receive the GPS coordinates or sensor data from the boat.
 * @param {Object} data Data received from the server.
 */
socket.on('info', function(data) {
    if(data.id == boatSelected) {
        $('#console').append('<div>' + JSON.stringify(data.info) + '</div>');
    }
    
    if(data.info) {
	    if(data.info.location) {
		addToMap(data.info.location)
		setStartPosition(data.info.location, getBoatById(data.id).name)
	    }
	    console.log(data.info);
	    if(data.info.controllable === true) {
		$('.controllable-state').removeClass('fa-ban').addClass('fa-check-circle');
	    }
            else if(data.info.controllable !== undefined && data.info.controllable === false) {
		$('.controllable-state').removeClass('fa-check-circle').addClass('fa-ban');
	    }
    }
    
})

/**
 * After the socket.emit('getBoats') is send to the server, the server will return all the boats that are already connected.
 * @param {Array} boatsin All the boats currently connected to the server.
 */
socket.on('getBoats', function(boatsin) {
    for(var i in boatsin.boats) {
        // Add to the local list of boats.
        boats.push(boatsin.boats[i]);
        // Updates the current followStates 'FollowQuay' and 'FollowCoords'. (Since the boat could already be in a session)
	    setFollowStates(boatsin.boats[i]);
    }
    // Update all the html of the boats based on the boats array.
    updateBoats();
});

/**
 * Boat connected post connect, add it to the array of boats.
 * @param {Object} boat A single boat.
 */
socket.on('boatConnected', function(boat) {
    boats.push(boat.boat);
    // Update all the html of the boats based on the boats array.
    updateBoats();
});

/**
 * If a boat is disconnected from the server, either by turning off or by losing connection.
 * @param {Object} boat A single boat.
 */
socket.on('boatDisconnected', function(boat) {
    var boat = boat.boat;
    for(var i in boats) {
        var _boat = boats[i];
        // Remove the boat from the array of boats.
        if(_boat.id == boat.id) {
            boats.splice(i, 1);
        }
    }
    // Update all the html of the boats based on the boats array.
    updateBoats();
});

/**
 * When page loaded.
 */
$(document).ready(function() {
    // On listener for the controller input, you can change which controller configuration you want to use.
    $('input[type=radio][name=controller]').change(function() {
        if (this.value == 'c1') {
            controllerConfig = configOne;
        }
        else if (this.value == 'c2') {
            controllerConfig = configTwo;
        }
        else if (this.value = 'c3'){
            controllerConfig = configThree;
        }
    });

    // If the selected boat changes, update the selected boat value.
    $('#boatRadios').on('change', 'input[type=radio][name=boats]', function() {
        boatSelected = this.value;
    });

});

/**
 * Updates the HTML of the ping from the boat given by the server.
 * @param {String} boatId The id of the boat of which the delay is measured.
 * @param {Int} ping Delay between server and boat
 */
function setUiPing(boatId, ping) {
	var parent = $("input[value="+ boatId +"]").parent();
	parent.find('.ping').remove();
	$("<span>").addClass('ping').html(" (" + ping + "ms)").appendTo(parent);
}


function getBoatById(id) {
    for(var i in boats) {
        if(boats[i].id == id)
            return boats[i];
    }
    return false;
}

function updateBoats() {
    var parent = $("#boatRadios");
    parent.empty();
    for(var i in boats) {
    console.log(boats[i]);
        var div = $('<div>', {
            class: 'boats',
            id: 'boat' + i
        });
        var boat = boats[i].name;
        var radio = $("<input>", {
            type: "radio",
            name: "boats"
        }).val(boats[i].id).appendTo(div);
        
        if(boats[i].id == boatSelected){
            radio.attr('checked', 'checked');
            boatSelected = boats[i].id;
        }
        else if(i == 0 && boatSelected == '') {
            radio.attr('checked', 'checked');
            boatSelected = boats[i].id;
        }

        $("<span>").html(" " + boat + " ").appendTo(div);
        var controllable = (boats[i].controllable) ? 'fa fa-check-circle controllable-state' : 'fa fa-ban controllable-state';
        $("<i>").addClass(controllable).appendTo(div);
        div.appendTo(parent);
    }
}

var viewport = $( window ).width() - 5;
var leftWidth = 360;


$(document).ready(function() {
    $("#left").width(leftWidth);
    $("#right").width(viewport - leftWidth);
});

$(window).resize(function() {
    viewport = $( window ).width() - 5;
    $("#left").width(leftWidth);
    $("#right").width(viewport - leftWidth);
});
