const express = require('express'),
    app = express(),
    server = require('http').createServer(app);

app.use(express.json());
app.use(express.urlencoded({
  extended: true
}));

app.get('/', function (req, res) {
    res.sendFile(__dirname + '/websocket_index.html');
});

server.listen(3000, function () {
    console.log('App listening on port 3000!');
});