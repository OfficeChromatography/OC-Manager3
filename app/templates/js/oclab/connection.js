window.onload = function(){}

// Send the POST request when 'Connect' button is pressed
$('.connection-form').submit(function(event){
    event.preventDefault()
    var $formData = $(this).serialize()
    console.log($formData);
    var $endpoint = window.location.href
    $.ajax({
        method: 'POST',
        url:    $endpoint,
        data:   $formData,
        success: connectionFormSuccess,
        error: connectionFormError,
    })
    function connectionFormSuccess(data, textStatus, jqXHR){}
    function connectionFormError(jqXHR, textStatus, errorThrown){}
})
$('#disconnectBttn').on('click',function(e){
  event.preventDefault();
  chatSocket.close()
  $.ajax({
    method: 'POST',
    url:    window.location.origin + '/connection/',
    data:   '&DISCONNECT',
    success: disconnectSuccess,
    error: disconnectError,
  })
  function disconnectSuccess(data, textStatus, jqXHR){}
  function disconnectError(jqXHR, textStatus, errorThrown){}
})


let getListElements = async () => {
  return getMethods()
}

let createEvent = async (filename) => {
    let res = await createMethod({
        filename: filename,
    })
    if(res.ok) console.log(`METHOD CREATED`);
    else console.log(`METHOD CREATION ERROR`);
}

let updateEvent = async (id,filename) => {
    let res = await updateMethod(id,{
        filename: filename,
    })
    if(res.ok) console.log(`METHOD UPDATED`);
    else console.log(`METHOD UPDATED ERROR`);
}

let loadEvent = async (method_id) => {
    let data = await getMethod(method_id)
    localStorage.setItem("method",data.id);
    return data
}

let deleteEvent = async (derivatization_id)=> {
  let res = await deleteMethod(derivatization_id)
  return res
}


let list_of_saved = new listOfSaved(
    getListElements,
    createEvent,
    updateEvent,
    loadEvent,
    deleteEvent,
)
$(document).ready(function() {
  list_of_saved.loadList()
});
