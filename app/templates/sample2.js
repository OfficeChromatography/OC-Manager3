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
$("#id_delta_pressure").change(
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
          $("#bandlengthform").fadeOut();
          $("#nbandsform").fadeIn();
          $("#lengthbandsrow").hide();
          $("#nbandsrow").show();
          break;
      case '2':
          $("#nbandsform").fadeOut();
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
    plotPreview.config.options.scales.xAxes[0].ticks.max = parseInt($(this).val());
    plotPreview.update();
    bandsmain()
    loadresume()
  }
)
$("#id_size_y").change(
  function(){
    console.log('sizey');
    plotPreview.config.options.scales.yAxes[0].ticks.max = parseInt($(this).val());
    plotPreview.update();
    bandsmain()
    loadresume()
  }
);

$("#id_offset_x").change(
    function(){
      bandsmain()
      loadresume()
    }
);
$("#id_offset_y").change(
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
$("#id_n_bands").change(
  function(){
    bandsmain()
    loadresume()
  }
)
$("#id_length").change(
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

  offset_x_size = parseFloat($("#id_offset_x").val());
  offset_y_size = parseFloat($("#id_offset_y").val());

  gap_size = parseFloat($("#id_gap").val());
  number_bands = parseFloat($("#id_n_bands").val());
  band_size = parseFloat($("#id_length").val());

  band_height = parseFloat($("#id_height").val());
  property = $("#id_main_property").val();

  // Check if theres missing parameters
  missing_parameter = (isNaN(plate_x_size)||isNaN(plate_y_size)||isNaN(offset_x_size)||isNaN(offset_y_size)||isNaN(gap_size)||isNaN(band_height))

  if(theres_error('#id_parameter_error',missing_parameter)){return}

  // Calculate the Working Area [x,y]
  working_area = nbands_working_area(plate_x_size,offset_x_size,plate_y_size,offset_y_size)

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
      newdata[0]={y:offset_y_size,x:offset_x_size}
      newdata[1]={y:offset_y_size+band_height,x:offset_x_size}
      newdata[2]={y:offset_y_size+band_height,x:band_size+offset_x_size}
      newdata[3]={y:offset_y_size,x:band_size+offset_x_size}
      newdata[4]=newdata[0]
    }
    else{
      newdata[0]={y:offset_y_size,x:i*(band_size+gap_size)+offset_x_size}
      newdata[1]={y:offset_y_size+band_height,x:i*(band_size+gap_size)+offset_x_size}
      newdata[2]={y:offset_y_size+band_height,x:(i+1)*band_size+(gap_size*i)+offset_x_size}
      newdata[3]={y:offset_y_size,x:(i+1)*band_size+(gap_size*i)+offset_x_size}
      newdata[4]=newdata[0]
    }
    addData(plotPreview,i,'black', newdata)
  }
  plotPreview.update();
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
function nbands_working_area(plate_x_size,offset_x_size,plate_y_size,offset_y_size){
  working_area = [plate_x_size-2*offset_x_size,plate_y_size-2*offset_y_size]
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
  $('#pressure_resume').text($("#id_pressure").val()+','+$("#id_delta_pressure").val())
  $('#sizes_resume').text($("#id_size_x").val()+','+$("#id_size_y").val())
  $('#offsets_resume').text($("#id_offset_x").val()+','+$("#id_offset_y").val())
  $('#band_properties_resume').text($("#id_main_property option:selected").text())
  $('#n_bands_resume').text($("#id_n_bands").val())
  $('#length_resume').text($("#id_length").val())
  $('#delta_resume').text($("#id_delta_x").val()+','+$("#id_delta_y").val())
  $('#height_resume').text($("#id_height").val())
  $('#gap_resume').text($("#id_gap").val())
}

$('#playbttn').on('click', function (e) {
  event.preventDefault()
  //
  $formData = $('#plateform').serialize()+'&'+$('#movementform').serialize()
  $endpoint = window.location.origin+'/sampleapp2/'
  $.ajax({
  method: 'POST',
  url:    $endpoint,
  data:   $formData,
  success: playMethodSuccess,
  error: playMethodError,
  })
})

function playMethodSuccess(data, textStatus, jqXHR){
  console.log(data);
}
function playMethodError(jqXHR, textStatus, errorThrown){}


// function get_data_from_table(){
//   data = {
//     motor_speed:'',
//     preassure:'',
//     delta_preassure:'',
//     delta_y:'',
//     delta_x:'',
//     main_property:'',
//     n_bands:'',
//     length:'',
//     height:'',
//     gap:'',
//   }
//   $("#resumetable .val").each(
//     function(){
//       console.log($(this).text());
//     }
//   )
// }
