var roomName = 'oc_lab';
var chatSocket = ''

window.onload = function(){
  // Load the text from the DataBase
  scrolldown()
  isConnectedEndpointRequest()
  loadDeviceInfo()
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
  scrolldown()
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
  checkconnection();
  scrolldown();
  // Delay until the OC is connected
  resolveAfter2Seconds()
  loadDeviceInfo();
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
    success: sendMessageSuccess,
    error: sendMessageError,
  })
})
function sendMessageSuccess(data, textStatus, jqXHR){
  document.getElementById('id_chattext').value = ''
  $ConnectionForm[0].reset()
  scrolldown()
}
function sendMessageError(jqXHR, textStatus, errorThrown){}

// Some monitor Functions
function scrolldown(){
  $("#MonitorTextArea").scrollTop($(this).height())
}

// Load device info in the bottom of Monitor card
function loadDeviceInfo(){
  data={}
  $.ajax({
    method: 'GET',
    url:    window.location.origin+'/isconnected/',
    data:   data,
    success: infoDeviceMethodSuccess,
    error: infoDeviceMethodError,
  })
  function infoDeviceMethodSuccess(data, textStatus, jqXHR){
    if(data.connected == true){
      $('#id_device_info').html("<b>"+data.port+"</b>");
      $('#id_baudrate_info').html("<b>"+data.baudrate+"</b>");
    }
    console.log(data);
  }
  function infoDeviceMethodError(jqXHR, textStatus, errorThrown){}

}

function resolveAfter2Seconds() {
  return new Promise(resolve => {
    setTimeout(() => {
      resolve('resolved');
    }, 2000);
  });
}
