<?php

$override = "/var/www/html/scratch/override";
$thefile = "/var/www/html/scratch/enabled";

if (isset($_GET['heating'])) {
    $json = json_encode($_POST);
    file_put_contents("scratch/heating.json", $json);
    print $json;
    exit;
}

if (isset($_GET['door'])) {
    $json = json_encode($_POST);
    file_put_contents("scratch/door.json", $json);
    print $json;
    exit;
}

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

    if (file_exists($thefile)) {
        $out .= "<tr><td><h5 class='good' id='doorarm'>Door is armed</h5></td></tr>";
    }
    if (!file_exists($thefile)) {
        $out .= "<tr><td><h5 class='bad' id='doorarm'>Door is disarmed</h5></td></tr>";
    }

    $out .= "<tr><td><span style='font-size:9pt'>" . date("F j, Y, G:i") . "</span></td></tr>";
    $out .= "<tr><td><br><button class='buttonopendoor' id='buttonopendoor' onclick='opendoor()'>One Time Open Door</button></td></tr>";
    $out .= "</table>";

    print $out;

    exit;
}

if (isset($_GET['settings'])) {
    print file_get_contents("scratch/heating.json");
    exit;
}

if (isset($_GET['door_settings'])) {
    print file_get_contents("scratch/door.json");
    exit;
}

if (isset($_GET['opendoor'])) {
    @shell_exec("/usr/bin/opendoor");
    exit;
}

$schedule_toggle = true;
$schedule_minutes_prior = 45;
$schedule_run_period = 30;
$schedule_on_temp = 18;
$schedule_cutoff_temp = 25;

$door_schedule_toggle = true;
$door_schedule_minutes_prior = 30;
$door_schedule_minutes_class_term = 45;

if (file_exists("scratch/heating.json")) {
    $heating_settings = json_decode(file_get_contents("scratch/heating.json"), true);
    $schedule_toggle = $heating_settings['schedule_toggle'];
    $schedule_minutes_prior = $heating_settings['schedule_minutes_prior'];
    $schedule_run_period = $heating_settings['schedule_run_period'];
    $schedule_on_temp = $heating_settings['schedule_on_temp'];
    $schedule_cutoff_temp = $heating_settings['schedule_cutoff_temp'];
} else {
    file_put_contents("scratch/heating.json", '{"schedule_toggle":"true","schedule_minutes_prior":"45","schedule_run_period":"30","schedule_on_temp":"18","schedule_cutoff_temp":"25"}');
}

if (file_exists("scratch/door.json")) {
    $door_settings = json_decode(file_get_contents("scratch/door.json"), true);
    $door_schedule_toggle = $door_settings['door_schedule_toggle'];
    $door_schedule_minutes_prior = $door_settings['door_schedule_minutes_prior'];
    $door_schedule_minutes_class_term = $door_settings['door_schedule_minutes_class_term'];
} else {
    file_put_contents("scratch/door.json", '{"door_schedule_toggle":"true","door_schedule_minutes_prior":"30","door_schedule_minutes_class_term":"45"}');
}

