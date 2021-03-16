var captureEndpoint = window.location.origin+'/capture/'
var colorSelected = [{name: "red", value: "0"},
                    {name: "green", value: "0"},
                    {name: "blue", value: "0"}]

window.onload = function(){
    ExposureFormsControl($('#id_auto_exposure').val())
    IsoFormsControl($('#id_iso_sensitivity_auto').val())
}


//////////////////////////////// Controls the Exposure Form ///////////////////////////
$('#id_auto_exposure').on('change',function(e){
    ExposureFormsControl(e.target.value)
})
function ExposureFormsControl(value){
    if(value=='1'){
        manualExposure()
    }
    else if(value==""){
        hideAllExposure()
    }
    else{
        autoExposure()
    }
}
function hideAllExposure(){
    $('#form_exposure_dynamic_framerate').hide()
    $('#form_auto_exposure_bias').hide()
    $('#form_exposure_metering_mode').hide()
    $('#form_exposure_time_absolute').hide()
}
function manualExposure(){
    $('#form_exposure_dynamic_framerate').hide()
    $('#form_auto_exposure_bias').hide()
    $('#form_exposure_metering_mode').hide()
    $('#form_scene_mode').hide()
    $('#form_iso_sensitivity_auto').show()
    $('#form_exposure_time_absolute').show()

}
function autoExposure(){
    $('#form_scene_mode').show()
    $('#form_exposure_dynamic_framerate').show()
    $('#form_auto_exposure_bias').show()
    $('#form_exposure_metering_mode').show()
    $('#form_exposure_time_absolute').hide()

//    Hides Iso
    $('#form_iso_sensitivity_auto').hide()
    $('#id_iso_sensitivity_auto').val(1)
    $('#id_iso_sensitivity_auto').change()
}

//////////////////////////////// Controls the ISO Form ///////////////////////////
$('#id_iso_sensitivity_auto').on('change',function(e){
    IsoFormsControl(e.target.value)
})
function IsoFormsControl(value){
    console.log(value)
    if(value=='1'){
        $('#form_iso_sensitivity').hide()
    }
    else if(value==""){
        $('#form_iso_sensitivity').hide()
    }
    else{
        $('#form_iso_sensitivity').show()
    }
}


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

var methodSelected = [{name: "id", value: "id"},{name: "filename", value: "filename"}]
function loadMethodSelected(){
    methodSelected[0].value = $('[aria-selected="true"]').attr("id"),
    methodSelected[1].value = $('[aria-selected="true"]').text()
}
                    

// TakePhoto Button
$('#shootbttn').on('click', function (e) {
  event.preventDefault()
  loadMethodSelected()
  $formData = [...$('form').serializeArray(),...colorSelected,...methodSelected]
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

//put camera into position
$('#cameraposbttn').on('click', function (e) {
    event.preventDefault()
    gcode = 'G28Y\nG1Y179'
    console.log(gcode);
    sendToMachine(gcode)
  })
