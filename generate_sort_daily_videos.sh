
for dir in processed_images/*; do
    # echo "Processing $dir"

    # remove "processed_images/" from the path
    dir=${dir#processed_images/}

    # first check if the mp4 exists and skip if it does
    if [ -f "processed_videos/$dir.mp4" ]; then
        echo "Skipping $dir.mp4, it already exists"
        continue
    fi

    if [ -f "processed_images/$dir/.processing" ]; then
        echo "Skipping $dir.mp4, it is currently being processed"
        continue
    fi

    echo "Creating $dir.mp4"

    ffmpeg \
        -framerate 24 \
        -pattern_type glob \
        -i "processed_images/$dir/**/*.jpg" \
        -s hd1080 \
        -c:v libx264 \
        -crf 18 \
        -vf "format=yuv420p" \
        -movflags +faststart \
        "processed_videos/$dir.mp4"

    echo "Created $dir.mp4"

    # if we want to speed up the video
    # ffmpeg -i ./uniform_test.mp4 -filter:v "setpts=0.5*PTS" ./uniform_test_2x.mp4
    # ffmpeg -i ./uniform_test_2x.mp4 -filter:v "setpts=0.5*PTS" ./uniform_test_4x.mp4
    # ffmpeg -i ./uniform_test_4x.mp4 -filter:v "setpts=0.5*PTS" ./uniform_test_8x.mp4
    # ffmpeg -i ./uniform_test_8x.mp4 -filter:v "setpts=0.5*PTS" ./uniform_test_16x.mp4
    # ffmpeg -i ./uniform_test_16x.mp4 -filter:v "setpts=0.5*PTS" ./uniform_test_32x.mp4
done
