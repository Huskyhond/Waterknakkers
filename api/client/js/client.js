var boats = [];
var boatSelected = '';
var socket = io();
socket.emit('getBoats');

socket.on('getBoats', function(boatsin) {
    console.log(boats);
    console.log(boatsin);
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