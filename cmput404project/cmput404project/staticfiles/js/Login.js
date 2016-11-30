function Login(){
  var div = document.getElementById("title");
  div.style.display = 'none';
  var loginDiv = document.getElementById("login");
  $(loginDiv).removeAttr('style');
  loginDiv.className = "login";
}
