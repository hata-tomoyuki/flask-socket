$(document).ready(function() {

    var socket = io.connect('http://127.0.0.1:5000');

    socket.on('connect', function() {
        socket.send('User has connected!');
    });

    socket.on('message', function(data) {
        $('#messages').append($('<p>').text(data[0] +" 感情のスコア：" + data[1]));
    });

    $('#sendBtn').on('click', function() {
        socket.send($('#message').val());
    });
});
