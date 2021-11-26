import argparse
from pathlib import Path
import os.path

import settings
import tiktok
import instagram

parser = argparse.ArgumentParser(description='Start your influencer career!')

parser.add_argument('-user', required=True)
parser.add_argument('-platform', required=True)
parser.add_argument('-avd', required=True)

args = parser.parse_args()

print("================")
print("😺 user:     %s" % args.user)
print("🚀 platform: %s" % args.platform)
print("📱 avd:      %s" % args.avd)
print("⌛ run for:  %s" % settings.run_for_seconds)
print("================")

caps = settings.desired_cap.copy()
caps['avd'] = settings.avds[args.avd]['avd']

# Create Dir if not exist
p = settings.data_root / args.user
if not p.exists():
    os.mkdir(p)

if args.platform == 'tiktok':
    tiktok.run(args.user, caps, settings.avds[args.avd]['port'])

elif args.platform == 'instagram':
    instagram.run(args.user, caps, settings.avds[args.avd]['port'])

else:
    raise Exception("Unknown Platform %s" % args.platform)