<?php
	const REFRESHINTERVAL = 61;

	$pi_status = new text("left: 25px; top:25px;", 
		'<table>
			<tr           ><th colspan="2">	UltraGarden server 				</th></tr>
			<tr           ><td>	State:	</td><td>	Fogging (XXs)			</td></tr>
			<tr           ><td>	&nbsp;	</td><td>							</td></tr>
			<tr           ><td>	CPU:	</td><td>	XXX MHz  XX%  XX�		</td></tr>
			<tr           ><td>	Memory:	</td><td>	XXXMB / XXXMB			</td></tr>
			<tr           ><td>	Video:	</td><td>	XXXXxXXXX (XX.XX fps)	</td></tr>
			<tr id="alert"><td> Network:</td><td>	192.168.0.104			</td></tr>
			<tr           ><td>	Storage:</td><td>	XXXXGB / XXXXGB (XX%)	</td></tr>
			<tr           ><td>	Kernel:	</td><td>	X.XX.X					</td></tr>
			<tr           ><td>	Uptime:	</td><td>	XX Days					</td></tr>
		</table>');

	$pump_tidegate = new image("pump_tidegate_", "closed", ".gif");
	$barrel_tidegate = new image("barrel_tidegate_", "closed", ".gif");

	$pump_dht  = new text("left: 178px; top:584px;", "<b>-99.0%<br>-99.0°C<br0</b>");
	$barrel_dht = new text("left: 700px; top:170px;", "<b>-99.0%<br>-99.0°C<br>0</b>");
	$outer_dht = new text("left: 1113px; top:552px;", "<b>-99.0%<br>-99.0°C<br>0</b>");

	$barrel_wlevel = new text("left: 655px; top:230px;", "<b>XX.Xcm (5 d)<br>today: -AA.Acm<br>yrday: -BB.Bcm</b>");

	$outer_light = new text("left: 950px; top:571px;", "<b>0 Lux</b>");
?>
