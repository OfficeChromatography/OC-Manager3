// Execute every time something happens wi
// let flowRateChart = new flowRateGraph()

$(".development-flowrate-insidence").on("change", function (){
  flowrateCalc()
})


$(".change-graph-size-parameter").on("change", function(){
  plotPreview.changeGraphSize()
  mainCalculations()
})

$("#id_fluid").change(function(){
  $(this).val()=='Specific' ? $('#specificFluidTable').show() : $('#specificFluidTable').hide()
});


// MAIN
function mainCalculations(){
  let plate_x_size = parseFloat($("#id_size_x").val());
  let plate_y_size = parseFloat($("#id_size_y").val());

  let offset_left_size = parseFloat($("#id_offset_left").val());
  let offset_right_size = parseFloat($("#id_offset_right").val());
  let offset_top_size = parseFloat($("#id_offset_top").val());
  let offset_bottom_size = parseFloat($("#id_offset_bottom").val());

  let volume = parseFloat($("#id_volume").val());
  let printBothways = $('#printBothwaysButton').text();

  let band_height = 0.1;


  // Check if theres missing parameters
  missing_parameter = (isNaN(plate_x_size)||isNaN(plate_y_size)||isNaN(offset_left_size)||isNaN(offset_right_size)||isNaN(offset_top_size)||isNaN(offset_bottom_size)||isNaN(volume))

  if(areErrors('#id_parameter_error',missing_parameter)){return}

  // Calculate the Working Area [x,y]
  working_area = nBandsWorkingArea(plate_x_size,offset_left_size,offset_right_size,plate_y_size,offset_top_size,offset_bottom_size)

  // Check if its not posible to calculate the wa
  if(areErrors('#id_offsets_error',isNaN(working_area[0]) && isNaN(working_area[1]))){return}

  // Check if the vertical sizes is enough
  if(areErrors('#id_space_error',working_area[1]<band_height)){return}

  band_size = working_area[0]

  plotPreview.eliminateAllPoints()
  newdata = []
  newdata[0]={y:offset_bottom_size,x:offset_left_size}
  newdata[1]={y:offset_bottom_size+band_height,x:offset_left_size}
  newdata[2]={y:offset_bottom_size+band_height,x:band_size+offset_left_size}
  newdata[3]={y:offset_bottom_size,x:band_size+offset_left_size}
  newdata[4]=newdata[0]
  plotPreview.addData2Chart('1','black', newdata)
}

//Calculates the Working Area
function nBandsWorkingArea(plate_x_size,offset_left_size,offset_right_size,plate_y_size,offset_top_size,offset_bottom_size){
  working_area = [plate_x_size-offset_left_size-offset_right_size,plate_y_size-offset_top_size-offset_bottom_size]
  if(working_area[0] <= 0 || working_area[1] <= 0 || isNaN(working_area[0]) || isNaN(working_area[1])){
    return [NaN,NaN];
  }
  else{
      return working_area;
  }
}


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
    $('.control-bttn').removeClass('btn-success btn-secondary').addClass('btn btn-danger')
  }
  function stopMethodError(jqXHR, textStatus, errorThrown){}
})
$('#pausebttn').on('click', function (e) {
  e.preventDefault()
  $formData = 'PAUSE&'
  $endpoint = window.location.origin+'/oclab/control/'
  $.ajax({
  method: 'POST',
  url:    $endpoint,
  data:   $formData,
  success: pauseMethodSuccess,
  error: pauseMethodError,
  })
  function pauseMethodSuccess(data, textStatus, jqXHR){
    console.log(data);
    $('.control-bttn').removeClass('btn-success btn-danger').addClass('btn btn-secondary')
  }
  function pauseMethodError(jqXHR, textStatus, errorThrown){}s
})
$('#startbttn').on('click', function (e) {
  e.preventDefault()
  $formData = 'START&'+$('#plateform').serialize()+'&'+$('#pressureform').serialize()+'&'+$('#saveform').serialize()
  +'&'+$('#zeroform').serialize()+getSpecificFluid(true)+flowGraph.saveSegment(true)
  $endpoint = window.location.origin+'/developmentplay/'
  $.ajax({
  method: 'POST',
  url:    $endpoint,
  data:   $formData,
  success: startMethodSuccess,
  error: startMethodError,
  })
  function startMethodSuccess(data, textStatus, jqXHR){
    console.log(data);
    $('.control-bttn').removeClass('btn-danger btn-secondary').addClass('btn btn-success')
  }
  function startMethodError(jqXHR, textStatus, errorThrown){}
})
$('#savebttn').on('click', function (e) {
  e.preventDefault()
  let $formData = $('#plateform').serialize()+'&'+$('#pressureform').serialize()+'&'+$('#saveform').serialize()
  +'&'+$('#zeroform').serialize()+getSpecificFluid(true)+flowGraph.saveSegment(true)
  let $endpoint = window.location.origin+'/development/save/'
  $.ajax({
    method: 'POST',
    url:    $endpoint,
    data:   $formData,
    success: saveMethodSuccess,
    error: saveMethodError,
  })
  function saveMethodSuccess(data, textStatus, jqXHR){
    console.log(typeof(data.error));
    if(data.error===undefined){
      $('#id_save_sucess').html(data.message)
      $( "#id_save_sucess" ).fadeIn().delay( 800 ).fadeOut( 400 );
    }
    else {
      $('#id_save_error').html(data.error)
      $( "#id_save_error" ).fadeIn().delay( 800 ).fadeOut( 400 );
    }


  }
  function saveMethodError(jqXHR, textStatus, errorThrown){
    console.log(data);
    $('#id_save_error').html(data.error)
    $( "#id_save_error" ).fadeIn().delay( 800 ).fadeOut( 400 );
  }
})
$('#list-load a').on('click', function (e) {
  e.preventDefault()
  data={'filename':$(this)[0].innerHTML}
  $.ajax({
    method: 'GET',
    url:    window.location.origin+'/developmentsave/',
    data:   data,
    success: loadMethodSuccess,
    error: loadMethodError,
  })
  function loadMethodSuccess(data, textStatus, jqXHR){
    // Load all the fields with the ones get in the database
    $("#id_speed").val(data.speed)
    $("#id_pressure").val(data.pressure)
    // $("#id_frequency").val(data.frequency)
    $("#id_temperature").val(data.temperature)
    // $("#id_delta_x").val(data.delta_x)
    $('#id_nozzlediameter').val(data.nozzlediameter)

    $("#id_zero_x").val(data.zero_x)
    $("#id_zero_y").val(data.zero_y)

    $("#id_size_x").val(data.size_x)
    $("#id_size_y").val(data.size_y)

    $("#id_offset_left").val(data.offset_left)
    $("#id_offset_right").val(data.offset_right)
    $("#id_offset_top").val(data.offset_top)
    $("#id_offset_bottom").val(data.offset_bottom)

    $("#id_volume").val(data.volume)
    $("#id_applications").val(data.applications)
    $("#id_precision").val(data.precision)
    $("#id_waitTime").val(data.waitTime)
    $("#id_description").val(data.description)

    if (data.printBothways==='On') {
      $("#printBothwaysButton").text('On');
    } else {
      $("#printBothwaysButton").text('Off');
    }

    $('#id_fluid').val(data.fluid)

    if (data.fluid === 'Specific') {
      $('#specificFluidTable').show()
    } else {
      $('#specificFluidTable').hide()
    }

    $('#densityval').text(data.density)
    $('#viscosityval').text(data.viscosity)

    $('#id_load_sucess').html(data.file_name+' successfully loaded!')
    $( "#id_load_sucess" ).fadeIn().delay( 800 ).fadeOut( 400 );
    mainCalculations()
    plotPreview.changeGraphSize()
    flowGraph.loadSegment(data.flowrate)
  }
  function loadMethodError(jqXHR, textStatus, errorThrown){
    console.log('error');
  }
})


