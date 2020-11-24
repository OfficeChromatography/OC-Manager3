
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

$("#tempOnButton").on('click',function(e){
    event.preventDefault();
    console.log($("#temp-form").serialize()+'&active=On');
    $.ajax({
    method: 'POST',
    url:    window.location.origin+'/tempControl/',
    data:   $("#temp-form").serialize()+'&active=On',
    success: staticCleanMethodSuccess,
    error: staticCleanMethodError,
    })
    function staticCleanMethodSuccess(data, textStatus, jqXHR){
    }
    function staticCleanMethodError(jqXHR, textStatus, errorThrown){}
    })

$("#tempOffButton").on('click',function(e){
    event.preventDefault();
    console.log($("#temp-form").serialize()+'&active=Off');
    $.ajax({
    method: 'POST',
    url:    window.location.origin+'/tempControl/',
    data:   $("#temp-form").serialize()+'&active=Off',
    success: staticCleanMethodSuccess,
    error: staticCleanMethodError,
    })
    function staticCleanMethodSuccess(data, textStatus, jqXHR){
    }
    function staticCleanMethodError(jqXHR, textStatus, errorThrown){}
    })

