# !!! VON TIKTOK ÜBERNEHMEN


from appium import webdriver
from appium.webdriver.common.mobileby import MobileBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import traceback

import settings
import botlib

def run(user, caps, port):

    log = []

    caps['app'] = settings.instagram_app
    caps['appActivity'] = 'com.instagram.mainactivity.MainActivity'

    # Create Driver
    driver = webdriver.Remote(
        settings.server % port,
        desired_capabilities=caps
    )

    # Test for user
    if botlib.test_insta_user(driver, user) == False:
        driver.quit()
        raise("Wrong Insta-User!")

    # Start Screen Recording
    driver.start_recording_screen()
    recording_time = time.time()
    video_name = "%s_%s_%s" % (user, 'instagram', time.strftime("%Y_%m_%d_%H%M%S"))

    # Read
    ident = "com.instagram.android:id/clips_swipe_refresh_container"
    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((MobileBy.ID, ident)))
    time.sleep(1.5)

    def read_data():
        def str_if_exists(id):
            try:
                e = driver.find_element_by_id(id)
                return e.text
            except:
                print("Exception")
                return None

        timeabs = time.time()
        timedelta = time.time() - recording_time
        
        user = str_if_exists("com.instagram.android:id/username")

        # Click on Video Caption
        try:
            driver.find_element_by_id("com.instagram.android:id/video_caption").click()
        except:
            # Nothing
            print("")
        text = str_if_exists("com.instagram.android:id/video_caption")
        
        likes = str_if_exists("com.instagram.android:id/like_count")
        comments = str_if_exists("com.instagram.android:id/comment_count")

        # Add Log-Entry
        log.append({
            'username': user,
            'message': text,
            'likes': likes,
            'comments': comments,
            'timein': timeabs,
            'videodelta': timedelta,
            'videoname': video_name,
            'platform': 'instagram'
        })
        
        print("User: %s" % user)
        print("Text: %s" % text)
        return {"user": user, "text": text}

    # Go 10 Times
    try:
        for i in range(0, 10):
            r = read_data()
            found = False
            if r['text']:
                for hash in settings.users[user]:
                    if hash in r['text'].lower():
                        print("Hashtag found! '%s'" % hash)
                        found = True
                        break
            if found:
                botlib.sleep('long')
            else:
                botlib.sleep('short')

            # Update old Log entry
            if(len(log) > 0):
                log[-1]['timeout'] = time.time()
            botlib.next(driver)

    except Exception as e:
        botlib.safe_log(video_name, log)
        botlib.safe_video(driver, video_name)
        print("Error occured")
        driver.quit()
        traceback.print_exc()
        #print(e)
        # print(type(e))
        raise e

    # Safe log & Video
    botlib.safe_log(video_name, log)
    botlib.safe_video(driver, video_name)

    driver.quit()

    print("finish")
