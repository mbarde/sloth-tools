## Setup

```
sudo apt install python3-flask
sudo apt-get install python3-opencv
```

Setup databse:

```
export FLASK_APP=server.py
flask init-db
```

## Run in dev mode:

```
env FLASK_APP=server.py flask run --host=0.0.0.0
```

## Deploy for production:

homecontrol.service

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
