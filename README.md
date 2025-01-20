# Automatic, universal push-button actuator, equipped with force gauge
## Table of contents
- [Overview](#overview)
- [Requirements](#requirements)
- [Pre-installation](#pre-installation)
- [Installation](#installation)
- [Interacting with the system](#interacting-with-the-system)

## Overview
This repository contains all the code to run the system, the PCB's files and the 3D designs.

## Requirements
This software is expected to run on a Raspberry Pi 4B (or equivalent), running **Raspberry Pi OS** not needing the graphical interface. 

## Pre-installation
Before installing, you must configure the way you want to connect to the Raspberry.
You can either connect it to the local network or use it has an access point.
> The former option is worse since you may run into conflits if the gateway ip of the local network and the ip of the DUT are the same.

To enable the access point run the command:

	sudo nmcli device wifi hotspot ssid <network-name> password <password>

If you want to disable it:

	sudo nmcli device disconnect wlan0
	sudo nmcli device up wlan0

The ethernet port must also be configured to have a static IPv4 (something like `192.168.1.5`), the gateway IP must be `192.168.1.1` and the route should not be set as default. That can be done using the `nmtui` command:

	sudo nmtui

## Installation
Start by installing `docker` and `docker-compose` with:

	sudo apt install docker.io docker-compose

then add your user to docker:

	sudo gpasswd -a $USER docker
	newgrp docker

finally clone the repository, `cd` into it and run a container with:

	docker compose up -d --build

Since this is the first time, it may take some minutes to finish building. After that you should see on port `:3000` the home page of the interface running, meaning the system is ready.

## Interacting with the system
The main way to interact with the system is to use the web interface on port `:3000`, however you can also use the a RESTful API on port `:8000`. On the **API Reference** page of the web interface you can see all the endpoints, what the returns are and a sample code to use it.

The API is independent of the web interface and can be run without it but the opposite is not possible.
