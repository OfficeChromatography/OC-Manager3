var t = $('#dataTable').DataTable();
$(document).ready( function () {
    loadlistofgcodes()
    // $('#dataTable > tbody').fadeIn(500,linear);
} );

function loadlistofgcodes(){
  $.ajax({
    method: 'GET',
    url:    window.location.origin+'/logdatatable/',
    data:   '&LISTLOAD',
    success: loadlistMethodSuccess,
    error: loadlistMethodError,
  })
  function loadlistMethodSuccess(data, textStatus, jqXHR){
    $.each(data, function(key, value) {
      t.row.add([
        value.auth_id,
        value.oc_lab,
        value.baudrate,
        value.timeout,
        value.time_of_connection,
      ]).draw(false)
    })
    return
  }
  function loadlistMethodError(jqXHR, textStatus, errorThrown){}
}
