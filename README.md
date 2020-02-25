
## Setup

```
sudo apt install python3-flask
sudo apt-get install python3-opencv
```

Setup database:

```
export FLASK_APP=server.py
flask init-db
```

## Run in dev mode:

```
env FLASK_APP=server.py flask run --host=0.0.0.0
```

## Deploy for production:

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
