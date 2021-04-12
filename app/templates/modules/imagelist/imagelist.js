

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

// Open image in new tab when clicked
$('#image_new_tab_bttn').on('click', function (e) {
    event.preventDefault()
    window.open($('#image_id').attr('src'))
})

$('#delete_image').on('click', function (e) {
    event.preventDefault()
    id = $("#image_id").attr('alt')
    $.ajax({
      type: 'DELETE',
      url:    window.location.origin+'/capture/delete/'+ id,
      success: deleteMethodSuccess,
      error: deleteMethodError,
    });
})
function deleteMethodSuccess(data, textStatus, jqXHR){
    list_of_saved.loadList()
}
function deleteMethodError(jqXHR, textStatus, errorThrown){console.log('error')}






