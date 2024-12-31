# Projeto-Industrial
## Table of contents
- [Control Code](#control-code)
- [Interface](#interface)
- [PCB's](#pcbs)

## Control Code
Code for the unit controller. Launching it exposes a RESTful API on port `:8000` being this only way to interact with the system.

Run it with:

	cd control-code
	python3 main.py

The code is divided in four modules:

| Module 		    | Description |
| :---------------- | :----------- |
| API    		    | Exposes a RESTful API on port `:8000` |
| SSH			    | Connects to the gateway via `SSH` |
| Sensor Reader     | Reads the force values from the Force Sensor |
| Control Signal    | Generates the control signals to drive the Linear Actuator |

## Interface
Code for the web interface. This an example of an interface to interact with system on port `:5173`. It formats the data from the [Control Code](#control-code) API.

Requires `npm`. Rut it with:

	cd interface 
	npm install
	sudo npm run dev

## PCB's
PCB designs for the controller circuit and the force sensor.