# rptl (Raspberry Pi Time Lapse)

Use a raspberry pi to take still images every 5 minutes and create timelapse videos from them.

### example

https://github.com/linnit/rptl/assets/15974789/212abc56-2e1e-4775-912c-c72ca147de03


## usage

Run the `rptl` command to start the daemon. This will take a picture every 5 minutes and save it to the `images` directory.
```bash
rptl
```

Run the flask web service to view the images and videos.
```bash
flask --app web run --host=0.0.0.0 --debug
```

# 

```bash
ffmpeg -f concat \
    -safe 0 \
    -i <(find /home/ryan/dev_timelapse/processed_videos \
    -type f \
    -name '*.mp4' \
    -exec echo "file '{}'" \; | sort) \
    -c:v copy \
    output.mp4
```

```bash
ffmpeg -i ./tsg_test2.mp4 -filter:v "setpts=0.5*PTS" ./tsg_test2_2x.mp4
ffmpeg -i ./tsg_test2_2x.mp4 -filter:v "setpts=0.5*PTS" ./tsg_test2_4x.mp4
ffmpeg -i ./tsg_test2_4x.mp4 -filter:v "setpts=0.5*PTS" ./tsg_test2_8x.mp4
ffmpeg -i ./tsg_test2_8x.mp4 -filter:v "setpts=0.5*PTS" ./tsg_test2_16x.mp4
```

## setup and notes

rpi venv

```bash
python3.9 -m venv rpi_venv --system-site-packages
source rpi_venv/bin/activate
pip install -e .
```

run the timelapse daemon
```bash
rptl
```

send a signal to the daemon to take a picture (have moved to flask endpoint, update.)
```bash
python src/timelapse/zmq_client_sender.py
```
