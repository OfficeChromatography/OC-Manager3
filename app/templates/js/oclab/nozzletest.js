function loadSelectedVariation(){
    var j = 0
    if ($('#id_pressure_axis').val()!= ""){
        j += 1
        $('#pressure-variation').show()
        $("#pressure_start").text("Start")
    } else {
        $('#pressure-variation').hide()
        $("#pressure_start").text("Value")
    }
    if ($('#id_frequency_axis').val()!= ""){
        j+=1
        $('#frequency-variation').show()
        $("#frequency_start").text("Start")
    } else {
        $('#frequency-variation').hide() 
        $("#frequency_start").text("Value")
    }
    if ($('#id_deltax_axis').val()!= ""){
        j+=1
        $('#deltax-variation').show()
        $("#deltax_start").text("Start")
    } else {
        $('#deltax-variation').hide() 
        $("#deltax_start").text("Value")
    }
    if (j!=2){
        //load alert
    }
}

$('.change-volume-parameter').change(function() {
    loadSelectedVariation();
}); 

var getData = function(){
    data = $("form").serialize()
    return data
}

var setData = function (data){
    $.each(data,function (key,value,array){
        $('input[name='+key+']').val(value)
        if(key=="pressure_axis" || key=="frequency_axis" || key=="deltax_axis"){
            $("#id_"+key).val(value)
        }
    })
  loadSelectedVariation();
}

var list_of_saved = new listOfSaved("http://127.0.0.1:8000/nozzletest/save/",
    "http://127.0.0.1:8000/nozzletest/list",
    "http://127.0.0.1:8000/nozzletest/load",
    getData,
    setData,
    "http://127.0.0.1:8000/nozzletest/delete",
    )

var application_control = new ApplicationControl('http://127.0.0.1:8000/oclab/control/',
                                                'http://127.0.0.1:8000/nozzletest/start/',
                                                getData)

$(document).ready(function() {
    list_of_saved.loadList();
    loadSelectedVariation();
  });