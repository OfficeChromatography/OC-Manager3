$(document).ready(function(){
  isConnectedEndpointRequest()
})

// Check if theres a current connection with the OC
function isConnectedEndpointRequest(){
  monitorendpoint = window.location.origin + '/isconnected/'
  $.ajax({
    method: 'GET',
    url:    monitorendpoint,
    success: isConnectedEndpointSucess,
    error: isConnectedEndpointError,
  })
}
function isConnectedEndpointSucess(data, textStatus, jqXHR){
  if(data['connected']==true){
    console.log('ESTA CONECTADO');
    monitorEndpointRequest();
  }
  else{
    console.log('no esta conectado');
  }
}
function isConnectedEndpointError(jqXHR, textStatus, errorThrown){}
