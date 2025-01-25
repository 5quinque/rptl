# rptl (Raspberry Pi Time Lapse)

Use a raspberry pi to take still images every 5 minutes and create timelapse videos from them.

### Installation

```bash
apt install python3-picamera2

git clone https://github.com/5quinque/rptl.git
cd rptl

python3 -m venv rpi_venv --system-site-packages
source rpi_venv/bin/activate
pip install -e .
```

run the timelapse daemon
```bash
rptl
```

### example

https://github.com/linnit/rptl/assets/15974789/212abc56-2e1e-4775-912c-c72ca147de03


## usage

Run the `rptl` command to start the daemon. This will take a picture every 5 minutes and save it to the `images` directory.
```bash
Raspberry Pi Time Lapse.

Usage:
  rptl [options]

Options:
  -h --help               Show this screen.
  --version               Show version.
  --interval=<seconds>    Interval [default: 300].
  --start-time=<HHMM>     Only take photos after this time.
  --end-time=<HHMM>       Stop taking photos after this time.
  --sort-colour-profile   Sort images by their colour profile and only keep the major colour
  --no-camera             Used when developing without a RPi camera connected
  --log-level=<LEVEL>     Log level [default: INFO]

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
