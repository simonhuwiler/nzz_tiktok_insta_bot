## Android konfigurieren

!Je nach APK heissen die IDs anders! Tipp: Andoid mit App-Store installieren, TikTok in Google Play öffnen, auf teilen und mittels Link APK herunterladen (APK Downloader)

* Auf Mac M1 Preview-Version (Stand Aug. 2021) installieren! https://developer.android.com/studio/preview
* Android SDK installieren
* FFMPEG installlieren (ansonsten kann max 3min aufgenommen werden)
* Bei Willkommensbildschirm auf drei Punkte und dann AVD Manager
* Android hinzufügen: 
* Pixel 4, 5.7
* Android 11.0 arm64-v8a (mit Appstore)
* Tiktok-APK reinziehen, einloggen und Bot starten

## Appium
* Default-Einstellungen starten
* Host: 0.0.0.0
* Port: 4723
* Um Appium-Inspektor zu starten, folgende Parameter verwenden
```
{
  "platformName": "Android"
}
```

## Run Script
`src/settings.py` ergänzen. Script starten über:  
```terminal
python main.py -user=NAME -platform=instagram -avd=bot1
```

## Topics
* **Depression** vs Dogs. #Sadgirl #sad #pain #sadstory #depression
* #weightloss #beauty
* #couple
* #summer #fashion
* #dancelove

## Root your Andoid
Works only with API 31, not 30...
* Create virtual Device (API 30, Nexus 5)
* Run it. check if in terminal "abd" works
* Start rooting:
```
cd /Users/simon/Documents/projects/rootAVD
./rootAVD.sh /Users/simon/Library/Android/sdk/system-images/android-30/google_apis/arm64-v8a/ramdisk.img
```

Install Props
https://github.com/Magisk-Modules-Repo/MagiskHidePropsConf/blob/master/README.md#installation

Install adb root NOPE
https://github.com/evdenis/adb_root/releases

IMPORTANT: Now choose **Canary**

Fun fact: Rooting only works with Api 31, but changing android id only with Api 30 (XML in api 31 not readable)

## Change Android ID
Download settings_secure.settings_ssaid from Device:  

Pull:  
`adb pull /data/system/users/0/settings_ssaid.xml ./settings_ssaid.xml`

Push:  
`adb push ./settings_ssaid.xml /data/system/users/0/settings_ssaid.xml`

Others
`adb pull /data/system/users/0/settings_secure.xml ./settings_secure.xml`
  
`adb push ./settings_secure.xml /data/system/users/0/settings_secure.xml`

## Set props
Termux installieren und starten
```
su
props
```
Set Fingerprint
```
1
f
26 (Samsung)
76


21 (OnePlus)
68 (Nord)
2 (Version 11)
```
REBOOT
Simulate Device:
```
3
s (simulate device)
a (enable all probs)

BOOTSTATE: 4 (both)
```
Reboot Device  
### Make debuggable
Open Termux
```
ro.debuggable = 1
ro.build.characteristics nosdcard
ro.boot.serialno A5830D037F02
persist.adb.wifi.guid ce0b37a3-f6f6-4967-bd41-48fc0e443ea3
```

API31 and Canary
https://github.com/newbit1/rootAVD
https://github.com/Magisk-Modules-Repo/MagiskHidePropsConf/blob/master/README.md#installation

