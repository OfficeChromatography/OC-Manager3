$('#notesModal').on('shown.bs.modal', function (e) {
  e.preventDefault()
  $.ajax({
  method: 'GET',
  url:    captureEndpoint,
  data:   '&LOAD_NOTE&id='+$('#image_id').attr('alt'),
  success: loadNoteMethodSuccess,
  error: loadNoteMethodError,
  })
})
$('#save_note_bttn').on('click', function (e) {
  event.preventDefault()
  $.ajax({
  method: 'POST',
  url:    captureEndpoint,
  data:   '&SAVE_NOTE&id='+$('#image_id').attr('alt')+'&note='+$('#notestextarea').val(),
  success: saveNoteMethodSuccess,
  error: saveNoteMethodError,
  })
})
function saveNoteMethodSuccess(data, textStatus, jqXHR){
  $('#notesModal').modal('hide')
}
function saveNoteMethodError(jqXHR, textStatus, errorThrown){}

function loadNoteMethodSuccess(data, textStatus, jqXHR){
    $('#notestextarea').val(data.note)
}
function loadNoteMethodError(jqXHR, textStatus, errorThrown){}