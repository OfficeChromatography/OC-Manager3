// Slider
function sliderChange(val,id){
  document.getElementById(id).value = val;
}

// Cleaning EndPoint
$('#id_clean').on('click', function (e) {
  event.preventDefault()
  //
  $formData = 'process'
  $endpoint = window.location.origin+'/cleanprocess/'
  $.ajax({
  method: 'POST',
  url:    $endpoint,
  data:   $formData,
  success: cleanMethodSuccess,
  error: cleanMethodError,
  })
})
function cleanMethodSuccess(data, textStatus, jqXHR){
  console.log(data);
  cleaningstatusalert(true, data.message)
  checkStatusInterval = setInterval("checkCleaningStatus()", 3000);
}
function cleanMethodError(jqXHR, textStatus, errorThrown){
  console.log(errorThrown)
}


// Cleaning status EndPoint
var checkStatusInterval
function checkCleaningStatus(){
  $formData = 'checkstatus'
  $endpoint = window.location.origin+'/cleanprocess/'
  $.ajax({
  method: 'GET',
  url:    $endpoint,
  data:   $formData,
  success: checkCleaningSuccess,
  error: checkCleaningError,
  })

  function checkCleaningSuccess(data, textStatus, jqXHR){
    console.log(data);
    if(data.busy=='true'){
      cleaningstatusalert(true, data.message)
      progressbar(data.duration,data.time_left,data.busy)
    }
    else{
      cleaningstatusalert(false, data.message)
      progressbar(data.duration,data.time_left,data.busy)
      clearInterval(checkStatusInterval)
    }
    // return true
  }
  function checkCleaningError(jqXHR, textStatus, errorThrown){
    console.log(errorThrown)
    // return true
  }
  return true
}
function cleaningstatusalert(show, message){
  alert = $('#id_cleaning_status')
  if(show==true){
    alert.removeClass('alert-success').addClass('alert-info')
    alert.html(message)
    alert.fadeIn()
  }
  else{
    alert.html(message)
    alert.removeClass('alert-info').addClass('alert-success')
    alert.fadeIn().delay(800).fadeOut( 400 );
  }
}

function progressbar(duration,time_left,state){
  progress_obj = $('#id_clean_progress_bar')
  if(state=='true'){
    progress_obj.fadeIn()
    progressval = 100-(parseInt(time_left)*100/parseInt(duration))+'%'
    $('#id_clean_progress_bar').width(progressval)
    console.log(progressval);
  }
  else{
    progress_obj.fadeOut()
  }

}
