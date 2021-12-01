import argparse
import os.path

import settings
import highscoretiktok
import instagram

parser = argparse.ArgumentParser(description='Highscore: Who gets more likes than me?')

parser.add_argument('-user', required=True)
parser.add_argument('-platform', required=True)
parser.add_argument('-port', required=False, default=4723)

serial = "73QDU16811001084"

args = parser.parse_args()

print("================")
print("😺 user:     %s" % args.user)
print("🚀 platform: %s" % args.platform)
print("🚢 Port:     %s" % args.port)
print("⌛ run for:  %s" % settings.run_for_seconds)
print("================")

caps = settings.desired_cap.copy()
# caps['avd'] = settings.avds[args.avd]['avd'] # Add for Emulator

# Create Dir if not exist
p = settings.data_root / args.user
if not p.exists():
    os.mkdir(p)

if args.platform == 'tiktok':
    highscoretiktok.run(args.user, serial, caps, args.port)

# elif args.platform == 'instagram':
#     instagram.run(args.user, serial, caps, settings.avds[args.avd]['port'])

else:
    raise Exception("Unknown Platform %s" % args.platform)