$('#newbttn').on('click', function (e) {
  event.preventDefault()
  editor.setValue('');
  $('#filename').val('');

})

$('#savebttn').on('click', function (e) {
  event.preventDefault()
  text = editor.getValue();
  $endpoint = window.location.origin+'/gcode-editor/'
  $.ajax({
  method: 'POST',
  url:    $endpoint,
  data:   '&SAVE&text='+text+'&name='+$('#filename').val(),
  success: savefileMethodSuccess,
  error: savefileMethodError,
  })
})

$('#list-load').on('click','#list-home-list', function (e) {
e.preventDefault()
data={'filename':$(this)[0].innerHTML, 'LOADFILE':''}
console.log(data);
$.ajax({
  method: 'GET',
  url:    window.location.origin+'/gcode-editor/',
  data:   data,
  success: loadfileMethodSuccess,
  error: loadfileMethodError,
})
})

$('#startbttn').on('click', function (e) {
  event.preventDefault()
  data =
  $endpoint = window.location.origin+'/gcode-editor/'
  $.ajax({
  method: 'POST',
  url:    $endpoint,
  data:   '&START&name='+$('#filename').val(),
  success: startFileMethodSuccess,
  error: startFileMethodError,
  })
})

// Functions after ajax call
function loadfileMethodSuccess(data, textStatus, jqXHR){
  editor.setValue(data.text);
  $('#filename').val(data.filename)
}
function loadfileMethodError(jqXHR, textStatus, errorThrown){}
function savefileMethodSuccess(data, textStatus, jqXHR){
  loadlistofgcodes()
}
function savefileMethodError(jqXHR, textStatus, errorThrown){}
function startFileMethodSuccess(data, textStatus, jqXHR){
  alertManager(data)
  console.log(data);
}
function startFileMethodError(jqXHR, textStatus, errorThrown){}

function alertManager(data){
  if (data.primary){
    alertAnimation('primary',data.primary)
  }
  if (data.secondary){
    alertAnimation('secondary',data.secondary)
  }
  if (data.success){
    alertAnimation('success',data.success)
  }
  if (data.danger){
    alertAnimation('danger',data.danger)
  }
  if (data.warning){
    alertAnimation('warning',data.warning)
  }
  if (data.info){
    alertAnimation('info',data.info)
  }
  if (data.light){
    alertAnimation('light',data.light)
  }
  if (data.dark){
    alertAnimation('dark',data.dark)
  }
}
function alertAnimation(typeofalert,message){
  $('#alert').addClass('alert-'+typeofalert)
  $('#alert').html(message)
  $('#alert').fadeIn().delay(800).fadeOut(400, function(){$('#alert').removeClass('alert-'+typeofalert)});
}
function loadlistofgcodes(){
  $.ajax({
    method: 'GET',
    url:    window.location.origin+'/gcode-editor/',
    data:   '&LISTLOAD',
    success: loadlistMethodSuccess,
    error: loadlistMethodError,
  })
  function loadlistMethodSuccess(data, textStatus, jqXHR){
    $('#list-load').empty()
    $.each(data, function(key, value) {
        $('#list-load').append('<a class="list-group-item list-group-item-action py-1" id="list-home-list" data-toggle="list" href="#list-home" role="tab" aria-controls="home">'+value+'</a>')
      })
    return
  }
  function loadlistMethodError(jqXHR, textStatus, errorThrown){}
}
