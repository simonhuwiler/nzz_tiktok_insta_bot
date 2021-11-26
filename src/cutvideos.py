"""

This Script does two things:

-cut FOLDER
    It cuts videos into small pieces to upload them to github.
    The Original-File is moved to the (git-ignored) folder "zzOriginal"

-merge FOLDER
    Does the opposites: Merges the files and puts the long video
    in the folder "zzOriginal

"""

import argparse
from os import mkdir
from pathlib import Path
import os, shutil, glob
import subprocess

# Consts
video_length_s = 300
video_folder = Path('../export/')

# Initialize Argument Parser
parser = argparse.ArgumentParser(description='Cut your most beautiful peace of work!')
parser.add_argument('-cut', required=False)
parser.add_argument('-merge', required=False)
parser.add_argument('-out', required=False)
args = parser.parse_args()

if args.cut:

    print("================")
    print("📁 cut: %s" % args.cut)
    print("================")

    video_folder = video_folder / Path(args.cut)

    # Create "zzOriginal" folder
    original = Path(video_folder) / 'zzOriginal'
    if not original.exists():
        mkdir(original)

    # Load all files
    videos = glob.glob(str(video_folder / Path("*.mp4")))

    for vid in videos:
        
        # Check if video folder already exists and skipt
        sub = video_folder / Path(vid).stem

        if sub.exists():
            print("⏭ Skip %s" % vid)
            continue
        else:
            # Create Folder
            print("create", sub)
            mkdir(sub)

        print("🎥 Video:    %s" % vid)

        cutter = subprocess.Popen(["ffmpeg",
            "-i", str(vid),
            "-c", "copy",
            "-map", "0",
            "-segment_time", "00:05:00",
            "-reset_timestamps", "1",
            "-f", "segment",
            str(sub / Path(Path(vid).stem + "_%03d.mp4"))
        ], stdout=subprocess.PIPE)

        print(cutter.communicate()[0])

        # Move Original-file to zzOriginal
        shutil.move(str(vid), original / Path(vid).name)


elif args.merge:

    print("================")
    print("📁 merge: %s" % args.merge)
    print("================")

    original = video_folder / Path(args.merge) / 'zzOriginal/'

    if original.exists():
        raise Exception("❌ zzOriginal-Folder already exists. Drop it to generate long files from cutted files.")
    else:
        mkdir(original)

    # Get all subfolders
    subfolders = glob.glob(str(video_folder / Path(args.merge) / '*/'))
    for subfolder in subfolders:

        if os.path.isdir(subfolder):

            if subfolder == str(original):
                continue

            print("🎞 %s" % subfolder)

            # Start Concatting
            sub = Path(subfolder) / Path("*.mp4")

            # Create concat file
            videos = glob.glob(str(sub))
            videos.sort()

            concat_list = Path(subfolder) / Path('_concatlist.txt')

            with open(concat_list, 'w') as f:
                for vid in videos:
                    f.write("file '%s'\n" % Path(vid).name)

            # Start merging
            out = original / Path("%s.mp4" % Path(subfolder).stem)
            merger = subprocess.Popen(["ffmpeg",
                        "-f", "concat",
                        "-safe", "0",
                        "-i", str(concat_list),
                        "-c", "copy",
                        str(out)], stdout=subprocess.PIPE)

            print(merger.communicate()[0])

            # Remove Concat List
            os.remove(concat_list)  

    