from modules import logger

import socket
import pickle

alive = True
on_stream = False
typing = False

bot_cookies = {}

# mention recognized ( global bot )

# speech recognized ( global bot )
# last message context recognized ( global bot )
# last chatter ( global bot )
# bot list ( global bot ) 

def RegisterBot(cookie,id,bot_id=0,server_call=False):
   global bot_cookies
   if server_call:
      bot_cookies[cookie.lower()] = id
      print(bot_cookies)
      return True
   else:
      s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
      s.connect(("127.0.0.1",7777+bot_id))
      msg = s.send(f"register|cookie|{id}|{cookie}".encode("utf-8"))
      msg = s.recv(1024)

      if msg.decode("utf-8") == "ok":
         logger.PrintColored("Cookie registered with the server...")
      else:
         logger.PrintColored("Failed to register cookie...","fail")

def GetRegisteredBots(bot_id=0,server_call = False):
   global bot_cookies
   if server_call:
      return pickle.dumps(list(bot_cookies.keys()))
   else:
      s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
      s.connect(("127.0.0.1",7777+bot_id))

      msg = s.send("get|registered_cookies".encode("utf-8"))
      msg = s.recv(2048)

      return pickle.loads(msg)


def GetIfAlive(bot_id=0,server_call = False):
   global alive
   if server_call:
      return alive
   else:
      s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
      s.connect(("127.0.0.1",7777+bot_id))

      msg = s.send("get|alive".encode("utf-8"))
      msg = s.recv(1024)

      if msg == bytes(False):
         return False
      elif msg == bytes(True):
         return True

def GetIfOnStream(bot_id=0,server_call = False):
   global on_stream
   if server_call:
      return on_stream
   else:
      s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
      s.connect(("127.0.0.1",7777+bot_id))

      msg = s.send("get|on_stream".encode("utf-8"))
      msg = s.recv(1024)

      if msg == bytes(False):
         return False
      elif msg == bytes(True):
         return True

def GetIfTyping(bot_id=0,server_call = False):
   global typing
   if server_call:
      return typing
   else:
      s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
      s.connect(("127.0.0.1",7777+bot_id))

      msg = s.send("get|typing".encode("utf-8"))
      msg = s.recv(1024)

      if msg == bytes(False):
         return False
      elif msg == bytes(True):
         return True

def SetIfAlive(new_alive,bot_id=0,server_call = False):
   global alive
   if server_call:
      alive = new_alive
   else:
      s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
      s.connect(("127.0.0.1",7777+bot_id))
      if new_alive:
         msg = s.send("set|alive|true".encode("utf-8"))
      else:
         msg = s.send("set|alive|false".encode("utf-8"))
      msg = s.recv(1024)

      if msg.decode("utf-8") != "ok":
         logger.PrintColored("Failed to set new alive...","fail")

      s.close()

def SetIfOnStream(new_on_stream,bot_id=0,server_call = False):
   global on_stream
   if server_call:
      on_stream = new_on_stream
   else:
      s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
      s.connect(("127.0.0.1",7777 + bot_id))
      if new_on_stream:
         msg = s.send("set|on_stream|true".encode("utf-8"))
      else:
         msg = s.send("set|on_stream|false".encode("utf-8"))

      msg = s.recv(1024)

      if msg.decode("utf-8") != "ok":
         logger.PrintColored("Failed to set new on_stream...","fail")

      s.close()

def SetIfTyping(new_typing, bot_id=0,server_call = False):
   global typing
   if server_call:
      typing = new_typing
   else:
      s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
      s.connect(("127.0.0.1",7777+bot_id))
      if new_typing:
         msg = s.send("set|typing|true".encode("utf-8"))
      else:
         msg = s.send("set|typing|false".encode("utf-8"))
      msg = s.recv(1024)

      if msg.decode("utf-8") != "ok":
         logger.PrintColored("Failed to set new typing...","fail")
      
      s.close()

def GetActiveCookiesViaAPI(token):
   #Make sure the ports are open
   try:
      s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
      s.settimeout(5)
      s.connect(("217.69.3.196",7777)) # IF SERVER IP CHANGES WHIS WON'T WORK

      s.send(f"get|cookies|{token}".encode("utf-8"))

      return pickle.loads(s.recv(2048))
   except:
      logger.PrintColored("Failed communicating with the API.","fail")
      return "fail"


def NotifyBotOfMention(cookie,mention,chatter):

   # SERVER CALL, FIND WHAT BOT TO NOTIFY VIA THE REGISTERED BOTS...
   s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
   s.connect(("127.0.0.1",7777+bot_cookies[cookie.lower()]))

   msg = s.send(f"mention|detected|{cookie}|{mention}|{chatter}".encode("utf-8"))
   msg = s.recv(2048)

   if msg.decode("utf-8") != "ok":
      logger.PrintColored("Failed mention delivery to bot...","fail")
   s.close()

def NotifyBotOfSpeechRecognition(cookie,text_recognized):

   # SERVER CALL, FIND WHAT BOT TO NOTIFY VIA THE REGISTERED BOTS...
   s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
   s.connect(("127.0.0.1",7777+bot_cookies[cookie.lower()]))

   msg = s.send(f"speech|detected|{cookie}|{text_recognized}".encode("utf-8"))
   msg = s.recv(2048)

   if msg.decode("utf-8") != "ok":
      logger.PrintColored("Failed speech delivery to bot...","fail")
   s.close()

def GetAdminPass():
   return "pne8gaQfGqXneyArZa380sb-sNvE$gZPFc2F2Tuz502qzLdI@6NTjxVgIGsD-0l^"
   # Here we need to check to see if we are server, if we are we don't need to send a client request.