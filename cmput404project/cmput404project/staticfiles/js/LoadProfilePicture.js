function getRandomInt(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
}
var div = document.getElementById("profile-picture");
var random = getRandomInt(0, 19);
var img = new Image();
img.src =  images+random.toString()+'.png';
div.appendChild(img);
