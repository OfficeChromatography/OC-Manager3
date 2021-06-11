var table_obj

$('#modalwaitingtimes').on('show.bs.modal',function (e){
    $('#waiting-time-modal-body').load(window.location.origin+'/development/waiting_time_view/', function (){
        table_obj = new TableWaitingTime()
    })

})

$('#modalwaitingtimes').on('hide.bs.modal', function (e) {
    table_obj.saveOnServer()
})


