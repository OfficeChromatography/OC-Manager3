$(document).ready(function(){
  $.get( window.location.origin + '/isconnected/', function( data ) {
    console.log(data);
    foot = document.getElementById("footer")
    footText = document.getElementById("footerText")
    if (data.port!=null){
      foot.classList.replace(foot.classList[1],'bg-success')
      footText.innerHTML="OC-Lab Connected to "+ data.port
    } else{
      foot.classList.replace(foot.classList[1],'bg-warning')
      footText.innerHTML="OC-Lab Disconnected"
    }
  });
})
