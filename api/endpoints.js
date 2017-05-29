class Endpoints {

    constructor(app) {
        this.app = app
    }

    root(req, res) {
        res.sendFile(__dirname + '/client/index.html')
    }

}

module.exports = function(app) {
    return new Endpoints(app)
}