var ctx = document.getElementById('plotPreview').getContext('2d');
var plotPreview = new Chart(ctx, {
   type: 'scatter',
   data: {
      datasets: [{
         borderColor: 'black',
         backgroundColor: 'transparent',
         borderWidth: 1,
         pointBackgroundColor: ['#000', '#000', '#000'],
         pointRadius: 1,
         pointHoverRadius: 1,
         fill: false,
         tension: 0,
         showLine: true,
      },]
   },
   options:{
      legend:{
        display:false
      },
      scales: {
        yAxes: [{
          stacked: true,
          ticks: {
            min: 0, // minimum value
            max: 100, // maximum value
            reverse: true,
          },
        }],
        xAxes: [{
          stacked: true,
          ticks: {
            min: 0, // minimum value
            max: 100, // maximum value
          },
        }]
    }
   },
});
var datatable
// Execute every time something happens wi
$("#id_motor_speed").change(
  function(){
    console.log('motor');
    
  }
)
$("#id_pressure").change(
  function(){
    console.log('pres');
    
  }
)
$("#id_frequency").change(
  function(){
    console.log('dpre');
    
  }
)
$("#id_delta_x").change(
  function(){
    console.log('dex');
    
  }
)

$("#id_size_x").change(
  function(){
    console.log('sizex');
    changegraphsize()
    bandsmain()
    
  }
)
$("#id_size_y").change(
  function(){
    console.log('sizey');
    changegraphsize()
    bandsmain()
    
  }
);

$("#id_offset_left").change(
    function(){
      bandsmain()
      
    }
);
$("#id_offset_right").change(
  function(){
    bandsmain()
    
  }
);
$("#id_offset_bottom").change(
    function(){
      bandsmain()
      
    }
);
$("#id_offset_top").change(
  function(){
    bandsmain()
    
  }
);

$("#id_volume").change(
  function(){
    bandsmain()
    
  }
);
$("#id_fluid").change(
  function(){   
    bandsmain()
    
    if ($(this).val() == 'Specific') {
      $('#specificFluidTable').show()
    } else {
      $('#specificFluidTable').hide()
    }
  }
);
$("#id_nozzlediameter").change(
  function(){
  }
);


function bandsmain(){
  plate_x_size = parseFloat($("#id_size_x").val());
  plate_y_size = parseFloat($("#id_size_y").val());

  offset_left_size = parseFloat($("#id_offset_left").val());
  offset_right_size = parseFloat($("#id_offset_right").val());
  offset_top_size = parseFloat($("#id_offset_top").val());
  offset_bottom_size = parseFloat($("#id_offset_bottom").val());

  volume = parseFloat($("#id_volume").val());
  printBothways = $('#printBothwaysButton').text();

  band_height = 0.1;


  // Check if theres missing parameters
  missing_parameter = (isNaN(plate_x_size)||isNaN(plate_y_size)||isNaN(offset_left_size)||isNaN(offset_right_size)||isNaN(offset_top_size)||isNaN(offset_bottom_size)||isNaN(volume))
  if(theres_error('#id_parameter_error',missing_parameter)){return}

  // Calculate the Working Area [x,y]
  working_area = nbands_working_area(plate_x_size,offset_left_size,offset_right_size,plate_y_size,offset_top_size,offset_bottom_size)

  // Check if its not posible to calculate the wa
  if(theres_error('#id_offsets_error',isNaN(working_area[0]) && isNaN(working_area[1]))){return}

  // Check if the vertical sizes is enough
  if(theres_error('#id_space_error',working_area[1]<band_height)){return}

  band_size = working_area[0]
  
  while(plotPreview.data.datasets.pop()!=undefined){}
  newdata = []
  newdata[0]={y:offset_bottom_size,x:offset_left_size}
  newdata[1]={y:offset_bottom_size+band_height,x:offset_left_size}
  newdata[2]={y:offset_bottom_size+band_height,x:band_size+offset_left_size}
  newdata[3]={y:offset_bottom_size,x:band_size+offset_left_size}
  newdata[4]=newdata[0]
  addData(plotPreview,'1','black', newdata)
  plotPreview.update();
  banddescrition(1);
}

function banddescrition(number_row){
  let newTr1 = `
  <tr class="hide">
  <td class="pt-3-half">`;
  let newTr2 = `</td>
  <td class="pt-3-half" contenteditable="true"></td>
  <td class="pt-3-half" contenteditable="true"></td>
  <td class="pt-3-half" contenteditable="true"></td>
  </tr>`
  $('#tbody_band').empty()
  //console.log(number_row);
  number_row = parseInt(number_row)
  for(i=0;i<number_row;i++){
    $('#tbody_band').append(newTr1+(i+1)+newTr2);
  }
}

function addData(chart, label, color, data) {
		chart.data.datasets.push({
	    label: label,
      backgroundColor: color,
      data: data,
      borderColor: 'black',
      borderWidth: 1,
      pointRadius: 2,
      pointHoverRadius: 4,
      fill: true,
      tension: 0,
      showLine: true,
    });
    chart.update();
}

//Calculates the Working Area
function nbands_working_area(plate_x_size,offset_left_size,offset_right_size,plate_y_size,offset_top_size,offset_bottom_size){
  working_area = [plate_x_size-offset_left_size-offset_right_size,plate_y_size-offset_top_size-offset_bottom_size]
  if(working_area[0] <= 0 || working_area[1] <= 0 || isNaN(working_area[0]) || isNaN(working_area[1])){
    return [NaN,NaN];
  }
  else{
      return working_area;
  }
}


