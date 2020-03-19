var ctx = document.getElementById('plotPreview').getContext('2d');

// Settings initial values
var motorspeed = $('#motorspeed')[0];
var pressure = $('#pressure')[0];
var deltapressure = $('#deltapressure')[0];

// Parameter Inital Values
  // Plate sizes
  var sizex = $('#sizex')[0]
  var sizey = $('#sizey')[0];
  // Offsets
  var offsety = $('#offsety')[0];
  var offsetx = $('#offsetx')[0];
  // Bands Properties
  var method = $('#method')[0]
  var nbands = $('#nbands')[0];
  var bandlength = $('#bandlength')[0];
  var gap = $('#gap')[0];
  var bandheight = $('#bandheight')[0];

// Plot Declaration
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


var workingarea = {x:0,y:0}

window.onload = function(){
  loadresume()
}

// OnChange Event Listeners
document.getElementById('method').onchange = function(e){
  configurationdisplay(e)
  loadresume()
}
document.getElementById('motorspeed').onchange = function(){
  loadresume()
}
document.getElementById('pressure').onchange = function(){
  loadresume()
}
document.getElementById('deltapressure').onchange = function(){
  loadresume()
}


// Event Listener of objects that cause a change on the graph
function changegraph(event){
  while(plotPreview.data.datasets.pop()!=undefined){}
  switch(event.target.id) {
    case 'sizex':
      plotPreview.config.options.scales.xAxes[0].ticks.max = parseInt(sizex.value);
      break;
    case 'sizey':
      plotPreview.config.options.scales.yAxes[0].ticks.max = parseInt(sizey.value);
      break;
    case 'offsetx':
      break;
    case 'offsety':
      break;
    case 'nbands':
      break;
    case 'gap':
      break;
    case 'bandheight':
      break;
    case 'bandlength':
      break;
  }
  pointgen(plotPreview)
  plotPreview.update();
}

// Calculation of Workingara=SIZE[]-OFFSETS[]
function workingareacalc(){
  calc = {x:sizexvalue-(2*offsetxvalue), y:sizeyvalue-(2*offsetyvalue)}
  return calc
}

// Offset calc for bandlength configuration
function newoffsetcalc(){
  var floatnbands = (workingarea.x+gapvalue)/(bandlengthvalue+gapvalue)
  nbandsvalue = Math.trunc(floatnbands)
  leftover = bandlengthvalue*(floatnbands%nbandsvalue)
  return offsetxvalue += leftover
}

// Ponits generator Function
function pointgen(graph, bandsize){
  nbandsvalue = parseInt(nbands.value)
  bandlengthvalue = parseInt(bandlength.value)
  bandheightvalue = parseInt(bandheight.value)
  gapvalue = parseInt(gap.value)
  sizexvalue = parseInt(sizex.value)
  sizeyvalue = parseInt(sizey.value)
  offsetxvalue = parseInt(offsetx.value)
  offsetyvalue = parseInt(offsety.value)

  workingarea = workingareacalc()

  if(method.selectedIndex==0){
    bandsize = (workingarea.x-(gapvalue*(nbandsvalue-1)))/nbandsvalue;
  }
  else{
    offsetxvalue=newoffsetcalc()
    bandsize = bandlengthvalue
  }
  if(bandsize>=0){
    for(i=0;i<nbandsvalue;i++){
      newdata = []
      if(i==0){
        newdata[0]={y:offsetyvalue,x:offsetxvalue}
        newdata[1]={y:offsetyvalue+bandheightvalue,x:offsetxvalue}
        newdata[2]={y:offsetyvalue+bandheightvalue,x:bandsize+offsetxvalue}
        newdata[3]={y:offsetyvalue,x:bandsize+offsetxvalue}
        newdata[4]={y:offsetyvalue,x:offsetxvalue}
      }
      else{
        newdata[0]={y:offsetyvalue,x:i*(bandsize+gapvalue)+offsetxvalue}
        newdata[1]={y:offsetyvalue+bandheightvalue,x:i*(bandsize+gapvalue)+offsetxvalue}
        newdata[2]={y:offsetyvalue+bandheightvalue,x:(i+1)*bandsize+(gapvalue*i)+offsetxvalue}
        newdata[3]={y:offsetyvalue,x:(i+1)*bandsize+(gapvalue*i)+offsetxvalue}
        newdata[4]={y:offsetyvalue,x:i*(bandsize+gapvalue)+offsetxvalue}
      }
      addData(graph,i,'black', newdata)
    }
    loadresume()
  }
  else if((!Number.isNaN(bandsizevalue) || !Number.isNaN(offsetxvalue)) && !Number.isNaN(nbandsvalue)){
    dataerror()
  }
}
// Error alert
function dataerror(){
  window.alert("Incorrect data");
}

