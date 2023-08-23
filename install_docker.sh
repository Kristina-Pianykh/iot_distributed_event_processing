#!/usr/bin/env bash

sudo apt-get update
sudo apt-get upgrade -y
python3 -m pip install --upgrade pip
sudo apt-get install -y ca-certificates curl gnupg
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/raspbian/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg
echo \
  "deb [arch="$(dpkg --print-architecture)" signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/raspbian \
  "$(. /etc/os-release && echo "$VERSION_CODENAME")" stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin docker-compose
systemctl start docker # you will be prompted for the password




    # @info(name = 'test2')
    # from every e1 = cseEventStream[sensor_id == 'accelerometer_y'] ->
    #     e2 = cseEventStream[sensor_id == 'accelerometer_x' and sensor_value > e1.sensor_value and e2.timestamp - e1.timestamp <= 5000] ->
    #     e3 = cseEventStream[sensor_id == 'joystick' and sensor_value == -1.0 timestamp >= e2.timestamp and timestamp - e2.timestamp <= 2000] ->
    #     e4 = cseEventStream[sensor_id == 'sound' and timestamp >= e3.timestamp and timestamp - e3.timestamp <= 2000]
    # select e1.device_id, e1.sensor_id, e1.sensor_value, e1.timestamp,
    #     e2.device_id, e2.sensor_id, e2.sensor_value, e2.timestamp,
    #     e3.device_id, e3.sensor_id, e3.sensor_value, e3.timestamp,
    #     e4.device_id, e4.sensor_id, e4.sensor_value, e4.timestamp
    # insert into outputStream;