
class TableWaitingTime{
    constructor() {
        this.table = $('#waitingTimeTable')
        this.row_template = $('#row_wait_template')
        this.numberOfApplications = parseInt($("input[name='applications']").val())
        this.development_id = $('#selected-element-id').val()
        this.loadFromServer()
    }

    notInServer(){
        this.eliminateRows()
        for(let i = 1;i<=this.numberOfApplications; i++){
            this.appendRow(i,3);
        }
    }

    eliminateRows(){
        $('.row_waiting_time').remove()
    }


    appendRow(id,value){
        let new_row = this.row_template.clone()
            .attr("id","row_waiting_time_"+id)
            .addClass("row_waiting_time")
        let input = new_row.find('input')
        let input_name = id

        new_row.find('.id_application').text(id)
        input.attr('name',input_name)
        input.val(value)

        this.table.append(new_row)
        new_row.show()
    }
    loadFromServer() {
        let table = this
        if(this.development_id!=''){
            let jqxhr = $.get( window.location.origin+'/development/waiting_time/'+this.development_id)
                .done(function (data){
                    if(table.numberOfApplications==data.length){
                        data.forEach(function (item,index){
                            table.appendRow(item.application, item.waitTime)
                        })
                    }
                    else{
                        let numberOfApplications = parseInt($("input[name='applications']").val())
                        table.notInServer(numberOfApplications)
                    }
                })
                .fail(
                    function (){
                        let numberOfApplications = parseInt($("input[name='applications']").val())
                        table.notInServer(numberOfApplications)
                    })
        }
        else{
            let numberOfApplications = parseInt($("input[name='applications']").val())
            table.notInServer(numberOfApplications)
        }
    }

    saveOnServer(){
        let table = this
        let data = {}
        data.waitingTimes = table.getValues()
        if(this.development_id!=''){
            data.development_id = this.development_id
            console.log("DATA TO BE SEND",data)
            let jqxhr = $.post( window.location.origin+'/development/waiting_time/', {'data': JSON.stringify(data)})
        }
    }

    getValues = () => {
        let values = $('.value').find("input").slice(1)
        let waitingTimes = []
        values.each(function (){
            let waitingTime = {}
            waitingTime['application'] = $(this).attr("name")
            waitingTime['waitingTime'] = $(this).val();
            waitingTimes.push(waitingTime)
        })
        console.log(waitingTimes)
        return waitingTimes
    }
}
//
//getValues = () => {
//    let values = $('.value').find("input").slice(1)
//    let dict = []
//    values.each(function (){
//        dict.push({
//            application_number: $(this).attr("name"),
//            waiting_time: $(this).val()
//        });
//    })
//    return dict
//}
