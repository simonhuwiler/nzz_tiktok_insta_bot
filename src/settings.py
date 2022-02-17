from pathlib import Path

users = {
    'myaccount': ['#doggy', '#dog']
}

# run_for_seconds = 1700
run_for_seconds = 1200

avds = {
  "bot1": {
    "port": 4723,
    "avd": "annabab_i1"
  },
}

desired_cap = {
  "platformName": "Android",
  "platformVersion": "7", # Remove for Emulator
  "automationName": "UiAutomator2",
  "noReset": True,
  "isHeadless": True,
  "disableWindowAnimation": True,
  "disableAndroidWatchers": True,
  "trackScrollEvents": False,
  "waitForIdleTimeout": 0,
}

tiktok_app = 'com.zhiliaoapp.musically'
instagram_app = 'com.instagram.android'

data_root = Path('../../nzz_tiktok_insta_bot_data/export/')

server = 'http://localhost:%s/wd/hub'
