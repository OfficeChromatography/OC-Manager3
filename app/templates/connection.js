var roomName = 'oc_lab';
var chatSocket = ''

window.onload = function(){
  // Load the text from the DataBase
  isConnectedEndpointRequest()
  loadDeviceInfo()
  // AJAX POST of the serial_port connection
}

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
