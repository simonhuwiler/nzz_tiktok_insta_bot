from selenium.webdriver.support.ui import WebDriverWait
from appium.webdriver.common.mobileby import MobileBy
from selenium.webdriver.support import expected_conditions as EC
import time
import json
import base64
from pathlib import Path
import os
import settings


def test_tiktok_user(driver, user):
    print("✔ Verify User")
    # Click on Profil
    ident = "com.zhiliaoapp.musically:id/cbr"
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((MobileBy.ID, ident)))
    driver.find_element_by_id(ident).click()

    # Get Username
    ident = "com.zhiliaoapp.musically:id/evr"
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((MobileBy.ID, ident)))
    logged_user = driver.find_element_by_id(ident).text

    # Back to Home Screen
    ident = "com.zhiliaoapp.musically:id/cbp"
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((MobileBy.ID, ident)))
    driver.find_element_by_id(ident).click()

    print("Task-User: %s" % user)
    print("TikTok-User: %s" % logged_user)

    return user.lower() == logged_user[1:].lower()

def test_insta_user(driver, user):
    print("✔ Verify User")
    # Click on Profil
    ident = "com.instagram.android:id/tab_avatar"
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((MobileBy.ID, ident)))
    driver.find_element_by_id(ident).click()
    print("Done")

    # Get Username
    ident = "com.instagram.android:id/action_bar_large_title_auto_size"
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((MobileBy.ID, ident)))
    logged_user = driver.find_element_by_id(ident).text

    # Back to Home Screen
    ident = '//android.widget.FrameLayout[@content-desc="Reels"]'
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((MobileBy.XPATH, ident)))
    driver.find_element_by_xpath(ident).click()

    print("Task-User: '%s'" % user)
    print("Insta-User: '%s'" % logged_user)

    return user.lower() == logged_user.lower()
    
def next(driver):
    driver.swipe(1000, 800, 1000, 500, 350)

def sleep(how):
    if how == 'long': time.sleep(10)
    if how == 'short': time.sleep(0.2)
    # else: print("Sleep %s not defined" % how)

def create_dir(p):
    if not p.exists():
        os.mkdir(p)

def safe_log(user, n, log):
    create_dir(settings.data_root / Path(user))

    with open(settings.data_root / Path('%s/%s.json' % (user, n)), 'w') as outfile:
        json.dump(log, outfile)    

def safe_video(driver, user, n):
    create_dir(settings.data_root / Path(user))

    video_rawdata = driver.stop_recording_screen()
    filepath = settings.data_root / Path("%s/%s.mp4" % (user, n))
    with open(filepath, "wb+") as vd:
        vd.write(base64.b64decode(video_rawdata))