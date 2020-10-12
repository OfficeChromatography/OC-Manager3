// Graph var
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

// Table constants
const $tableID = $('#table');
const $BTN = $('#export-btn');
const $EXPORT = $('#export');
var tablevalues
  // A few jQuery helpers for exporting only
jQuery.fn.pop = [].pop;
jQuery.fn.shift = [].shift;


$( document ).ready(function(){
  loadlistofsampleapps()
})


// Execute every time something happens
$("#id_motor_speed").change(
  function(){
    console.log('motor');
  }
)
$("#id_pressure").change(
  function(){
    console.log('pres');
    calcVol()
  }
)

$("#id_nozzlediameter").change(
  function(){
    calcVol()
  }
)

$("#id_frequency").change(
  function(){
    console.log('dpre');
    calcVol()
  }
)
$("#id_delta_y").change(
  function(){
    console.log('dey');
    calcVol()
  }
)
$("#id_delta_x").change(
  function(){
    console.log('dex');
    calcVol()
  }
)
$("#id_main_property").change(
  // The default hiden is in the html file
  function(){
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
    calcVol()
  }
)

$("#id_size_x").change(
  function(){
    console.log('sizex');
    changeGraphSize()
    calcVol()
  }
)
$("#id_size_y").change(
  function(){
    console.log('sizey');
    changeGraphSize()
    calcVol()
  }
);

$("#id_offset_left").change(
    function(){
      mainCalculations()
      calcVol()
    }
);
$("#id_offset_right").change(
  function(){
    mainCalculations()
    calcVol()
  }
);
$("#id_offset_bottom").change(
    function(){
      mainCalculations()
      calcVol()
    }
);
$("#id_offset_top").change(
  function(){
    mainCalculations()
    calcVol()
  }
);

$("#id_main_property").change(
  function(){
    mainCalculations()
    createBandsTable()
    calcVol()
  }
)
$("#id_value").change(
  function(){
    mainCalculations()
    createBandsTable()
    calcVol()
    
  }
)
$("#id_height").change(
  function(){
    mainCalculations()
    calcVol()
  }
)
$("#id_gap").change(
  function(){
    mainCalculations()
    calcVol()
  }
)

$('#table').change(function(){
  calcVol();
  $(".fluidSelect").each(function(){
    if ($(this).val() == 'Specific') {
      $(this).parent().find($('.specificFluidTable')).show()
    } else {
      $(this).parent().find($('.specificFluidTable')).hide()
    }
  })
})
function createBandsTable(){
  number_bands = parseFloat($("#id_value").val());
  property = $("#id_main_property").val();
  gap_size = parseFloat($("#id_gap").val());
  band_size = parseFloat($("#id_value").val());
  plate_x_size = parseFloat($("#id_size_x").val());
  plate_y_size = parseFloat($("#id_size_y").val());
  offset_left_size = parseFloat($("#id_offset_left").val());
  offset_right_size = parseFloat($("#id_offset_right").val());
  offset_top_size = parseFloat($("#id_offset_top").val());
  offset_bottom_size = parseFloat($("#id_offset_bottom").val());
  working_area = nBandsWorkingArea(plate_x_size,offset_left_size,offset_right_size,plate_y_size,offset_top_size,offset_bottom_size)
  if (property=='2'){number_bands = Math.trunc(working_area[0]/(band_size+gap_size))}
  newComponentsTable(number_bands);
}
// MAIN
function mainCalculations(){
  plate_x_size = parseFloat($("#id_size_x").val());
  plate_y_size = parseFloat($("#id_size_y").val());

  offset_left_size = parseFloat($("#id_offset_left").val());
  offset_right_size = parseFloat($("#id_offset_right").val());
  offset_top_size = parseFloat($("#id_offset_top").val());
  offset_bottom_size = parseFloat($("#id_offset_bottom").val());

  gap_size = parseFloat($("#id_gap").val());
  number_bands = parseFloat($("#id_value").val());
  band_size = parseFloat($("#id_value").val());

  band_height = parseFloat($("#id_height").val());
  property = $("#id_main_property").val();

  // Check if theres missing parameters
  missing_parameter = (isNaN(plate_x_size)||isNaN(plate_y_size)||isNaN(offset_left_size)||isNaN(offset_right_size)||isNaN(offset_top_size)||isNaN(offset_bottom_size)||isNaN(gap_size)||isNaN(band_height))

  if(thereAreErrors('#id_parameter_error',missing_parameter)){return}

  // Calculate the Working Area [x,y]
  working_area = nBandsWorkingArea(plate_x_size,offset_left_size,offset_right_size,plate_y_size,offset_top_size,offset_bottom_size)

  // Check if its not posible to calculate the wa
  if(thereAreErrors('#id_offsets_error',isNaN(working_area[0]) && isNaN(working_area[1]))){return}

  // Check if the vertical sizes is enough
  if(thereAreErrors('#id_space_error',working_area[1]<band_height)){return}

  switch (property) {
    // N Bands
    case '1':
    //Gap process
      sum_gaps_size = totalGapLength(number_bands, gap_size)
      if(thereAreErrors('#id_gap_error',isNaN(sum_gaps_size) || sum_gaps_size>= working_area[0])){return}

    //Bands Sizes
      band_size = totalBandsLength(working_area,sum_gaps_size,number_bands)
      if(thereAreErrors('#id_space_error',isNaN(band_size))){return}
      break;
    // Length
    case '2':
      number_bands = Math.trunc(working_area[0]/(band_size+gap_size))
      if(thereAreErrors('#id_space_error',number_bands<1)){return}
      break;
  }

  while(plotPreview.data.datasets.pop()!=undefined){}
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
    addData2Chart(plotPreview,i,'black', newdata)
  }
  plotPreview.update();
}

