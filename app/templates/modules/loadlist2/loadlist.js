class listOfSaved{
    constructor(loadListEvent, createEvent, updateEvent,loadEvent, deleteEvent){
        this.loadListEvent = loadListEvent;
        this.createEvent = createEvent;
        this.loadEvent = loadEvent;
        this.deleteEvent = deleteEvent;
        this.updateEvent = updateEvent;

        this.$click_new_button_handler()
        this.$click_save_button_handler()
        this.$click_export_button_handler()

    }

     $renderListInScreen = (elements) => {
        // Render list of saved in screen
        this.$cleanList()
        elements.forEach(element => this.$addToList(element))
    }

    $afterListRendered = (selected_id) => {
        // After rendering, load the first or create a new
        if($("#list-load").children().length>0){
            this.$loadEventsHandler();
            if(selected_id){
                $(`[value_saved=${selected_id}]`).trigger("click")
            }else {
                $("#list-load a").first().trigger("click")
            }
        }
        else{
            $("#new_method_bttn").trigger("click")
        }
    }

    loadList = async () => {
        let selected_id = $('.list-group-item-action.active').find('a').attr('value_saved')
        let saved_elements = await this.loadListEvent()
        this.$renderListInScreen(saved_elements)
        this.$afterListRendered(selected_id)
    }

    $cleanList(){
        // Removes all the elements from the DOM list
        $('#list-load').empty()
    }

    $addToList(element){
        //Add the new item to the List
        let newListObject = this.$newListElement(element.filename,element.id, {})
        $('#list-load').append(newListObject)
    }

    $newListElement(text, db_id, iconOpacity){
        // Creates the new element in list
        let flex_container = $("<div class=\"d-flex py-0 flex-row justify-content-between align-items-center\"></div>")
        let element = $("<a class=\"saved_element py-2\" style=\"width:100%\">"+ text +"</a>")
        let trash_can = $("<i class=\"fas fa-trash saved_element_trash_can\"></i>")

        flex_container.addClass('list-group-item list-group-item-action')
        flex_container.attr('role','tab')
        flex_container.attr('href','#list-home')
        flex_container.attr('data-toggle','list')
        flex_container.attr('aria-controls',"home")

        element.attr('value_saved',db_id)

        flex_container.append(element,trash_can)
        return flex_container
    }

    $loadEventsHandler(){
        this.$click_element_handler()
        this.$delete_element_handler()
    }

    $click_element_handler(){
        $(".saved_element").on("click", (e) => this.$get_element_data($(e.currentTarget)))
    }

    async $get_element_data(e){
        //Gets the data save it in data_received
        let data = await this.loadEvent(e.attr('value_saved'))
        $('#filename').val(data.filename)
        $('#app-id').val(data.id)
    }

    $delete_element_handler(){
        $(".saved_element_trash_can").on("dblclick click mouseover mouseout", (e) => {
            switch (e.type){
                case "click":
                    this.$delete_element($(e.currentTarget).siblings('a'))
                    break;
                case "mouseover":
                    $(e.currentTarget).animate({
                        opacity: '0.3'
                    });
                    break;
                case "mouseout":
                    $(e.currentTarget).animate({
                        opacity: '1'
                    });
                    break;
            }
        })
    }

    $click_new_button_handler(){
        $("#new_method_bttn").on("click",function(){
            $("#list-load").find('.active').removeClass('active')
            $('#app-id').val("")
            $('#app-id').val("")
            $('#filename').val('')
        })
    }

    $click_save_button_handler(){
        $("#save_bttn").on("click", async (e) => {
            e.preventDefault()
            let id = $('#app-id').val()
            let filename = $('#filename').val()
            if (id == '') {
                await this.createEvent(filename)
            }else{
                await this.updateEvent(id, filename)
            }
            await this.loadList()
        })
    }

    async $delete_element(object){
        let res = await this.deleteEvent(object.attr("value_saved"))
        if(res.ok){
            await this.loadList()
        }
    }

    $click_export_button_handler(){
        $("#export_bttn").on("click",(e) => {
            e.preventDefault();
            this.$exportToCsv();
        })
    }

    $exportToCsv = function(){
        // let data = $('form').serializeArray();
        let methodID = $('[aria-selected="true"]').find("a").attr("value_saved")
        $.get(window.location.origin+'/export/'+methodID+"/").done(function (data){
            let filename = $(".active").find(".saved_element").text();
            let csvContent = "data:text/csv;charset=utf-8,"+data;
            var encodedUri = encodeURI(csvContent);
            var link = document.createElement("a");
            link.setAttribute("href", encodedUri);
            link.setAttribute("download", filename + ".csv");
            document.body.appendChild(link); // Required for FF
            link.click();
        })

    };
}






