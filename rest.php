<?php

$override = "/var/www/html/override";
$heating = "/var/www/html/heating.json";
$heating_status = "/var/www/html/heating_status";

if (isset($_GET['action'])) {

    $heatingschedule = isset($_GET['heatingschedule']) ? $_GET['heatingschedule'] : 0;
    $heatingbefore = isset($_GET['heatingbefore']) ? $_GET['heatingbefore'] : 0;
    $heatingruntime = isset($_GET['heatingruntime']) ? $_GET['heatingruntime'] : 0;
    $heatinglow = isset($_GET['heatinglow']) ? $_GET['heatinglow'] : 0;
    $haitingcutoff = isset($_GET['haitingcutoff']) ? $_GET['haitingcutoff'] : 0;
    $boost = isset($_GET['boost']) ? $_GET['boost'] : 0;

    $doorarm = isset($_GET['doorarm']) ? $_GET['doorarm'] : 0;
    $dooropen = isset($_GET['dooropen']) ? $_GET['dooropen'] : 0;

    $content = '{"schedule_toggle":"' . $heatingschedule . '","schedule_minutes_prior":"' . $heatingbefore . '","schedule_run_period":"' . $heatingruntime . '","schedule_on_temp":"' . $heatinglow . '","schedule_cutoff_temp":"' . $haitingcutoff . '"}';

    file_put_contents($heating, $content);

    if ($boost !== 0) {
        if (file_exists($heating_status) == false) {
            $res = shell_exec("/usr/bin/heater on");
            file_put_contents($heating_status, $res);
        } else {
            shell_exec("/usr/bin/heater off");
        }
    }

    if ($doorarm !== 0) {
        if ($doorarm == "false") {
            unlink($override);
        } else {
            file_put_contents($override, time());
        }
    }

    if ($dooropen !== 0) {
        shell_exec("/usr/bin/opendoor");
    }
}

if (file_exists($heating_status)) {
    if (filemtime($heating_status) < time() - 900) {
        unlink($heating_status);
    }
}

$json = json_decode(file_get_contents($heating), true);
$json['doorarm'] = !file_exists($override);
$json['boost'] = file_exists($heating_status);
$json['temperature'] = file_get_contents('/var/www/html/temperature');
$json['humidity'] = file_get_contents('/var/www/html/humidity');
print json_encode($json);
