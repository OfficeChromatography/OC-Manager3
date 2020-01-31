url =  window.location.href;
var onProgress=0;
var onProgressDetail=[];

btt_erase = document.getElementById('btt_erase')
btt_play = document.getElementById('btt_play')
btt_upload = document.getElementById('btt_upload')
function move(a ,event){
  // event.preventDefault();
  $.post(url, a)
}

btt_erase.addEventListener("click", function(event){
    event.preventDefault();
    document.getElementById('Gcode').value="";
})

btt_play.addEventListener("click", function(event){
  event.preventDefault();
  console.log("HOLAAA");
  gcode = document.getElementById('Gcode').value
  $.post(url, gcode = {
    "Gcode":gcode
  })
})
