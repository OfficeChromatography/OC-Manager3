$( document ).ready(function(){
  loadlistofimages()
  $('#list-of-images').multiSelect()
})

// Select and unselect functions
$('#list-of-images').multiSelect({
  afterSelect: function(values){
    getImages(values)
  },
  afterDeselect: function(values){
    // eliminate images
    $("#card-"+values[0]).remove()
  }
});
function getImages(values){
  data = {'filename':values[0], 'LOADFILE':''}
  $.ajax({
    method: 'GET',
    url:    window.location.origin+'/capture/',
    data:   data,
    success: loadfileMethodSuccess,
    error: loadfileMethodError,
  })
  function loadfileMethodSuccess(data, textStatus, jqXHR){
    $('.card-columns').append(`<div class="card" id='card-`+data.filename+`'>
      <img class="card-img-top" src="`+data.url+`" alt="Card image cap">
      <div class="card-body">
        <h5 class="card-title">`+data.filename+`</h5>
        <p class="card-text">`+data.meta+`</p>
      </div>
    </div>`)
  }
  function loadfileMethodError(jqXHR, textStatus, errorThrown){}
}
// Get the list of images
function loadlistofimages(){
  $.ajax({
    method: 'GET',
    url:    window.location.origin+'/capture/',
    data:   '&LISTLOAD',
    success: loadlistMethodSuccess,
    error: loadlistMethodError,
  })
  function loadlistMethodSuccess(data, textStatus, jqXHR){
    var i = 0;
    $.each(data, function(key, value) {
        $('#list-of-images').multiSelect('addOption', { value: value, text: value});
        i++;
      })
    return
  }
  function loadlistMethodError(jqXHR, textStatus, errorThrown){}
}

// $('#processbttn').on('click', function (e) {
//   event.preventDefault()
//   $formData =
//   $endpoint = window.location.origin+'/capture/'
//   $.ajax({
//   method: 'POST',
//   url:    $endpoint,
//   data:   $formData,
//   success: shootMethodSuccess,
//   error: shootMethodError,
//   })
// })
// function shootMethodSuccess(data, textStatus, jqXHR){
//   $("#image_id").attr("src",data.url);
// }
// function shootMethodError(jqXHR, textStatus, errorThrown){}
