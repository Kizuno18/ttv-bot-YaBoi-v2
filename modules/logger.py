def PrintColored(text,message_type="ok"):

    OK = '\033[92m'
    WARNING = '\033[93m'
    FAIL    = '\033[91m'
    ENDC    = '\033[0m'

    if message_type == "warning":
        print(f"{WARNING}" + text + f"{ENDC}")
    elif message_type == "ok":
        print(f"{OK}" + text + f"{ENDC}")
    elif message_type == "fail":
        print(f"{FAIL}" + text + f"{ENDC}")
    with open("log/log.ybl","a+") as f:
        f.write(text + "\n")