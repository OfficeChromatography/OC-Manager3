var roomName = 'oc_lab';
var chatSocket = ''

$(document).ready(function(){
  // Load the text from the DataBase
  document.querySelector('#sentit').value = monitor_text
  scrolldown()

  // AJAX POST of the serial_port connection
  var $myConnectionForm = $('.connection-form')
  $myConnectionForm.submit(function(event){
    event.preventDefault()
    document.querySelector('#sentit').value = ''
    var $formData = $(this).serialize()
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
    scrolldown()
    document.querySelector('#sentit').value += data['monitor']
    device = data['device']
    connect.connect = data['connected']
    document.querySelector('#sentit').value
    console.log(data);
  }
  function connectionFormError(jqXHR, textStatus, errorThrown){}



  var $myConnectionForm = $('.message-form')
  $myConnectionForm.submit(function(event){
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

  function handleFormSuccess1(data, textStatus, jqXHR){scrolldown()
  }
  function handleFormError1(jqXHR, textStatus, errorThrown){}
})

if(connectionStatus='true'){
  chatSocket = new WebSocket(
      'ws://' + window.location.host +
      '/ws/monitor/' + roomName + '/');

  // MONITOR FUNCTIONS
  chatSocket.onmessage = function(e) {
      var data = JSON.parse(e.data);
      var message = data['message'];
      document.querySelector('#sentit').value += (message + '\n');
      scrolldown()
  };

  chatSocket.onclose = function(e) {
      console.error('Chat socket closed unexpectedly');
  };

}

//Monitor Function
function scrolldown(){
    document.getElementById('sentit').scrollTop = document.getElementById("sentit").scrollHeight
    document.getElementById('id_chattext').value = ''
    document.getElementById('id_chattext').focus();
}
