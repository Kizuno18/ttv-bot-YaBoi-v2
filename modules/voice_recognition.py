from modules import logger
from modules import bot_actions
from modules import radio_functions
from modules import utility_fetcher

import os
import time
import random
import speech_recognition


def VoiceRecognition(driver,bot_id):
    logger.PrintColored("Starting voice recognition module...")
    command = "arecord -D loopout -d 5 -r 44100 -f cd dump.wav"
    recognizer = speech_recognition.Recognizer()
    responses = utility_fetcher.GetResponseMessages("speech_recognition_responses.txt")
    while radio_functions.GetIfAlive(bot_id):
        recognized = ""
        os.system(command)
        time.sleep(.1)
        os.system("sox -t wav -r 44100 -e signed-integer -L -b 16 -c 2 dump.wav sound_sample.flac")
        os.system("rm dump.wav")
        try:
            with speech_recognition.AudioFile("sound_sample.flac") as rec:
                audio = recognizer.record(rec)
                recognized = recognizer.recognize_google(audio)
                recognized = recognized.lower()
        except:
            recognized = ""

        #    PrintColored("Text recognized: "+ recognized,"ok")
        for response in responses:
            if response in recognized:
                logger.PrintColored("Found a speech recognition sentence.")
                
                active_bots = radio_functions.GetRegisteredBots(bot_id)
                print(active_bots)
                # Calculate how much bots respond ( 1 to 10 allowed) based on the ammount of active bots.
                if len(active_bots) > 1:
                    for _ in range(random.randint(1,len(active_bots)-1)):
                        bot_to_notify = active_bots[random.randint(0,len(active_bots)-1)]
                        active_bots.remove(bot_to_notify)
                        radio_functions.NotifyBotOfSpeechRecognition(bot_to_notify,response)
                    break
                else:
                    break


def HandleRecognizedVoiceRecognition(driver,recognized_text,bot_id,token):
    
    responses = utility_fetcher.GetResponseMessages("speech_recognition_responses.txt")
    time.sleep(random.randint(2,5))    
    bot_actions.SendMessage(driver,bot_id,responses[recognized_text][random.randint(0,len(responses[recognized_text])-1)],token)

                
