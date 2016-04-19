var refresh = function() {
  h = window.innerHeight;
  elemh = document.getElementById("image-text").offsetHeight;
  document.getElementById("image-text").style.paddingTop = (h - elemh-94)/2 + "px";
  document.getElementById("image-text").style.paddingBottom = (h - elemh-94)/2 + "px";
};
refresh();
