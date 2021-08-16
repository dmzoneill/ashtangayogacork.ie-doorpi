<?php

if(isset($_GET['id'])){
    print("opening\n");

    $url = "https://ashtangayoga.ie/classes/?action=door_action_applied&id=" . $_GET['id'] . "&daction=open&dmessage=successfully%20opened";
    print($url . "\n");

    echo shell_exec("sudo whoami"); 
    echo shell_exec("sudo /var/www/html/bin/opendoor-delayed");
    echo shell_exec("sudo /usr/bin/curl \"$url\"");
    print(".");
} else {
    print("not opening\n");
}
