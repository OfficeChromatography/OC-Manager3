getAirSensor = () => {
    $.get( window.location.origin+"/oclab/airsensor/", function(data) {
      $("#air_temperature").text(data.temperature+"°C")
      $("#air_humidity").text(data.humidity+"%")
    })
}

$("#air_sensor_sync").on("click", getAirSensor)
