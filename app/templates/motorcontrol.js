// AJAX POST
var roomName = 'oc_lab';


$(document).ready(function(){
  scrolldown()
  isConnectedEndpointRequest()
})

// Sigle GCODE form
$("#Gcode_form").submit(function(event){
  event.preventDefault()
  var $formData = $(this).serialize()
  var $endpoint = window.location.href
  $.ajax({
    method: 'POST',
    url:    $endpoint,
    data:   $formData,
    success: handleFormSuccess,
    error: handleFormError,
  })
})
function handleFormSuccess(data, textStatus, jqXHR){
    scrolldown()
    console.log(textStatus)
    $("#Gcode_form")[0].reset(); // reset form data
}
function handleFormError(jqXHR, textStatus, errorThrown){
}
  // Erase button
  function erase(){
    event.preventDefault()
    document.getElementById("id_chattext").value = ''
}

// Some monitor Functions
function scrolldown(){
  //Move the Scroll to the bottom every time a message is add
    document.getElementById('MonitorTextArea').scrollTop = document.getElementById("MonitorTextArea").scrollHeight
  //Clean the 'chattext' field and Focus it.
    document.getElementById('id_chattext').value = ''
    document.getElementById('id_chattext').focus();
}

// Upload form
document.querySelector('.custom-file-input').addEventListener('change',function(e){
  var fileName = document.getElementById("GFile").files[0]
  document.getElementById('upload_label').innerHTML = fileName.name
  document.getElementById('localpath').innerHTML = 'Size: '+ Math.round(fileName.size/1000) + ' Kbytes'


  // Enable the buttons son you can run or erase empty file
  document.getElementById('play_upload').disabled = false;
  document.getElementById('erase_upload').disabled = false;
  document.getElementById('erase_upload').classList.remove("disabled");
})
function erase_upload(){
  document.getElementById('GFile').value = "";
  document.getElementById('upload_label').innerHTML ='Choose file'

  // Disable the buttons son you can not run or erase empty file
  document.getElementById('play_upload').disabled = true
  document.getElementById('erase_upload').disabled = true;
  document.getElementById('erase_upload').classList.add("disabled");
}

// Buttons move
$(".move-form").submit(function(event){
  button_pressed = document.activeElement.id
  event.preventDefault()
  var $formData = $(this).serialize() + "&button="+button_pressed
  var $endpoint = window.location.href
  var $speedrange = document.getElementById("speedrange").value
  $.ajax({
    method: 'POST',
    url:    $endpoint,
    data:   $formData,
    success: moveFormSuccess,
    error: moveFormError,
  })
})
function moveFormSuccess(data, textStatus, jqXHR){
  scrolldown()
  $(".move-form")[0].reset()
}
function moveFormError(jqXHR, textStatus, errorThrown){
  scrolldown()
}

// Slider
function sliderChange(val,id){
  document.getElementById(id).value = val;
}

// CHAT SOCKET WITH THE OCLAB
chatSocket = new WebSocket(
    'ws://' + window.location.host +
    '/ws/monitor/' + roomName + '/');
chatSocket.onmessage = function(e) {
    var data = JSON.parse(e.data);
    var message = data.message
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
    console.log('ESTA CONECTADO');
    monitorEndpointRequest();
  }
  else{
    console.log('no esta conectado');
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
