init:
	pip3 install -r requirements.txt

install: init
	# TODO

test:
	sudo PYTHONPATH="./server" python3 server/garden/test.py
	sudo PYTHONPATH="./server" python3 server/records/test.py

.PHONY: init install test
