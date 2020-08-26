var zero_position = [0,0]
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
  sendToMachine(gcode)
})
$('#left_arrow').on('click',function(){
  gcode = movement('X-')
  sendToMachine(gcode)
})
$('#up_arrow').on('click',function(){
  gcode = movement('Y')
  sendToMachine(gcode)
})
$('#down_arrow').on('click',function(){
  gcode = movement('Y-')
  sendToMachine(gcode)
})
$('#homming').on('click',function(){
  gcode = 'G28XY'
  sendToMachine(gcode)
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

function sendToMachine(value){
  data={'gcode':value}
  console.log(data);
  $.ajax({
    method: 'POST',
    url:    window.location.origin+'/send/',
    data:   data,
    success: setHommingEndpointSucess,
    error: setHommingEndpointError,
  })
  function setHommingEndpointSucess(data, textStatus, jqXHR){}
  function setHommingEndpointError(jqXHR, textStatus, errorThrown){}
}
