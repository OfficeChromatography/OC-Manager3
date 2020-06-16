var roomName = 'oc_lab';
var chatSocket = ''

window.onload = function(){
  // Load the text from the DataBase
  scrolldown()
  isConnectedEndpointRequest()
  // AJAX POST of the serial_port connection
}

// CHAT SOCKET WITH THE OCLAB
chatSocket = new WebSocket(
'ws://' + window.location.host +
'/ws/monitor/' + roomName + '/');
chatSocket.onmessage = function(e) {
var data = JSON.parse(e.data);
var message = data['message'];
document.querySelector('#MonitorTextArea').value += (message + '\n');
scrolldown()
};
chatSocket.onclose = function(e) {
console.error('Chat socket closed unexpectedly');
};

// Check if theres a current connection with the OC
function isConnectedEndpointRequest(){
  monitorendpoint = window.location.origin + '/isconnected/'
  $.ajax({
    method: 'GET',
    url:    monitorendpoint,
    success: isConnectedEndpointSucess,
    error: isConnectedEndpointError,
  })
}
function isConnectedEndpointSucess(data, textStatus, jqXHR){
  if(data['connected']==true){
    console.log('It is connected');
    monitorEndpointRequest();
  }
  else{
    console.log('It is not connected');
  }
}
function isConnectedEndpointError(jqXHR, textStatus, errorThrown){}

// If theres a current connection with the OC then load the previous chats
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
  document.querySelector('#MonitorTextArea').value += data['monitortext']
}
function monitorEndpointError(jqXHR, textStatus, errorThrown){}

// Send the POST request when 'Connect' button is pressed
$('.connection-form').submit(function(event){
  event.preventDefault()
  document.querySelector('#MonitorTextArea').value = ''
  var $formData = $(this).serialize()
  console.log($formData);
  var $endpoint = window.location.href
  $.ajax({
    method: 'POST',
    url:    $endpoint,
    data:   $formData,
    success: connectionFormSuccess,
    error: connectionFormError,
  })
})
function connectionFormSuccess(data, textStatus, jqXHR){
  scrolldown();
  checkconnection();
}
function connectionFormError(jqXHR, textStatus, errorThrown){}

// Send the POST request when 'Send' button is pressed
$('.message-form').submit(function(event){
  event.preventDefault()
  var $formData = $(this).serialize()
  var $endpoint = window.location.href
  $.ajax({
    method: 'POST',
    url:    $endpoint,
    data:   $formData,
    success: handleFormSuccess1,
    error: handleFormError1,
  })
})
function handleFormSuccess1(data, textStatus, jqXHR){
  scrolldown()
  document.getElementById('id_chattext').value = ''
  $ConnectionForm[0].reset()
}
function handleFormError1(jqXHR, textStatus, errorThrown){}

// Some monitor Functions
function scrolldown(){
  //Move the Scroll to the bottom every time a message is add
    document.getElementById('MonitorTextArea').scrollTop = document.getElementById("MonitorTextArea").scrollHeight
  //Clean the 'chattext' field and Focus it.
    // document.getElementById('id_chattext').value = ''
    // document.getElementById('id_chattext').focus();
}
