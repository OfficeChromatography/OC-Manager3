

$("#pump_manual").on('click',function(e){
    event.preventDefault();
    console.log($("#rinse-form").serialize());
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

$("#valveToggle").on('click',function(e){
    event.preventDefault();
    sendToMachine('G40');
    if ($("#toggleText").html() == "Open Valve"){
        $("#toggleText").html("Close Valve");
    } else {
        $("#toggleText").html("Open Valve");
    }
})

$('#rinseVolModal').on('shown.bs.modal', function (e) {
    sendToMachine('G28XY');
})
