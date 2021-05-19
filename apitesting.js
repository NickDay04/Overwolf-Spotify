var XMLHttpRequest = require("xmlhttprequest").XMLHttpRequest;

function reqListener(){
    console.log(this.responseText)
}

var code = "AQCyngT1moFIg0UQw53_413Yy49n5RcPeshXAC_0wO6IOVX7RcpGV7B_4gNx4YLoAxPEjjvewTy2XklLG6As3qQ_2TiTJKI4MkqJgIxNNhPpIlnn9KlettnHreYnK28KaL-bj2cvpUJIJZ-QAXZVWKZX3atq8yxDAOlvRwvBJIsfKBsEXm59Egex8cpDm8IELxarpQ";

var oReq = new XMLHttpRequest();
oReq.addEventListener("load", reqListener);
oReq.open("POST", "https://overwolf-spotify-code.herokuapp.com/clip/authorisation?code=" + code);
oReq.send();