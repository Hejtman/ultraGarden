void secs2time(unsigned int sec, unsigned int& number, char& suffix)
{
	if (sec < 60) {
		number = sec;
		suffix = 's';
	} 
	else if (sec < 60*60) {
		number = sec / 60;
		suffix = 'm';
	}
	else if (sec < 24*60*60) {
		number = sec / (60*60);
		suffix = 'h';
	} else {
		number = sec / (24*60*60);
		suffix = 'd';
	}
}
