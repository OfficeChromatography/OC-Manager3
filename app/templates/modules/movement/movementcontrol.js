$('#speedrange').on('change',function(){
  $('#speedtext').val($(this).val())
})
$('#speedtext').on('change',function(){
  $('#speedrange').val($(this).val())
})

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


function movement(direction){
  mm = $('#steptext').val()
  value = 'G0'+direction+$('#steptext').val()
  if(direction.includes("X")){
    if(direction.includes("-")){
      zero_position[0]=parseInt(zero_position[0])-parseInt(mm);
    }
    else{
      zero_position[0]+=parseInt(mm);
    }
  }
  if(direction.includes("Y")){
    if(direction.includes("-")){
      zero_position[1]-=parseInt(mm);
    }
    else{
      zero_position[1]+=parseInt(mm);
    }
  }
  return value;
}

function sendToMachine(value,task){
  data={'gcode':value, 'task':task}
  console.log(data);
  $.ajax({
    method: 'POST',
    url:    window.location.origin + '/setuphomming/',
    data:   data,
    success: setHommingEndpointSucess,
    error: setHommingEndpointError,
  })
  function setHommingEndpointSucess(data, textStatus, jqXHR){}
  function setHommingEndpointError(jqXHR, textStatus, errorThrown){}
}
