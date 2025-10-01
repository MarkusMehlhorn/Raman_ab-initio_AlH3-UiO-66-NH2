#!/bin/bash

# Target directory
outdir="/home/mehlhorn/mnt/TUBAF_home_drive/_Diplomarbeit/einkleben/Auswertung/AlH3/cluster/"
mkdir -p "$outdir"

left=28
right=28
top=12
bottom=18

# Loop through images 1.png to 8.png
for i in {1..8}; do
    img="${i}.png"

    # Check file exists
    if [ ! -f "$img" ]; then
        echo "File $img not found, skipping."
        continue
    fi

    # Get width and height
    read w h <<< $(identify -format "%w %h" "$img")

    # Calculate cropping dimensions
    x_off=$(( w * $left / 100 ))                        
    new_w=$(( w - (w*$left/100) - (w*$right/100) ))
    y_off=$(( h * $top / 100))
    new_h=$(( h - (h*$top/100) - (h*$bottom/100) ))

    # Output filename (identical to input, but in target dir)
    outfile="$outdir/${i}.png"

    # Crop with ImageMagick
    magick "$img" -crop "${new_w}x${new_h}+${x_off}+${y_off}" +repage "$outfile"
    echo "Cropped $img -> $outfile"
done

