
$('#steprangeRins').on('change',function(e){
    $('#steptextRins').val($(this).val())
})
$('#steptextRins').on('change',function(e){
    $('#steprangeRins').val($(this).val())
})
$("#pump_manual").on('click',function(e){
    event.preventDefault();
    console.log($("#static-form").serialize());
    $.ajax({
    method: 'POST',
    url:    window.location.origin+'/staticpurge/',
    data:   $("#static-form").serialize(),
    success: staticCleanMethodSuccess,
    error: staticCleanMethodError,
    })
    function staticCleanMethodSuccess(data, textStatus, jqXHR){
    }
    function staticCleanMethodError(jqXHR, textStatus, errorThrown){}
    })

