var categories = ["tutorial", "dog", "corgi", "dogs", "not a cat", "dogs 4 lyfe"];
var div = document.getElementById("category");
for(var i=0; i < categories.length;i++){
  var checkbox = document.createElement('input');
  checkbox.type = "checkbox";
  checkbox.name = "categories";
  checkbox.value = categories[i];
  checkbox.className = "category";
  var label = document.createElement('label');
  label.className = "category";
  label.appendChild(document.createTextNode(categories[i]));
  div.appendChild(checkbox);
  div.appendChild(label);
}
