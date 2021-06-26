<?php

if(isset($_GET['id'])){
    print("opening");

    $ch = curl_init();
    $url = "http://ashtangayoga.ie/classes/?action=door_action_applied&id=" . $_GET['id'] . "&daction=open&dmessage=successfully opened";
    curl_setopt($ch, CURLOPT_URL, $url);
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