//  ERROR DISPLAY MANAGER
function thereAreErrors(error_id, bolean_exp){
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
function nBandsWorkingArea(plate_x_size,offset_left_size,offset_right_size,plate_y_size,offset_top_size,offset_bottom_size){
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

// add new bands to the chart
function addData2Chart(chart, label, color, data) {
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

// Create a new Table with a given number of rows
function newComponentsTable(number_row){
  let newTr1 = `
  <tr class="hide trClass">
  <td class="pt-3-half bcomponents">`;
  let newTr2 = `</td>
  <td class="pt-3-half bcomponents" contenteditable="true"></td>
  <td class="pt-3-half bcomponents vol" contenteditable="true"><small><br></small></td>
  <td class="pt-3-half bcomponents"><select class="form-control fluidSelect" id="fluidSelect`
  let newTr3 = `" ><option>Water</option><option>Methanol</option><option>Acetone</option><option>Specific</option></select>
  <div style="display: none;" class="specificFluidTable"><table class="table table-bordered table-responsive-md table-striped text-center">
  <tr class="hide"><td class="pt-3-half">density [g/cm³]</td><td class="pt-3-half densityval" contenteditable="true"></td></tr>
  <tr class="hide"><td class="pt-3-half">viscosity [cSt]</td><td class="pt-3-half viscosityval" contenteditable="true"></td></tr>
  `
  $('#tbody_band').empty()
  console.log(number_row);
  number_row = parseInt(number_row)
  for(i=0;i<number_row;i++){
    $('#tbody_band').append(newTr1+(i+1)+newTr2+(i+1)+newTr3+'</div></td></tr>');
  }
}
// Load the table with data from de DB or from file
function loadComponentsTable(band,fromDB){
  console.log(band);
  var newTr1
  $('#tbody_band').empty()
  if(fromDB==true){
    idbandname = "band_number"
    idvolumename= "volume"
  }
  else{
    idbandname= "band"
    idvolumename= "volume (ul)"
  }
  console.log(Object.keys(band))
  for (i = 0; i < Object.keys(band).length; i++){
    
    selectOption = '<select id="fluidSelect'+(i+1)+'" class="form-control fluidSelect"><option value="Water">Water</option><option value="Methanol">Methanol</option><option value="Acetone">Acetone</option><option value="Specific">Specific</option></select>'
      
    newTr1 = `
    <tr class="hide trClass">
    <td class="pt-3-half bcomponents">`+band[i][idbandname]+`</td>
    <td class="pt-3-half bcomponents" contenteditable="true">`+band[i]["description"]+`</td>
    <td class="pt-3-half bcomponents vol" contenteditable="true"><small>`+band[i][idvolumename]+`</small></td>
    <td class="pt-3-half bcomponents">`+selectOption+`<div style="display: none;" class="specificFluidTable"><table class="table table-bordered table-responsive-md table-striped text-center">
    <tr class="hide"><td class="pt-3-half">density</td><td class="pt-3-half densityval" contenteditable="true">`+band[i]["density"]+`</td></tr>
    <tr class="hide"><td class="pt-3-half">viscosity</td><td class="pt-3-half viscosityval" contenteditable="true">`+band[i]["viscosity"]+`</td></tr></div></td>
    </tr>`;
    $('#tbody_band').append(newTr1);
    fluidString = '#fluidSelect'+(i+1)
    $(fluidString).val(band[i]["type"])
      if (band[i]["type"] == "Specific") {
        $(fluidString).parent().find($('.specificFluidTable')).show()
      }
  }
  calcVol()
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
  $( "#id_load_sucess" ).fadeIn().delay( 800 ).fadeOut( 400 );
}

// Returns a string or an Object with the table values
function getTableValues(toString){

 const $rows = $tableID.find('.trClass');
 const headers = [];
 const data = [];

 // Get the headers (add special header logic here)
 $tableID.find('th').each(function () {
   headers.push($(this).text().toLowerCase());
 });
 // Turn all existing rows into a loopable array
 $rows.each(function (j) {
   const $td = $(this).find('.bcomponents');
   const h = {};
   // Use the headers from earlier to name our hash keys
   headers.forEach((header, i) => {
    if (header == 'type') {
      stringFluidSelect = 'select[id="fluidSelect'+(j+1)+'"] option:selected';
      h[header] = $(stringFluidSelect).val();

        if (h[header]=='Specific') {
          h['density'] = $(stringFluidSelect).parent().parent().find('.densityval').text();
          h['viscosity'] = $(stringFluidSelect).parent().parent().find('.viscosityval').text();
        } else {
          h['density'] = ''
          h['viscosity'] = ''
        }
    } else if ((header == 'volume (ul)')) {
      h[header] = $td.eq(i).find("small").html().split('<b')[0];
    } else {
      h[header] = $td.eq(i).text();
    }
   });
   console.log(h);
   data.push(h);
 });

 // Output the result
 if(toString){
   tablevalues = '&table='+JSON.stringify(data)
 }
 else{
   tablevalues = data
 }
 return tablevalues
};

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
    loadComponentsTable(jsonObject['bands'],false)
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
    url:    window.location.origin+'/sample/',
    data:   '&LISTLOAD',
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
            data={'filename':$(this).attr('value_saved')}
            console.log(data);
            $.ajax({
              method: 'GET',
              url:    window.location.origin+'/samplesave/',
              data:   data,
              success: loadMethodSuccess,
              error: loadMethodError,
            })
            })
    }
  function loadlistMethodError(jqXHR, textStatus, errorThrown){}
}

