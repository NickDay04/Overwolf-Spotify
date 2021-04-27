var _plugin = null;
overwolf.extensions.current.getExtraObject("simple-io-plugin", (result) => {
  if (result.status === "success") {
    _plugin = result.object;
  }
})



function openAuthLink(){
  overwolf.utils.openUrlInDefaultBrowser("https://accounts.spotify.com/authorize?client_id=91b7ed5b61984131a7d7425d890dbdcf&response_type=code&redirect_uri=https%3A%2F%2Foverwolf-spotify-code.herokuapp.com%2Fmain.html&show_dialog=false")
}

function writeCallback(){
  console.log("[INFO] Refresh token saved");
}

function readCallback(result){
  console.log(result.content);
}

function readResponse(getRefresh){
  getRefresh.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      console.log(this.responseText);
      return refreshToken = JSON.parse(this.responseText).refresh_token;
    }

    else{
      console.log("[ERROR] Error in refresh token POST request");
      console.log(getRefresh.responseText);
    }
  } 
}

function authenticationCodeSave(){
  var ReadFileOptions = {encoding: "UTF8",
  maxBytesToRead: 0,
  offset: 0}
  var refreshToken = "";

  var bodyData = {"grant_type": "authorization_code", "code": document.getElementById("authentication_code_input").value, "redirect_uri": "https://overwolf-spotify-code.herokuapp.com/main.html", "client_id": "91b7ed5b61984131a7d7425d890dbdcf", "client_secret": "35557b16e54348f2a386df61ece15d06"};

  var authToken = document.getElementById("authentication_code_input").value;
  // overwolf.web.FetchHeader = [{ key: "Content-Type", value: "application/json" }];
  // var pogchamp;

  // overwolf.web.sendHttpRequest("https://accounts.spotify.com/api/token", overwolf.web.enums.HttpRequestMethods["POST"], overwolf.web.FetchHeader, JSON.stringify(bodyData), function(result) { console.log(result); });

  fetch("https://accounts.spotify.com/api/token", data={
    method: "POST",
    mode: "cors",
    credentials: "same-origin",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(bodyData)
  })
    .then(response => console.log(response))
    .then(data => {
      console.log(data);
    })
    .then((error) => console.log(error));

  // refreshToken = readResponse(getRefresh);

  // overwolf.io.writeFileContents("sokenToRefresh.txt", refreshToken, "UTF8", true, writeCallback());
  // overwolf.io.readTextFile("C:\\Windows\\System32\\sokenToRefresh.txt", ReadFileOptions, function(result) { console.log(result.content); });
}