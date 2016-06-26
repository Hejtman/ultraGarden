<?php

class image
{
	private $prefix;
	private $state;
	private $extension;

	public function __construct($p, $s, $e) {
		$this->prefix = $p;
		$this->state = $s;
		$this->extension = $e;
	}

	public function getImgPath() {
		return $this->prefix . $this->state . $this->extension;
	}
}

class text
{
	private $style;
	private $text;

	public function __construct($s, $t) {
		$this->style = $s;
		$this->text = $t;
	}

	public function getStyle() {
		return $this->style;
	}

	public function getText() {
		return $this->text;
	}
}

function time2text($second)
{
	if ($second < 60)       return       $second             . 's';
	if ($second < 60*60)    return round($second/60)         . 'm';
	if ($second < 60*60*24) return round($second/(60*60))    . 'h';
	else                    return round($second/(60*60*24)) . 'd';
}

?>
