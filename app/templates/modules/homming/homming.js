$('#hommingModal').on('shown.bs.modal', function (e) {
    gcode = 'G28\nG91'
    sendToMachine(gcode,'move')
    zero_position = [0,0];
})
$('#hommingModal').on('hidden.bs.modal', function (e) {
    gcode = 'G90'
    sendToMachine(gcode,'move')
    zero_position = [0,0];
})
$('#loadHome').on('click', function(e){
  // Load the last homming place saved.
  gcode = ''
  sendToMachine(gcode,'loadzerofromdb')
})
$('#loadHome').on('click', function(e){
  // Load the last homming place saved.
  gcode = ''
  sendToMachine(gcode,'loadzerofromdb')
})
$('#setHome').on('click',function(e){
  sendToMachine(zero_position.toString(),'setzero')
})
$('#getHome').on('click',function(e){
  data={'task':'getzero'}
  $.ajax({
    method: 'GET',
    url:    window.location.origin + '/setuphomming/',
    data:   data,
  })
})
