class listOfSaved{
    constructor(save_url, list_url, get_url, saveEvent){
        this.save_url = save_url;
        this.list_url = list_url;
        this.get_url = get_url;
        this.saveEvent = saveEvent;
    }

    loadList(){
        // Query the elements
        let mainList = this;
        $.get( this.list_url, function( elements ) {
            elements.forEach(element => mainList.$addToList(element))
        }).done(function (e){
            mainList.$loadEventsHandler();
            $("#list-load a").first().trigger("click")
        });
    }

    $addToList(element){
        //Add the new item to the List
        let newListObject = this.$newListElement(element[0],element[1])
        $('#list-load').append(newListObject)
    }

    $newListElement(text, db_id){
        // Creates the new element in list
        let mainList = this;

        let flex_container = $("<div class=\"d-flex flex-row justify-content-between align-items-center\"></div>")
        let element = $("<a class=\"saved_element\" style=\"width:100%\">"+ text +"</a>")
        let trash_can = $("<i class=\"fas fa-trash saved_element_trash_can\"></i>")

        flex_container.addClass('list-group-item list-group-item-action py-1')
        flex_container.attr('role','tab')
        flex_container.attr('href','#list-home')
        flex_container.attr('data-toggle','list')
        flex_container.attr('aria-controls',"home")

        element.attr('value_saved',db_id)

        flex_container.append(element,trash_can)
        return flex_container
    }

    $loadEventsHandler(){
        this.$click_new_button_handler()
        this.$click_save_button_handler()
        this.$click_rename_button_handler()
        this.$delete_element_handler()
        this.$click_element_handler()
    }

    $click_element_handler(){
        let mainList = this;
        $(".saved_element").on("click", function (e){
            mainList.$get_element_data($(this))
        })
    }

    $delete_element_handler(){
        let mainList = this;
        $(".saved_element_trash_can").on("click mouseover mouseout", function (e){
            switch (e.type){
                case "click":
                    mainList.$delete_element($(this).siblings('a'))
                    break;
                case "mouseover":
                    $(this).animate({
                        opacity: '0.3'
                    });
                    break;
                case "mouseout":
                    $(this).animate({
                        opacity: '1'
                    });
                    break;
            }
        })
    }

    $click_rename_button_handler(){
        //    FALTA MANDAR A API PARA RENOMBRAR
        $("#rename_bttn").on("click",function (){
            let id = $("#selected-element-id").val()
            let name = $("new_filename").val()
        })
    }

    $click_new_button_handler(){
        $("#new_method_bttn").on("click",function(){
            $("#list-load").find("a.active").removeClass("active")
            $('#new_filename').val("")
            $('#selected-element-id').val("")
            $('#rename_bttn').hide()
        })
    }

    $click_save_button_handler(){
        //    FALTA MANDAR A API PARA guardar
        let mainList = this;
        $("#save_bttn").on("click",function (){
            data = mainList.saveEvent()
            mainList.$save(data)
        })
    }

    $save(data){
        let mainList = this;
        var jqxhr = $.post( mainList.save_url, data,function() {
//          alert( "success" );
        })
        .done(function(data) {
//        alert( "second success" );
        console.log(data)
        })
        .fail(function(data) {
//        alert( "error" );
        })
        .always(function(data) {
//        alert( "finished" );
        });
    }

    $delete_element(object){
        console.log(object.attr("value_saved"))
    }


    $get_element_data(e){
        //Gets the data save it in data_received
        let mainList = this;
        $.get(this.get_url+"/"+e.attr('value_saved')+"/").done(function (data){
            mainList.data_recieved = data
            $('#new_filename').val(data.file_name)
            $('#selected-element-id').val(data.id)
            $('#rename_bttn').show()
            console.log(data)
        })
    }
}






