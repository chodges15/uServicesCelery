
$(document).ready(function(){
    //connect to the socket server.
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/test');
    var locations_received = [];

    //receive details from server
    socket.on('location', function(msg) {
        console.log("Received location" + msg);
        //maintain a list of ten numbers
        if (locations_received.length >= 20){
            locations_received.shift()
        }            
        locations_received.push(msg);
        location_string = '';
        for (var i = 0; i < locations_received.length; i++){
            location_string = location_string + '<p>' + locations_received[i] + '</p>';
        }
        $('#log').html(location_string);
    });

});