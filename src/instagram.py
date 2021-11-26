from appium import webdriver
from appium.webdriver.common.mobileby import MobileBy
from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import traceback
import time

import settings
import botlib

def run(user, caps, port):
    log = []

    # caps['app'] = settings.instagram_app
    caps['appPackage'] = settings.instagram_app
    caps['appActivity'] = 'com.instagram.mainactivity.MainActivity'

    # Create Driver
    driver = webdriver.Remote(
        settings.server % port,
        desired_capabilities=caps
    )
    driver.update_settings({"waitForIdleTimeout": 0})

    # Test for user
    if botlib.test_insta_user(driver, user) == False:
        driver.quit()
        raise("Wrong Insta-User!")

    # Start Screen Recording
    driver.start_recording_screen(
        timeLimit = "1800",
        bitRate = "3000000",
    )
    recording_time = time.time()
    video_name = "%s_%s_%s" % (user, 'insta', time.strftime("%Y_%m_%d_%H%M%S"))
    log_name = "%s_%s_%s" % (user, 'insta', time.strftime("%Y_%m_%d_%H%M%S"))

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
                print("Could not find %s" % id)
                return None

        timeabs = time.time()
        timedelta = time.time() - recording_time

        # Click on Video Caption
        try:
            el = driver.find_element_by_id("com.instagram.android:id/video_caption")
            if ('more' in el.text) or ('mehr' in el.text):
                point = [
                    el.location['x'] + el.size['width'] - 10,
                    el.location['y'] + el.size['height'] - 10
                ]
                actions = TouchAction(driver)
                actions.press(x = point[0], y = point[1]).release()
                actions.perform()
        except:
            # Nothing
            pass

        user = str_if_exists("com.instagram.android:id/username")
        text = str_if_exists("com.instagram.android:id/video_caption")
        likes = str_if_exists("com.instagram.android:id/like_count")
        comments = str_if_exists("com.instagram.android:id/comment_count")        
        # shares = str_if_exists("com.zhiliaoapp.musically:id/dls")

        # print("User: %s | Message: %s | Likes: %s | Comments: %s | Shares: %s" % (user, text, likes,comments,shares))
        #print("User: %s" % user)
        #print("Text: %s" % text)
        return {
            'username': user,
            'message': text,
            'likes': likes,
            # 'shares': shares,
            'comments': comments,
            'timein': timeabs,
            'videodelta': timedelta,
            'videoname': video_name,
            'platform': 'instagram'
        }

        # print("User: %s" % user)
        # print("Text: %s" % text)   

    # Go 10 Times
    errorcount = 0
    try:
        t = time.time()
        r = {"user": None, "text": None}
        startedat = time.time()
        run = True
        while run:

            print("Speed: %s" % (t - time.time()))
            t = time.time()

            # Read Data
            r = read_data()

            # Sometimes swipe is not executed correctly. Check if same story as before and reswipe
            if len(log) > 0:
                if(log[-1]['username'] == r['username']) and (log[-1]['message'] == r['message']):
                    print("Same story as before: Swipe again")
                    botlib.next(driver)
                    continue

            # Store Data
            if r['username'] == None:
                print("User not found!")
                errorcount += 1
            else:
                # Add Log-Entry
                errorcount = 0
                log.append({
                    'username': r['username'],
                    'message': r['message'],
                    'likes': r['likes'],
                    'comments': r['comments'],
                    # 'shares': r['shares'],
                    'timein': r['timein'],
                    'videodelta': r['videodelta'],
                    'videoname': r['videoname'],
                    'platform': r['platform'],
                    "hashtags": settings.users[user]
                })            

            if errorcount >= 3:
                # Hm, something went wrong. Stop it.
                raise Exception("⛔ Something went wrong, could not find user name. App crashed?")

            

            found = False
            if r['message'] and r['username']:
                for hash in settings.users[user]:
                    if (hash.lower() in r['message'].lower()) or (hash.lower() in r['username']):
                        print("✅ Hashtag found! '%s'" % hash)
                        found = True
                        break
            if found:
                botlib.sleep('long')
            else:
                botlib.sleep('short')

            # Update old Log entry
            if(len(log) > 0):
                log[-1]['timeout'] = time.time()

            # Rerun?
            if time.time() - startedat >= settings.run_for_seconds:
                run = False
            else:
                botlib.next(driver)

    except Exception as e:
        botlib.safe_log(user, log_name, log)
        botlib.safe_video(driver, user, video_name)
        print("⛔ Error occured")
        driver.quit()
        traceback.print_exc()
        #print(e)
        # print(type(e))
        raise e

    # Safe log & Video
    botlib.safe_log(user, log_name, log)
    botlib.safe_video(driver, user, video_name)

    driver.quit()

    print("finish")
