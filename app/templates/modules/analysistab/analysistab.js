$('#analysistab-list a').on('click', function (e) {
    e.preventDefault()
    $(this).tab('show')
    loadWhichTabIsSelected()
  })

function loadWhichTabIsSelected(){
  selectedTab = $('.nav-link.active').text()
  if (selectedTab=="Chromatogram"){
    loadChromatogram()
  } else if (selectedTab=="Trackinspect"){
    loadTrackInspect()
  } else if (selectedTab=="Tracksort"){
    loadTracksort()
  } else if (selectedTab=="PCA"){
    loadPCA()
  } else if (selectedTab=="HCA"){
    loadHCA()
  } else if (selectedTab=="Heatmap"){
    loadHeatmap()
  }
}