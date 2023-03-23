from modules import logger
from modules import radio_functions

import requests
import time

def AdTracker(driver,token,bot_id,debug):    
    logger.PrintColored("Ad tracker active...")
    while radio_functions.GetIfAlive(bot_id):
        try:
            while radio_functions.GetIfOnStream(bot_id) == False and radio_functions.GetIfTyping(bot_id) == False and bot_id != 0:
                driver.switch_to.window(driver.window_handles[0])
                radio_functions.SetIfOnStream(True,bot_id) 
        except Exception as e:
            print(e)
        try:
            ad_notification = driver.execute_script("return document.querySelector(\"[data-a-target=\'video-ad-countdown\']\");")
        except:
            try:
                ad_notification = driver.execute_script("return document.querySelector(\"[data-a-target=\'video-ad-label\']\");")
            except:
                ad_notification = ""
        try:
            if "ad" in ad_notification.text.lower():
                if not debug:
                    requests.post("http://unkwn-services.com/update-analytics",json={"bot":"yaboi","to_update":"ads_viewed","value":1,"override":False,"username":token,"ADMINPASS":radio_functions.GetAdminPass()})
                logger.PrintColored("Ad detected...")
                time.sleep(29)
                pass
        except Exception as e:
            pass
        try:
            if radio_functions.GetIfTyping(bot_id) == False and bot_id != 0:
                driver.switch_to.window(driver.window_handles[1])
                radio_functions.SetIfOnStream(False,bot_id)
        except Exception as e:
            print(e)
        time.sleep(30)