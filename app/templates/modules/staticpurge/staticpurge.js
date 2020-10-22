$('#pump_manual').on('click',function(e){
  event.preventDefault();
    console.log($("#static-form").serialize());
    $.ajax({
    method: 'POST',
    url:    window.location.origin+'/staticpurge/',
    data:   $("#static-form").serialize(),
    success: staticCleanMethodSuccess,
    error: staticCleanMethodError,
    })
    function staticCleanMethodSuccess(data, textStatus, jqXHR){
    }
    function staticCleanMethodError(jqXHR, textStatus, errorThrown){}
  }
)
$('#steprange').on('change',function(e){
  $('#steptext').val($(this).val())
})
$('#steptext').on('change',function(e){
  $('#steprange').val($(this).val())
})


$("#next_bttn_stat").on('click',function(e){
  $.when($("#staticpurgecard").fadeOut()).done(function() {
         $("#stepscounter").text('Step 2/3')
         $("#dinamicpurgecard").fadeIn();
  });
})

