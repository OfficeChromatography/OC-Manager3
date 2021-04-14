var list_of_saved = new listOfSaved("http://127.0.0.1:8000/evaluation/save/",
"http://127.0.0.1:8000/evaluation/list",
"http://127.0.0.1:8000/evaluation/load",
getData,
setData,
"http://127.0.0.1:8000/evaluation/deleteall"
);
  
function getData(){
//     //check if this is working, because saving is done using take photo
//     imageID = $("#image_id").attr("alt")
//     data = $('form').serialize()+'&colorSelected'
//     +JSON.stringify(colorSelected)
//     +'&image_id='+imageID+'&note='+$('#notestextarea').val()
//     // +'&id='+$('[aria-selected="true"]').find("a").attr("value_saved")
//     console.log(data)
// return data
    return {}
};

function setData(data){
    id_list = data.id_list
    console.log(id_list)
    url = data.url
    $(".show-image").empty()
    if (id_list != undefined ){
        length = id_list.length
        width = 100 / length
        for (var i=0; i<length; i++) {
            console.log(url[i])
            $(".show-image").append('<img id="'+id_list[i]+'" src='+url[i]+' onclick="selectImage('+id_list[i]+',['+id_list+']);"  style="width:'+width+'%">')
        }
    }
};

function selectImage(imageID, idList){
    length = idList.length
    width = 100 / length
    zoom = 1.4
    for (var i=0; i<length; i++) {
        if (imageID == idList[i]) {
            string = "width:" + width*zoom + "%"
            $("#"+imageID).attr("style",string)
        } else {
            newWidth = (100 - width*zoom) / (length - 1)
            string = "width:" + newWidth + "%"
            $("#"+idList[i]).attr("style",string)
        }
    }
};

function getBandSetup(){
    methodID= $('[aria-selected="true"]').find("a").attr("value_saved")
    $.get(window.location.origin+'/evaluation/bandsetup/'+methodID+"/").done(function (data){
        if (data.main_property == 1){
            number_of_tracks = parseInt(data.value)
            track_width = (data.size_x - data.offset_left - data.offset_right ) / number_of_tracks - (number_of_tracks - 1) * data.gap
        } else {
            track_width = parseInt(data.value)
            number_of_tracks = - (track_width - data.gap) / (2 * data.gap) 
            + Math.sqrt(((track_width - data.gap) / (2 * data.gap))**2 + (data.size_x - data.offset_left - data.offset_right) / data.gap)
        }
        bands_start = parseInt(data.offset_left)
        return {number_of_tracks, track_width, bands_start}
    })
}

$(document).ready(function() {
    list_of_saved.loadList()
});