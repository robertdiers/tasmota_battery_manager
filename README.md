# tasmota_battery_manager
use Tasmota devices to charge batteries and feed in back to home energy network

### Setup
I'm using a combination of a 24V (car batteries) and a 48V (lifepo4) storage:
* 1 Tasmota to activate battery charge (normal 24V charger + 48V Lifepo4 charger)
* 1 Tasmota to activate 24V feed-in (using 24V Grid-Tie-Inverter, around 300 watt)
* 1 Tasmota to activate 48V feed-in (using 48V Grid-Tie-Inverter, around 400 watt)
* Kostal Inverter / Energy Meter to read actual house consumption and generation

In addition I'm running a few more inverters directly "decreasing" my home consumption value. They are not relevant for this solution, but it's good to know that this is possible.

### Dockerhub
https://hub.docker.com/repository/docker/robertdiers/xxx

### Development
Please start Visual Studio Code Server using script vsc_start.sh, open http://localhost:8080 to code.
