import json
from pathlib import Path
import os
import subprocess
import argparse

# Define ins and outs
folderdata = Path('../export/')
folderframes = Path('../frames/')

# Initialize Argument Parser
parser = argparse.ArgumentParser(description='I will show you the best of your videos, in pictures!')
parser.add_argument('-video', required=True)
args = parser.parse_args()

exportfolder = Path(folderframes / Path(args.video).parent)

print(Path(args.video).parent)
print(Path(args.video).stem)

# Load JSON
with open(folderdata / Path(args.video).parent / ("%s.json" % Path(args.video).stem)) as json_file:
    data = json.load(json_file)

# Create Screenshot Folder
if not exportfolder.exists():
    os.mkdir(exportfolder)

videofile = folderdata / Path(args.video).parent / 'zzOriginal' / Path(args.video).name

subtracting_factor = data[0]['videodelta']

for i, d in enumerate(data):
    framename = exportfolder / ("%s_%03d.jpg" % (d['videoname'], i))

    cutter = subprocess.Popen(["ffmpeg",
        "-ss", str(d['videodelta'] - subtracting_factor),
        "-accurate_seek",
        "-i", str(videofile),
        "-frames:v", "1",
        # "-q:v", "2",
        str(str(framename))
    ], stdout=subprocess.PIPE)
    print(cutter.communicate()[0])

    # if i > 10:
    #     break