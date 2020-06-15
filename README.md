
# Sloth tools

Web application for controlling remote-controlled power sockets at home via smartphone using a [Raspberry Pi and a 433Mhz transmitter](https://tutorials-raspberrypi.com/control-raspberry-pi-wireless-sockets-433mhz-tutorial/).
Supports timed events - even based on current sunrise/sunset time.

![enter image description here](https://raw.githubusercontent.com/mbarde/sloth-tools/master/docs/slothtools.gif)


## Prerequisites

Hardware and [433Mhz library from Ninjablocks](https://github.com/ninjablocks/433Utils.git) set up as described [here](https://tutorials-raspberrypi.com/control-raspberry-pi-wireless-sockets-433mhz-tutorial/).


## Setup

### 1. Install
```
git clone https://github.com/mbarde/sloth-tools.git
cd sloth-tools
pip3 install -r requirements.txt
```

### 2. Configure

Edit `config.json`:

* `codesend-bin-path`: (string) Path to the compiled codesend-binary (see [prerequisites](#Prerequisites))
* `longitude` and `latitude`:  (float) Longitute and latitude of your location - needed for sunrise/sunset computation

### 3. Setup database (once!)

```
export FLASK_APP=server.py
flask init-db
```


## Run in dev mode

```
env FLASK_APP=server.py flask run --host=0.0.0.0
```


## Deploy for production

This application is based on [Flask](https://flask.palletsprojects.com/en/1.1.x/), so you should take a look at its official [deployment guidelines](https://flask.palletsprojects.com/en/1.1.x/tutorial/deploy/#run-with-a-production-server).

### Set timezone

In order to ensure timed events to work as expected, your server has to use the same timezone as the application users. For Ubuntu server see: https://help.ubuntu.com/community/UbuntuTime#Using_the_Command_Line_.28terminal.29

### System service

To ensure the application is always running as soon as the machine is up you should create a service as described here: https://wiki.debian.org/systemd

In combination with [waitress](https://pypi.org/project/waitress/) your service configuration could look like following:

**homecontrol.service**

```
[Unit]
Description=Sloth-Tools
After=network.target

[Service]
User=pi
WorkingDirectory=/home/pi/server
ExecStart=/home/pi/.local/bin/waitress-serve --port=5000 --call "server:create_app"
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable:

```
sudo systemctl enable homecontrol.service
```
