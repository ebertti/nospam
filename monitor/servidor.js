var express = require('express')
  , app = express()
  , server = require('http').createServer(app)
  , io = require('socket.io').listen(server)
  , net = require('net');

server.listen(8000);

app.use('/', express.static(__dirname + '/public'));

var serverSocket = net.createServer(function(c) { //'connection' listener
    c.on('data', function(data){
        io.sockets.emit('news', JSON.parse(data.toString()));
    });
});

serverSocket.listen(8124, function() { //'listening' listener
  console.log('server bound');
});