// Endpoints
$('#stopbttn').on('click', function (e) {
  event.preventDefault()
  //
  $formData = 'STOP&'
  $endpoint = window.location.origin+'/sampleapp/'
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
  $endpoint = window.location.origin+'/sampleapp/'
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
  $formData = 'START&'+$('#plateform').serialize()+'&'+$('#movementform').serialize()+'&'+$('#saveform').serialize()+'&'+$('#zeroform').serialize()+getTableValues(true)
  $endpoint = window.location.origin+'/sampleapp/'
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
  $formData = $('#plateform').serialize()+'&'+$('#movementform').serialize()+'&'+$('#saveform').serialize()+'&'+$('#zeroform').serialize()+getTableValues(true)
  $endpoint = window.location.origin+'/samplesave/'
  $.ajax({
  method: 'POST',
  url:    $endpoint,
  data:   $formData,
  success: saveMethodSuccess,
  error: saveMethodError,stopbttn
  })
})

// Import/Export DATA
$('#downloadfilebttn').on('click', function (e) {
  event.preventDefault()
  var element = document.createElement('a');

  var plate = getFormData($('#plateform'))
  var movement = getFormData($('#movementform'))
  var zero = getFormData($('#zeroform'))
  var table = {bands:getTableValues(false)}
  items = Object.assign(plate,movement,table,zero)

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


function hommingMethodSuccess(data, textStatus, jqXHR){
  if(data.error!=''){
    thereAreErrors('#id_parameter_error',false)
  }
  else{
    thereAreErrors('#id_parameter_error',true)
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
  //console.log(data);
  $('.control-bttn').removeClass('btn-danger btn-secondary')
  $('.control-bttn').addClass('btn btn-success')
}
function startMethodError(jqXHR, textStatus, errorThrown){}

function loadMethodSuccess(data, textStatus, jqXHR){
  // Load all the fields with the ones get in the database
  loadFieldsValues(data);
  loadComponentsTable(data['bands'],true)
  changeGraphSize()
  calcVol()
}
function loadMethodError(jqXHR, textStatus, errorThrown){
  console.log('error');
}

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

//sets the initial setting of main_property
$(window).on('beforeunload', function(){
  $('#id_main_property').val("1")
});

function calcVol(){
  $formData = $('#plateform').serialize()+'&'+$('#movementform').serialize()+getTableValues(true)
  $endpoint = window.location.origin+'/samplecalc/'
  $.ajax({
  method: 'POST',
  url:    $endpoint,
  data:   $formData,
  success: calcMethodSuccess,
  error: saveMethodError
  })
}

function calcMethodSuccess(data, textStatus, jqXHR){
  //console.log(typeof(data.error));
  if(data.error==undefined){
    var i;
    for (i = 0; i < data.results.length; i++) {
      findString = '#fluidSelect'+(i+1)
      console.log($(findString).parent().prev())
      volumeString = $(findString).parent().prev().find("small").html().split('<b')[0]
      //console.log(volumeString)
      //console.log(data.results[i][1].toFixed(3))
      $(findString).parent().prev().find("small").html(volumeString
       + '<br> estimated vol: ' + data.results[i][1].toFixed(3)  + '<br> estimated dropvol: ' + data.results[i][0].toFixed(3))
    }
  }
  else {
    
  }
  
}

$(document).ready(function() {
  createBandsTable()
  calcVol();
  $(document).on("blur", ".vol", function() {
    calcVol();
  })
});



