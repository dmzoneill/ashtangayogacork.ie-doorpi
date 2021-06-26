<?php

if(isset($_GET['id'])){
    print("opening");

    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, "http://ashtangayoga.ie/classes?door_action_applied=yes&id=" . $_GET['id'] . "&action=open&message=successfully opened");
    curl_setopt($ch, CURLOPT_HEADER, false);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_CONNECTTIMEOUT, 0); 
    curl_setopt($ch, CURLOPT_TIMEOUT, 3); //timeout in seconds
    $response = curl_exec($ch);
    curl_close($ch);

    shell_exec("/usr/bin/nohup /var/www/html/bin/opendoor-delayed");
} else {
    print("not opening");
}
