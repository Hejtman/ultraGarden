<?php
	const REFRESHINTERVAL = 60;

	$pi_status = new text("left: 25px; top:25px;", 
		'<table>
			<tr 			  ><th colspan="2"> UltraGarden server 				</th></tr>
			<tr           ><td>	State:	</td><td>	Fogging (XXs)			</td></tr>
			<tr           ><td>	&nbsp;	</td><td>								</td></tr>
			<tr           ><td>	CPU:		</td><td>	XXX MHz  XX%  XX°C	</td></tr>
			<tr           ><td>	Memory:	</td><td>	XXXMB / XXXMB			</td></tr>
			<tr           ><td>	Video:	</td><td>	XXXXxXXXX (XX.XX fps)</td></tr>
			<tr id="alert"><td>	Network:	</td><td>	192.168.0.104			</td></tr>
			<tr           ><td>	Storage:	</td><td>	XXXXGB / XXXXGB (XX%)</td></tr>
			<tr           ><td>	Kernel:	</td><td>	X.XX.X					</td></tr>
			<tr           ><td>	Uptime:	</td><td>	XX Days					</td></tr>
		</table>');

	$pump_tidegate = new image("pump_tidegate_", "opened", ".gif");
	$barel_tidegate = new image("barel_tidegate_", "opened", ".gif");

	$pump_dht  = new text("left: 168px; top:594px;", "<b>X1%<br>XX°C</b>");
	$barel_dht = new text("left: 690px; top:180px;", "<b>X2%<br>XX°C</b>");
	$outer_dht = new text("left: 1103px; top:562px;", "<b>X3%<br>XX°C</b>");

	$outer_light = new text("left: 950px; top:571px;", "<b>XXXX Lux</b>");
?>
