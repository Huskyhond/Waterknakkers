var boats = [];
var boatSelected = '';
var socket = io();


socket.on('connect', function(){
   socket.emit('authentication', {token : '918d87a8171860a8e5181a0f249bccff98378278'});
});

socket.on('controlledBoat', function(data) {
    console.log(data)
    if(data.boat != boatSelected) return;
    $('#motor_one').html(data.motion.leftEngine.toFixed(2));
    $('#motor_two').html(data.motion.rightEngine.toFixed(2));
    $('#rudder').html(data.motion.rudder.toFixed(2));
})

socket.on('authenticated', function (){
    console.log('client authenticated!');
    socket.emit('getBoats');
})

socket.on('unauthorized', function (err) {
    console.log(err)
})
var dt = Date.now();

socket.on('pong', function(data) {
	console.log("received Pong:", data)
	setUiPing(data.boat, data.ping);
});

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

socket.on('getBoats', function(boatsin) {
    for(var i in boatsin.boats) {
        boats.push(boatsin.boats[i]);
	setFollowStates(boatsin.boats[i]);
    }
    updateBoats();
});

socket.on('boatConnected', function(boat) {
    boats.push(boat.boat);
    updateBoats();
});

socket.on('boatDisconnected', function(boat) {
    var boat = boat.boat;
    for(var i in boats) {
        var _boat = boats[i];
        if(_boat.id == boat.id) {
            boats.splice(i, 1);
        }
    }
    updateBoats();
});

$(document).ready(function() {
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

    $('#boatRadios').on('change', 'input[type=radio][name=boats]', function() {
        boatSelected = this.value;
    });

});

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
