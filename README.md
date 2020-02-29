
# Sloth tools

Web application for controlling remote-controlled power sockets at home via smartphone using a [Raspberry Pi and a 433Mhz transmitter](https://tutorials-raspberrypi.com/control-raspberry-pi-wireless-sockets-433mhz-tutorial/).

![enter image description here](https://raw.githubusercontent.com/mbarde/sloth-tools/master/docs/slothtools.gif)

## Prerequisites

Hardware and [433Mhz library from Ninjablocks](https://github.com/ninjablocks/433Utils.git) set up as described [here](https://tutorials-raspberrypi.com/control-raspberry-pi-wireless-sockets-433mhz-tutorial/).

## Setup

### 1. Install
```
git clone https://github.com/mbarde/sloth-tools.git
cd sloth-tools
pip install -r requirements.txt
```

### 2. Configure

Edit the variable [`codesendBinPath`](https://github.com/mbarde/sloth-tools/blob/master/server.py#L22) in `server.py` to make sure it points to the compiled codesend-binary (see [prerequisites](#Prerequisites)).

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

### Set timezone

In order to ensure timed events to work as expected, your server has to use the same timezone as the application users. For Ubuntu server see: https://help.ubuntu.com/community/UbuntuTime#Using_the_Command_Line_.28terminal.29

### System service

To ensure the application is always running as soon as the machine is up you should create a service as described here: https://wiki.debian.org/systemd

In combination with [waitress](https://pypi.org/project/waitress/) your service configuration could look like following:

**homecontrol.service**

```
[Unit]
Description=Homecontrol
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/server
ExecStart=/home/ubuntu/.local/bin/waitress-serve --port=5000 --call "server:create_app"
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable:

```
sudo systemctl enable homecontrol.service
```
