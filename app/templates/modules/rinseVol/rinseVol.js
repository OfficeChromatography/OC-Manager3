

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
    if ($("#toggleText").html() == "Open Valve"){
        $("#toggleText").html("Close Valve");
        sendToMachine('G41');
    } else {
        $("#toggleText").html("Open Valve");
        sendToMachine('G40');
    }
})

$('#rinseVolModal').on('shown.bs.modal', function (e) {
    sendToMachine('G28XY');
})
