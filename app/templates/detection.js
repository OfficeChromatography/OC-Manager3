var new_name;
$('#shootbttn').on('click', function (e) {
  event.preventDefault()
  $formData = $('#cameraControlsForm').serialize()+'&'+$('#userControlsForm').serialize()+'&'+$('#codecControlsForm').serialize()
  $endpoint = window.location.origin+'/capture/'
  $.ajax({
  method: 'POST',
  url:    $endpoint,
  data:   $formData,
  success: shootMethodSuccess,
  error: shootMethodError,
  })
})
$('#savebttn').on('click', function (e) {
  event.preventDefault()
  $endpoint = window.location.origin+'/capture/'
  $.ajax({
  method: 'POST',
  url:    $endpoint,
  data:   '&SAVE&url='+$('#image_id').attr('src')+'&filename='+$('#filename').val(),
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
  url:    window.location.origin+'/capture/',
  data:   data,
  success: loadfileMethodSuccess,
  error: loadfileMethodError,
})
})
$('#removebttn').on('click', function (e) {
  event.preventDefault()
  $endpoint = window.location.origin+'/capture/'
  $.ajax({
  method: 'POST',
  url:    $endpoint,
  data:   '&REMOVE&filename='+$('#filename').val(),
  success: removeFileMethodSuccess,
  error: removeFileMethodError,
  })
})
function savefileMethodSuccess(data, textStatus, jqXHR){
  loadlistofimages()
}
function savefileMethodError(jqXHR, textStatus, errorThrown){}
function shootMethodSuccess(data, textStatus, jqXHR){
  $("#image_id").attr("src",data.url);
  console.log(data.new_name);
}
function shootMethodError(jqXHR, textStatus, errorThrown){}
function loadfileMethodSuccess(data, textStatus, jqXHR){
  $("#image_id").attr("src",data.url);
  $("#filename").val(data.filename)
}
function loadfileMethodError(jqXHR, textStatus, errorThrown){}
function removeFileMethodSuccess(data, textStatus, jqXHR){
  loadlistofimages()
}
function removeFileMethodError(jqXHR, textStatus, errorThrown){}

function loadlistofimages(){
  $.ajax({
    method: 'GET',
    url:    window.location.origin+'/capture/',
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
