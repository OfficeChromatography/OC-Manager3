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
    loadresume()
  }
)
$("#id_pressure").change(
  function(){
    console.log('pres');
    loadresume()
  }
)
$("#id_frequency").change(
  function(){
    console.log('dpre');
    loadresume()
  }
)
$("#id_delta_y").change(
  function(){
    console.log('dey');
    loadresume()
  }
)
$("#id_delta_x").change(
  function(){
    console.log('dex');
    loadresume()
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
          break;
      case '2':
          $("#id_valuesform").fadeOut();
          $("#id_valuesunit").html('mm');
          $("#id_valuesform").fadeIn();
          $("#bandlengthform").fadeIn();
          $("#nbandsrow").hide();
          $("#lengthbandsrow").show();
        break;
    loadresume()
    }
  }
)


$("#id_size_x").change(
  function(){
    console.log('sizex');
    plotPreview.config.options.scales.xAxes[0].ticks.max = parseFloat($(this).val());
    plotPreview.update();
    bandsmain()
    loadresume()
  }
)
$("#id_size_y").change(
  function(){
    console.log('sizey');
    plotPreview.config.options.scales.yAxes[0].ticks.max = parseFloat($(this).val());
    plotPreview.update();
    bandsmain()
    loadresume()
  }
);

$("#id_offset_left").change(
    function(){
      bandsmain()
      loadresume()
    }
);
$("#id_offset_right").change(
  function(){
    bandsmain()
    loadresume()
  }
);
$("#id_offset_bottom").change(
    function(){
      bandsmain()
      loadresume()
    }
);
$("#id_offset_top").change(
  function(){
    bandsmain()
    loadresume()
  }
);

$("#id_main_property").change(
  function(){
    bandsmain()
    loadresume()
  }
)
$("#id_value").change(
  function(){
    bandsmain()
    loadresume()
  }
)
$("#id_height").change(
  function(){
    bandsmain()
    loadresume()
  }
)
$("#id_gap").change(
  function(){
    bandsmain()
    loadresume()
  }
)

function bandsmain(){
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

  if(theres_error('#id_parameter_error',missing_parameter)){return}

  // Calculate the Working Area [x,y]
  working_area = nbands_working_area(plate_x_size,offset_left_size,offset_right_size,plate_y_size,offset_top_size,offset_bottom_size)

  // Check if its not posible to calculate the wa
  if(theres_error('#id_offsets_error',isNaN(working_area[0]) && isNaN(working_area[1]))){return}

  // Check if the vertical sizes is enough
  if(theres_error('#id_space_error',working_area[1]<band_height)){return}


  switch (property) {
    case '1':
    //Gap process
      sum_gaps_size = total_gap_length(number_bands, gap_size)
      if(theres_error('#id_gap_error',isNaN(sum_gaps_size) || sum_gaps_size>= working_area[0])){return}

    //Bands Sizes
      band_size = total_bands_length(working_area,sum_gaps_size,number_bands)
      if(theres_error('#id_space_error',isNaN(band_size))){return}
      break;


    case '2':
      number_bands = Math.trunc(working_area[0]/(band_size+gap_size))
      if(theres_error('#id_space_error',number_bands<1)){return}
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
    addData(plotPreview,i,'black', newdata)
  }
  plotPreview.update();
  banddescrition(number_bands);
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
  console.log(number_row);
  number_row = parseInt(number_row)
  for(i=0;i<number_row;i++){
    $('#tbody_band').append(newTr1+(i+1)+newTr2);
  }
}

function lenghtcalc(){}

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

function total_gap_length(number_bands, gap_size){
  number_of_gaps = number_bands - 1;
  if(number_of_gaps<0){
    return NaN
  }
  else{
    return gap_size*number_of_gaps;
  }
}

