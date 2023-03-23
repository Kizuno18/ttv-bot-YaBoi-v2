from modules import logger
from modules import bot_actions
from modules import radio_functions

import time

def CrashTracker(driver,token,bot_id,restarts = 0):
    logger.PrintColored("Crash tracker active...")
    while radio_functions.GetIfAlive(bot_id):
        typing = radio_functions.GetIfTyping(bot_id)
        try:
            if typing == False and bot_id != 0:
                driver.switch_to.window(driver.window_handles[0])
                on_stream = True
                radio_functions.SetIfOnStream(on_stream,bot_id)
        except:
            pass
        try:
            divs = driver.execute_script("return document.querySelectorAll(\"[data-a-target=\'tw-core-button-label-text\']\");") #find where text has "click here to reload player".lower
            for div in divs:
                if "reload player" in div.get_attribute("innerText").lower():
                    div.click()
                    logger.PrintColored("Restarted player because it crashed...","fail")
                    #restarts +=1
                    #if restarts >= 4:
                    #    alive = False
                    #    radio_functions.SetIfAlive(alive,bot_id)
                    #return CrashTracker(driver,bot_id,restarts)
        except:
            pass
        if bot_id == 0:
            try:
                mute_button = driver.execute_script("return document.querySelector(\"[data-a-target=\'player-mute-unmute-button\']\");")
                unmute_trials = 0
                while "unmute" in  mute_button.get_attribute("aria-label").lower():
                    if unmute_trials == 0:
                        logger.PrintColored("Clicking unmute button...")
                    else:
                        logger.PrintColored("Unmute button clicking again...","fail")
                    driver.execute_script("document.querySelector(\"[data-a-target=\'player-mute-unmute-button\']\").click();")
                    time.sleep(1)
                    unmute_trials +=1
                    if unmute_trials >=4:
                        alive = False
                        radio_functions.SetIfAlive(alive,bot_id)
            except:
                logger.PrintColored("Cannot find unmute button...","fail")
        try:
            if "failed" in driver.execute_script("return document.querySelector(\"[data-a-target=\'core-error-message\']\");").get_attribute("innerText").lower():
                logger.PrintColored("Module load error, refreshing stream...","warning")
                bot_actions.EnterStream(driver,token)
        except:
            pass
        try:
            if typing == False and bot_id != 0:
                driver.switch_to.window(driver.window_handles[1])
                on_stream = False
                radio_functions.SetIfOnStream(on_stream,bot_id)
            else:
                on_stream = True
                radio_functions.SetIfOnStream(on_stream,bot_id)
        except:
            on_stream = True
            radio_functions.SetIfOnStream(on_stream,bot_id)
            pass

       

        time.sleep(60)