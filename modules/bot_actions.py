from modules import logger
from modules import radio_functions
from modules import randact
from modules import utility_fetcher

from settings import settings
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import random
import time
import requests

def Follow(driver,messages,cookie,bot_id,token,debug=False):
    while radio_functions.GetIfTyping(bot_id) == False and radio_functions.GetIfOnStream(bot_id) == False and bot_id != 0:
        try:
            driver.switch_to.window(driver.window_handles[0])
            radio_functions.SetIfOnStream(True,bot_id)
        except:
            pass

    try:
        driver.execute_script("document.querySelector(\"[data-a-target=\'unfollow-button\']\").innerText;")
        logger.PrintColored("Already following streamer, skipping...")
        while radio_functions.GetIfTyping(bot_id) == False and radio_functions.GetIfOnStream(bot_id) == True and bot_id != 0:
            try:
                driver.switch_to.window(driver.window_handles[1])
                radio_functions.SetIfOnStream(True,bot_id)
            except:
                pass
        return randact.RandomAction(driver,cookie,messages,token,bot_id)
    except:
        pass
    try:
        driver.execute_script("document.querySelector(\"[data-a-target=\'follow-button\']\").click();")
        if not debug:
            requests.post("http://unkwn-services.com/update-analytics",json={"bot":"yaboi","to_update":"bots_followed","value":1,"override":False,"username":token,"ADMINPASS":radio_functions.GetAdminPass()})
        time.sleep(1)
    except:
        logger.PrintColored("Could not follow streamer...","fail")
        while radio_functions.GetIfTyping(bot_id) == False and radio_functions.GetIfOnStream(bot_id) == True and bot_id != 0:
            try:
                driver.switch_to.window(driver.window_handles[1])
                radio_functions.SetIfOnStream(False,bot_id)
            except:
                pass
        return randact.RandomAction(driver,cookie,messages,token,bot_id)

def SendMessage(driver,bot_id,message,token,debug=False,sent_fails = 0):

    if radio_functions.GetIfTyping(bot_id) == False:
        radio_functions.SetIfTyping(True,bot_id)
        try:
            if radio_functions.GetIfOnStream(bot_id) == False:
                try:
                    driver.switch_to.window(driver.window_handles[0])
                    radio_functions.SetIfOnStream(True,bot_id)
                    try:
                        driver.execute_script("document.getElementsByClassName(\'persistent-player\')[0].style = \"top: 0px; left: 0px; position: absolute; max-height: 1px; overflow: hidden; z-index: 1; height: auto; transition: transform 0.5s ease 0s; transform-origin: left top; transform: scale(1); max-width:1px;\";")
                        logger.PrintColored("1pixel exploit ran successfully...")
                    except:
                        logger.PrintColored("1pixel method not ran successfully...","fail")
                except Exception as e:
                    print(e)

        except Exception as e:
            print(e)
        try:
            chat_message = driver.execute_script("return document.querySelector(\"[data-test-selector=\'chat-input-tray-click-container\']\").innerText")
            if "follow" in chat_message.lower():
                try:
                    driver.execute_script("document.querySelector(\"[data-a-target=\'unfollow-button\']\").innerText;")
                    pass
                except:
                    logger.PrintColored("[!] Followers only chat, skipping message...","warning")
                    try:
                        if bot_id != 0:
                            #top: 0px; height: auto; left: 0px; position: absolute; overflow: hidden; z-index: 1; max-height: calc(100vh - 16rem); transition: transform 0.5s ease 0s; transform-origin: left top; transform: scale(1);
                            try:
                                driver.execute_script("document.getElementsByClassName(\'persistent-player\')[0].style = \"top: 0px; height: auto; left: 0px; position: absolute; overflow: hidden; z-index: 1; max-height: calc(100vh - 16rem); transition: transform 0.5s ease 0s; transform-origin: left top; transform: scale(1);\";")
                                logger.PrintColored("1pixel reset...")
                            except:
                                logger.PrintColored("1pixel not reset...","fail")                            
                            driver.switch_to.window(driver.window_handles[1])
                            radio_functions.SetIfOnStream(False,bot_id)
                        radio_functions.SetIfTyping(False,bot_id)
                    except:
                        pass
                    return
        except:
            pass

        try:
            element = driver.find_element(By.CLASS_NAME,"chat-input")
            element.click()
            cypher = 1
            while cypher<=10:
                try:
                    element = driver.find_element(By.XPATH,f"//*[@id='live-page-chat']/div/div/div/div/div/section/div/div[{cypher}]/div[2]/div[1]/div[2]/div/div/div[1]/div/div/div/div/div[2]")
                    break
                except:
                    cypher +=1
            for letter in message:
                element.send_keys(letter)
                time.sleep(random.uniform(0,0.5))
            element.send_keys(Keys.ENTER)
            if not debug:
                requests.post("http://unkwn-services.com/update-analytics",json={"bot":"yaboi","to_update":"messages_sent","value":1,"override":False,"username":token,"ADMINPASS":radio_functions.GetAdminPass()})
            radio_functions.SetIfTyping(False,bot_id)
            try:
                if not radio_functions.GetIfTyping(bot_id):
                    try:
                        if bot_id != 0:
                            try:
                                driver.execute_script("document.getElementsByClassName(\'persistent-player\')[0].style = \"top: 0px; height: auto; left: 0px; position: absolute; overflow: hidden; z-index: 1; max-height: calc(100vh - 16rem); transition: transform 0.5s ease 0s; transform-origin: left top; transform: scale(1);\";")
                                logger.PrintColored("1pixel reset...")
                            except:
                                logger.PrintColored("1pixel not reset...","fail")
                            driver.switch_to.window(driver.window_handles[1])
                            radio_functions.SetIfOnStream(False,bot_id)
                    except:
                        pass
            except:
                pass
            return
        except:
            if sent_fails >=4:
                return
            time.sleep(10)
            sent_fails +=1
            radio_functions.SetIfTyping(False,bot_id)
            try:
                if bot_id != 0:
                    try:
                        driver.execute_script("document.getElementsByClassName(\'persistent-player\')[0].style = \"top: 0px; height: auto; left: 0px; position: absolute; overflow: hidden; z-index: 1; max-height: calc(100vh - 16rem); transition: transform 0.5s ease 0s; transform-origin: left top; transform: scale(1);\";")
                        logger.PrintColored("1pixel reset...","ok")
                    except:
                        logger.PrintColored("1pixel method not reset...","fail")   
                    driver.switch_to.window(driver.window_handles[1])
                    radio_functions.SetIfOnStream(False,bot_id)
            except:
                pass
            return SendMessage(driver,bot_id,message,token,sent_fails)
    else:
        time.sleep(5)
        if not radio_functions.GetIfTyping(bot_id):
            return SendMessage(driver,bot_id,message,token,sent_fails)

