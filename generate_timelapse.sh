# This script will generate a timelapse video for each directory in the images
# directory. It will skip any directories that already have a video in the
# videos directory.


for dir in images/*; do
    # echo "Processing $dir"

    # remove "images/" from the path
    dir=${dir#images/}

    # first check if the mp4 exists and skip if it does
    if [ -f "videos/$dir.mp4" ]; then
        echo "Skipping $dir.mp4"
        continue
    fi

        # -vf "drawtext=fontfile=DejaVuSansMono.ttf: \
        #     text='%{metadata\\:datetime}': \
        #     x=10:y=h-text_h-10: \
        #     fontcolor=white:fontsize=20" \


    echo "Creating $dir.mp4"
    ffmpeg \
        -framerate 24 \
        -pattern_type glob \
        -i "images/$dir/*.jpg" \
        -s hd1080 \
        -c:v libx264 \
        -crf 18 \
        -vf "format=yuv420p" \
        -movflags +faststart \
        "videos/$dir.mp4"
    # ffmpeg \
    #     -framerate 24 \
    #     -pattern_type glob \
    #     -i "$dir/*.jpg" \
    #     -s hd1080 \
    #     -c:v libx265 \
    #     -crf 18 \
    #     -vf "format=yuv420p" \
    #     "videos/$dir.mp4"
    
    echo "Created $dir.mp4"

    # remove the images
    # rm -rf "images/$dir"
done

