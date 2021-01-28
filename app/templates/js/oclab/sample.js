window.table = new Table(0, calcVol);

$(document).ready(function() {
    loadlistofsampleapps()
    createBandsTable()
    calcVol()
});

$(".change-graph-size-parameter").on("change", function(){
    changeGraphSize()
    mainCalculations()
    //createBandsTable()
    calcVol()
})

$(".change-bands-table").on("change", function(){
    createBandsTable()
})

$(".change-volume-parameter").on("change", function(){
    calcVol()
});

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
    gap_size = parseFloat($("#id_gap").val());
    band_size = parseFloat($("#id_value").val());
    property = $("#id_main_property").val();
    number_bands = parseFloat($("#id_value").val());

    working_area = nBandsWorkingArea()
    if (property=='2'){number_bands = Math.trunc(working_area[0]/(band_size+gap_size))}
    newComponentsTable(number_bands);
}
// MAIN
function mainCalculations(){
    let plate_x_size = parseFloat($("#id_size_x").val());
    let plate_y_size = parseFloat($("#id_size_y").val());

    let offset_left_size = parseFloat($("#id_offset_left").val());
    let offset_right_size = parseFloat($("#id_offset_right").val());
    let offset_top_size = parseFloat($("#id_offset_top").val());
    let offset_bottom_size = parseFloat($("#id_offset_bottom").val());

    let gap_size = parseFloat($("#id_gap").val());
    let number_bands = parseFloat($("#id_value").val());
    let band_size = parseFloat($("#id_value").val());

    let band_height = parseFloat($("#id_height").val());
    let property = $("#id_main_property").val();

  // Check if theres missing parameters
  missing_parameter = (isNaN(plate_x_size)||isNaN(plate_y_size)||isNaN(offset_left_size)||isNaN(offset_right_size)||isNaN(offset_top_size)||isNaN(offset_bottom_size)||isNaN(gap_size)||isNaN(band_height))

  if(areErrors('#id_parameter_error',missing_parameter)){return}

  // Calculate the Working Area [x,y]
  working_area = nBandsWorkingArea()

  // Check if its not posible to calculate the wa
  if(areErrors('#id_offsets_error',isNaN(working_area[0]) && isNaN(working_area[1]))){return}

  // Check if the vertical sizes is enough
  if(areErrors('#id_space_error',working_area[1]<band_height)){return}

  switch (property) {
    // N Bands
    case '1':
    //Gap process
      sum_gaps_size = totalGapLength(number_bands, gap_size)
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
  for(i=0;i<number_bands;i++){
    newdata = []
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

// Load field values with 'data' Object
function loadFieldsValues(data){
  $("#id_motor_speed").val(data.motor_speed)
  $("#id_pressure").val(data.pressure)
  $("#id_frequency").val(data.frequency)
  $("#id_temperature").val(data.temperature)
  $("#id_delta_y").val(data.delta_y)
  $("#id_delta_x").val(data.delta_x)
  $('#id_nozzlediameter').val(data.nozzlediameter)

  $('#id_zero_x').val(data.zero_x)
  $('#id_zero_y').val(data.zero_y)

  $("#id_size_x").val(data.size_x)
  $("#id_size_y").val(data.size_y)

  $("#id_offset_left").val(data.offset_left)
  $("#id_offset_right").val(data.offset_right)
  $("#id_offset_top").val(data.offset_top)
  $("#id_offset_bottom").val(data.offset_bottom)

  $("#id_main_property").val(data.main_property)
  $("#id_value").val(data.value)
  $("#id_height").val(data.height)
  $("#id_gap").val(data.gap)

  $("#id_file_name").val(data.file_name)
  $("#id_value").trigger( "change" );
  $('#id_load_sucess').html(data.file_name+' successfully loaded!')
  $("#id_load_sucess").fadeIn().delay( 800 ).fadeOut( 400 );
}

// Change the Graph sizes with the size x and y field values.
function changeGraphSize(){
  plotPreview.config.options.scales.xAxes[0].ticks.max = parseFloat($("#id_size_x").val());
  plotPreview.config.options.scales.yAxes[0].ticks.max = parseFloat($("#id_size_y").val());
  plotPreview.update();
}

// Return form data as Object
function getFormData($form){
    var unindexed_array = $form.serializeArray();
    var indexed_array = {};

    $.map(unindexed_array, function(n, i){
        indexed_array[n['name']] = n['value'];
    });

    return indexed_array;
}

// Method that control the file load
function getAsText(readFile) {

  var reader = new FileReader();

  // Read file into memory as UTF-16
  reader.readAsText(readFile, "UTF-8");

  // Handle progress, success, and errors
  reader.onload = loaded;
  reader.onerror = errorHandler;

  function loaded(evt) {
    var fileString = evt.target.result;
    console.log(fileString);
    jsonObject = JSON.parse(fileString)
    loadFieldsValues(jsonObject)
    console.log(jsonObject)
    table.loadTable(jsonObject['bands'])
    changeGraphSize()
  }
  function errorHandler(evt) {
    if(evt.target.error.name == "NotReadableError") {
      // The file could not be read
    }
  }
}

// Handles list filling with the saved sampleapps
function loadlistofsampleapps(){
  $.ajax({
    method: 'GET',
    url:    window.location.origin+'/sample/list',
    success: loadlistMethodSuccess,
    error: loadlistMethodError,
  })
  function loadlistMethodSuccess(data, textStatus, jqXHR){
    $('#list-load').empty()
    $.each(data, function(key, value) {
        element = $("<a></a>").text(value[0])
        element.attr('value_saved',value[1])
        element.addClass('list-group-item list-group-item-action py-1')
        element.attr('id',value[1])
        element.attr('role','tab')
        element.attr('href','#list-home')
        element.attr('data-toggle','list')
        element.attr('aria-controls',"home")
        $('#list-load').append(element)
        })
    $('.list-group-item').on('click', function (e) {
            e.preventDefault()
            url = window.location.origin+'/sample/load/'+$(this).attr('value_saved')
            $.ajax({
              method: 'GET',
              url:    url,
              data:   data,
              success: loadMethodSuccess,
              error: loadMethodError,
            })
            function loadMethodSuccess(data, textStatus, jqXHR){
              // Load all the fields with the ones get in the database
                loadFieldsValues(data);
                table.getTableValues()
                table.loadTable(data.bands)
                changeGraphSize()
                calcVol()
            }
            function loadMethodError(jqXHR, textStatus, errorThrown){}
        })
    }
  function loadlistMethodError(jqXHR, textStatus, errorThrown){}
}

// Endpoints
$('#stopbttn').on('click', function (e) {
  e.preventDefault()
  $formData = 'STOP&'
  $endpoint = window.location.origin+'/oclab/control/',
  $.ajax({
  method: 'POST',
  url:    $endpoint,
  data:   $formData,
  success: stopMethodSuccess,
  error: stopMethodError,
  })
  function stopMethodSuccess(data, textStatus, jqXHR){
    console.log(data);
    $('.control-bttn').removeClass('btn-success btn-secondary')
    $('.control-bttn').addClass('btn btn-danger')
  }
  function stopMethodError(jqXHR, textStatus, errorThrown){}
})
$('#pausebttn').on('click', function (e) {
  e.preventDefault()
  //
  $formData = 'PAUSE&'
  $endpoint = window.location.origin+'/oclab/control/',
  $.ajax({
  method: 'POST',
  url:    $endpoint,
  data:   $formData,
  success: pauseMethodSuccess,
  error: pauseMethodError,
  })
  function pauseMethodSuccess(data, textStatus, jqXHR){
    console.log(data);
      $('.control-bttn').removeClass('btn-success btn-danger')
    $('.control-bttn').addClass('btn btn-secondary')
  }
  function pauseMethodError(jqXHR, textStatus, errorThrown){}
})
$('#startbttn').on('click', function (e) {
  e.preventDefault()
  //
  $formData = 'START&'+$('#plateform').serialize()+'&'+$('#movementform').serialize()+'&'+$('#saveform').serialize()+'&'+$('#zeroform').serialize()+'&table='+JSON.stringify(table.getTableValues())
  $endpoint = window.location.origin+'/sampleapp/'
  $.ajax({
  method: 'POST',
  url:    $endpoint,
  data:   $formData,
  success: startMethodSuccess,
  error: startMethodError,
  })
  function startMethodSuccess(data, textStatus, jqXHR){
    //console.log(data);
    $('.control-bttn').removeClass('btn-danger btn-secondary')
    $('.control-bttn').addClass('btn btn-success')
  }
  function startMethodError(jqXHR, textStatus, errorThrown){}
})
$('#savebttn').on('click', function (e) {
  event.preventDefault()
  $formData = $('#plateform').serialize()+'&'+$('#movementform').serialize()+'&'+$('#saveform').serialize()+'&'+$('#zeroform').serialize()+'&table='+JSON.stringify(table.getTableValues())
  $endpoint = window.location.origin+'/sample/save/'
  $.ajax({
  method: 'POST',
  url:    $endpoint,
  data:   $formData,
  success: saveMethodSuccess,
  error: saveMethodError,
  })
  function saveMethodSuccess(data, textStatus, jqXHR){
    console.log(typeof(data.error));
    if(data.error==undefined){
      $('#id_save_sucess').html(data.message)
      $("#id_save_sucess").fadeIn().delay( 800 ).fadeOut( 400 );
    }
    else {
      $('#id_save_error').html(data.error)
      $( "#id_save_error" ).fadeIn().delay( 800 ).fadeOut( 400 );
    }
    //console.log("funciono");
    loadlistofsampleapps();
  }
  function saveMethodError(data, jqXHR, textStatus, errorThrown){
    console.log(data);
    $('#id_save_error').html(data.error)
    $( "#id_save_error" ).fadeIn().delay( 800 ).fadeOut( 400 );
  }
})

var calcVol = function calcVol(){
  $formData = $('#plateform').serialize()+'&'+$('#movementform').serialize()+'&table='+JSON.stringify(table.getTableValues())
  $endpoint = window.location.origin+'/samplecalc/'
  $.ajax({
  method: 'POST',
  url:    $endpoint,
  data:   $formData,
  success: calcMethodSuccess,
  error: calcMethodError,
  })
  function calcMethodSuccess(data, textStatus, jqXHR){
    table.setTableCalculationValues(data.results)
    console.log(data.results)
  }
  function calcMethodError(jqXHR, textStatus, errorThrown){
      alert("Error calculating estimated volumes")
    }
}







