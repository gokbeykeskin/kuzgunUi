# kuzgunUi
 An interface for analyzing real-time data on UAV fligts.
 
## Dependencies
- ArduPilot and Dronekit-SITL for simulated flights
- Dronekit for connecting and receiving/sending data to UAV

## Port and Baud Rate
If you are going to connect a real UAV with USB cable or Telemetry, edit the port on line 80
instead of 127.0.0.1:14550, type the name of the port
- Usually the USB port for Linux based OS is /dev/ttyACM0/
- 
If you are connecting with telemetry, specify your telemetry's baud rate. ArduPilot suggests 57600 as baud rate so I set my telemetry's baud as this value.

## Simulation
Open 2 terminals
### Starting the simulation
```
cd ArduPilot/ArduPlane
../Tools/autotest/sim_vehicle.py --map --console
```
### Uploading a mission to a simulated vehicle
I used MissionPlanner for missions (automatically connects when simulation is on)

### Take-Off for Simulated Auto-Mission

On simulation terminal:
```
arm throttle
mode auto
```

### Starting the interface
On the other terminal
```
cd kuzgunUi\
python3 kuzgunUi.py
```
