#!/usr/bin/env sh
while true; do 
	venv/bin/python pablub.py >index2.html && mv index2.html index.html
       	sleep 60;
done
