var roomName = 'oc_lab';
var chatSocket = ''

$(document).ready(function(){
  // Load the text from the DataBase
  document.querySelector('#MonitorTextArea').value = monitor_text
  scrolldown()

  // AJAX POST of the serial_port connection
  var $ConnectionForm = $('.connection-form')
  $ConnectionForm.submit(function(event){
    event.preventDefault()
    document.querySelector('#MonitorTextArea').value = ''
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
    document.querySelector('#MonitorTextArea').value += data['monitor']
    device = data['device']
    connect.connect = data['connected']
    document.querySelector('#MonitorTextArea').value
    console.log(data);
  }
  function connectionFormError(jqXHR, textStatus, errorThrown){}



  var $ConnectionForm = $('.message-form')
  $ConnectionForm.submit(function(event){
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
      document.querySelector('#MonitorTextArea').value += (message + '\n');
      scrolldown()
  };

  chatSocket.onclose = function(e) {
      console.error('Chat socket closed unexpectedly');
  };

}

//Monitor Function
function scrolldown(){
    document.getElementById('MonitorTextArea').scrollTop = document.getElementById("MonitorTextArea").scrollHeight
    document.getElementById('id_chattext').value = ''
    document.getElementById('id_chattext').focus();
}
