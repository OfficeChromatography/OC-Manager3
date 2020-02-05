$(document).ready(function(){
  var $myForm = $(".ajax-form")
  $myForm.submit(function(event){
    event.preventDefault()
    var $formData = $(this).serialize()
    var $endpoint = window.location.href

    $.ajax({
      method: 'POST',
      url:    $endpoint,
      data:   $formData,
      success: handleFormSuccess,
      error: handleFormError,
    })
  })

  function handleFormSuccess(data, textStatus, jqXHR){
      document.getElementById("sentit").value = data.monitor
      scrollit()
      console.log(data);
      console.log(textStatus)
      console.log(jqXHR)
      $myForm[0].reset(); // reset form data
  }

  function handleFormError(jqXHR, textStatus, errorThrown){
      console.log(jqXHR)
      console.log(textStatus)
      console.log(errorThrown)
  }
})

//Monitor Function
function scrollit(){
    document.getElementById("sentit").scrollTop = document.getElementById("sentit").scrollHeight
}
