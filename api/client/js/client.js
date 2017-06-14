var boats = [];
var boatSelected = '';
var socket = io();


socket.on('connect', function(){
    socket.emit('authentication', {token : '918d87a8171860a8e5181a0f249bccff98378278'});
});


socket.on('authenticated', function (){
    console.log('client authenticated!')
    socket.emit('getBoats');
})

socket.on('unauthorized', function (err) {
    console.log(err)
})

socket.on('info', function(data) {
    if(data.id == boatSelected) {
	setUiPing(data.id, data.info.timestamp, Date.now());
        $('#console').append('<div>' + JSON.stringify(data.info) + '</div>');
    }
    
    if(data.info && data.info.location) {
        addToMap(data.info.location)
        setStartPosition(data.info.location, getBoatById(data.id).name)
    }
})

socket.on('getBoats', function(boatsin) {
    for(var i in boatsin.boats) {
        boats.push(boatsin.boats[i]);
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

function setUiPing(boatId, boatTimestamp, clientTimestamp) {
	var ping = clientTimestamp - boatTimestamp;
	var parent = $("input[value="+ boatId +"]").parent();
	parent.find('span').remove()
	$("<span>").html(getBoatById(boatId).name + " (" + ping + "ms)").appendTo(parent);
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

        $("<span>").html(" " + boat).appendTo(div);
        div.appendTo(parent);
    }
}

var viewport = $( window ).width() - 5;
var leftWidth = 360;


$(document).ready(function() {
    $("#left").width(leftWidth);
    $("#right").width(viewport - leftWidth);
    $('#startQuay').on('click', function() {
	socket.emit('controller', { boat: boatSelected, motion: { leftEngine: 0, rightEngine: 0, rudder: 0 }, followQuay: true});
    });
    $('#stopQuay').on('click', function() {
	socket.emit('controller', { boat: boatSelected, motion: { leftEngine: 0, rightEngine: 0, rudder: 0 }, followQuay: false});
    });
});

$(window).resize(function() {
    viewport = $( window ).width() - 5;
    $("#left").width(leftWidth);
    $("#right").width(viewport - leftWidth);
});
