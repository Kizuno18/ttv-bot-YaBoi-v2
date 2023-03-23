from settings import settings
from modules import logger
from modules import bot_actions
from modules import radio_functions

import random
import time

def RandomAction(driver,cookie,messages,token,bot_id,debug):
    actions = ["chat","follow","mention_another_chatter"]

    while True:
        for _ in range(int(int(settings["bot_event_rate"])* random.uniform(1,2))): # 120 * random (1,2)
            if radio_functions.GetIfAlive(bot_id):
                time.sleep(1)
            else:
                driver.quit()
                logger.PrintColored("[!] Bot is quitting...","ok")
                exit(-1)

        action_selected = actions[random.randint(0,len(actions)-1)]
        if action_selected == "chat":
            if settings["bots_should_chat"] == "yes":
                if len(messages) > 0:
                    message_to_send = messages[random.randint(0,len(messages)-1)]
                    messages.remove(message_to_send)#This is to ensure that the bot does not send the same message twice...
                    if random.randint(0,10) == 0:
                        message_to_send = "@"+settings["streamer"]+" " + message_to_send
                    
                    # Check to see if there is a {then} in the message
                    if "{then}" in message_to_send:
                        bot_actions.SendMessage(driver,bot_id,message_to_send.split("{then}")[0],token,debug)
                        time.sleep(random.radnint(5,10))
                        message_to_send = message_to_send
                        bot_actions.SendMessage(driver,bot_id,message_to_send.split("{then}")[1],token,debug)
                    else:
                        bot_actions.SendMessage(driver,bot_id,message_to_send,token,debug)
                    
                    
                else:
                    logger.PrintColored("No more unique messages... Skipping message send.","warning")# add override for this
            else:
                logger.PrintColored("Bot wanted to chat, stopped because bots_should_chat = no")
                        
        if action_selected == "follow":
            if settings["bots_should_follow"] == "yes" and random.randint(0,2) == 0:
                bot_actions.Follow(driver,messages,cookie,bot_id,token,debug)
            else:
                if settings["bots_should_follow"] == "yes":
                    logger.PrintColored("Bot wanted to follow, skipping because following is disabled...")
                else:
                    logger.PrintColored("Bot wanted to follow, skipping because the 50p chance failed....")

        if action_selected == "mention_another_chatter" and random.randint(0,3) == 0:
            if settings["bots_chat_amongst"] == "yes":
                bot_actions.MentionRecentChatter(driver,bot_id,token,cookie)

            else:
                logger.PrintColored("[!] Bot wanted to mention another bot, stopped because bots_chat_amongst = no","ok")