function total_bands_length(workingarea,sum_gaps_size,number_bands){
  bands_size = (working_area[0]-sum_gaps_size)/number_bands
  if(bands_size<=0){
    return NaN
  }
  else{
    return bands_size
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

function loadresume(){
  $('#motorspeed_resume').text($("#id_motor_speed").val())
  $('#appconst_resume').text($("#id_pressure").val()+','+$("#id_frequency").val())
  $('#sizes_resume').text($("#id_size_x").val()+','+$("#id_size_y").val())
  $('#offsets_resume').text($("#id_offset_left").val()+','+$("#id_offset_right").val()+','+$("#id_offset_top").val()+','+$("#id_offset_bottom").val())
  $('#band_properties_resume').text($("#id_main_property option:selected").text())
  $('#n_bands_resume').text($("#id_value").val())
  $('#length_resume').text($("#id_value").val())
  $('#delta_resume').text($("#id_delta_x").val()+','+$("#id_delta_y").val())
  $('#height_resume').text($("#id_height").val())
  $('#gap_resume').text($("#id_gap").val())
}

function loadtable(band){
  console.log(band);
  var newTr1
  $('#tbody_band').empty()
  for (i = 0; i < Object.keys(band).length; i++){
    newTr1 = `
    <tr class="hide">
    <td class="pt-3-half">`+band[i]["band_number"]+`</td>
    <td class="pt-3-half" contenteditable="true">`+band[i]["description"]+`</td>
    <td class="pt-3-half" contenteditable="true">`+band[i]["volume"]+`</td>
    <td class="pt-3-half" contenteditable="true">`+band[i]["type"]+`</td>
    </tr>`;
    $('#tbody_band').append(newTr1);
  }
}

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
  $formData = 'START&'+$('#plateform').serialize()+'&'+$('#movementform').serialize()+'&'+$('#saveform').serialize()
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
  $formData = $('#plateform').serialize()+'&'+$('#movementform').serialize()+'&'+$('#saveform').serialize()
  $formData = $formData.concat(gettablevalues())
  $endpoint = window.location.origin+'/samplesave/'
  $.ajax({
  method: 'POST',
  url:    $endpoint,
  data:   $formData,
  success: saveMethodSuccess,
  error: saveMethodError,stopbttn
  })
})
$('#list-load a').on('click', function (e) {
e.preventDefault()
data={'filename':$(this)[0].innerHTML}
console.log(data);
$.ajax({
  method: 'GET',
  url:    window.location.origin+'/samplesave/',
  data:   data,
  success: loadMethodSuccess,
  error: loadMethodError,
})
})
$('#hommingbttn').on('click', function (e) {
  event.preventDefault()
  sizes=[,parseFloat($("#id_size_y").val())]
  $formData = 'HOMMING&x='+$("#id_size_x").val()+'&y='+$("#id_size_y").val()
  $endpoint = window.location.origin+'/gohomming/'
  // if
  $.ajax({
  method: 'POST',
  url:    $endpoint,
  data:   $formData,
  success: hommingMethodSuccess,
  error: hommingMethodError,
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
  $("#id_motor_speed").val(data.motor_speed)
  $("#id_pressure").val(data.pressure)
  $("#id_frequency").val(data.frequency)
  $("#id_temperature").val(data.temperature)
  $("#id_delta_y").val(data.delta_y)
  $("#id_delta_x").val(data.delta_x)


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

  $( "#id_value" ).trigger( "change" );
  $('#id_load_sucess').html(data.file_name+' successfully load!')
  $( "#id_load_sucess" ).fadeIn().delay( 800 ).fadeOut( 400 );
  loadtable(data['bands'])
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


// TABLE FUNCTIONS
const $tableID = $('#table');
const $BTN = $('#export-btn');
const $EXPORT = $('#export');
var tablevalues

// A few jQuery helpers for exporting only
jQuery.fn.pop = [].pop;
jQuery.fn.shift = [].shift;

function gettablevalues(){

 const $rows = $tableID.find('tr:not(:hidden)');
 const headers = [];
 const data = [];

 // Get the headers (add special header logic here)
 $($rows.shift()).find('th:not(:empty)').each(function () {

   headers.push($(this).text().toLowerCase());
 });

 // Turn all existing rows into a loopable array
 $rows.each(function () {
   const $td = $(this).find('td');
   const h = {};

   // Use the headers from earlier to name our hash keys
   headers.forEach((header, i) => {

     h[header] = $td.eq(i).text();
   });

   data.push(h);
 });

 // Output the result
 tablevalues = '&table='+JSON.stringify(data)
 return tablevalues
};
