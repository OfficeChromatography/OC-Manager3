$(document).ready(function() {
    loadlistofimages()
});

//Load List of images and select the first one
function loadlistofimages(){
  $.ajax({
    method: 'GET',
    url:    window.location.origin+'/capture/',
    data:   '&LISTLOAD',
    success: loadlistMethodSuccess,
    error: loadlistMethodError,
  })
  function loadlistMethodSuccess(data, textStatus, jqXHR){
    console.log(data)
    $('#list-load').empty()
    $.each(data, function(key, value) {
        console.log(value[0])
        $('#list-load').append('<a class="list-group-item list-group-item-action py-1" id='+value[1]+' data-toggle="list" href="#list-home" role="tab" aria-controls="home">'+value[0]+'</a>')
      })
    listener4LoadedImages()
    $('#list-load a:first-child').click()
    return
  }
  function loadlistMethodError(jqXHR, textStatus, errorThrown){}
}
// Action on list element clicking
function listener4LoadedImages(){
$('.list-group-item').on('click', function (e) {
    e.preventDefault()
    data={'id':$(this)[0].id, 'LOADFILE':''}
    console.log(data)
    console.log(data);
    $.ajax({
    method: 'GET',
    url:    window.location.origin+'/capture/',
    data:   data,
    success: loadImageMethodSuccess,
    error: loadImageMethodError,
    })
    })
function loadImageMethodSuccess(data, textStatus, jqXHR){
$("#image_id").attr("src",data.url);
$("#image_id").attr("alt",data.id);
$("#image_id").attr("name",data.filename);
$("#new_filename").val(data.filename)
}
function loadImageMethodError(jqXHR, textStatus, errorThrown){}
}

//Save Button
$('#savebttn').on('click', function (e) {
  event.preventDefault()
  $.ajax({
  method: 'POST',
  url:    captureEndpoint,
  data:   '&SAVE&id='+$('#image_id').attr('alt')+'&filename='+$('#new_filename').val(),
  success: savefileMethodSuccess,
  error: savefileMethodError,
  })
})
function savefileMethodSuccess(data, textStatus, jqXHR){
  loadlistofimages()
  $('#removebttn').fadeIn()
}
function savefileMethodError(jqXHR, textStatus, errorThrown){}

//Remove Button
$('#removebttn').on('click', function (e) {
  event.preventDefault()
  $endpoint = window.location.origin+'/capture/'
  $.ajax({
  method: 'POST',
  url:    $endpoint,
  data:   '&REMOVE&id='+$("#image_id").attr("alt"),
  success: removeFileMethodSuccess,
  error: removeFileMethodError,
  })
})
function removeFileMethodSuccess(data, textStatus, jqXHR){
  loadlistofimages()
  $('#list-load a:first-child').click()
  console.log(data)
}
function removeFileMethodError(jqXHR, textStatus, errorThrown){
    console.log(data)
}

//Export Button
$('#exportbttn').on('click', function (e) {
    event.preventDefault()
    var element = document.createElement('a');
    element.setAttribute('href', $('#image_id').attr('src'));
    element.setAttribute('download', $('#image_id').attr('name'));
    element.style.display = 'none';
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
})

// fadeIn/Out Remove Button
$('#new_filename').on('focusin',function(e){
    $('#removebttn').fadeOut()
})
$('#new_filename').on('focusout',function(e){
    $('#removebttn').fadeIn()
})