import os
import slack
import ssl as ssl_lib
import certifi
import sys
import readline
import pprint
from threading import Timer

_my_user_id = 'U2VMD4VD3'
_my_channel_id = 'DLVS4DN22'


def get_formatted_msg(channel, text):
    DIVIDER_BLOCK = {"type": "divider"}
    return {
        "channel" : channel,
        "username" : "friend_computer",
        "icon_emoji" : ":minidisc:",
        "blocks": [
            {"type": "section", "text": {"type": "mrkdwn", "text": text}}
        ]
    }

def send_msg(client, text):
    message = get_formatted_msg(_my_channel_id, text)
    #print(message)
    response = client.chat_postMessage(**message)
    assert response["ok"]

def passFnc():
    pass
    

def getResp():
    response = client.conversations_history(channel=_my_channel_id, limit=10)
    assert response['ok']
    for resp in response['messages']:
        if 'subtype' in resp and resp['subtype'] == 'bot_message':
            continue
        else:
            pp.pprint(resp)

if __name__ == "__main__":
    pp = pprint.PrettyPrinter(indent=2)
    ssl_context = ssl_lib.create_default_context(cafile=certifi.where())
    slack_token = os.environ["SLACK_BOT_TOKEN"]

    client = slack.WebClient(token=slack_token)

    tmr = Timer(10, getResp)
    
    stdin = os.fdopen(os.dup(sys.stdin.fileno()),sys.stdin.mode)

    while(True):
        print("Enter/Paste your content. Double <Enter> to submit.")
        contents = []
        tmr.start()
        
        while True:
            line = input()
            if (len(contents)) > 0 and (contents[-1] == '') and (line == ''):
                contents.pop()
                break
            contents.append(line)

        if contents != []:
            
            msg = '\n'.join(contents)
        
            send_msg(client, msg)

        tmr.cancel()
            
       
