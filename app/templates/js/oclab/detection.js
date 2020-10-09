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


function changeRGB(){
  red = $("#id_red").val()
  green = $("#id_green").val()
  blue = $("#id_blue").val()
  $("#rgbPicture").css("background-color", 'rgb(' + red + ',' + green + ',' + blue + ')')
  console.log(red,green,blue)
}

$("#id_red").change(
  function(){
    changeRGB()
  }
)
$("#id_green").change(
  function(){
    changeRGB()
  }
)
$("#id_blue").change(
  function(){
    changeRGB()
  }
)

$(document).ready(function() {
  changeRGB()
});
