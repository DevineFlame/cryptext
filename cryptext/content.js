
// let list = [][];
// let fluct = [][];

let coins = ["ZRX", "AE", "AION", "ETH","BTC","LTC","XRP","BCH","OMG","REQ","GNT","BAT","TRX","XLM","NEO","GAS","XRB","NCASH","EOS"]

var fluct = new Array(3);
var list = new Array(19);
for (var i = 0; i < 19; i++) {
  list[coins[i]] = new Array();
  fluct[coins[i]] = new Array(3);
}


function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}
function init(){
  console.log("hi");
  for (var i=0; i < coins.length; i++)
  log_data(coins[i]);
}


async function log_data(coin) {
	while(true){

	 var val = document.getElementsByClassName(coin)[0].childNodes[3].innerText
	  //document.getElementById("data").innerHTML=data;  
    

   val = parseFloat(val.replace(",", ""));

    if (list[coin].length <= 100 && val != fluct[2])
    {
     list[coin].push(val);
    }
    else
    {
      list[coin].pop();
      list[coin].push(val);
    }
  // console.log(coin + list[coin]);
   fluct[coin][0] = Math.min(...list[coin]);
   fluct[coin][1] = Math.max(...list[coin]);
   fluct[coin][2] = val;


   var diff = parseFloat(fluct[coin][1]- fluct[coin][0])/fluct[coin][0];
   /// fluct[0])*100; 
  //console.log(coin + "  " + fluct[coin][0] + "  " + fluct[coin][1] +"  " + fluct[coin][2]+ " "  + diff*100);
 // num.toFixed(3).slice(0,-1)
   if (diff*100 > 5 )
   {
    notify(coin+ " " +fluct[coin][0] + " " + fluct[coin][1] + " "+ (diff*100).toFixed(3).slice(0,-1),coin );
   }

	 await sleep(5000);}
}

function notify(change,coin)
{


var settings = {
  "async": true,
  "crossDomain": true,
  "url": "https://onesignal.com/api/v1/notifications",
  "method": "POST",
  "headers": {
    "authorization": "Basic MzUzY2UyOTYtZDQ3Ni00YTQ2LWE3ZDMtYjQ3ZTQ0N2UzZGIw",
    "content-type": "application/json"
  },
  "android_group":true,
  "processData": false,
  "data": " {\r\n  \"app_id\": \"e76da36d-2560-486b-933c-6f9367de652c\",\r\n  \"included_segments\": [\"All\"],\r\n  \"tag\": [\""+coin+"\"],\r\n  \"data\": {\"foo\": \""+coin+"\"},\r\n  \"android_group_message\":{\"en\": \"$[notif_count]\"},\r\n  \"contents\": {\"en\": \""+change+"\"}\r\n}"
}

$.ajax(settings).done(function (response) {
  console.log(response);
});

}

  setTimeout(init,2000);


