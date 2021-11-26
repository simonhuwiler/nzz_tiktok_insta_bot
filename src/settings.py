from pathlib import Path

users = {
    'tt1ds': ['#doggy', '#dog'],
    # 'ttalfred': ['#doggy', '#dog'],
    'tt2ds': ['sadgirl', 'sad', 'pain', 'sadstory', 'depression', 'dog', 'puppy'],
    'tt3ds2': ['summer', 'fashion'],
    'tt4ds': ['sad', 'broken', 'dead', 'crying', 'anxiety', 'pain', 'depression', 'dog', 'puppy'],
    'tt5ds': ['sad', 'broken', 'dead', 'crying', 'anxiety', 'pain', 'depression', 'dog', 'puppy'],
    'tt6ds': ['summer', 'fashion'],
    'tt7ds': ['allah', 'islam', 'mufti', 'meka', 'quran'],
    #'tt8ds': ['zertifikat', 'covid', 'corona', 'pandemie', 'pandemic', 'virus', 'impfung', 'vaccin', 'lockdown'],
    'tt8ds': ['mood', 'love', 'sick', 'pain', 'sad', 'anxiety', 'depression', 'couple', 'dark'],
    'ttalfred': ['mood', 'love', 'sick', 'pain', 'sad', 'anxiety', 'depression', 'couple', 'dark'],
    'is4daspe': ['mood', 'love', 'sick', 'pain', 'sad', 'anxiety', 'depression', 'couple', 'dark'],
    'is6daspe': ['beauty', 'fashion', 'mylook', 'teen'],
    'annabab_i1': ['beauty', 'fashion', 'mylook', 'teen', 'style'],
}

# run_for_seconds = 1700
run_for_seconds = 1200

avds = {
  "bot1": {
    "port": 4723,
    "avd": "annabab_i1"
  },
  "bot4": {
    "port": 4723,
    "avd": "smbot_4"
  }
}

desired_cap = {
  "platformName": "Android",
  "automationName": "UiAutomator2",
  "noReset": True,
  "isHeadless": True,
  "disableWindowAnimation": True,
  "disableAndroidWatchers": True,
  "trackScrollEvents": False,
  "waitForIdleTimeout": 0,
}

#tiktok_app = '/Users/simon/Documents/projects/tiktok_insta_bot/lib/TikTok_v20.9.3_apkpure.com.apk'
tiktok_app = 'com.zhiliaoapp.musically'
# instagram_app = '/Users/simon/Documents/projects/tiktok_insta_bot/lib/Instagram_v202.0.0.37.123_apkpure.com.apk'
instagram_app = 'com.instagram.android'

data_root = Path('../../nzz_tiktok_insta_bot_data/export/')

server = 'http://localhost:%s/wd/hub'