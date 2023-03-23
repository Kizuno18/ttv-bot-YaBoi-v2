from modules import logger
from modules import utility_fetcher
from modules import bot
from settings import settings
import time
import random
import sys
import requests
import multiprocessing
import threading

cookies = utility_fetcher.GetCookies()
proxy_pairs = utility_fetcher.GetProxyPairs()
bot_instances = []

ADMINPASS = "pne8gaQfGqXneyArZa380sb-sNvE$gZPFc2F2Tuz502qzLdI@6NTjxVgIGsD-0l^"
BOTS_ACTIVE = 0
TOKEN = sys.argv[1]
BOT_AMOUNT = int(sys.argv[2])

try:
    if sys.argv[3] == "debug":
        debug = True
        logger.PrintColored("Starting in debug mode!","warning")
    else:
        debug = False
except:
    debug = False





def BotStarter(id,cookie_override,MESSAGES):
    if cookie_override == None:
        if len(cookies) > 0:
            cookie = cookies[random.randint(0,len(cookies)-1)]
            proxy = proxy_pairs[cookie.split(".")[0]]
            cookies.remove(cookie)

            process = multiprocessing.Process(target=bot.InitiateStart,args=(cookie,proxy,MESSAGES,TOKEN,debug,id))
        else:
            proxy = ""
            process = multiprocessing.Process(target=bot.InitiateStart,args=(None,proxy,MESSAGES,TOKEN,debug,id))
            cookie = None
            
    else:
        proxy = proxy_pairs[cookie_override.split(".")[0]]
        process = multiprocessing.Process(target=bot.InitiateStart,args=(cookie_override,proxy,MESSAGES,TOKEN,debug,id))
        cookie = cookie_override
    process.start()
    bot_instances.append([process,id,cookie,MESSAGES,TOKEN,debug])


def BotCrashDetector():
    logger.PrintColored("[!] Bot crash detector active...","ok")
    while True:
        for i in range(BOTS_ACTIVE):
            if bot_instances[i][0].is_alive() == False:
                logger.PrintColored("[!] Bot has died..."+" restarting with cookie" + bot_instances[i][2],"warning")
                bot_instances[i][0].close()
                if bot_instances[i][2] != None:
                    if bot_instances[i][5]:
                        BotStarter(bot_instances[i][1],bot_instances[i][2],bot_instances[i][3])
                    else:
                        BotStarter(bot_instances[i][1],bot_instances[i][2],bot_instances[i][3])
                else:
                    BotStarter(bot_instances[i][1],None,bot_instances[i][3],radio_server=False)
                bot_instances.remove(bot_instances[i])

        time.sleep(10)


if __name__ == "__main__":
    messages = utility_fetcher.GetRandomMessages()
    # Get messages bots can send ^^ 

    if settings["type_of_stream"] != "gaming":
        settings["type_of_stream"] = "gaming"
        messages += utility_fetcher.GetRandomMessages()
    # Get generic messages and add them to the list ^^

    # Get emotes and add them to the list ^^

    crash_detector_thread = threading.Thread(target=BotCrashDetector)
    crash_detector_thread.start()
    # Start the crash detector thread ^^

    switch = True
    previousRandNumber = 0
    time_to_join_minutes = int(60*int(settings["bot_max_join_time"]))
    for i in range(BOT_AMOUNT):
        timeToJoinPerBot = int(time_to_join_minutes/BOT_AMOUNT)
        randNumb = random.randint(1,10)
        if switch:
            timeToJoinPerBot += randNumb
            switch = False
            previousRandNumber = randNumb
        else:
            timeToJoinPerBot -= previousRandNumber
            switch = True

        logger.PrintColored("Starting bot: "+str(i+1))
        BotStarter(i,None,messages[-int(len(messages) / BOT_AMOUNT):])
        messages = messages[: -int(len(messages) / BOT_AMOUNT)]

        try:
            if not debug:
                requests.post("http://unkwn-services.com/update-analytics",json={"bot":"yaboi","to_update":"bots_in_stream","value":1,"override":False,"username":TOKEN,"ADMINPASS":ADMINPASS},timeout=5)
            pass
        except requests.exceptions.ReadTimeout: 
            logger.PrintColored("Error in source.py -> No response from server, skipping analytics update...","fail")
        
        BOTS_ACTIVE+=1
        mention_recognition_server = False
        speech_recognition_server = False
        radio_server = False
        if not debug:
            time.sleep(60 * timeToJoinPerBot)
        else:
            time.sleep(20)
        # 60 * timeToJoinPerBot