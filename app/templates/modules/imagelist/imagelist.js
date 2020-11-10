$(document).ready(function() {
    loadlistofimages()
});

// Load List of images and select the first one
function loadlistofimages(){
  $.ajax({
    method: 'GET',
    url:    window.location.origin+'/capture/',
    data:   '&LISTLOAD',
    success: loadlistMethodSuccess,
    error: loadlistMethodError,
  })
  function loadlistMethodSuccess(data, textStatus, jqXHR){
        $('#list-load').empty()

        $.each(data, function(key, value) {
            row = $('<a class="list-group-item list-group-item-action py-1" data-toggle="list" href="#list-home" role="tab" aria-controls="home"></a>')
            row.text(value[0])
            row.attr('id',value[1])
            $('#list-load').append(row)
          })

        listener4LoadedImages()
        $('.list-group-item:first-child').click()
    }
  function loadlistMethodError(jqXHR, textStatus, errorThrown){}
}


// Action when list element is clicked
function listener4LoadedImages(){
$('.list-group-item').on('click', function (e) {
    e.preventDefault()
    data={'id':this.id, 'LOADFILE':''}
    console.log(data)
    console.log(data);
    $.ajax({
    method: 'GET',
    url:    window.location.origin+'/capture/',
    data:   data,
    success: loadImageMethodSuccess,
    error: loadImageMethodError,
    })
})
function loadImageMethodSuccess(data, textStatus, jqXHR){
$("#image_id").attr("src",data.url);
$("#image_id").attr("alt",data.id);
$("#image_id").attr("name",data.filename);
$("#new_filename").val(data.filename)

}
function loadImageMethodError(jqXHR, textStatus, errorThrown){}
}

//Save name Button
$('#renamebttn').on('click', function (e) {
  event.preventDefault()
  $.ajax({
  method: 'POST',
  url:    captureEndpoint,
  data:   '&RENAME&id='+$('#image_id').attr('alt')+'&filename='+$('#new_filename').val(),
  success: renamefileMethodSuccess,
  error: renamefileMethodError,
  })
})
function renamefileMethodSuccess(data, textStatus, jqXHR){
  loadlistofimages()
  $('#removebttn').fadeIn()
}
function renamefileMethodError(jqXHR, textStatus, errorThrown){}
// Remove image Button
$('#removebttn').on('click', function (e) {
  event.preventDefault()
  $endpoint = window.location.origin+'/capture/'
  $.ajax({
  method: 'POST',
  url:    $endpoint,
  data:   '&REMOVE&id='+$("#image_id").attr("alt"),
  success: removeFileMethodSuccess,
  error: removeFileMethodError,
  })
})
function removeFileMethodSuccess(data, textStatus, jqXHR){
  loadlistofimages()
  console.log(data)
}
function removeFileMethodError(jqXHR, textStatus, errorThrown){}

// Export Button
$('#exportbttn').on('click', function (e) {
    event.preventDefault()
    var element = document.createElement('a');
    element.setAttribute('href', $('#image_id').attr('src'));
    element.setAttribute('download', $('#image_id').attr('name'));
    element.style.display = 'none';
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
})

// fadeIn/Out Remove Button
$('#new_filename').on('focusin',function(e){
    $('#removebttn').fadeOut()
})
$('#new_filename').on('focusout',function(e){
    $('#removebttn').fadeIn()
})

// Open image in new tab when clicked
$('#image_new_tab_bttn').on('click', function (e) {
    event.preventDefault()
    window.open($('#image_id').attr('src'))
})

// Load image config
$('#load_config').on('click', function (e) {
    $.ajax({
        method: 'GET',
        url:    window.location.origin+'/capture/',
        data:   {'GETCONFIG':'','id':$("#image_id").attr('alt')},
        success: getConfigMethodSuccess,
        error: getConfigMethodError,
    })

    function getConfigMethodSuccess(data, textStatus, jqXHR){
        //Load User Controls

        for (var [key, value] of Object.entries(data.user_conf)) {
            $("#id_"+key).val(String(value))
        }
        // Load LEDs conf
        $("#id_uv255_power").val(data.leds_conf.uv255_power).change()
        $("#id_uv365_power").val(data.leds_conf.uv365_power).change()
        $('#picker').colpickSetColor({r:data.leds_conf.red, g:data.leds_conf.green, b:data.leds_conf.blue})

        // Load Camera conf
        for (var [key, value] of Object.entries(data.camera_conf)) {
            $("#id_"+key).val(String(value))
        }
    }
    function getConfigMethodError(jqXHR, textStatus, errorThrown){}
})