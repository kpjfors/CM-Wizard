#!/bin/sh
while :
do
	python3 updater.py
	python3 poster.py
	echo "Done. Sleep for 4h"
	sleep 4h
done
