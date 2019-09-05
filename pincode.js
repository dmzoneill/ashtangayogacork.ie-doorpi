pincode_visible = false;

function update_schedule() {
  $.get("index.php?schedule", function (data) {
    $("#scheduletable").html(data);
  });
}

$(document).ready(function () {

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

  $("#controls").hide();
  $("#pincode").hide();
  $("#schedule").show();

  $("#buttonred").click(function () {
    $("#controls").hide();
    $("#pincode").hide();
    $("#schedule").show();

    $.get("index.php?status=1", function (data) {
      update_schedule();
    });
  });

  $("#buttongreen").click(function () {
    $("#controls").hide();
    $("#pincode").hide();
    $("#schedule").show();

    $.get("index.php?status=0", function (data) {
      update_schedule();
    });
  });

  $.get("index.php?schedule", function (data) {
    $("#scheduletable").html(data);
  });

  window.setInterval(function () {
    $.get("index.php?armdoor", function (data) {
      $.get("index.php?schedule", function (data) {
        $("#scheduletable").html(data);
      });
    });
  }, 15000);

});
