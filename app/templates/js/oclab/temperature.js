
$("#start_temp").on('click',function(e){
    event.preventDefault();
    console.log($("#temp-form").serialize());
    $.ajax({
    method: 'POST',
    url:    window.location.origin+'/tempControl/',
    data:   $("#temp-form").serialize(),
    success: staticCleanMethodSuccess,
    error: staticCleanMethodError,
    })
    function staticCleanMethodSuccess(data, textStatus, jqXHR){
    }
    function staticCleanMethodError(jqXHR, textStatus, errorThrown){}
    })