def EnterStream(driver,token,cookie,bot_id,override = None):
    try:
        driver.switch_to.window(driver.window_handles[1])
        driver.close()
    except:
        pass
    try:
        driver.execute_cdp_cmd("Emulation.setAutomationOverride",{"enabled":True})
        driver.execute_cdp_cmd("Emulation.setIdleOverride",{"isUserActive":True,"isScreenUnlocked":True})
        driver.execute_cdp_cmd("Emulation.setFocusEmulationEnabled",{"enabled":True})
        logger.PrintColored("[!] cdp exploits ran successfully","ok")
    except:
        logger.PrintColored("[!] FATAL ERROR failed running the CDP exploits...","fail")
        exit()

    if override == None:
        ways_to_enter = ["search","followed","direct"]
        way_chosen = ways_to_enter[random.randint(0,len(ways_to_enter)-1)]
    else:
        way_chosen = override

    if  way_chosen == "search":
        driver.get("https://www.twitch.tv/search?term=%s" % settings["streamer"])
        time.sleep(2)
        try:
            elements = driver.find_elements(By.TAG_NAME,"a")
            for element in elements:
                if element.text.lower() == settings["streamer"].lower():
                    element.click()
                    break
        except:
            logger.PrintColored("[!] Failed to search for the streamer, going direct...","warning")
            return EnterStream(driver,token,cookie,bot_id,"direct")
    elif way_chosen == "followed":
            driver.get("https://www.twitch.tv/directory/following")
            time.sleep(2)
            try:
                driver.execute_script("document.querySelector(\"[title=\'%s\']\").click();" % settings["streamer"])
            except:
                logger.PrintColored("[!] Could not find streamer on the followed tab...","warning")
                return EnterStream(driver,token,cookie,bot_id,"direct")
    elif way_chosen == "direct":
        driver.get("https://www.twitch.tv/%s" % settings["streamer"])
    try:
        time.sleep(2)
        driver.execute_script("document.querySelector(\"[data-a-target=\'player-overlay-mature-accept\']\").click();")
        logger.PrintColored("[!] Mature button clicked...","warning")
            
    except:
        
            logger.PrintColored("[!] Streamer can be watched without aggreeing.","ok")
    driver.execute_script("window.onblur = function() { window.onfocus(); }")
    time.sleep(2)
    try:
        driver.execute_script("document.querySelector(\"[data-a-target=\'player-settings-button\']\").click();")
        time.sleep(1)
        driver.execute_script("document.querySelector(\"[data-a-target=\'player-settings-menu-item-quality\']\").click();")

    except:
        logger.PrintColored("[!] Could not find quality button...","fail")
        return EnterStream(driver,token,cookie,bot_id,"direct")
    cypher = 10
    while cypher > 1:
        try:
            driver.execute_script(f"document.querySelectorAll(\"[data-a-target = \'tw-radio\']\")[{cypher}].click()") 
            logger.PrintColored("[!] Lowest quality selected...","ok")
            break
        except:
            cypher -= 1
            if cypher <= 1:
                logger.PrintColored("[!] Quality could not be set to lowest...","warning")
                #os.system("killall chrome")
                #requests.post("http://unkwn-services.com/dashboard-yaboi/status-update",{"state":-1,"token":f"{TOKEN}","serverIP":"0","ADMINPASS":ADMINPASS})
                #os.system("killall python3")
    try:
        time.sleep(2)
        driver.execute_script("document.querySelector(\"[data-a-target=\'player-settings-button\']\").click();")
        time.sleep(0.5)
        driver.execute_script("document.querySelector(\"[data-a-target=\'player-settings-button\']\").click();")
        time.sleep(0.5)
        driver.execute_script("document.querySelector(\"[data-a-target=\'player-settings-menu-item-advanced\']\").click();")
        time.sleep(0.5)
        driver.execute_script("document.querySelector(\"[data-test-selector=\'low-latency-toggle\']\").querySelector(\"input\").click();")
    except:
        logger.PrintColored("[!] Streamer has no low latency toggle...","warning")

    try:
        time.sleep(4)
        element = driver.find_element(By.CLASS_NAME,"chat-wysiwyg-input__editor") 
        element.click()
    except:
        pass

    time.sleep(random.uniform(.5,2))
    
    try:
        driver.execute_script("document.querySelector(\"[data-test-selector=\'chat-rules-ok-button\']\").click();")
    except:
        try:
            driver.execute_script("document.querySelector(\"[data-test-selector=\'chat-rules-continue-button\']\").click();")
        except:
            logger.PrintColored("[!] No chat rules, skipping...","ok")
    try:
        chat_message = driver.execute_script("return document.querySelector(\"[data-test-selector=\'chat-input-tray-click-container\']\").innerText")
        if "verified" in chat_message.lower():
            settings["bots_should_chat"] = "no"
            logger.PrintColored("[!] Disabling bot chatting since verified accounts are a must...","warning")
    except:
        pass
        
    try:
        if bot_id != 0:
            driver.switch_to.new_window('tab')
            radio_functions.SetIfOnStream(False,bot_id)
        else:
            radio_functions.SetIfOnStream(True,bot_id)
            logger.PrintColored("[!] Skipping new tab, active listener detected...")
    except:
        pass

    radio_functions.RegisterBot(cookie,int(bot_id))
    return 

