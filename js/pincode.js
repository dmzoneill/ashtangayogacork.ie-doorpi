pincode_visible = false;
boost_running = false;
boost_timer = null;
boost_count = 900;

function update_schedule() {
  $.get("index.php?schedule=true", function (data) {
    $("#scheduletable").html(data);
  });
}

function update_heating() {
  console.log($("#schedule_toggle").is(":checked"));
  console.log($("#schedule_minutes_prior").val());
  console.log($("#schedule_run_period").val());
  console.log($("#schedule_on_temp").val());
  console.log($("#schedule_cutoff_temp").val());

  $.post("index.php?heating=true", {
    schedule_toggle: $("#schedule_toggle").is(":checked"),
    schedule_minutes_prior: $("#schedule_minutes_prior").val(),
    schedule_run_period: $("#schedule_run_period").val(),
    schedule_on_temp: $("#schedule_on_temp").val(),
    schedule_cutoff_temp: $("#schedule_cutoff_temp").val()
  }, function (data) {
    var obj = JSON.parse(data);
    console.log(obj);
  });
}

function update_door() {
  console.log($("#door_schedule_toggle").is(":checked"));
  console.log($("#door_schedule_minutes_prior").val());
  console.log($("#door_schedule_minutes_class_term").val());

  $.post("index.php?door=true", {
    door_schedule_toggle: $("#door_schedule_toggle").is(":checked"),
    door_schedule_minutes_prior: $("#door_schedule_minutes_prior").val(),
    door_schedule_minutes_class_term: $("#door_schedule_minutes_class_term").val()
  }, function (data) {
    var obj = JSON.parse(data);
    console.log(obj);
  });
}

function door_controls() {

  $("#door_schedule_toggle").change(function () {
    setTimeout(update_door, 200);

    var checked = $("#door_schedule_toggle").is(":checked");

    if (checked) {
      $.get("index.php?status=0", function (data) {
        update_door();
      });
      return;
    }

    $.get("index.php?status=1", function (data) {
      update_door();
    });

  });

  $(".door-icon-plus").click(function () {
    setTimeout(update_door, 200);
  });

  $(".door-icon-minus").click(function () {
    setTimeout(update_door, 200);
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
  $("#schedule_toggle").change(function () {
    setTimeout(update_heating, 200);
  });

  $(".icon-plus").click(function () {
    setTimeout(update_heating, 200);
  });

  $(".icon-minus").click(function () {
    setTimeout(update_heating, 200);
  });

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

function function_switcher() {
  $(".door-manager").click(function () {
    $("#heat-manager").hide();
    $("#door-manager").show();
  });

  $(".heat-manager").click(function () {
    $("#door-manager").hide();
    $("#heat-manager").show();
  });
}

function opendoor() {
  $.get("index.php?opendoor=true");
}

function pin_controls() {
  // http://www.jsfuck.com/
  //var pin = (+!![] + []) + (!+[] + !![] + []) + (!+[] + !![] + !![] + []) + (!+[] + !![] + !![] + !![] + []);
  var pin = "1972";
  var enterCode = "";
  enterCode.toString();

  $("#numbers button").click(function () {

    var clickedNumber = $(this).text().toString();
    enterCode = enterCode + clickedNumber;
    var lengthCode = parseInt(enterCode.length);
    lengthCode--;
    $("#fields .numberfield:eq(" + lengthCode + ")").addClass("active");

    if (lengthCode == 3) {
      // Check the PIN
      if (enterCode == pin) {
        // Right PIN!
        $("#fields .numberfield").addClass("right");
        $("#numbers").addClass("hide");
        $("#pincode").hide();
        $("#controls").show();
        enterCode = "";
        $("#fields .numberfield").removeClass("active");
        $("#fields .numberfield").removeClass("right");
        $("#numbers").removeClass("hide");
        $("#gridheader p").html("<strong>Please enter your PIN-Code</strong>");
      } else {
        // Wrong PIN!
        $("#fields").addClass("miss");
        enterCode = "";
        setTimeout(function () {
          $("#fields .numberfield").removeClass("active");
        }, 200);
        setTimeout(function () {
          $("#fields").removeClass("miss");
        }, 500);

      }
    }
  });

  $("#logofade").click(function () {
    if (pincode_visible == false) {
      $("#controls").hide();
      $("#schedule").hide();
      $("#pincode").show();
      pincode_visible = true;
      return;
    }

    $("#controls").hide();
    $("#pincode").hide();
    $("#schedule").show();
    pincode_visible = false;
  });
}

$(document).ready(function () {

  $('.number-spinner>.ns-btn>a').click(function () {
    var btn = $(this),
      oldValue = btn.closest('.number-spinner').find('input').val().trim(),
      newVal = 0;

    if (btn.attr('data-dir') === 'up') {
      newVal = parseInt(oldValue) + 1;
    } else {
      if (oldValue > 1) {
        newVal = parseInt(oldValue) - 1;
      } else {
        newVal = 1;
      }
    }
    btn.closest('.number-spinner').find('input').val(newVal);
  });

  $('.number-spinner>input').keypress(function (evt) {
    evt = (evt) ? evt : window.event;
    var charCode = (evt.which) ? evt.which : evt.keyCode;
    if (charCode > 31 && (charCode < 48 || charCode > 57)) {
      return false;
    }
    return true;
  });

  pin_controls();
  door_controls();
  heating_controls();
  function_switcher();

  $("#controls").hide();
  $("#pincode").hide();
  $("#schedule").show();

  window.setInterval(function () {
    $.get("index.php?armdoor", function (data) {
      $.get("index.php?schedule=true", function (data) {
        $("#scheduletable").html(data);
      });
    });
    $.get("index.php?settings=true", function (data) {
      var settings = JSON.parse(data);
      if ($("#schedule_toggle").is(":checked") != settings.schedule_toggle) {
        $("#schedule_toggle").prop("checked", settings.schedule_toggle);
      }

      if ($("#schedule_minutes_prior").val() != settings.schedule_minutes_prior) {
        $("#schedule_minutes_prior").val(settings.schedule_minutes_prior);
      }

      if ($("#schedule_run_period").val() != settings.schedule_run_period) {
        $("#schedule_run_period").val(settings.schedule_run_period);
      }

      if ($("#schedule_on_temp").val() != settings.schedule_on_temp) {
        $("#schedule_on_temp").val(settings.schedule_on_temp);
      }

      if ($("#schedule_cutoff_temp").val() != settings.schedule_cutoff_temp) {
        $("#schedule_cutoff_temp").val(settings.schedule_cutoff_temp);
      }
    });

    $.get("index.php?door_settings=true", function (data) {
      var settings = JSON.parse(data);
      if ($("#door_schedule_toggle").is(":checked") != settings.door_schedule_toggle) {
        $("#door_schedule_toggle").prop("checked", settings.door_schedule_toggle);
      }

      if ($("#door_schedule_minutes_prior").val() != settings.door_schedule_minutes_prior) {
        $("#door_schedule_minutes_prior").val(settings.door_schedule_minutes_prior);
      }

      if ($("#door_schedule_minutes_class_term").val() != settings.door_schedule_minutes_class_term) {
        $("#door_schedule_minutes_class_term").val(settings.door_schedule_minutes_class_term);
      }
    });
  }, 15000);

  $.get("index.php?schedule=true", function (data) {
    $("#scheduletable").html(data);
  });
});
