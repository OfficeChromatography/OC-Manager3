$(document).ready(function(){
  document.querySelector('#sentit').value = monitor_text
  var $myForm = $(".ajax-form")
  $myForm.submit(function(event){
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
      // document.getElementById("sentit").value = data.monitor
      afterSentit()
      console.log(data);
      console.log(textStatus)
      console.log(jqXHR)
      $myForm[0].reset(); // reset form data
  }

  function handleFormError(jqXHR, textStatus, errorThrown){
      console.log(jqXHR)
      console.log(textStatus)
      console.log(errorThrown)
  }
})



//Monitor Function
var roomName = 'oc_lab';
var chatSocket = new WebSocket(
    'ws://' + window.location.host +
    '/ws/monitor/' + roomName + '/');

chatSocket.onmessage = function(e) {
    var data = JSON.parse(e.data);
    var message = data['message'];
    document.querySelector('#sentit').value += (message + '\n');
    afterSentit()
};

chatSocket.onclose = function(e) {
    console.error('Chat socket closed unexpectedly');
};


function afterSentit(){
    document.getElementById('sentit').scrollTop = document.getElementById("sentit").scrollHeight
    document.getElementById('id_chattext').value = ''
    document.getElementById('id_chattext').focus();
}
