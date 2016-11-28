function getRandomInt(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
}
var div = document.getElementsByClassName("post-image");
for (var element in div) {
  var random = getRandomInt(0, 19);
  var img = new Image();
  img.src =  images+random.toString()+'.png';
  element.appendChild(img);
}
