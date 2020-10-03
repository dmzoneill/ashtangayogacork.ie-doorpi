boost_running = false;
boost_timer = null;
boost_count = 900;

var ws;
var ws2;
function init() {

    ws = new WebSocket("ws://192.168.8.2:9001/");

    ws.onopen = function() {
        output("onopen");
    };

    ws.onmessage = function(e) {
        output(e.data);
    };

    ws.onclose = function() {
        output("onclose");
    };

    ws.onerror = function(e) {
        output("onerror");
        console.log(e);
    };
}

function init2() {
    ws2 = new WebSocket("ws://192.168.8.2:9002/");

    ws2.onopen = function() {
        console.log("onopen");
    };

    ws2.onmessage = function(e) {
        output2(e.data);
    };

    ws2.onclose = function() {
        console.log("close");
    };

    ws2.onerror = function(e) {
        console.log(e)
    };
}

function output(str) {
   console.log( "x:" + str)
}

function output2(str) {
   console.log( "x:" + str)
   if(str.localeCompare("") == 0) {
        return;
   }

   if(str.indexOf(',') > 0 ){
       var parts = str.split(',');
       celcius = parseFloat((parts[0]).substring(0,4))
       hum = parseFloat((parts[1]).substring(0,4))

       if(celcius > 0 && hum > 0) {
          $("#metric_temp").text(celcius + "C");
          $("#metric_humid").text(hum + "%");
       }
   }
}

function update_schedule() {
  $.get("index.php?schedule=true", function (data) {
    $("#schedule").show();
    $("#scheduletable").html(data);
    heating_controls();
  });
}

function counterdown() {
  boost_count = boost_count - 1;
  if (boost_count == 0) {
    boost_running = false;
    clearInterval(boost_timer);
    $("#schedule_boost").text("15 Mins");
    boost_count = 900;
    return;
  }

  mins = Math.floor(boost_count / 60);
  secs = boost_count % 60;
  if( secs % 3 > 0 )
  {
    $("#schedule_boost").text(mins + " mins " + secs + " secs");
  }
  else
  {
    $("#schedule_boost").text("Reset heaters");
  }
}

function heating_controls() {  
  $("#schedule_boost").click(function () {
    if (boost_running == false) {
      boost_timer = setInterval(counterdown, 1000);
      boost_running = true;
    }
    else {
      $.get("index.php?heatingreset=true");
      boost_running = false;
      clearInterval(boost_timer);
      $("#schedule_boost").text("15 Mins");
      boost_count = 900;
    }
    ws2.send("boost");
  });
}

function opendoor() {
  $.get("index.php?opendoor=true");
}

$(document).ready(function () {
  init2();
  init();
  update_schedule();

  window.setInterval(function () {
    update_schedule();
  }, 60000);
});