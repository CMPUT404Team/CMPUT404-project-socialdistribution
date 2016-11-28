var div = document.getElementById("background");
var numOfPhotos = 18;
for(var i=0; i < numOfPhotos;i++){
    var img = new Image();
    img.src =  images+i.toString()+'.png';
    img.className = "tiled-photo";
    div.appendChild(img);
}
