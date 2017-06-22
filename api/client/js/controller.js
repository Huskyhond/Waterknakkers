/**
 * This script uses the Controller API of the browser, most things were written by another author.
 */
var haveEvents = 'GamepadEvent' in window;
var haveWebkitEvents = 'WebKitGamepadEvent' in window;
var controllers = {};
// Define the motion that we curently have.
var oldMotion = { leftEngine: 0, rightEngine: 0, rudder: 0 };
var followQuay = null;
// Setup all buttons to a object.
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

/**
 * If the controller connects, then tell the html its connected and add the gamepad.
 * @param {*} e Event 
 */
function connecthandler(e) {
    console.log('connected', e);
    $('.connected_box').addClass("connected");
    $('.connected_box').removeClass("disconnected");
    addgamepad(e.gamepad);
}

/**
 * Add to array of controllers and request animation frame.
 * @param {Object} gamepad Gamepad object of the event.
 */
function addgamepad(gamepad) {
    controllers[gamepad.index] = gamepad;
    // Request animation frame and callback to updateStatus.
    rAF(updateStatus);
}

/**
 * On disconnect do the reverse of connect.
 * @param {*} e Event
 */
function disconnecthandler(e) {
    console.log('disconnected');
    $('.connected_box').addClass("disconnected");
    $('.connected_box').removeClass("connected");
    removegamepad(e.gamepad);
}

/**
 * This is called upon disconnecting and will remove it from the array of controllers.
 * @param {*} gamepad The gamepad
 */
function removegamepad(gamepad) {
    delete controllers[gamepad.index];
}

/**
 * Set the current values to the xbone object.
 * @param {*} controller 
 */
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

/**
 * Apply the xbone values and calculate motor and rudder values.
 */
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


// Currently active controller.
var controllerConfig = configThree;

/**
 * This is the update called by the browser when a frame is updated.
 */
function updateStatus() {
    scangamepads();
    for (j in controllers) {
        var controller = controllers[j];
        var xboneController = updateXbone(controller);
        var motion = controllerConfig.calculateMotion(xboneController);
        setMotionInHtml(motion);
        // Only send if its not duplicate.
        if(motion.leftEngine != oldMotion.leftEngine || motion.rightEngine != oldMotion.rightEngine || motion.rudder != oldMotion.rudder) {
	        var toEmit = {boat: boatSelected, motion: motion };
            // Emit the data to the server and the server to the boat.
            socket.emit('controller', toEmit);
        }
        oldMotion = motion;
    }
    // Request another frame to the browser.
    rAF(updateStatus);
}

/**
 * Change currently set motion in the html
 * @param {Object} motion Object of motion
 */
function setMotionInHtml(motion) {
    $('#motor_one').html(motion.leftEngine.toFixed(2));
    $('#motor_two').html(motion.rightEngine.toFixed(2));
    $('#rudder').html(motion.rudder.toFixed(2));
}

/**
 * Scan if a gamepad connects.
 */
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
