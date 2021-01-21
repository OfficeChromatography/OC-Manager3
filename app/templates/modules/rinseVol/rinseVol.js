

$("#pump_manual").on('click',function(e){
    event.preventDefault();
    console.log($("#static-form").serialize());
    $.ajax({
    method: 'POST',
    url:    window.location.origin+'/staticpurge/',
    data:   $("#rinse-form").serialize(),
    success: staticCleanMethodSuccess,
    error: staticCleanMethodError,
    })
    function staticCleanMethodSuccess(data, textStatus, jqXHR){
    }
    function staticCleanMethodError(jqXHR, textStatus, errorThrown){}
    })