def GetRecentChatter(driver,bot_id):
    while radio_functions.GetIfTyping(bot_id) == False and radio_functions.GetIfOnStream(bot_id) == False and bot_id != 0:
        try:
            driver.switch_to.window(driver.window_handles[0])
            radio_functions.SetIfOnStream(True,bot_id)
        except:
            pass
    chatter = driver.execute_script("let arr = document.querySelectorAll(\"[data-a-target=\'chat-message-username\']\");return arr[arr.length - 1].innerText")

    while radio_functions.GetIfTyping(bot_id) == False and radio_functions.GetIfOnStream(bot_id) == True and bot_id != 0:
        try:
            driver.switch_to.window(driver.window_handles[1])
            radio_functions.SetIfOnStream(False,bot_id)
        except:
            pass

    return chatter

def GetRecentMessage(driver,bot_id):
    while radio_functions.GetIfTyping(bot_id) == False and radio_functions.GetIfOnStream(bot_id) == False and bot_id != 0:
        try:
            driver.switch_to.window(driver.window_handles[0])
            radio_functions.SetIfOnStream(True,bot_id)
        except:
            pass
    message = driver.execute_script("let arr = document.querySelectorAll(\"[data-test-selector=\'chat-line-message-body\']\");return arr[arr.length - 1].innerText")

    while radio_functions.GetIfTyping(bot_id) == False and radio_functions.GetIfOnStream(bot_id) == True and bot_id != 0:
        try:
            driver.switch_to.window(driver.window_handles[1])
            radio_functions.SetIfOnStream(False,bot_id)
        except:
            pass

    return message

def MentionRecentChatter(driver,bot_id,token,cookie):

    bot_mention_questions = utility_fetcher.GetResponseMessages("mention_questions.txt")

    if radio_functions.GetIfTyping(bot_id) == False:

        try:
            recent_chatter = GetRecentChatter(driver,bot_id) # TEST, MIGHT NEED TO BE REWORKED
        except:
            logger.PrintColored("No other chatters active, skipping mention...","warning")
            return
	if recent_chatter == cookie:
            logger.PrintColored("Recent chatter was the bot itself. Skipping mention","warning")
            return
        message_to_send = "@"+recent_chatter+f" {list(bot_mention_questions.keys())[random.randint(0,len(bot_mention_questions.keys())-1)]}"
        logger.PrintColored("Sending message "+message_to_send,"ok")
        time.sleep(5)
        return SendMessage(driver,bot_id,message_to_send,token)

    else:
        logger.PrintColored("Bot was already typing, skipping mentioning another chatter...")
        return
