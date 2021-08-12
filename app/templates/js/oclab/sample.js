window.table = new Table(0);

//

//
// $(document).ready(function() {
//     createBandsTable()
//     calcVol()
//     list_of_saved.loadList()
// });
//



let loadListEvent = async () => {
    let method = localStorage.getItem("method")
    if(method){
        return await getSampleApps(method)
    }else{
        alert("Please Select a Method!")
    }
}

let getDataFromForm = (class_id) => {
    let obj = {}
    $(`.${class_id}`).each(function( index ) {
        obj[$( this ).attr('name')] = $( this ).val()
    })
    return obj
}

let setDataInForm = (obj, class_id) => {
    $(`.${class_id}`).each(function( index ) {
        let property = $(this).attr('name')
        $(this).val(obj[property])
    })
    $(".change-graph-size-parameter").trigger("change")
    // table.loadTable(data.bands_components)
}

function formData(filename){
    return {
        filename: filename,
        method: localStorage.getItem("method"),
        application_settings: getDataFromForm('application_settings'),
        band_settings: getDataFromForm("band_settings"),
        step_settings: getDataFromForm("step_settings"),
        zero_position: getDataFromForm("zero_position"),
        plate_size: getDataFromForm("plate_size"),
        offset: getDataFromForm("offset"),
        band_components: table.getTableValues(),
    }
}

let createEvent = async (filename) => {
    let data = formData(filename)
    let res = await createSampleApp(data)
}

let updateEvent = async (id, filename) => {
    let data = formData(filename)
    let res = await updateSampleApp(id, data)
}

let loadEvent = async (sample_id) => {
    let data = await getSampleApp(sample_id)
    localStorage.setItem("sample_id", data.id)
    for (const [key, value] of Object.entries(data)) {
        setDataInForm(value,key)
    }
    return data
}

let deleteEvent = async (id) => {
    let res =  await deleteSampleApp(id)
    return res
}

let list_of_saved = new listOfSaved( loadListEvent,
    createEvent,
    updateEvent,
    loadEvent,
    deleteEvent
)

let startEvent = async () => {
    return await startSampleApp(formData())
}

let stopEvent = async () => {
    return await controlMachineApp({'method':'STOP'})
}

let resumeEvent = async () => {
    return await controlMachineApp({'method':'RESUME'})
}

let pauseEvent = async () => {
    return await controlMachineApp({'method':'PAUSE'})
}


let application_control = new ApplicationControl(
    startEvent,
    stopEvent,
    pauseEvent,
    resumeEvent)

$(document).ready(function() {
    list_of_saved.loadList()
    createBandsTable()
    calcVol()
});



$(".change-graph-size-parameter").on("change", function(){
    plotPreview.changeGraphSize($('#id_size_x').val(),$('#id_size_y').val())
    mainCalculations()
    // calcVol()
})


$(".change-bands-table").on("change", function(){
    createBandsTable()
    // calcVol()
})

$(".change-volume-parameter").on("change", function(){
    // calcVol()
});
//

$("#id_main_property").on("change",function(){
        switch ($("#id_main_property").val()) {
            case '1':
                $("#id_valuesform").fadeOut();
                $("#id_valuesunit").html('#');
                $("#id_valuesform").fadeIn();
                $("#lengthbandsrow").hide();
                $("#nbandsrow").show();
                $("#valueLabel").text('Number')
                break;
            case '2':
                $("#id_valuesform").fadeOut();
                $("#id_valuesunit").html('[mm]');
                $("#id_valuesform").fadeIn();
                $("#bandlengthform").fadeIn();
                $("#nbandsrow").hide();
                $("#lengthbandsrow").show();
                $("#valueLabel").text('Length')
                break;
        }
        createBandsTable()
        $('.change-graph-size-parameter').trigger("change")
    });


function createBandsTable(){
    let data = formData().band_settings

    let gap_size = parseFloat(data.gap);
    let value = parseFloat(data.value);
    let property = data.main_property;

    let working_area = nBandsWorkingArea()
    if (property=='2'){value = Math.trunc(working_area[0]/(value+gap_size))}
    newComponentsTable(value);
}