// Data plotter
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

// Configuration Properties
function configurationdisplay(event){
  value=event.target.selectedIndex
  switch (value) {
    case 0:
        $("#nbandsform").prop('disabled',false)
        $("#nbandsform").fadeIn();
        $("#bandlengthform").fadeOut();
        $("#bandlengthform").value = 0
        $("#bandlengthform").prop('disabled',true)
      break;
    case 1:
        $("#bandlengthform").prop('disabled',false)
        $("#bandlengthform").removeAttr('hidden')
        $("#bandlengthform").fadeIn();
        $("#nbandsform").fadeOut();
        $("#nbandsform").value = 0
        $("#nbandsform").prop('disabled',true)
      break;
  }
}

// Load resume table
function loadresume(){
  $('#resumemotorspeed')[0].value = motorspeed.value
  $('#resumepressure')[0].value = ['P: '+pressure.value+', '+ 'Δ: '+deltapressure.value]
  $('#resumeoffsets')[0].value = ['x: '+parseFloat(offsetx.value).toFixed(2)+', '+ 'y: '+parseFloat(offsety.value).toFixed(2)]
  $('#resumesizes')[0].value = ['x: '+sizex.value+', '+'y: '+sizey.value]
  $('#resumebandproperties')[0].value = method.value
  if(method.selectedIndex==0){
    $('#nbandsrow').hidden = false
    $('#resumenbands')[0].value = nbands.value
    $('#lengthbandsrow').hidden = true
  }
  else{
    $('#lengthbandsrow').hidden = false
    $('#resumelengthbands')[0].value = bandlength.value
    $('#nbandsrow').hidden = true
  }
  $('#resumeheigth')[0].value = bandheight.value
  $('#resumegap')[0].value = gap.value
}

$(document).ready(function(){
  // AJAX POST of the serial_port connection
  var $SaveSampleApplicationForm = $('.savesampleapplication-form')
  $SaveSampleApplicationForm.submit(function(event){
    event.preventDefault()
    let $formData = $(this).serialize()
    let $endpoint = window.location.origin+'/samplesave/'
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
  $.ajax({
    method: 'GET',
    url:    window.location.origin+'/samplesave/',
    data:   data,
    success: loadMethodSuccess,
    error: loadMethodError,
  })
})

  $('#playbttn').on('click', function (e) {
    event.preventDefault()
    let $formData = $('.savesampleapplication-form').serialize()
    let $endpoint = window.location.origin+'/samplesave/'
    $.ajax({
    method: 'POST',
    url:    window.location.origin+'/sampleapp/',
    data:   $formData,
    success: playMethodSuccess,
    error: playMethodError,
    })
  })

  $('#stopbttn').on('click', function (e) {
    data=''
    event.preventDefault()
    $.ajax({
    method: 'GET',
    url:    window.location.origin+'/samplestop/',
    data:   {'stop':''},
    success: stopMethodSuccess,
    error: stopMethodError,
    })
  })

  $('#pausebttn').on('click', function (e) {
    event.preventDefault()
    $.ajax({
    method: 'GET',
    url:    window.location.origin+'/samplestop/',
    data:   {'pause':''},
    success: pauseMethodSuccess,
    error: pauseMethodError,
    })
  })
})

function loadMethodSuccess(data, textStatus, jqXHR){
  motorspeed.value = data.motorspeed
  pressure.value = data.pressure
  deltapressure.value = data.deltapressure
  sizex.value = data.sizex
  sizey.value = data.sizey
  offsetx.value = data.offsetx
  offsety.value = data.offsety
  method.value = data.bandsetting
  nbands.value = data.nbands
  bandlength.value = data.lengthbands
  bandheight.value = data.height
  gap.value = data.gap
  if(method.value=='N° Bands'){
    $('#nbands').change()
  }
  else{
    $('#bandlength').change()
  }
}
function loadMethodError(jqXHR, textStatus, errorThrown){
  console.log('error');
}
function saveMethodSuccess(data, textStatus, jqXHR){
  console.log('todo ok');
}
function saveMethodError(jqXHR, textStatus, errorThrown){}
function playMethodSuccess(jqXHR, textStatus, errorThrown){
  console.log(data);
}
function playMethodError(jqXHR, textStatus, errorThrown){}
function stopMethodSuccess(jqXHR, textStatus, errorThrown){}
function stopMethodError(jqXHR, textStatus, errorThrown){}
function pauseMethodSuccess(jqXHR, textStatus, errorThrown){}
function pauseMethodError(jqXHR, textStatus, errorThrown){}
