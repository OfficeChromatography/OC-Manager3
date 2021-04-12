class listOfSaved{
    constructor(save_url, list_url, get_url, saveEvent, loadEvent, delete_app_url){
        this.save_url = save_url;
        this.list_url = list_url;
        this.get_url = get_url;
        this.saveEvent = saveEvent;
        this.loadEvent = loadEvent;
        this.delete_app_url = delete_app_url;

        this.$click_new_button_handler()
        this.$click_save_button_handler()
        this.$click_export_button_handler()
    }

    loadList(){
        // Query the elements
        let mainList = this;
        $.get( this.list_url, function( elements ) {
            mainList.$cleanList()
            elements.forEach(element => mainList.$addToList(element))
        }).done(function (e){
            if($("#list-load").children().length>0){
                mainList.$loadEventsHandler();
                $("#list-load a").first().trigger("click")
            }
            else{
                $("#new_method_bttn").trigger("click")
            }
        });
    }

    $cleanList(){
        $('#list-load').empty()
    }

    $addToList(element){
        //Add the new item to the List
        let newListObject = this.$newListElement(element[0],element[1],element[2])
        $('#list-load').append(newListObject)
    }

    $newListElement(text, db_id, iconOpacity){
        // Creates the new element in list
        let mainList = this;
        console.log(iconOpacity)
        let flex_container = $("<div class=\"d-flex py-0 flex-row justify-content-between align-items-center\"></div>")
        let element = $("<a class=\"saved_element py-2\" style=\"width:100%\">"+ text +"</a>")
        let icons = $("<i class=\"fas fa-eye-dropper\" style=\"padding-right:5px;opacity:"+iconOpacity[0]+";\"></i><i class=\"fas fa-shower\" style=\"padding-right:5px;opacity:"+iconOpacity[1]+";\"></i><i class=\"fas fa-spray-can\" style=\"padding-right:5px;opacity:"+iconOpacity[2]+";\"></i><i class=\"fas fa-microscope\" style=\"padding-right:20px;opacity:"+iconOpacity[3]+";\"></i>")
        let trash_can = $("<i class=\"fas fa-trash saved_element_trash_can\"></i>")

        flex_container.addClass('list-group-item list-group-item-action')
        flex_container.attr('role','tab')
        flex_container.attr('href','#list-home')
        flex_container.attr('data-toggle','list')
        flex_container.attr('aria-controls',"home")

        element.attr('value_saved',db_id)

        flex_container.append(element,icons,trash_can)
        return flex_container
    }

    $loadEventsHandler(){
        this.$click_element_handler()
        this.$delete_element_handler()
    }

    $click_element_handler(){
        let mainList = this;
        $(".saved_element").on("click", function (e){
            mainList.$get_element_data($(this))
        })
    }

    $delete_element_handler(){
        let mainList = this;
        $(".saved_element_trash_can").on("dblclick click mouseover mouseout", function (e){
            switch (e.type){
                case "dblclick":
                    mainList.$delete_element($(this).siblings('a'))
                    break;
                case "click":
                    mainList.$delete_element_app($(this).siblings('a'))
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

    $click_new_button_handler(){
        $("#new_method_bttn").on("click",function(){
            $("#list-load").find("a.active").removeClass("active")
            $('#new_filename').val("")
            $('#selected-element-id').val("")
        })
    }

    $click_save_button_handler(){
        let mainList = this;
        $("#save_bttn").on("click",function (e){
            e.preventDefault()
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
            mainList.loadList()
        })
        .fail(function(data) {
//        alert( "error" );
        })
        .always(function(data) {
//        alert( "finished" );
        });
    }

    $delete_element(object){
        let mainList = this;
        $.ajax({
            url: mainList.get_url+"/"+object.attr("value_saved"),
            type: 'DELETE',
        }).done(function (){
            mainList.loadList()
        })
    }

    $delete_element_app(object){
        let mainList = this;
        $.ajax({
            url: mainList.delete_app_url+"/"+object.attr("value_saved"),
            type: 'DELETE',
        }).done(function (){
            mainList.loadList()
        })
    }


    $get_element_data(e){
        //Gets the data save it in data_received
        let mainList = this;
        $.get(this.get_url+"/"+e.attr('value_saved')+"/").done(function (data){
            mainList.data_recieved = data
            $('#new_filename').val(data.filename)
            $('#selected-element-id').val(data.id)
            console.log(data)
            mainList.loadEvent(data)
        })
    }

    $click_export_button_handler(){
        let mainList = this;
        $("#export_bttn").on("click",function (e){
            e.preventDefault();
            mainList.$exportToCsv();
        })
    }

    $exportToCsv = function(){
        let data = $('form').serializeArray();
        let filename = $(".active").find(".saved_element").text();
      
        let csvContent = "data:text/csv;charset=utf-8,";
      
        data.forEach(function(dataPart) {
            let row = [dataPart["name"], dataPart["value"]]
            csvContent += row + "\r\n";
        });
      
        var encodedUri = encodeURI(csvContent);
        var link = document.createElement("a");
        link.setAttribute("href", encodedUri);
        link.setAttribute("download", filename + ".csv");
        document.body.appendChild(link); // Required for FF
      
        link.click();
      }
}