if (isset($_GET['armdoor'])) {

    $json = file_get_contents("scratch/schedule.json");
    $classes = json_decode($json, true);

    $now = new DateTime(date("Y-m-d"));
    $now_time = date("H:i", time());

    $enabled = false;

    foreach ($classes as $class) {
        $date = new DateTime($class['date']);
        $start_time = date("H:i", strtotime($class['start_time']) - ($door_schedule_minutes_prior * 60));
        $end_time = date("H:i", strtotime($class['end_time']) - ($door_schedule_minutes_class_term * 60));

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
        chmod($thefile, 0777);
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
    <link rel="stylesheet" href="css/pincode.css">
</head>
<body>
    <div class="center">
        <table class='tablewrapper'>
            <tr>
                <td><img src='images/logo-500.png' id='logofade' style='width:260px; margin-right:20px; margin-left:20px' /></td>
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
                                <button class='door-manager'><img width='48' src='images/door-small.png'></button> <button><img width='48' class='heat-manager' src='images/heating-small.png'></button>
                                <br>
                                <br>
                                <div id='door-manager'>
                                    <br>
                                    <table style='margin:auto'>
                                        <tr>
                                            <td colspan='2'>
                                                <h4>Schedule</h4>
                                                <label class="switch">
                                                    <input type="checkbox" <?php print $door_schedule_toggle == "true" ? 'checked=checked' : '';?> id="door_schedule_toggle" class="door_schedule_changed">
                                                    <span class="slider"></span>
                                                </label>
                                            </td>
                                        </tr>
                                    </table>
                                    <br>
                                    <table style='margin:auto'>
                                        <tr>
                                            <td>
                                                <h4>Minutes Prior</h4>
                                                <div class="number-spinner">
                                                    <span class="ns-btn">
                                                        <a data-dir="dwn"><span class="icon-minus door-icon-minus"></span></a>
                                                    </span>
                                                    <input type="text" class="pl-ns-value door_schedule_changed" value="<?php print $door_schedule_minutes_prior;?>" maxlength="3" id="door_schedule_minutes_prior">
                                                    <span class="ns-btn">
                                                        <a data-dir="up"><span class="icon-plus door-icon-plus"></span></a>
                                                    </span>
                                                </div>
                                            </td>
                                            <td>
                                                <h4>Minutes End</h4>
                                                <div class="number-spinner">
                                                    <span class="ns-btn">
                                                        <a data-dir="dwn"><span class="icon-minus door-icon-minus"></span></a>
                                                    </span>
                                                    <input type="text" class="pl-ns-value door_schedule_changed" value="<?php print $door_schedule_minutes_class_term;?>" maxlength="3" id="door_schedule_minutes_class_term">
                                                    <span class="ns-btn">
                                                        <a data-dir="up"><span class="icon-plus door-icon-plus"></span></a>
                                                    </span>
                                                </div>
                                            </td>
                                        </tr>
                                    </table>
                                </div>
                                <div id='heat-manager' style='display: none'>
                                    <table style='margin:auto'>
                                        <tr>
                                            <td>
                                                <h4>Boost</h4>
                                                <button id="schedule_boost" class="boost">15 Mins</button>
                                            </td>
                                            <td>
                                                <h4>Schedule</h4>
                                                <label class="switch">
                                                    <input type="checkbox" <?php print $schedule_toggle == "true" ? 'checked=checked' : '';?> id="schedule_toggle" class="schedule_changed">
                                                    <span class="slider"></span>
                                                </label>
                                            </td>
                                        </tr>
                                    </table>
                                    <br>
                                    <table style='margin:auto'>
                                        <tr>
                                            <td>
                                                <h4>Minutes Prior</h4>
                                                <div class="number-spinner">
                                                    <span class="ns-btn">
                                                        <a data-dir="dwn"><span class="icon-minus"></span></a>
                                                    </span>
                                                    <input type="text" class="pl-ns-value schedule_changed" value="<?php print $schedule_minutes_prior;?>" maxlength="2" id="schedule_minutes_prior">
                                                    <span class="ns-btn">
                                                        <a data-dir="up"><span class="icon-plus"></span></a>
                                                    </span>
                                                </div>
                                            </td>
                                            <td>
                                                <h4>Run Period</h4>
                                                <div class="number-spinner">
                                                    <span class="ns-btn">
                                                        <a data-dir="dwn"><span class="icon-minus"></span></a>
                                                    </span>
                                                    <input type="text" class="pl-ns-value schedule_changed" value="<?php print $schedule_run_period;?>" maxlength="2" id="schedule_run_period">
                                                    <span class="ns-btn">
                                                        <a data-dir="up"><span class="icon-plus"></span></a>
                                                    </span>
                                                </div>
                                            </td>
                                        </tr>
                                    </table>

                                    <br>
                                    <table style='margin:auto'>
                                        <tr>
                                            <td>
                                                <h4>On Temp</h4>
                                                <div class="number-spinner">
                                                    <span class="ns-btn">
                                                        <a data-dir="dwn"><span class="icon-minus"></span></a>
                                                    </span>
                                                    <input type="text" class="pl-ns-value schedule_changed" value="<?php print $schedule_on_temp;?>" maxlength="2" id="schedule_on_temp">
                                                    <span class="ns-btn">
                                                        <a data-dir="up"><span class="icon-plus"></span></a>
                                                    </span>
                                                </div>
                                            </td>
                                            <td>
                                                <h4>Cutoff Temp</h4>
                                                <div class="number-spinner">
                                                    <span class="ns-btn">
                                                        <a data-dir="dwn"><span class="icon-minus"></span></a>
                                                    </span>
                                                    <input type="text" class="pl-ns-value schedule_changed" value="<?php print $schedule_cutoff_temp;?>" maxlength="2" id="schedule_cutoff_temp">
                                                    <span class="ns-btn">
                                                        <a data-dir="up"><span class="icon-plus"></span></a>
                                                    </span>
                                                </div>
                                            </td>
                                        </tr>
                                    </table>

                                    <br>
                                    <table style='margin:auto'>
                                        <tr>
                                            <td>
                                                Temperature: <span id='metric_temp'>0C</span>
                                                <br>
                                                Humidity: <span id='metric_humid'>0%</span>
                                            </td>
                                        </tr>
                                    </table>
                                </div>
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

    <script src='js/jq.js'></script>
    <script type="text/javascript">

    var ws;
    var ws2;
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
            console.log(e);
        };
    }

    function init2() {
        ws2 = new WebSocket("ws://<?php print $_SERVER['SERVER_ADDR'];?>:9002/");

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

    $(document).ready(function() {
        init2();
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
       } else if(str.localeCompare("refresh") == 0) {
           location.refresh();
       }
    }

    function output2(str) {
       console.log( "x:" + str)
       if(str.localeCompare("") == 0) {
            return;
       }

       if(str.indexOf(',') > 0 ){
           var parts = str.split(',');
            $("#metric_temp").text((parts[0]).substring(0,4) + "C");
            $("#metric_humid").text((parts[1]).substring(0,4) + "%");
       }
    }

    </script>
    <script src="js/pincode.js"></script>
</body>
</html>
