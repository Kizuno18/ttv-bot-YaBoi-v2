import configparser

config = configparser.ConfigParser()
config.read("config.ini")

settings = {}
settings["streamer"] = config["stream"]["streamer"]
settings["proxy_type"] = config["stream"]["proxy_type"]
settings["bots_should_chat"] = config["stream"]["bots_should_chat"]
settings["bots_should_follow"] = config["stream"]["bots_should_follow"]
settings["bot_max_join_time"] = config["stream"]["bot_max_join_time"]
settings["bot_event_rate"] = config["stream"]["bot_event_rate"]
settings["bots_chat_amongst"] = config["stream"]["bots_chat_amongst"]
settings["speech_recognition"] = config["stream"]["speech_recognition"]
settings["mention_recognition"] = config["stream"]["bots_mention_recognition"]
settings["type_of_stream"] = config["stream"]["type_of_stream"]