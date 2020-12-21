//$(document).ready(function(){
//    checkConnection();
//})
//
//function footerState(data){
//    foot = $('#footer')
//    footText = $('#footerText')
//    if (data.connected==true){
//      $('#footer').removeClass("bg-warning").addClass("bg-success");
//      footText.html("OC-Lab Connected to "+ data.port)
//    } else{
//      foot.removeClass("bg-success").addClass("bg-warning");
//      footText.html("OC-Lab Disconnected")
//    }
//}
//
//function checkConnection(){
////This promise will resolve when the network call succeeds
//var networkPromise = fetch(window.location.origin + '/isconnected/')
//                    .then(response=>response.json())
//                    .then(data=>footerState(data));
//
////This promise will resolve when 2 seconds have passed
//var timeOutPromise = new Promise(function(resolve, reject) {
//  // 4 Second delay
//  setTimeout(resolve, 4000, 'Timeout Done');
//});
//
//Promise.all(
//[networkPromise, timeOutPromise]).then(function(values) {
//  checkConnection();
//});
//}

