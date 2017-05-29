var haveEvents = 'GamepadEvent' in window;
var haveWebkitEvents = 'WebKitGamepadEvent' in window;
var controllers = {};
var oldMotion = { leftEngine: 0, rightEngine: 0, rudder: 0 };
var xbone = {
    leftTrigger: 0,
    rightTrigger: 0,
    xButton: 0,
    bButton: 0,
    l1Button: 0,
    r1Button: 0,
    xLeft: 0,
    yLeft: 0,
    xRight: 0,
    yRight: 0
};
var rAF = window.mozRequestAnimationFrame ||
    window.webkitRequestAnimationFrame ||
    window.requestAnimationFrame;

function connecthandler(e) {
    console.log('connected', e);
    $('.connected_box').addClass("connected");
    $('.connected_box').removeClass("disconnected");
    addgamepad(e.gamepad);
}

function addgamepad(gamepad) {
    controllers[gamepad.index] = gamepad; var d = document.createElement("div");
    rAF(updateStatus);
}

function disconnecthandler(e) {
    console.log('disconnected');
    $('.connected_box').addClass("disconnected");
    $('.connected_box').removeClass("connected");
    removegamepad(e.gamepad);
}

function removegamepad(gamepad) {
    var d = document.getElementById('controller' + gamepad.index);
    document.body.removeChild(d);
    delete controllers[gamepad.index];
}

function updateXbone(controller) {
    for (var i = 0; i < controller.buttons.length; i++) {
        switch (i) {
            case 0: // a
                break;
            case 1: // b
                xbone.bButton = controller.buttons[i].value;
                break;
            case 2: // x
                xbone.xButton = controller.buttons[i].value;
                break;
            case 4: // L1
                xbone.l1Button = controller.buttons[i].value;
            case 5: // R1
                xbone.r1Button = controller.buttons[i].value;
            case 6: // left trigger
                xbone.leftTrigger = controller.buttons[i].value;
                break;
            case 7: // right trigger
                xbone.rightTrigger = controller.buttons[i].value;
                break;
        }
    }

    for (var i = 0; i < controller.axes.length; i++) {
        switch (i) {
            case 0: // X-left
                xbone.xLeft = controller.axes[i];
                break;
            case 1: // Y-left
                xbone.yLeft = controller.axes[i];
                break;
            case 2: // X-right
                xbone.xRight = controller.axes[i];
                break;
            case 3: // Y-right
                xbone.yRight = controller.axes[i];
                break;
        }
    }
    return xbone;
}

var configOne = {
    calibrate: function(xbone) {
        xbone.xLeft = (xbone.xLeft < 0.1 && xbone.xLeft > - 0.1) ? 0 : xbone.xLeft;
        xbone.xRight = (xbone.xRight < 0.1 && xbone.xRight > - 0.1) ? 0 : xbone.xRight;
        xbone.xLeft = (xbone.xLeft > 0.9) ? 1 : xbone.xLeft;
        xbone.xLeft = (xbone.xLeft <  -0.9) ? -1 : xbone.xLeft;
        xbone.xRight = (xbone.xRight > 0.9) ? 1 : xbone.xRight;
        xbone.xRight = (xbone.xRight < -0.9) ? -1 : xbone.xRight;
        return xbone;
    },
    calculateMotion: function(xbone) {
        xbone = configOne.calibrate(xbone);
        var speed = (xbone.rightTrigger > 0) ? xbone.rightTrigger : -xbone.leftTrigger;
        var leftEngine = (xbone.xLeft == 0 ?  speed : xbone.xLeft * speed)
        var rightEngine = (xbone.xLeft == 0 ? speed : -xbone.xLeft * speed)
        return { leftEngine: leftEngine, rightEngine: rightEngine, rudder: xbone.xRight }
    }
}

var configTwo = {
    calculateMotion: function(xbone) {
        xbone = configOne.calibrate(xbone);
        var leftEngine = xbone.l1Button == 1 ? -xbone.leftTrigger : xbone.leftTrigger;
        var rightEngine = xbone.r1Button == 1 ? -xbone.rightTrigger : xbone.rightTrigger;
        var rudder = xbone.xLeft;
        return { leftEngine: leftEngine, rightEngine: rightEngine, rudder: rudder}
    }
}


var configThree = {
    calibrate: function(xbone) {
        xbone.xLeft = (xbone.xLeft < 0.15 && xbone.xLeft > - 0.15) ? 0 : xbone.xLeft;
        xbone.xRight = (xbone.xRight < 0.15 && xbone.xRight > - 0.15) ? 0 : xbone.xRight;
        xbone.yLeft = (xbone.yLeft < 0.15 && xbone.yLeft > - 0.15) ? 0 : xbone.yLeft;
        xbone.yRight = (xbone.yRight < 0.15 && xbone.yRight > - 0.15) ? 0 : xbone.yRight;
        return xbone;
    },
    calculateMotion: function(xbone) {  
        xbone = configThree.calibrate(xbone);
        var leftEngine = xbone.yLeft*-1 + xbone.xLeft;
        var rightEngine = xbone.yLeft*-1 - xbone.xLeft;
        var rudder = xbone.xRight;
        return { leftEngine: leftEngine, rightEngine: rightEngine, rudder: rudder}
    }
}



var controllerConfig = configOne;

function updateStatus() {
    scangamepads();
    for (j in controllers) {
        var controller = controllers[j];
        var xboneController = updateXbone(controller);
        var motion = controllerConfig.calculateMotion(xboneController);
        setMotionInHtml(motion);
        if(motion.leftEngine != oldMotion.leftEngine || motion.rightEngine != oldMotion.rightEngine || motion.rudder != oldMotion.rudder) {
            socket.emit('controller', {boat: boatSelected, motion: motion});
        }
        oldMotion = motion;
    }
    rAF(updateStatus);
}

function setMotionInHtml(motion) {
    $('#motor_one').html(motion.leftEngine);
    $('#motor_two').html(motion.rightEngine);
    $('#rudder').html(motion.rudder);
}

function scangamepads() {
    var gamepads = navigator.getGamepads ? navigator.getGamepads() : (navigator.webkitGetGamepads ? navigator.webkitGetGamepads() : []);
    for (var i = 0; i < gamepads.length; i++) {
        if (gamepads[i]) {
            if (!(gamepads[i].index in controllers)) {
                addgamepad(gamepads[i]);
            } else {
                controllers[gamepads[i].index] = gamepads[i];
            }
        }
    }
}

if (haveEvents) {
    window.addEventListener("gamepadconnected", connecthandler);
    window.addEventListener("gamepaddisconnected", disconnecthandler);
} else if (haveWebkitEvents) {
    window.addEventListener("webkitgamepadconnected", connecthandler);
    window.addEventListener("webkitgamepaddisconnected", disconnecthandler);
} else {
    setInterval(scangamepads, 500);
}
