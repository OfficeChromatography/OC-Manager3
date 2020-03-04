var ctx = document.getElementById('plotPreview').getContext('2d');
var plotPreview = new Chart(ctx, {
   type: 'scatter',
   data: {
      datasets: [{
         // data: [{
         //    x: 1,
         //    y: 1
         // }, {
         //    x: 3,
         //    y: 7
         // }, {
         //    x: 6,
         //    y: 5
         // }, { // add same data as the first one, to draw the closing line
         //    x: 1,
         //    y: 1
         // }],
         borderColor: 'black',
         backgroundColor: 'transparent',
         borderWidth: 3,
         pointBackgroundColor: ['#000', '#000', '#000'],
         pointRadius: 3,
         pointHoverRadius: 3,
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
          display: true,
          stacked: true,
          ticks: {
            min: 0, // minimum value
            max: 100, // maximum value
          }
        }],
        xAxes: [{
          display: true,
          stacked: true,
          ticks: {
            min: 0, // minimum value
            max: 100, // maximum value
          }
        }]

    }
   },
});

function changegraph(event){
  while(plotPreview.data.datasets.pop()!=undefined){}
  switch(event.target.id) {
    case 'sizex':
      plotPreview.config.options.scales.xAxes[0].ticks.max = parseInt(document.getElementById('sizex').value);
      break;
    case 'sizey':
      plotPreview.config.options.scales.yAxes[0].ticks.max = parseInt(document.getElementById('sizey').value);
      break;
    case 'nbands':
      pointgen(plotPreview)
      break;
    case 'offsetx':
      pointgen(plotPreview)
      break;
    case 'offsety':
      pointgen(plotPreview)
      break;
    case 'gap':
      pointgen(plotPreview)
      break;
  }
  plotPreview.update();
}

document.i

function pointgen(graph){
  sizex = parseInt(document.getElementById('sizex').value);
  offsety = parseInt(document.getElementById('offsety').value);
  offsetx = parseInt(document.getElementById('offsetx').value);
  workarea = sizex-(2*offsetx);
  gap = parseInt(document.getElementById('gap').value);
  nbands = parseInt(document.getElementById('nbands').value);
  bandheight = parseInt(document.getElementById('bandheight').value);
  bandlength = (workarea-(gap*(nbands-1)))/nbands;
  if(bandlength>=0){
    for(i=0;i<nbands;i++){
      newdata = []
      if(i==0){
        newdata[0]={y:offsety,x:offsetx}
        newdata[1]={y:offsety+bandheight,x:offsetx}
        newdata[2]={y:offsety+bandheight,x:bandlength+offsetx}
        newdata[3]={y:offsety,x:bandlength+offsetx}
        newdata[4]={y:offsety,x:offsetx}
      }
      else{
        newdata[0]={y:offsety,x:i*(bandlength+gap)+offsetx}
        newdata[1]={y:offsety+bandheight,x:i*(bandlength+gap)+offsetx}
        newdata[2]={y:offsety+bandheight,x:(i+1)*bandlength+(gap*i)+offsetx}
        newdata[3]={y:offsety,x:(i+1)*bandlength+(gap*i)+offsetx}
        newdata[4]={y:offsety,x:i*(bandlength+gap)+offsetx}
      }
      addData(graph,i,'black', newdata)
    }
  }
  else if(!Number.isNaN(bandlength)){
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
      borderWidth: 3,
      pointBackgroundColor: ['#000', '#000', '#000'],
      pointRadius: 3,
      pointHoverRadius: 1,
      fill: true,
      tension: 0,
      showLine: true,
    });
    chart.update();
}

// window.addEventListener("resize",function(){})
