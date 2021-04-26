var captureEndpoint = window.location.origin+'/capture/takeimage'
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
    methodSelected[0].value = $('[aria-selected="true"]').find("a").attr("value_saved"),
    methodSelected[1].value = $('[aria-selected="true"]').text()
}

// TakePhoto Button
$('#shootbttn').on('click', function (e) {
  event.preventDefault()
  loadMethodSelected()
  $formData = [...$('form').serializeArray(),...colorSelected,...methodSelected]
  $endpoint = captureEndpoint
  $.ajax({
  method: 'POST',
  url:    $endpoint,
  data:   $formData,
  success: shootMethodSuccess,
  error: shootMethodError,
  })
})

//save the id and url lists in shootmethodsuccess to html

function shootMethodSuccess(data, textStatus, jqXHR){
    //console.log(data)
  
    list_of_saved.loadList()
}
function shootMethodError(jqXHR, textStatus, errorThrown){}

//put camera into position
$('#cameraposbttn').on('click', function (e) {
    event.preventDefault()
    gcode = 'G28Y\nG1Y165'
    console.log(gcode);
    sendToMachine(gcode)
  })

var list_of_saved = new listOfSaved("http://127.0.0.1:8000/capture/save/",
"http://127.0.0.1:8000/capture/list",
"http://127.0.0.1:8000/capture/load",
getData,
setData,
"http://127.0.0.1:8000/capture/deleteall"
);
  
function getData(){
    //check if this is working, because saving is done using take photo
    imageID = $("#image_id").attr("alt")
    data = $('form').serialize()+'&colorSelected'
    +JSON.stringify(colorSelected)
    +'&image_id='+imageID+'&note='+$('#notestextarea').val()
    // +'&id='+$('[aria-selected="true"]').find("a").attr("value_saved")
    console.log(data)
return data
};

function setData(data){
    if (typeof data.id_list === 'undefined') {
        
    } else {
    pos = data.id_list.length - 1

    $("#image_id").attr("src",data.url[pos]);
    $("#image_id").attr("alt",data.id_list[pos]);
    $("#image_id").attr("src-list",data.url);
    $("#image_id").attr("alt-list",data.id_list);
    $('#image_id').attr("position", pos)

    setConf(data.user_conf,data.leds_conf,data.camera_conf)}
};

function setConf(user_conf,leds_conf,camera_conf){
    for (var [key, value] of Object.entries(user_conf)) {
        $("#id_"+key).val(String(value));
    };
    // Load LEDs conf
    $("#id_uv255_power").val(leds_conf.uv255_power).change();
    $("#id_uv365_power").val(leds_conf.uv365_power).change();
    $('#picker').colpickSetColor({r:leds_conf.red, g:leds_conf.green, b:leds_conf.blue});

    // Load Camera conf
    for (var [key, value] of Object.entries(camera_conf)) {
        $("#id_"+key).val(String(value));}
}

function switchPicture(direction){
    src_list = $("#image_id").attr("src-list").split(',');
    alt_list = $("#image_id").attr("alt-list").split(',');
    position = $("#image_id").attr("position");
    if (direction == 'left'){
      position -= 1
      if (position < 0){
        position = src_list.length - 1;
      } 
    } else {
      position = parseInt(position) + 1
      if (position >= src_list.length){
        position = 0;
      }
    }
    //console.log(position)
    $("#image_id").attr("src",src_list[position]);
    $("#image_id").attr("alt",alt_list[position]);
    $("#image_id").attr("position",position);
  }

  $('#right').on('click', function (e) {
    switchPicture('right');
    id = $("#image_id").attr('alt')
    $.ajax({
      method: 'GET',
      url:    window.location.origin+'/capture/getconfig/'+ id,
      success: getConfigMethodSuccess,
      error: getConfigMethodError,
    });
  })
  
  $('#left').on('click', function (e) {
    switchPicture('left');
    id = $("#image_id").attr('alt')
    $.ajax({
      method: 'GET',
      url:    window.location.origin+'/capture/getconfig/'+ id,
      success: getConfigMethodSuccess,
      error: getConfigMethodError,
    });
  })

  function getConfigMethodSuccess(data, textStatus, jqXHR){
      console.log(data)
      setConf(data.user_conf,data.leds_conf,data.camera_conf)
      $('#notestextarea').val(data.note)
  }
  function getConfigMethodError(jqXHR, textStatus, errorThrown){console.log('error')}

$(document).ready(function() {
    list_of_saved.loadList()
});
