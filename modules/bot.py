from modules import ad_tracker
from modules import crash_tracker
from modules import mention_recognition
from modules import voice_recognition
from modules import randact
from modules import utility_fetcher
from modules import bot_actions
from modules import logger
from modules import radio_functions
from settings import settings

from xvfbwrapper import Xvfb

import undetected_chromedriver as uc
import threading
import random
import pickle
import socket
import time

# If server spawn a listener, create a thread for every response the clients request
def Radio(bot_id,driver,token):
    if bot_id == 0:
        logger.PrintColored("Radio server started for global bot...")
    else:
        logger.PrintColored("Radio server started for slave bot...")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 7777 + bot_id)) # MAIN BOT THAT DOES SPEECH RECOGNITION AND MENTION RECOGNITION
        s.listen()
        while radio_functions.GetIfAlive(server_call=True):
            conn, addr = s.accept()
            with conn:
                # add send to other bots ( mention recognized, speech recognized )
                data = conn.recv(2048).decode("utf-8")
                if "register|cookie" in data:
                    id_associated = data.split("|")[2]
                    cookie = data.split("|")[3]
                    if radio_functions.RegisterBot(cookie,int(id_associated),server_call=True):
                        response = "ok".encode("utf-8")

                if data == "get|registered_cookies":
                    response = radio_functions.GetRegisteredBots(server_call=True)

                # ^^ COOKIE REGISTRATION

                if "mention|detected" in data:
                    cookie = data.split("|")[2]
                    mention = data.split("|")[3]
                    chatter = data.split("|")[4]
                    threading.Thread(target=mention_recognition.HandleRecognizedMention,args=(driver,cookie,mention,chatter,bot_id,token)).start()
                    # ^^ must spawn thread if the function will call any radio functions
                    response = "ok".encode("utf-8")
                # ^^ mention recognition

                if "speech|detected" in data:
                    cookie = data.split("|")[2]
                    recognized_text = data.split("|")[3]
                    print(cookie,recognized_text)
                    threading.Thread(target=voice_recognition.HandleRecognizedVoiceRecognition,args=(driver,recognized_text,bot_id,token)).start()
                    # ^^ must spawn thread if the function will call any radio functions
                    response = "ok".encode("utf-8")
                # ^^ Speech recognition

                if data == "get|alive":
                    response = radio_functions.GetIfAlive(server_call=True)

                if data == "get|on_stream":
                    response = radio_functions.GetIfOnStream(server_call=True)

                if data == "get|typing":
                    response = radio_functions.GetIfTyping(server_call=True)

                if data == "set|alive|true":
                    radio_functions.SetIfAlive(True,server_call=True)
                    response = "ok".encode("utf-8")

                if data == "set|alive|false":
                    radio_functions.SetIfAlive(False,server_call=True)
                    response = "ok".encode("utf-8")

                if data == "set|on_stream|true":
                    radio_functions.SetIfOnStream(True,server_call=True)
                    response = "ok".encode("utf-8")

                if data == "set|on_stream|false":
                    radio_functions.SetIfOnStream(False,server_call=True)
                    response = "ok".encode("utf-8")

                if data == "set|typing|true":
                    radio_functions.SetIfTyping(True,server_call=True)
                    response = "ok".encode("utf-8")

                if data == "set|typing|false":
                    radio_functions.SetIfTyping(False,server_call=True)
                    response = "ok".encode("utf-8")

                if not data:
                    pass
                # ^^ BASIC SET OF VARIABLES
                conn.sendall(bytes(response))
                conn.close()      
        return




# Bot should have a listener socket that will notify other threads/processes of the current state. If the bot is on stream tab or not, if it's typing  and other things.

def InitiateStart(cookie,proxy,messages,token,debug,bot_id):
    logger.PrintColored(f"Got start request for cookie: {cookie}...")
    cookie_name = cookie.split(".")[0]
    if debug:
        pass
    else:
        vdisplay = Xvfb(width=1920, height=1080)
        vdisplay.start()

    chrome_options = uc.ChromeOptions()# add user agent generation
    if bot_id != 0: 
        chrome_options.add_argument("--mute-audio")

    width = random.randint(1500,1920)
    height = random.randint(800,1080)

    chrome_options.add_argument(f"--proxy-server={proxy}")
    chrome_options.add_argument(f"--window-size={width},{height}")
    if not debug:
        driver = uc.Chrome(version_main=106,options=chrome_options)
    else:
        driver = uc.Chrome(options=chrome_options)


    driver.get("https://www.twitch.tv/")
    if cookie != None:
        if ".ybb" in cookie:
            cookie_loaded = pickle.load(open(f"tools/cookies/{cookie}","rb"))
            for part in cookie_loaded:
                if 'sameSite' in part:
                    if part["sameSite"] == "None":
                        part["sameSite"] = "Strict"
                    driver.add_cookie(part)
        elif ".v2" in cookie:
            cookies = []
            with open("tools/cookies/"+cookie,"r") as f:
                cookie_raw = f.read()
                cookie_raw = cookie_raw.split(";")
                for i in range(len(cookie_raw)):
                    cookie_raw[i] = cookie_raw[i].strip()
                    cookies.append(
                        {
                            "name":cookie_raw[i].split("=")[0],
                            "value":cookie_raw[i].split("=")[1]
                        })
            for cookie in cookies:
                driver.add_cookie(cookie)
        
        time.sleep(1)
        driver.refresh()
    
    logger.PrintColored("Chrome startup complete, starting services and entering stream...")

    radio = threading.Thread(target=Radio,args=(bot_id,driver,token))
    radio.start()

    bot_actions.EnterStream(driver,token,cookie_name,bot_id)

    crash_tracker_t = threading.Thread(target=crash_tracker.CrashTracker,args=(driver,token,bot_id))
    crash_tracker_t.start()


    ad_tracker_t = threading.Thread(target=ad_tracker.AdTracker,args=(driver,token,bot_id,debug))
    ad_tracker_t.start()

 

    if settings["mention_recognition"] == "yes":
        if bot_id == 0:
            mention_listener_thread = threading.Thread(target=mention_recognition.MentionRecognition,args=(driver,cookie_name,token,bot_id))
            mention_listener_thread.start()
            # Listener thread only for the listener bot. It will send notifications to other bots and they will respond accordingly.


    if settings["speech_recognition"] == "yes":
        if bot_id == 0:
            speech_listener_thread = threading.Thread(target=voice_recognition.VoiceRecognition,args=(driver,bot_id))
            speech_listener_thread.start()

    if settings["bots_should_chat"] == "yes":
        if random.randint(0,7) == 0:
            hello_messages = ["Hi","Hello!","What\'s up?","sup","supp","hey hey","hi my guy","what\'s poppin"]
            bot_actions.SendMessage(driver,bot_id,hello_messages[random.randint(0,len(hello_messages)-1)],token)
            hello_messages.clear()

    #restarter_thread = threading.Thread(target=Restarter)
    #restarter_thread.start()
    randact.RandomAction(driver,cookie_name,messages,token,bot_id,debug)

