// function sleep(ms) {
//   return new Promise(resolve => setTimeout(resolve, ms));
// }
// async function log_data() {
// 	while(true){

// 	 console.log(document.getElementsByClassName("ZRX")[0].innerText);
// 	  //document.getElementById("data").innerHTML=data;  

// 	 await sleep(2000);}
// }
var settings = {
  "async": true,
  "crossDomain": true,
  "url": "https://onesignal.com/api/v1/notifications",
  "method": "POST",
  "headers": {
    "authorization": "Basic MzUzY2UyOTYtZDQ3Ni00YTQ2LWE3ZDMtYjQ3ZTQ0N2UzZGIw",
    "content-type": "application/json"
  },
  "processData": false,
  "data": " {\r\n  \"app_id\": \"e76da36d-2560-486b-933c-6f9367de652c\",\r\n  \"included_segments\": [\"All\"],\r\n  \"data\": {\"foo\": \"bar\"},\r\n  \"contents\": {\"en\": \"English Message\"}\r\n}"
}

$.ajax(settings).done(function (response) {
  console.log(response);
});


//setTimeout(log_data,2000);
