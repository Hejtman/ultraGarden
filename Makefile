SERVER_PATH := $(shell pwd)/server/server.py
INIT_FILE := /etc/init.d/ultragarden

install_requirements: requirements.txt
	pip3 install -r $<

$(INIT_FILE): init
	$(shell sed -e 's%SERVER_PATH=.*%SERVER_PATH="$(SERVER_PATH)"%' $< > $@)
	chmod +x $@


#install: $(INIT_FILE) install_requirements
install: $(INIT_FILE)
	$(shell update-rc.d ultragarden defaults)

uninstall:
	$(shell update-rc.d -f ultragarden remove)
	rm $(INIT_FILE)

test:
	sudo PYTHONPATH="./server" python3 server/garden/test.py
	sudo PYTHONPATH="./server" python3 server/records/test.py


.PHONY: install_requirements install uninstall test
