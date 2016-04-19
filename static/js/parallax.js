(function(){

  var parallax = document.querySelectorAll(".parallax"),
  speed = 0.3;

  window.onscroll = function(){
    [].slice.call(parallax).forEach(function(el,i){

      var windowYOffset = window.pageYOffset,
      elBackgrounPos = "50% " + (windowYOffset * speed * 0.8) + "px";
              
      el.style.backgroundPosition = elBackgrounPos;

      });
  };

window.addEventListener("resize", function(e) {
    var mapElement = document.getElementById("splash-bg");
    mapElement.style.height = mapElement.offsetWidth * .5;
});

})();
