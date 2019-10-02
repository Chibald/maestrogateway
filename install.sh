#!/bin/sh

sudo cp maestro /etc/init.d/
sudo chmod 0755 /etc/init.d/maestro
sudo systemctl daemon-reload
sudo update-rc.d maestro defaults
