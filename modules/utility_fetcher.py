from os import listdir, getcwd
from os.path import isfile,join
from settings import settings
from modules import logger
import random

def GetCookies():
    try:
        cookies = [f for f in listdir(getcwd()+"/tools/cookies/") if isfile(join(getcwd()+ "/tools/cookies/",f))]
    except:
        logger.PrintColored("Error in GetCookies -> No file or directory tools/cookies","fail")
        return []
    try:
        cookies.remove(".gitignore")
        logger.PrintColored("Removing .gitingore...","ok")
    except:
        logger.PrintColored("Warning in GetCookies -> Removing .gitingore from folder failed, not found...","warning")
        pass
    return cookies

def GetProxyPairs():
    try:
        prox_pair = {}
        with open("tools/proxies.txt","r") as f:
            proxy_list = f.readlines()
            for i in range(len(proxy_list)):
                proxy_list[i] = proxy_list[i].strip()
                prox_pair[proxy_list[i].split("-")[0]] = proxy_list[i].split("-")[1]
        proxy_list.clear()
    except:
        logger.PrintColored("Error in GetProxyPairs -> No file or directory tools/proxies.txt","fail")
        return {}
    return prox_pair

def GetRandomMessages():
    messages = []
    ok = False
    try:
        with open("tools/chatting/messages_to_send.txt") as f:
            raw = f.readlines()
            for i in range(len(raw)):
                raw[i] = raw[i].strip()
                try:
                    if raw[i].split(":")[1] == settings["type_of_stream"]:
                        ok = True
                        continue
                except:
                    pass
                if ok:
                    if ":" in raw[i]:
                        ok = False
                        break
                    messages.append(raw[i])
    except:
        logger.PrintColored("Error in GetRandomMessages -> No file or directory tools/chatting/messages_to_send.txt","fail")
        return []
    messages_mixed = []
    for i in range(len(messages)):
        ran_msg = messages[random.randint(0,len(messages)-1)]
        messages.remove(ran_msg)
        messages_mixed.append(ran_msg)
    return messages_mixed


def GetResponseMessages(file):
    responses = {}
    question = ""
    with open(f"tools/chatting/{file}","r") as f:
        raw = f.readlines()
        for i in range(len(raw)):
            raw[i] = raw[i].strip()
            if ":" in raw[i]:
                question = raw[i].split(':')[1].split(':')[0]
                responses[question] = []
                continue
            responses[question].append(raw[i])
    return responses