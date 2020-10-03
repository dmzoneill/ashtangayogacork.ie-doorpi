<?php

$doorArmedFile = "/var/www/html/scratch/enabled";

if (isset($_GET['heatingreset'])) {
    print shell_exec("/var/www/html/bin/heater reboot");
    exit;
}

if (isset($_GET['schedule'])) {

    $json = file_get_contents("scratch/schedule.json");
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

    if (file_exists($doorArmedFile)) {
        $out .= "<tr><td><h1 class='good' id='doorarm'>Door is armed</h1></td></tr>";
    }
    if (!file_exists($doorArmedFile)) {
        $out .= "<tr><td><h1 class='bad' id='doorarm'>Door is disarmed</h1></td></tr>";
    }

    $cel = file_get_contents("/var/www/html/scratch/temperature");
    $hum = file_get_contents("/var/www/html/scratch/humidity");

    $out .= "<tr><td><span style='font-size:9pt'>" . date("F j, Y, G:i") . "</span></td></tr>";
    $out .= "<tr><td><br><button id='buttonopendoor' onclick='opendoor()' class='boost'>Open Door</button></td></tr>";
    $out .= "</table><br>";

    $out .= "<button id=\"schedule_boost\" class=\"boost\">Boost Heating</button><br><br>";

    $out .= "<table style='margin:auto'><tr><td style='padding-bottom:5px'>";
    $out .= "Temperature: <span id='metric_temp'>" . $cel . "C</span>";
    $out .= "</td></tr><tr><td>";
    $out .= "Humidity: <span id='metric_humid'>" . $hum . "%</span>";
    $out .= "</td></tr></table>";

    print $out;

    exit;
}

if (isset($_GET['opendoor'])) {
    print shell_exec("sudo /var/www/html/bin/opendoor");
    exit;
}

?>
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Ashtanga Yoga Cork</title>
    <link rel="stylesheet" href="css/doorpi.css">
</head>
<body>
    <div class="center">
        <table class='tablewrapper'>
            <tr>
                <td><img src='images/logo-500.png' id='logofade' style='width:380px; margin-right:40px; margin-left:40px' /></td>
                <td style='width:460px; text-align: right'>                    
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
    <script src='js/jq.js'></script>
    <script src="js/doorpi.js"></script>
</body>
</html>
