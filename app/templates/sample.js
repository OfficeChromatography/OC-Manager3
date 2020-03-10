var ctx = document.getElementById('plotPreview').getContext('2d');

// Parameter Inital Values
  // Plate sizes
  var sizex = parseInt(document.getElementById('sizex').value);
  var sizey = parseInt(document.getElementById('sizey').value);
  // Offsets
  var offsety = parseInt(document.getElementById('offsety').value);
  var offsetx = parseInt(document.getElementById('offsetx').value);
  // Bands Properties
  var method = $('#method')[0]
  var nbands = parseInt(document.getElementById('nbands').value);
  var bandlength = parseInt(document.getElementById('bandlength').value);
  var gap = parseInt(document.getElementById('gap').value);
  var bandheight = parseInt(document.getElementById('bandheight').value);

// Settings initial values
var motorspeed = document.getElementById('motorspeed').value
var pressure = document.getElementById('pressure').value
var deltapressure = document.getElementById('deltapressure').value


var workingarea = {x:0,y:0}

window.onload = function(){
  loadresume()
}

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


// OnChange Event Listeners
document.getElementById('method').onchange = function(e){
  configurationdisplay(e)
  loadresume()
}
document.getElementById('motorspeed').onchange = function(){
  motorspeed=this.value
  loadresume()
}
document.getElementById('pressure').onchange = function(){
  pressure=this.value
  loadresume()
}
document.getElementById('deltapressure').onchange = function(){
  deltapressure=this.value
  loadresume()
}


// Event Listener of objects that cause a change on the graph
function changegraph(event){
  while(plotPreview.data.datasets.pop()!=undefined){}
  switch(event.target.id) {
    case 'sizex':
      sizex = parseInt(document.getElementById('sizex').value);
      plotPreview.config.options.scales.xAxes[0].ticks.max = parseInt(document.getElementById('sizex').value);
      break;
    case 'sizey':
      sizey = parseInt(document.getElementById('sizey').value);
      plotPreview.config.options.scales.yAxes[0].ticks.max = parseInt(document.getElementById('sizey').value);
      break;
    case 'offsetx':
      offsetx = parseInt(document.getElementById('offsetx').value);
      break;
    case 'offsety':
      offsety = parseInt(document.getElementById('offsety').value);
      break;
    case 'nbands':
      nbands = parseInt(document.getElementById('nbands').value);
      break;
    case 'gap':
      gap = parseInt(document.getElementById('gap').value);
      break;
    case 'bandheight':
      bandheight = parseInt(document.getElementById('bandheight').value);
      break;
    case 'bandlength':
      bandlength = parseInt(document.getElementById('bandlength').value);
      break;
  }
  pointgen(plotPreview)
  plotPreview.update();
}

// Calculation of Workingara=SIZE[]-OFFSETS[]
function workingareacalc(){
  workingarea = {x:sizex-(2*offsetx), y:sizey-(2*offsety)}
}

// Offset calc for bandlength configuration
function newoffsetcalc(){
  workingareacalc()
  var floatnbands = (workingarea.x+gap)/(bandlength+gap)
  nbands = Math.trunc(floatnbands)
  leftover = bandlength*(floatnbands%nbands)
  offsetx += leftover
}

// Ponits generator Function
function pointgen(graph, bandsize){
  workingareacalc()
  if(method.selectedIndex==0){
    bandsize = (workingarea.x-(gap*(nbands-1)))/nbands;
  }
  else{
    newoffsetcalc()
    bandsize = bandlength
  }
  if(bandsize>=0){
    for(i=0;i<nbands;i++){
      newdata = []
      if(i==0){
        newdata[0]={y:offsety,x:offsetx}
        newdata[1]={y:offsety+bandheight,x:offsetx}
        newdata[2]={y:offsety+bandheight,x:bandsize+offsetx}
        newdata[3]={y:offsety,x:bandsize+offsetx}
        newdata[4]={y:offsety,x:offsetx}
      }
      else{
        newdata[0]={y:offsety,x:i*(bandsize+gap)+offsetx}
        newdata[1]={y:offsety+bandheight,x:i*(bandsize+gap)+offsetx}
        newdata[2]={y:offsety+bandheight,x:(i+1)*bandsize+(gap*i)+offsetx}
        newdata[3]={y:offsety,x:(i+1)*bandsize+(gap*i)+offsetx}
        newdata[4]={y:offsety,x:i*(bandsize+gap)+offsetx}
      }
      addData(graph,i,'black', newdata)
    }
    loadresume()
  }
  else if((!Number.isNaN(bandsize) || !Number.isNaN(offsetx)) && !Number.isNaN(nbands)){
    dataerror()
  }
}

// Error alert
function dataerror(){
  window.alert("Incorrect data");
}

// Configuration Properties
function configurationdisplay(event){
  value=event.target.selectedIndex
  switch (value) {
    case 0:
        $("#nbandsform").prop('disabled',false)
        $("#nbandsform").fadeIn();
        $("#bandlengthform").fadeOut();
        $("#bandlengthform").prop('disabled',true)
      break;
    case 1:
        $("#bandlengthform").prop('disabled',false)
        $("#bandlengthform").removeAttr('hidden')
        $("#bandlengthform").fadeIn();
        $("#nbandsform").fadeOut();
        $("#nbandsform").prop('disabled',true)
      break;
  }
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

// Load resume table
function loadresume(){
  document.getElementById('resumemotorspeed').value = motorspeed
  document.getElementById('resumepressure').value = ['P: '+pressure+', '+ 'Δ: '+deltapressure]
  document.getElementById('resumeoffsets').value = ['x: '+offsetx.toFixed(2)+', '+ 'y: '+offsety.toFixed(2)]
  document.getElementById('resumesizes').value = ['x: '+sizex+', '+'y: '+sizey]
  document.getElementById('resumebandproperties').value = method.value
  if(method.selectedIndex==0){
    document.getElementById('nbandsrow').hidden = false
    document.getElementById('resumenbands').value = nbands
    document.getElementById('lengthbandsrow').hidden = true
  }
  else{
    document.getElementById('lengthbandsrow').hidden = false
    document.getElementById('resumelengthbands').value = bandlength
    document.getElementById('nbandsrow').hidden = true
  }
  document.getElementById('resumeheigth').value = bandheight
  document.getElementById('resumegap').value = gap
}

$(document).ready(function(){
  // AJAX POST of the serial_port connection
  var $SaveSampleApplicationForm = $('.savesampleapplication-form')
  $SaveSampleApplicationForm.submit(function(event){
    event.preventDefault()
    var $formData = $(this).serialize()
    var $endpoint = window.location.origin+'/samplesave/'
    $.ajax({
      method: 'POST',
      url:    $endpoint,
      data:   $formData,
      success: connectionFormSuccess,
      error: connectionFormError,
    })
  })
})
function connectionFormSuccess(data, textStatus, jqXHR){
  console.log(data)
}
function connectionFormError(jqXHR, textStatus, errorThrown){
  console.log('error');
}
