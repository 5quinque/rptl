# timelapse

Use a raspberry pi to take still images every 5 minutes and create timelapse videos from them.

### image example

![image](20230809_225113.jpg)

#### [Video example](tsg_test2_8x.mp4)



## usage

Run the `timelapse` command to start the daemon. This will take a picture every 5 minutes and save it to the `images` directory.
```bash
timelapse
```

Run the flask web service to view the images and videos.
```bash
flask --app web run --host=0.0.0.0 --debug
```

Add the timestamp to the images and save them to the `timestamped_images` directory.
```bash
python src/timelapse/timestamp_images.py
```

Create a complete timelapse video from the images in the `timestamped_images` directory.
```bash
ffmpeg \
    -framerate 30 \
    -pattern_type glob \
    -i "timestamped_images/**/*.jpg" \
    -s hd1080 \
    -c:v libx265 \
    -crf 18 \
    -vf "format=yuv420p" \
    "./tsg_test2.mp4" # [TODO] use date for filename
```

Double the speed of the `./tsg_test2.mp4` video.
```bash
ffmpeg -i ./tsg_test2.mp4 -filter:v "setpts=0.5*PTS" ./tsg_test2_2x.mp4
```

Generate individual timelapse videos for each day from the images in the `images` directory.
```bash
./generate_timelapse.sh
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
timelapse
```

send a signal to the daemon to take a picture (will move to flask endpoint)
```bash
python src/timelapse/zmq_client_sender.py
```