function getSpecificFluid(toString){
  data = {}
  data['fluid'] = $('#id_fluid').val()
  data['printBothways'] = $('#printBothwaysButton').text()
  data['volume'] = $('#id_volume').val()
  data['density'] = $('#densityval').text()
  data['viscosity'] = $('#viscosityval').text()
  data['applications'] = $('#id_applications').val()
  data['precision'] = $('#id_precision').val()
  data['waitTime'] = $('#id_waitTime').val()
  data['description'] = $('#id_description').val()

  if(toString){
    data = '&devBandSettings='+JSON.stringify(data)
  }
  return data
}

$('#printBothwaysButton').on('click', function (e) {
  e.preventDefault()
  if ($('#printBothwaysButton').text()=='Off') {
    $("#id_printBothways").prop('checked', true);
    $('#printBothwaysButton').text('On');
    $('#printBothways_resume').text('On');
  } else {
    $("#id_printBothways").prop('checked', false);
    $('#printBothwaysButton').text('Off');
    $('#printBothways_resume').text('Off');
  }
})


// Import/Export DATA
$('#downloadfilebttn').on('click', function (e) {
  event.preventDefault()
  var element = document.createElement('a');

  var plate = getFormData($('#plateform'))
  var pressure = getFormData($('#pressureform'))
  var zero = getFormData($('#zeroform'))
  var table = getSpecificFluid(false)
  
  items = Object.assign(plate,pressure,table,zero)

  content = JSON.stringify(items);
  filename = new Date().toLocaleString()+".json"

  element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(content));
  element.setAttribute('download', filename);
  element.style.display = 'none';
  document.body.appendChild(element);
  element.click();
  document.body.removeChild(element);
})
$('#loadfilebttn').on('click', function (e) {
  event.preventDefault()
  var file = $('#file')[0].files[0];
  getAsText(file);
})
$('#removefilebttn').on('click', function (e) {
  $('#file').next('.custom-file-label').html('');
  $('#file').val('')
  $('#sizesfile').html('')
})
$('#file').on('change',function(e){
                //get the file name
                var fileName = e.target.files[0];
                $(this).next('.custom-file-label').html(fileName.name);
            })

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
    loadMethodSuccess(jsonObject)
    console.log(jsonObject)
  }
  function errorHandler(evt) {
    if(evt.target.error.name == "NotReadableError") {
      // The file could not be read
    }
  }
}

function flowrateCalc(){
  length = $("#id_size_x").val() - $("#id_offset_left").val() - $("#id_offset_right").val();
  speed = $("#id_speed").val();
  volume = $("#id_volume").val();
  applications = $("#id_applications").val();
  time = length / speed;
  flowrate = Math.round(volume / time / applications, 3);
  $('#flowrate').text('estimated flowrate: ' + flowrate + " ul/s");
}
var list_of_saved = new listOfSaved("http://127.0.0.1:8000/development/save/",
    "http://127.0.0.1:8000/development/list",
    "http://127.0.0.1:8000/development/load")

$(document).ready(function() {
  flowrateCalc();
  list_of_saved.loadList()
});









