.DEFAULT_GOAL := help

.PHONY: help install run status stop
.PHONY: voice_get service_setup

help:
	@cat Makefile

install:
	sudo apt-get update
	sudo apt-get install -y open-jtalk open-jtalk-mecab-naist-jdic hts-voice-nitech-jp-atr503-m00
	$(MAKE) voice_get
	$(MAKE) service_setup

run:
	sudo systemctl enable raspi_shutdown_daemon
	sudo systemctl start raspi_shutdown_daemon

stop:
	sudo systemctl disable raspi_shutdown_daemon
	sudo systemctl stop raspi_shutdown_daemon

status:
	tail /tmp/raspi_shutdown_daemon.info
	sudo systemctl status raspi_shutdown_daemon


voice_get:
	wget https://sourceforge.net/projects/mmdagent/files/MMDAgent_Example/MMDAgent_Example-1.7/MMDAgent_Example-1.7.zip --no-check-certificate
	unzip MMDAgent_Example-1.7.zip
	sudo cp -R ./MMDAgent_Example-1.7/Voice/mei /usr/share/hts-voice/

service_setup:
	sudo chmod 755 ./raspi_shutdown_daemon.py
	sudo cp raspi_shutdown_daemon.py /opt/
	sudo cp raspi_shutdown_daemon.service /usr/lib/systemd/system/
	sudo chmod 755 ./jtalk.sh
	sudo cp ./jtalk.sh /usr/local/bin/
