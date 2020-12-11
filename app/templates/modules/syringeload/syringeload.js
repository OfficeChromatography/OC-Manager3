$('#loadrange').on('change',function(){
  zMovement = 40-40*$(this).val()/1000
  value = 'G1Z'+zMovement
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
})

