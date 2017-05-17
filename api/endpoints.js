class Endpoints {

    constructor(app) {
        this.app = app
    }

    root(req, res) {
        res.sendFile(__dirname + '/client/index.html')
    }

    clientController(req, res) {
        res.sendFile(__dirname + '/client/controller.js')
    }

    jQuery(req, res) {
        res.sendFile(__dirname + '/client/jquery.min.js')
    }

}

module.exports = function(app) {
    return new Endpoints(app)
}