# TikTok and Instagram-Python-Bot
Here you will find a fully automated TikTok and Instagram bot that we developed for research purposes. There are two variants of the scripts:
* Swipe through Tiktok and stop when certain **hashtags** are found.
* Swipe through Tiktok and stop when the video has **more likes** than all previous videos.
The scripts will create a `json` with contains User, Likes, Comments, etc and it will export an `mp4-video` (without sound) from the screen.

In this doc you will find all our experiences, what worked and where we failed.

## Our learnings
### Emulator, device farm or real device?
We performed our tests on the **Android emulator**.  
Advantage: Reading the data is faster than on a real smartphone.  
Disadvantage: Despite root access, changing serial numbers, VPN, etc., TikTok recognized that we were not a real smartphone. Among other things, we did not receive a localized feed (despite imitating the coordinates) and advertisements were not displayed.

We did not use a **device farm** because they did not allow to log in beforehand (manually).
We performed our tests on the **Android emulator**.  

**Real devices** simulated real users best, which is why we used a real smartphone.

### Searching for hashtags
We noticed that TikTok users rarely add hashtags or descriptive descriptions to their videos.

### Apple Silicon
For now: If you use an Apple silicon chip and want to test on emulator: Have fun! It works, but you will need perseverance.

## Installation
### Appium
Install [Appium](https://appium.io/) and start the server with the default settings.
* Host: 0.0.0.0
* Port: 4723

## Android Emulator
This tutorial is for the emulator on a Mac Silicon. If you want to use an emulator, download (as of December 2021) the [Canary build](https://developer.android.com/studio/preview).

At the welcome screen, click on the three dots and select `AVD Manager` or `Virtual Device Manager` 
* `Create Device`
* `Pixel 5`
* Choose `R` (API Level 30) on `arm64-v8a` (this is important! It must be an `arm64-v8a` on a mac silicon)
* `Show Advanced Settings`
* Add some more `internal storage`

Install TikTok: Drag Tiktok-App from the `lib`-folder and drop it on the emulator.

## Real device
Activate developer-Mode on your device:
* Go to `Settings`
* `Device information`
* Tab 6 times on the `Build-Number`
* Back to `settings` -> `Developer options`
* Activate: `UBS-Debugging`

Install TikTok:  
Install Android Studio. Then get device serial. Open Terminal and write `adb devices`.  
If `adb` is not found, add the following path to your system:  
```
/Users/[YOURUSER]/Library/Android/sdk/emulator
/Users/[YOURUSER]/Library/Android/sdk/platform-tools
```
If you got the serial number, push Tiktok-APK to device:
```
adb -s [SERIALNUMBER] install /[PATH_TO_THIS_REPO]/lib/TikTok_v20.9.3_apkpure.com.apk
```

## Install scripts
First, install [FFMPEG](http://www.ffmpeg.org/). Otherwise appiums build-in recorder will stop after 3 minutes.

Install virtual environment and launch it
```
python3 -m venv env
source env/bin/activate
```
In the virtual environment, install dependencies
```
python -r requirements.txt
```

Our Huawei-Phone does not supports Appium screencast. That why some scripts use [scrcpy](https://github.com/Genymobile/scrcpy) as screencasting software. Install it:
```
brew install scrcpy
```

## Config scripts
You need to edit `src/settings.py`:

`users`  
Holds your TikTok-Users and hashtag, it should stops on.

`run_for_seconds`  
How long the script should run. If you use appiums build-in recorder, do not run it longer than 20 minutes.

`avds`  
Contains your virtual devices (if you use the emulator). Add the Appium-Port and the name of the `avd`

`desired_cap`  
Stores, how your device is found. You need to edit this.  
With real devide:
* Add: `"platformVersion": "[VERSION]"`

On emulator:
* Remove `platformVersion`
* In `src/main.py` and/or `src/highscore.py` add `caps['avd'] = settings.avds[args.avd]['avd']` at around line 25.

`data_root`  
Where the data (videos and json) should be stored.  

There may be other options you d'like to change.

## Run scripts
There are two essential scripts: `main.py` (looks for hashtags) and `highscore.py` (looks for highscores)

Run **main.py**. In your virtual env, run:
```terminal
python main.py -user=NAME -platform=tiktok -avd=bot1
```
Supported platforms: `tiktok` and `instagram`

Run **highscore.py**. In your virtual env run: 
```terminal
python highscore.py -user=NAME -platform=tiktok -port=4723
```
Supported platforms: tiktok

To split your videos in to buckets of 100mb (for github), use this script:
```terminal
python cutvideos.py -cut PATH_TO_FOLDER
```
It will move the original file to the folder `zz_original` (add it to gitignore).

To merge videos together:
```terminal
python cutvideos.py -merge PATH_TO_FOLDER
```

To get screenshots from the videos based on the `json`-file, run this script:
```
python exprotframes.py -video PATH_TO_MP4
```

## Root your emulator
If you need to root your emulator ond Mac Silicon, here are some hints. Works only with API 30!
* Create virtual Device (API 30, Nexus 5)
* Run it. check if in terminal `abd` works. If not, add path (see chapter **Real Device**)
* Clone or download [rootAVD](https://github.com/newbit1/rootAVD)
* Start rooting. Open Terminal and navigate to **rootAVD**
```
cd PATHTO/rootAVD
./rootAVD.sh /Users/[YOUR_USER]/Library/Android/sdk/system-images/android-30/google_apis/arm64-v8a/ramdisk.img
```
**IMPORTANT: Now choose *Canary* (be fast!)**  
Now you should have `Magisk` installed. Start it. If you do not get any Apps in the Magisk Store, ups. Try the following: Download an older Magisk-Version from their website, replace it in the rootAVD-Folder and rund rooting again (but first: Reverse everything! `rootAVD.sh reverse`)

### How to change Device ID?
There is more than one device id, each app gets its own. Download `settings_secure.xml` from Device:  
```
adb pull /data/system/users/0/settings_ssaid.xml ./settings_ssaid.xml
```
Change IDs in XML and push it back to the emulator:
```
adb push ./settings_ssaid.xml /data/system/users/0/settings_ssaid.xml
```
If you cannot open the xml (because its binary): Switch your emulator API-Version (had the same problem with API 31)

### How to imitate an other devide?
* Install [Props](https://github.com/Magisk-Modules-Repo/MagiskHidePropsConf/blob/master/README.md#installation).
* Install [Termux](https://termux.com/) (you'll find it in the `lib` folder)

Now open `termux` on your emulated phone. 

* Type: `su`
* Type: `props`
* `1` (Set Fingerprint)
* Follow instructions and reboot. We've chosen: f -> 26 (Samsung) -> 76

To simulate devide, open `props` again:
* choose `3` (simulate device)
* `a` (enable all props)
* `4` (both)
* Reboot

### Make debuggable
While imitating a device, it may be possible, that you can not pull and push files to the device. In that case, make it debuggable again:
* Open Termux on your device
* change following props (`props name value`):
```
ro.debuggable = 1
```

# Other notes
Inspect emulated device in Appium:
```
{
  "platformName": "Android"
}
```

Fake other IDs additional to `props`
```
ro.build.characteristics nosdcard
ro.boot.serialno A5830D037F02
persist.adb.wifi.guid ce0b37a3-f6f6-4967-bd41-48fc0e443ea3
```

# Contact
[journalist.sh](https://www.journalist.sh)