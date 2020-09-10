$(document).ready(function() {
    loadlistofvolumes()
});
function loadlistofvolumes(){

  $.ajax({
    method: 'GET',
    url:    window.location.origin+'/syringeload/',
    data:   '&LISTLOAD',
    success: loadlistMethodSuccess,
    error: loadlistMethodError,
  })
  function loadlistMethodSuccess(data, textStatus, jqXHR){
    console.log(data)
    $('#list_syringe_vol').empty()
    $.each(data, function(key, value) {
        $('#list_syringe_vol').append('<a class="list-group-item list-group-item-action py-1 volume-list" id='+value+' data-toggle="list" href="#list-home" role="tab" aria-controls="home">'+value+'</a>')
      })
    $('#list-load a:first-child').click()

    $('.volume-list').on('click', function (e) {
        e.preventDefault()
        $("#syringe_volume").val($(this)[0].id)
        console.log($(this)[0].id)
    })

    return
  }
  function loadlistMethodError(jqXHR, textStatus, errorThrown){}
}

$("#moveSyringeMotor").on("click",function(e){
    e.preventDefault()
    $.ajax({
        method: 'POST',
        url:    window.location.origin+'/syringeload/',
        data:   '&MOVEMOTOR='+$("#syringe_volume").val(),
        success: moveSyringeMotorSuccess,
        error: moveSyringeMotorError,
      })
   function moveSyringeMotorSuccess(data, textStatus, jqXHR){console.log("FUNCIONO")}
   function moveSyringeMotorError(jqXHR, textStatus, errorThrown){}
})

$("#save_syringe_volume").on("click",function(e){
    e.preventDefault()
    $.ajax({
            method: 'POST',
            url:    window.location.origin+'/syringeload/',
            data:   '&SAVEMOVEMOTOR='+$("#syringe_volume").val(),
            success: saveSyringeMotorSuccess,
            error: saveSyringeMotorError,
          })
   function saveSyringeMotorSuccess(data, textStatus, jqXHR){
    loadlistofvolumes()
   }
   function saveSyringeMotorError(jqXHR, textStatus, errorThrown){}
})

$("#delete_syringe_volume").on("click",function(e){
    e.preventDefault()
    $.ajax({
            method: 'POST',
            url:    window.location.origin+'/syringeload/',
            data:   '&DELETE='+$(".volume-list.active")[0].id,
            success: deleteSyringeMotorSuccess,
            error: deleteSyringeMotorError,
          })
   function deleteSyringeMotorSuccess(data, textStatus, jqXHR){
    loadlistofvolumes()
   }
   function deleteSyringeMotorError(jqXHR, textStatus, errorThrown){}
})