function theres_error(error_id, bolean_exp){
  if(bolean_exp){
    $(error_id).fadeIn();
    return true
  }
  else{
    $(error_id).fadeOut();
    return false
  }
}

function changegraphsize(){
  plotPreview.config.options.scales.xAxes[0].ticks.max = parseFloat($("#id_size_x").val());
  plotPreview.config.options.scales.yAxes[0].ticks.max = parseFloat($("#id_size_y").val());
  plotPreview.update();
}

$('#stopbttn').on('click', function (e) {
  event.preventDefault()
  //
  $formData = 'STOP&'
  $endpoint = window.location.origin+'/developmentplay/'
  $.ajax({
  method: 'POST',
  url:    $endpoint,
  data:   $formData,
  success: stopMethodSuccess,
  error: stopMethodError,
  })
})
$('#pausebttn').on('click', function (e) {
  event.preventDefault()
  //
  $formData = 'PAUSE&'
  $endpoint = window.location.origin+'/developmentplay/'
  $.ajax({
  method: 'POST',
  url:    $endpoint,
  data:   $formData,
  success: pauseMethodSuccess,
  error: pauseMethodError,
  })
})

$('#startbttn').on('click', function (e) {
  event.preventDefault()
  //
  $formData = 'START&'+$('#plateform').serialize()+'&'+$('#pressureform').serialize()+'&'+$('#saveform').serialize()+'&'+$('#zeroform').serialize()+getSpecificFluid(true)
  $endpoint = window.location.origin+'/developmentplay/'
  $.ajax({
  method: 'POST',
  url:    $endpoint,
  data:   $formData,
  success: startMethodSuccess,
  error: startMethodError,
  })
})
$('#savebttn').on('click', function (e) {
  event.preventDefault()
  $formData = $('#plateform').serialize()+'&'+$('#pressureform').serialize()+'&'+$('#saveform').serialize()+'&'+$('#zeroform').serialize()+getSpecificFluid(true)
  $endpoint = window.location.origin+'/developmentsave/'
  $.ajax({
  method: 'POST',
  url:    $endpoint,
  data:   $formData,
  success: saveMethodSuccess,
  error: saveMethodError,
  })
})
$('#list-load a').on('click', function (e) {
e.preventDefault()
data={'filename':$(this)[0].innerHTML}
//console.log(data);
$.ajax({
  method: 'GET',
  url:    window.location.origin+'/developmentsave/',
  data:   data,
  success: loadMethodSuccess,
  error: loadMethodError,
})
})

function hommingMethodSuccess(data, textStatus, jqXHR){
  if(data.error!=''){
    theres_error('#id_parameter_error',false)
  }
  else{
    theres_error('#id_parameter_error',true)
  }

}
function hommingMethodError(jqXHR, textStatus, errorThrown){}

function stopMethodSuccess(data, textStatus, jqXHR){
  console.log(data);
  $('.control-bttn').removeClass('btn-success btn-secondary')
  $('.control-bttn').addClass('btn btn-danger')
}
function stopMethodError(jqXHR, textStatus, errorThrown){}

function pauseMethodSuccess(data, textStatus, jqXHR){
  console.log(data);
    $('.control-bttn').removeClass('btn-success btn-danger')
  $('.control-bttn').addClass('btn btn-secondary')
}
function pauseMethodError(jqXHR, textStatus, errorThrown){}

function startMethodSuccess(data, textStatus, jqXHR){
  console.log(data);
  $('.control-bttn').removeClass('btn-danger btn-secondary')
  $('.control-bttn').addClass('btn btn-success')
}
function startMethodError(jqXHR, textStatus, errorThrown){}

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

  if (data.printBothways=='On') {
    $("#printBothwaysButton").text('On');
  } else {
    $("#printBothwaysButton").text('Off');
  }
  
  $('#id_fluid').val(data.fluid)

  if (data.fluid == 'Specific') {
    $('#specificFluidTable').show()
  } else {
    $('#specificFluidTable').hide()
  }

  $('#densityval').text(data.density)
  $('#viscosityval').text(data.viscosity)

  $('#id_load_sucess').html(data.file_name+' successfully loaded!')
  $( "#id_load_sucess" ).fadeIn().delay( 800 ).fadeOut( 400 );
  bandsmain()
  changegraphsize()
}
function loadMethodError(jqXHR, textStatus, errorThrown){
  console.log('error');
}

function saveMethodSuccess(data, textStatus, jqXHR){
  console.log(typeof(data.error));
  if(data.error==undefined){
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

  if(toString){
    data = '&devBandSettings='+JSON.stringify(data)
  }
  return data
}

$('#printBothwaysButton').on('click', function (e) {
  event.preventDefault()
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

function checkSpecificValues() {
  if ($("#id_fluid").val() == 'Specific') {
    if ($("#densityval").text() == "" || $("#viscosityval").text() == "" ) {
      alert("Please specify density and viscosity!")
    }
  }
} 

function calcMethodSuccess(data, textStatus, jqXHR){
  // console.log(typeof(data.error));
  if(data.error==undefined){
    $('.vol').html("<br>estimated vol: " + data.results[1].toFixed(3) + "<br>estimated dropvol: " + data.results[0].toFixed(3))
    }
  else {
    console.log('error')
  }
  
}
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

$(document).ready(function() {
  
  $('#devModal').modal('show');
});