// MAIN
function mainCalculations(){
    let data = formData()

    let plate_x_size = parseFloat(data.plate_size.x);
    let plate_y_size = parseFloat(data.plate_size.y);

    let offset_left_size = parseFloat(data.offset.left);
    let offset_right_size = parseFloat(data.offset.right);
    let offset_top_size = parseFloat(data.offset.top);
    let offset_bottom_size = parseFloat(data.offset.bottom);

    let gap_size = parseFloat(data.band_settings.gap);
    let number_bands = parseFloat(data.band_settings.value);
    let band_size = parseFloat(data.band_settings.value);

    let band_height = parseFloat(data.band_settings.height);
    let property = data.band_settings.main_property;

  // Check if theres missing parameters
  let missing_parameter = (isNaN(plate_x_size)||isNaN(plate_y_size)||isNaN(offset_left_size)||isNaN(offset_right_size)||isNaN(offset_top_size)||isNaN(offset_bottom_size)||isNaN(gap_size)||isNaN(band_height))

  if(areErrors('#id_parameter_error',missing_parameter)){return}

  // Calculate the Working Area [x,y]
  let working_area = nBandsWorkingArea()

  // Check if its not posible to calculate the wa
  if(areErrors('#id_offsets_error',isNaN(working_area[0]) && isNaN(working_area[1]))){return}

  // Check if the vertical sizes is enough
  if(areErrors('#id_space_error',working_area[1]<band_height)){return}

  switch (property) {
    // N Bands
    case '1':
    //Gap process
      let sum_gaps_size = totalGapLength(number_bands, gap_size)
      if(areErrors('#id_gap_error',isNaN(sum_gaps_size) || sum_gaps_size>= working_area[0])){return}

    //Bands Sizes
      band_size = totalBandsLength(working_area,sum_gaps_size,number_bands)
      if(areErrors('#id_space_error',isNaN(band_size))){return}
      break;
    // Length
    case '2':
      number_bands = Math.trunc(working_area[0]/(band_size+gap_size))
      if(areErrors('#id_space_error',number_bands<1)){return}
      break;
  }

  plotPreview.eliminateAllPoints()
  for(let i=0;i<number_bands;i++){
    let newdata = []
    if(i==0){
      newdata[0]={y:offset_bottom_size,x:offset_left_size}
      newdata[1]={y:offset_bottom_size+band_height,x:offset_left_size}
      newdata[2]={y:offset_bottom_size+band_height,x:band_size+offset_left_size}
      newdata[3]={y:offset_bottom_size,x:band_size+offset_left_size}
      newdata[4]=newdata[0]
    }
    else{
      newdata[0]={y:offset_bottom_size,x:i*(band_size+gap_size)+offset_left_size}
      newdata[1]={y:offset_bottom_size+band_height,x:i*(band_size+gap_size)+offset_left_size}
      newdata[2]={y:offset_bottom_size+band_height,x:(i+1)*band_size+(gap_size*i)+offset_left_size}
      newdata[3]={y:offset_bottom_size,x:(i+1)*band_size+(gap_size*i)+offset_left_size}
      newdata[4]=newdata[0]
    }
    plotPreview.addData2Chart(i,'black', newdata)
  }
  plotPreview.update();
}

//  ERROR DISPLAY MANAGER
function areErrors(error_id, bolean_exp){
  if(bolean_exp){
    $(error_id).fadeIn();
    return true
  }
  else{
    $(error_id).fadeOut();
    return false
  }
}

//  Calculates the Working Area
function nBandsWorkingArea(){
    let plate_x_size = parseFloat($("#id_size_x").val());
    let plate_y_size = parseFloat($("#id_size_y").val());
    let offset_left_size = parseFloat($("#id_offset_left").val());
    let offset_right_size = parseFloat($("#id_offset_right").val());
    let offset_top_size = parseFloat($("#id_offset_top").val());
    let offset_bottom_size = parseFloat($("#id_offset_bottom").val());

    working_area = [plate_x_size-offset_left_size-offset_right_size,plate_y_size-offset_top_size-offset_bottom_size]
    if(working_area[0] <= 0 || working_area[1] <= 0 || isNaN(working_area[0]) || isNaN(working_area[1])){
        return [NaN,NaN];
    }
    else{
      return working_area;
    }
}

//  Calculate the sum of gaps lenght
function totalGapLength(number_bands, gap_size){
  number_of_gaps = number_bands - 1;
  if(number_of_gaps<0){
    return NaN
  }
  else{
    return gap_size*number_of_gaps;
  }
}


//  Calculate the sum of bands lenght
function totalBandsLength(working_area,sum_gaps_size,number_bands){
  bands_size = (working_area[0]-sum_gaps_size)/number_bands
  if(bands_size<=0){
    return NaN
  }
  else{
    return bands_size
  }
}


// Create a new Table with a given number of rows
function newComponentsTable(number_row){
    table.destructor()
    table = new Table(number_row, calcVol);
}


let calcVol = async function calcVol(){

    let data = {
        filename: $('#filename').val(),
        method: localStorage.getItem("method"),
        sample_application: localStorage.getItem("sample_id"),
        application_settings: getDataFromForm('application_settings'),
        band_settings: getDataFromForm("band_settings"),
        step_settings: getDataFromForm("step_settings"),
        zero_position: getDataFromForm("zero_position"),
        plate_size: getDataFromForm("plate_size"),
        offset: getDataFromForm("offset"),
        table: table.getTableValues()
    }
    return await tableDataRequest(data)
}





