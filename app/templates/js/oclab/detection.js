var captureEndpoint = window.location.origin+'/capture/'

// TakePhoto Button
$('#shootbttn').on('click', function (e) {
  event.preventDefault()
  $formData = $('form').serializeArray()
  $endpoint = captureEndpoint
  $.ajax({
  method: 'POST',
  url:    $endpoint,
  data:   $formData,
  success: shootMethodSuccess,
  error: shootMethodError,
  })
})
function shootMethodSuccess(data, textStatus, jqXHR){
  $("#image_id").attr("src",data.url);
  $("#image_id").attr("alt",data.id);
  loadlistofimages()
}
function shootMethodError(jqXHR, textStatus, errorThrown){}


