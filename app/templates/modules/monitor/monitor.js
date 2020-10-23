var roomName = 'oc_lab';
var chatSocket = ''

// CHAT SOCKET WITH THE OCLAB
chatSocket = new WebSocket(
'ws://' + window.location.host +
'/ws/monitor/' + roomName + '/');
chatSocket.onmessage = function(e) {
  var data = JSON.parse(e.data);
  writeOnTextBox(data['message']+'\n')
};
chatSocket.onclose = function(e) {
  console.error('Chat socket closed unexpectedly');
};
function writeOnTextBox(text){
  document.querySelector('#MonitorTextArea').value += text;
  $("#MonitorTextArea").scrollTop($("#MonitorTextArea").prop('scrollHeight'))
  // document.getElementById('MonitorTextArea').scrollTop = document.getElementById("MonitorTextArea").scrollHeight
}

// Send the POST request when 'Send' button is pressed
$('#chatform').on('submit', function(event){
  event.preventDefault()
  var data = {'gcode':$('#id_chattext').val()}
  $.ajax({
    method: 'POST',
    url:    window.location.origin+'/send/',
    data:   data,
    success: sendMessageSuccess,
    error: sendMessageError,
    })
    function sendMessageSuccess(data, textStatus, jqXHR){    }
    function sendMessageError(jqXHR, textStatus, errorThrown){}
})

// If theres a current connection with the OC then loads the previous chats
function monitorEndpointRequest(){
  monitorendpoint = window.location.origin + '/monitor/'
  $.ajax({
    method: 'GET',
    url:    monitorendpoint,
    success: monitorEndpointSucess,
    error: monitorEndpointError,
  })
}
function monitorEndpointSucess(data, textStatus, jqXHR){
  writeOnTextBox(data['monitortext'])
  console.log(data)
  $('#id_device_info').text(data.oc_lab)
  $('#id_baudrate_info').text(data.baudrate)
}
function monitorEndpointError(jqXHR, textStatus, errorThrown){}
