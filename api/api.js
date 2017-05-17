class Api {

    onMotion(motion) {
        console.log(motion)
    }

}

module.exports = function() {
    return new Api()
}