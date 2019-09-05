<?php

$override = "/var/www/html/override";
$thefile = "/var/www/html/enabled";

if (isset($_GET['status'])) {
    if ($_GET['status'] == "0") {
        unlink($override);
        print "disable";
    } else {
        touch($override);
        file_put_contents($override, time());
        chmod($override, 777);
        print "enable";
    }
    exit;
}

if (isset($_GET['schedule'])) {

    $json = file_get_contents("schedule.json");

    $classes = json_decode($json, true);

    $now = new DateTime(date("Y-m-d"));
    $now_time = date("H:i");

    $out = "<table width='100%'>";

    $i = 0;

    foreach ($classes as $class) {
        $date = new DateTime($class['date']);
        $start_time = substr($class['start_time'], 0, 5);
        $end_time = substr($class['end_time'], 0, 5);
        $teacher = $class['name'];
        $cname = $class['ctname'];

        if ($date == $now) {
            if ($i == 0 && $now_time >= $end_time) {
                continue;
            }
            if ($now_time > $start_time && $now_time < $end_time) {
                $out .= "<tr><td><h1>Now</h1></td></tr>";
            } else {
                $out .= "<tr><td><h1>Next</h1></td></tr>";
            }
            $out .= "<tr><td><h3>$cname<br>with $teacher</h3></td></tr>";
            $out .= "<tr><td><h4>$start_time - $end_time</h4></td></tr>";

            $i++;

            if ($i > 1) {
                break;
            }
        }
    }

    if (file_exists($thefile)) {
        $out .= "<tr><td><h5 class='good' id='doorarm'>Door is armed</h5></td></tr>";
    }
    if (!file_exists($thefile)) {
        $out .= "<tr><td><h5 class='bad' id='doorarm'>Door is disarmed</h5></td></tr>";
    }

    $out .= "<tr><td><br><span style='font-size:9pt'>" . date("F j, Y, G:i") . "</span></td></tr>";

    $out .= "</table>";

    print $out;

    exit;
}

if (isset($_GET['armdoor'])) {

    $json = file_get_contents("schedule.json");
    $classes = json_decode($json, true);

    $now = new DateTime(date("Y-m-d"));
    $now_time = date("H:i", time());

    $enabled = false;

    foreach ($classes as $class) {
        $date = new DateTime($class['date']);
        $start_time = date("H:i", strtotime($class['start_time']) - 1800 );
        $end_time = date("H:i", strtotime($class['end_time']) - 1800 );

        if ($date == $now) {
            if ($now_time >= $end_time) {
                continue;
            }
            if ($now_time > $start_time && $now_time < $end_time) {
                print "== T\n";
                print $start_time . "\n";
                print $now_time . "\n";
                print $end_time . "\n";
                $enabled = true;
            } else {
                print "== F\n";
                print $start_time . "\n";
                print $now_time . "\n";
                print $end_time . "\n";
            }
        }
    }

    if ($enabled == true && file_exists($override) == false) {
        touch($thefile);
        file_put_contents($thefile, time());
        chmod($thefile, 777);
    } else {
        @unlink($thefile);
    }
    exit;
}

?>
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Ashtanga Yoga Cork</title>
    <link rel="stylesheet" href="pincode.css">
</head>
<body>
    <div class="center">
        <table class='tablewrapper'>
            <tr>
                <td><img src='logo-500.png' id='logofade' style='width:260px; margin-right:20px; margin-left:20px' /></td>
                <td style='width:200px; text-align: right'>

                    <div id="pincode">
                        <div class="table">
                            <div class="cell">

                                <div id="gridheader">
                                    <p>
                                        <strong>Please enter your PIN-Code</strong>
                                    </p>
                                </div>

                                <div id="fields">
                                    <div class="grid">
                                        <div class="grid__col grid__col--1-of-4 numberfield"><span></span></div>
                                        <div class="grid__col grid__col--1-of-4 numberfield"><span></span></div>
                                        <div class="grid__col grid__col--1-of-4 numberfield"><span></span></div>
                                        <div class="grid__col grid__col--1-of-4 numberfield"><span></span></div>
                                    </div>
                                </div>

                                <div id="numbers">
                                    <div class="grid">
                                        <div class="grid__col grid__col--1-of-3">
                                            <button>1</button>
                                        </div>
                                        <div class="grid__col grid__col--1-of-3">
                                            <button>2</button>
                                        </div>
                                        <div class="grid__col grid__col--1-of-3">
                                            <button>3</button>
                                        </div>

                                        <div class="grid__col grid__col--1-of-3">
                                            <button>4</button>
                                        </div>
                                        <div class="grid__col grid__col--1-of-3">
                                            <button>5</button>
                                        </div>
                                        <div class="grid__col grid__col--1-of-3">
                                            <button>6</button>
                                        </div>

                                        <div class="grid__col grid__col--1-of-3">
                                            <button>7</button>
                                        </div>
                                        <div class="grid__col grid__col--1-of-3">
                                            <button>8</button>
                                        </div>
                                        <div class="grid__col grid__col--1-of-3">
                                            <button>9</button>
                                        </div>

                                        <div class="grid__col grid__col--1-of-3"></div>
                                        <div class="grid__col grid__col--1-of-3">
                                            <button>0</button>
                                        </div>
                                        <div class="grid__col grid__col--1-of-3"></div>

                                    </div>
                                </div>

                            </div>
                        </div>
                    </div>
                    <div class="slide" id="controls">
                        <div class="table">
                            <div class="cell">
                                <br>
                                <button class='buttonred' id='buttonred'>Disarm Door</button>
                                <br>
                                <br>
                                <button class='buttongreen' id='buttongreen'>Arm Door</button>
                                <br>
                            </div>
                        </div>
                    </div>

                    <div class="slide" id="schedule">
                        <div class="table">
                            <div class="cell" id="scheduletable">
                                schedule
                            </div>
                        </div>
                    </div>
                </td>
            </tr>
        </table>

    </div>

    <script src='jq.js'></script>
    <script src="pincode.js"></script>
    <script type="text/javascript">

    var ws;

    function init() {

      ws = new WebSocket("ws://<?php print $_SERVER['SERVER_ADDR'];?>:9001/");

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
        console.log(e)
      };

    }

    $(document).ready(function() {
	    init();
    });


    function output(str) {
       console.log( "x:" + str)
       if(str.localeCompare("") == 0) {
            return;
       } else if(str.localeCompare("True") == 0) {
           $("#logofade").animate({opacity: 0}, 1000);
       } else if(str.localeCompare("False") == 0) {
           $("#logofade").animate({opacity: 1}, 1000);
       }
    }

    </script>
</body>
</html>
