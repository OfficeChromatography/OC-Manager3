$(document).ready(function(){
  checkconnection();
})

// function checkconnection(){
//   $.get( window.location.origin + '/isconnected/', function( data ) {
//     foot = document.getElementById("footer")
//     footText = document.getElementById("footerText")
//     if (data.port!=null){
//       foot.classList.replace(foot.classList[1],'bg-success')
//       footText.innerHTML="OC-Lab Connected to "+ data.port
//     } else{
//       foot.classList.replace(foot.classList[1],'bg-warning')
//       footText.innerHTML="OC-Lab Disconnected"
//     }
//   });
// }

function checkconnection(){
  $.get( window.location.origin + '/isconnected/', function( data ) {
    foot = $('#footer')
    footText = $('#footerText')
    if (data.connected==true){
      $('#footer').removeClass("bg-warning").addClass("bg-success");
      footText.html("OC-Lab Connected to "+ data.port)
    } else{
      foot.removeClass("bg-success").addClass("bg-warning");
      footText.html("OC-Lab Disconnected")
    }
  });
}
