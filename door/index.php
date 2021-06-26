<?php

if(isset($_GET['id'])){
    print("opening\n");

    $url = "https://ashtangayoga.ie/classes/?action=door_action_applied&id=" . $_GET['id'] . "&daction=open&dmessage=successfully%20opened";
    print($url . "\n");
    
    shell_exec("/usr/bin/curl \"$url\"");
    shell_exec("/usr/bin/nohup /var/www/html/bin/opendoor-delayed");
    print(".");
} else {
    print("not opening\n");
}
