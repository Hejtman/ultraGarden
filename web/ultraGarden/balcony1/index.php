<!DOCTYPE html>
<html lang="en">
<head>
	<link rel="stylesheet" type="text/css" href="../../style.css">
	<meta name="Description" content="self-sustaining aerophonics system version 1">
	<meta name="Keywords" content="Raspbery Pi,aerophonics,ultraphonics,garden">
	<meta name="author" content="Michal Hejtm&aacute;nek, http://malina.moxo.cz">
	<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
</head>
<body>

<img src="background.jpg" alt="background picture">

<?php

require '../common.php';
require 'status.php';
echo '<div class="sensorText" style="' . $pi_status->getStyle()  . '">' . $pi_status->getText()  . '</div>';

echo '<img src="' . $pump_tidegate->getImgPath()  . '" style="position: absolute; left:0px; top:0px;">';
echo '<img src="' . $barrel_tidegate->getImgPath() . '" style="position: absolute; left:0px; top:0px;">';

echo '<div class="sensorText" style="' . $pump->getStyle()  . '">' . $pump->getText()  . '</div>';

echo '<div class="sensorText" style="' . $pump_dht->getStyle()  . '">' . $pump_dht->getText()  . '</div>';
echo '<div class="sensorText" style="' . $barrel_dht->getStyle() . '">' . $barrel_dht->getText() . '</div>';
echo '<div class="sensorText" style="' . $outer_dht->getStyle() . '">' . $outer_dht->getText() . '</div>';

echo '<div class="sensorText" style="' . $barrel_wlevel->getStyle() . '">' . $barrel_wlevel->getText() . '</div>';

echo '<div class="sensorText" style="' . $outer_light->getStyle() . '">' . $outer_light->getText() . '</div>';


// Next refresh set 2s after expected status.php update.
$lastSync = time() - filemtime('status.php');
$nextSync = 2 + REFRESHINTERVAL - $lastSync % REFRESHINTERVAL;
header("Refresh: " . $nextSync);

$alert = ($lastSync > REFRESHINTERVAL) ? 'id="alert"' : '';
echo '<table class="sensorText" style="left: 1000px; top:55px;">
		<tr               ><th colspan="2"> Web hosting 										</th></tr>
		<tr               ><td>	IP				</td><td>' . $_SERVER['SERVER_ADDR']	. '</td></tr>
		<tr ' . $alert . '><td>	Last sync 	</td><td>' . time2text($lastSync) 		. '</td></tr>
		<tr               ><td>	Next sync	</td><td>' . time2text($nextSync) 		. '</td></tr>
		<tr               ><td>	Interval 	</td><td>' . time2text(REFRESHINTERVAL). '</td></tr>
	</table>';
?>

</body>
</html>
