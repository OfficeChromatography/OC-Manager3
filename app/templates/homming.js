$('#steprange').on('change',function(){
  $('#steptext').val($(this).val())
})
$('#steptext').on('change',function(){
  $('#steprange').val($(this).val())
})
$('#right_arrow').on('click',function(){
  gcode = movement('X')
  sendToMachine(gcode,'move')
})
$('#left_arrow').on('click',function(){
  gcode = movement('X-')
  sendToMachine(gcode,'move')
})
$('#up_arrow').on('click',function(){
  gcode = movement('Y')
  sendToMachine(gcode,'move')
})
$('#down_arrow').on('click',function(){
  gcode = movement('Y-')
  sendToMachine(gcode,'move')
})
$('#homming').on('click',function(){
  gcode = 'G28'
  sendToMachine(gcode,'move')
})
$('#setHome').on('click',function(){
  gcode = 'G92X0Y0'
  sendToMachine(gcode,'move')
})

function movement(direction){
  value = 'G0'+direction+$('#steptext').val()
  return value;
}

function sendToMachine(value,task){
  data={'gcode':value, 'task':task}
  console.log(data);
  $.ajax({
    method: 'POST',
    url:    window.location.origin + '/gohomming/',
    data:   data,
    success: setHommingEndpointSucess,
    error: setHommingEndpointError,
  })
  function setHommingEndpointSucess(data, textStatus, jqXHR){}
  function setHommingEndpointError(jqXHR, textStatus, errorThrown){}
}
