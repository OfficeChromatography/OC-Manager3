var captureEndpoint = window.location.origin+'/capture/'
var colorSelected = [{name: "red", value: "0"},
                    {name: "green", value: "0"},
                    {name: "blue", value: "0"}]

$('#picker').colpick({
	flat:true,
	layout:'rgbhex',
	color:'000000',
	submit:0,
	onChange:loadNewRgb,
});

function loadNewRgb(hsb,hex,rgb,el,bySetColor){
    colorSelected[0].value = rgb.r
    colorSelected[1].value  = rgb.g
    colorSelected[2].value = rgb.b

}

$('#id_uv365_power').on('change',function(){
  $('#uv365text').val($(this).val())
})
$('#uv365text').on('change',function(){
  $('#id_uv365_power').val($(this).val())
})
$('#id_uv255_power').on('change',function(){
  $('#uv255text').val($(this).val())
})
$('#uv255text').on('change',function(){
  $('#id_uv255_power').val($(this).val())
})

// TakePhoto Button
$('#shootbttn').on('click', function (e) {
  event.preventDefault()
  $formData = [...$('form').serializeArray(),...colorSelected]
  console.log($formData);
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




