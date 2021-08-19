boost_running = false;
boost_timer = null;
boost_count = 900;

var host = window.location.host; 

function update_schedule() {
  $.get("http://" + host + "/index.php?schedule=true", function (data) {
    $("#schedule").show();
    $("#scheduletable").html(data);
    heating_controls();
    $.get("http://" + host + "/scratch/temperature", function (data) {
      $("#metric_temp").text(data + "C");    
    });
    $.get("http://" + host + "/scratch/humidity", function (data) {
      $("#metric_humid").text(data + "%");    
    });
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
      $.get("http://" + host + ":8000/boost");
    }
    else {
      $.get("http://" + host + ":8000/reset");
      boost_running = false;
      clearInterval(boost_timer);
      $("#schedule_boost").text("15 Mins");
      boost_count = 900;
    }
  });
}

function opendoor() {
  $.get("http://" + host + "/index.php?opendoor=true");
}

$(document).ready(function () {
  update_schedule();

  window.setInterval(function () {
    update_schedule();
  }, 10000);
});
