url =  window.location.href;
var onProgress=0;
var onProgressDetail=[];

btt_erase = document.getElementById('btt_erase')
btt_upload = document.getElementById('btt_upload')
function move(a ,event){
  event.preventDefault();
  $.post(url, a)
  console.log(a);
  onProgress++;
  onProgressDetail.push(a);
}

function run(event){
  event.preventDefault();
  gcode = document.getElementById('Gcode').value
  console.log("apretee");
  $.post(url, gcode = {
    "Gcode":gcode
  })
}

btt_erase.addEventListener("click", function(event){
    event.preventDefault();
    document.getElementById('Gcode').value="";
})

btt_upload.addEventListener("click", function(event){
    event.preventDefault();
    document.getElementById('file_input').click()
})



// function connectionVerify(connectionStatus){
//   if (connectionStatus=='False'){
//     document.getElementById("footer").classList.remove('bg-white');
//     document.getElementById("footer").classList.add('bg-warning');
//     document.getElementById("footerText").innerHTML="Arduino Disconnected"
//   }
// }
