var ctx = document.getElementById('plotPreview').getContext('2d');
var sizex = parseInt(document.getElementById('sizex').value);
var sizey = parseInt(document.getElementById('sizey').value);
var offsety = parseInt(document.getElementById('offsety').value);
var offsetx = parseInt(document.getElementById('offsetx').value);
var gap = parseInt(document.getElementById('gap').value);
var nbands = parseInt(document.getElementById('nbands').value);
var workingarea = {x:0,y:0}


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
      bandsizecalc()
      break;
  }
  pointgen(plotPreview)
  plotPreview.update();
}


function workingareacalc(){
  workingarea = {x:sizex-(2*offsetx), y:sizey-(2*offsety)}
}

function bandsizecalc(){
  workingareacalc()
  var floatnbands = (workingarea.x+gap)/(bandlength+gap)
  nbands = Math.trunc(floatnbands)
  leftover = bandlength*(floatnbands%nbands)
  offsetx += leftover
}


function pointgen(graph, bandsize){
  workingareacalc()
  if($('#method')[0].selectedIndex==0){
    bandsize = (workingarea.x-(gap*(nbands-1)))/nbands;
  }
  else{
    bandsizecalc()
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
  }
  else if((!Number.isNaN(bandsize) || !Number.isNaN(offsetx)) && !Number.isNaN(nbands)){
    dataerror()
  }
}

function dataerror(){
  window.alert("Incorrect data");
}

function configurationdisplay(event){
  value=event.target.selectedIndex
  switch (value) {
    case 0:
        $("#nbandsform").fadeIn();
        $("#bandlengthform").fadeOut();
      break;
    case 1:
        $("#bandlengthform").removeAttr('hidden')
        $("#bandlengthform").fadeIn();
        $("#nbandsform").fadeOut();
      break;
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

// window.addEventListener("resize",function(){})
