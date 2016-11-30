var mdClasses = document.getElementsByClassName('md-content');
for (var i = 0; i < mdClasses.length; i++) {
	var mdInner = mdClasses[i].innerText;
	mdClasses[i].innerHTML = marked(mdInner);
}