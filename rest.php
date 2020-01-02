<?php

$override = "/var/www/html/scratch/override";
$heating = "/var/www/html/scratch/heating.json";
$heating_status = "/var/www/html/scratch/heating_status";

function websocket_open($url)
{
    $key = base64_encode(openssl_random_pseudo_bytes(16));
    $query = parse_url($url);
    $header = "GET / HTTP/1.1\r\n"
        . "pragma: no-cache\r\n"
        . "cache-control: no-cache\r\n"
        . "Upgrade: WebSocket\r\n"
        . "Connection: Upgrade\r\n"
        . "Sec-WebSocket-Key: $key\r\n"
        . "Sec-WebSocket-Version: 13\r\n"
        . "\r\n";
    $sp = fsockopen($query['host'], $query['port'], $errno, $errstr, 1);
    if (!$sp) {
        die("Unable to connect to server " . $url);
    }

    // Ask for connection upgrade to websocket
    fwrite($sp, $header);
    stream_set_timeout($sp, 5);
    $reaponse_header = fread($sp, 1024);
    if (!strpos($reaponse_header, " 101 ")
        || !strpos($reaponse_header, 'Sec-WebSocket-Accept: ')) {
        die("Server did not accept to upgrade connection to websocket"
            . $reaponse_header);
    }
    return $sp;
}

function websocket_write($sp, $data, $final = true)
{
    // Assamble header: FINal 0x80 | Opcode 0x02
    $header = chr(($final ? 0x80 : 0) | 0x02); // 0x02 binary

    // Mask 0x80 | payload length (0-125)
    if (strlen($data) < 126) {
        $header .= chr(0x80 | strlen($data));
    } elseif (strlen($data) < 0xFFFF) {
        $header .= chr(0x80 | 126) . pack("n", strlen($data));
    } elseif (PHP_INT_SIZE > 4) // 64 bit
    {
        $header .= chr(0x80 | 127) . pack("Q", strlen($data));
    } else // 32 bit (pack Q dosen't work)
    {
        $header .= chr(0x80 | 127) . pack("N", 0) . pack("N", strlen($data));
    }

    // Add mask
    $mask = pack("N", rand(1, 0x7FFFFFFF));
    $header .= $mask;

    // Mask application data.
    for ($i = 0; $i < strlen($data); $i++) {
        $data[$i] = chr(ord($data[$i]) ^ ord($mask[$i % 4]));
    }

    return fwrite($sp, $header . $data);
}

function websocket_read($sp, $wait_for_end = true, &$err = '')
{
    $out_buffer = "";
    do {
        // Read header
        $header = fread($sp, 2);
        if (!$header) {
            die("Reading header from websocket failed");
        }

        $opcode = ord($header[0]) & 0x0F;
        $final = ord($header[0]) & 0x80;
        $masked = ord($header[1]) & 0x80;
        $payload_len = ord($header[1]) & 0x7F;

        // Get payload length extensions
        $ext_len = 0;
        if ($payload_len >= 0x7E) {
            $ext_len = 2;
            if ($payload_len == 0x7F) {
                $ext_len = 8;
            }

            $ext = fread($sp, $ext_len);
            if (!$ext) {
                die("Reading header extension from websocket failed");
            }

            // Set extented paylod length
            $payload_len = 0;
            for ($i = 0; $i < $ext_len; $i++) {
                $payload_len += ord($header[$i]) << ($ext_len - $i - 1) * 8;
            }

        }

        // Get Mask key
        if ($masked) {
            $mask = fread($sp, 4);
            if (!$mask) {
                die("Reading header mask from websocket failed");
            }

        }

        // Get payload
        $frame_data = '';
        do {
            $frame = fread($sp, $payload_len);
            if (!$frame) {
                die("Reading from websocket failed.");
            }

            $payload_len -= strlen($frame);
            $frame_data .= $frame;
        } while ($payload_len > 0);

        // if opcode ping, reuse headers to send a pong and continue to read
        if ($opcode == 9) {
            // Assamble header: FINal 0x80 | Opcode 0x02
            $header[0] = chr(($final ? 0x80 : 0) | 0x0A); // 0x0A Pong
            fwrite($sp, $header . $ext . $mask . $frame_data);

            // Recieve and unmask data
        } elseif ($opcode < 3) {
            $data = "";
            if ($masked) {
                for ($i = 0; $i < $data_len; $i++) {
                    $data .= $frame_data[$i] ^ $mask[$i % 4];
                }
            } else {
                $data .= $frame_data;
            }

            $out_buffer .= $data;
        }

        // wait for Final
    } while ($wait_for_end && !$final);

    return $out_buffer;
}

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
            //$res = shell_exec("/usr/bin/heater on");
            $sp=websocket_open('127.0.0.1:9002',$errstr);
            websocket_write($sp,"boost");
            echo websocket_read($sp,true);
            file_put_contents($heating_status, "on");
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
$json['temperature'] = file_get_contents('/var/www/html/scratch/temperature');
$json['humidity'] = file_get_contents('/var/www/html/scratch/humidity');

print json_encode($json);
