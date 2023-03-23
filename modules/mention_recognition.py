from modules import radio_functions
from modules import utility_fetcher
from modules import logger
from modules import bot_actions

import time
import random


def MentionRecognition(driver,cookie,token,bot_id): # previous tag? So you know if you have tagged that bot and sohuld not reply on tag no. 2
    previous_message = ""
    while radio_functions.GetIfAlive(bot_id):
        time.sleep(.1)
        try:
            message = driver.execute_script("let arr = document.querySelectorAll(\"[data-test-selector=\'chat-line-message-body\']\");return arr[arr.length - 1].innerText")
            message = message.split("?")[0]
            chatter = driver.execute_script("let arr = document.querySelectorAll(\"[data-a-target=\'chat-message-username\']\");return arr[arr.length - 1].innerText")
        except:
            message = ""
            chatter = ""
        try: 
            mention = message.split("@")[1].split(" ")[0]
            message = message.split("@")[1].split(" ")[1:]
            message = ' '.join(message)
            #print("MENTION",mention)
        except:
            mention = ""

        # Get all cookies from the radio
        try:
            cookies = radio_functions.GetRegisteredBots(bot_id)
            if mention.lower() in cookies and previous_message != message:
                logger.PrintColored("Mention detected for bot")
                radio_functions.NotifyBotOfMention(mention,message,chatter)
                previous_message = message
                # Make sure to do once.
        except:
            logger.PrintColored("Failed communicating with the radio...","fail")

        # Get mention username and who is mentioned
        # Place a person that chatted the last into a que of last chatters, if that que is larger than 10 replace the newest one with the last one


def HandleRecognizedMention(driver,cookie,mention,chatter,bot_id,token):
    responses = utility_fetcher.GetResponseMessages("mention_responses.txt")

    mention_parts = []

    slicer_mention = ""
    words = mention.split(" ")
    if ',' in mention:
        words = mention.split(",") + words
    if '.' in mention:
        words = mention.split(".") + words
    if '!' in mention:
        words = mention.split("!") + words

    for i in range(len(words)):
        for word in words:
            slicer_mention += " " + word
            for response in responses:
                if slicer_mention.lower() == " "+response.lower():
                    mention_parts.append(" ".join(slicer_mention.lower().split(" ")[1:]))
        slicer_mention = ""
        words.pop(0)
    
    reply = ""

    size = len(mention_parts)        

    if size == 0:
        reply += responses["GENERIC"][random.randint(0,len(responses["GENERIC"])-1)]

    reply_separators = [", "," ",". "]
    for part in mention_parts:
        if size > 1:
            reply += responses[part][random.randint(0,len(responses[part])-1)] + reply_separators[random.randint(0,len(reply_separators)-1)]
        else:
            reply += responses[part][random.randint(0,len(responses[part])-1)]
        size -= 1

        
    
    print("Reply DBG = ",reply)

    active_bots = radio_functions.GetActiveCookiesViaAPI(token)

    if active_bots != "fail":
        # If we an get the list
        if chatter in active_bots:
            # The mention was from a bot, skip
            pass
        else:
            reply = "@"+chatter+" "+reply

    time.sleep(random.randint(5,10))
    bot_actions.SendMessage(driver,bot_id,reply,token)

    # Implement bot gets annoyed
    