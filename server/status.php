<?php
	const REFRESHINTERVAL = 60;

	$pi_status = new text("left: 25px; top:25px;", 
		'<table>
			<tr           ><th colspan="2">	UltraGarden server 				</th></tr>
			<tr           ><td>	State:	</td><td>	IDLING (0s / 60s)			</td></tr>
			<tr           ><td>	Time:	</td><td>	0s						</td></tr>
			<tr           ><td>	CPU:	</td><td>	XXX MHz  XX%  XX		</td></tr>
			<tr           ><td>	Memory:	</td><td>	XXXMB / XXXMB			</td></tr>
			<tr           ><td>	Video:	</td><td>	XXXXxXXXX (XX.XX fps)	</td></tr>
			<tr id="alert"><td> Network:</td><td>	192.168.0.104			</td></tr>
			<tr           ><td>	Storage:</td><td>	XXXXGB / XXXXGB (XX%)	</td></tr>
			<tr           ><td>	Kernel:	</td><td>	X.XX.X					</td></tr>
			<tr           ><td>	Uptime:	</td><td>	XX Days					</td></tr>
		</table>');

	$pump_tidegate = new image("pump_tidegate_", "closed", ".gif");
	$barrel_tidegate = new image("barrel_tidegate_", "closed", ".gif");

	$pump = new text("left: 400px; top:574px; ", "<b>WAITING<br>last: 0s<br>next: 0s</b>");

	$pump_dht  = new text("left: 168px; top:584px; background-color:red; opacity:1;", "<b>-99.0%<br>-99.0°C<br>255</b>");
	$barrel_dht = new text("left: 690px; top:170px; background-color:red; opacity:1;", "<b>-99.0%<br>-99.0°C<br>255</b>");
	$outer_dht = new text("left: 1103px; top:552px; background-color:red; opacity:1;", "<b>-99.0%<br>-99.0°C<br>255</b>");

	$barrel_wlevel = new text("left: 655px; top:230px;", "<b>86mm (X d)<br>today: -AAmm<br>yrday: -BBmm</b>");

	$outer_light = new text("left: 950px; top:571px; background-color:red; opacity:1;", "<b>0 Lux</b>");
?>
