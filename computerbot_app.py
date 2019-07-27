import os
import logging
import slack
import ssl as ssl_lib
import certifi
from computerbot import ComputerBot

# For simplicity we'll store our app data in-memory with the following data structure.
# messages_sent = {"channel": {"user_id": ComputerBot}}
messages_sent = {}
_my_user_id = 'U2VMD4VD3'
_my_channel_id = 'DLVS4DN22'


def start_computerbot(web_client: slack.WebClient, user_id: str, channel: str):
    # Create a new onboarding tutorial.
    computerbot = ComputerBot(channel)

    # Get the onboarding message payload
    text = "```\nThis is a test message\n```"
    message = computerbot.get_message_payload(text)

    # Post the onboarding message in Slack
    response = web_client.chat_postMessage(**message)

    # Capture the timestamp of the message we've just posted so
    # we can use it to update the message after a user
    # has completed an onboarding task.
    computerbot.timestamp = response["ts"]

    # Store the message sent in messages_sent
    if channel not in messages_sent:
        messages_sent[channel] = {}
    messages_sent[channel][user_id] = computerbot


## # ================ Team Join Event =============== #
## # When the user first joins a team, the type of the event will be 'team_join'.
## # Here we'll link the onboarding_message callback to the 'team_join' event.
## @slack.RTMClient.run_on(event="team_join")
## def onboarding_message(**payload):
##     """Create and send an onboarding welcome message to new users. Save the
##     time stamp of this message so we can update this message in the future.
##     """
##     # Get WebClient so you can communicate back to Slack.
##     web_client = payload["web_client"]
## 
##     # Get the id of the Slack user associated with the incoming event
##     user_id = payload["data"]["user"]["id"]
## 
##     # Open a DM with the new user.
##     response = web_client.im_open(user_id)
##     channel = response["channel"]["id"]
## 
##     # Post the onboarding message.
##     start_computerbot(web_client, user_id, channel)


## # ============= Reaction Added Events ============= #
## # When a users adds an emoji reaction to the onboarding message,
## # the type of the event will be 'reaction_added'.
## # Here we'll link the update_emoji callback to the 'reaction_added' event.
## @slack.RTMClient.run_on(event="reaction_added")
## def update_emoji(**payload):
##     """Update the onboarding welcome message after receiving a "reaction_added"
##     event from Slack. Update timestamp for welcome message as well.
##     """
##     data = payload["data"]
##     web_client = payload["web_client"]
##     channel_id = data["item"]["channel"]
##     user_id = data["user"]
## 
##     if channel_id not in messages_sent:
##         return
## 
##     # Get the original tutorial sent.
##     computerbot = messages_sent[channel_id][user_id]
## 
##     # Mark the reaction task as completed.
##     computerbot.reaction_task_completed = True
## 
##     # Get the new message payload
##     message = computerbot.get_message_payload()
## 
##     # Post the updated message in Slack
##     updated_message = web_client.chat_update(**message)
## 
##     # Update the timestamp saved on the onboarding tutorial object
##     computerbot.timestamp = updated_message["ts"]
## 
## 
## # =============== Pin Added Events ================ #
## # When a users pins a message the type of the event will be 'pin_added'.
## # Here we'll link the update_pin callback to the 'reaction_added' event.
## @slack.RTMClient.run_on(event="pin_added")
## def update_pin(**payload):
##     """Update the onboarding welcome message after receiving a "pin_added"
##     event from Slack. Update timestamp for welcome message as well.
##     """
##     data = payload["data"]
##     web_client = payload["web_client"]
##     channel_id = data["channel_id"]
##     user_id = data["user"]
## 
##     # Get the original tutorial sent.
##     computerbot = messages_sent[channel_id][user_id]
## 
##     # Mark the pin task as completed.
##     computerbot.pin_task_completed = True
## 
##     # Get the new message payload
##     message = computerbot.get_message_payload()
## 
##     # Post the updated message in Slack
##     updated_message = web_client.chat_update(**message)
## 
##     # Update the timestamp saved on the onboarding tutorial object
##     computerbot.timestamp = updated_message["ts"]
## 

# ============== Message Events ============= #
# When a user sends a DM, the event type will be 'message'.
# Here we'll link the message callback to the 'message' event.
@slack.RTMClient.run_on(event="message")
def message(**payload):
    """Display the onboarding welcome message after receiving a message
    that contains "start".
    """
    data = payload["data"]
    web_client = payload["web_client"]
    channel_id = data.get("channel")
    user_id = data.get("user")
    text = data.get("text")

    user_list = web_client.users_list()['members']
    users = [user["name"] for user in user_list if user["id"] == user_id]
    
    print(users)

    if text and text.lower() == "start":
        return start_computerbot(web_client, user_id, channel_id)
    
    elif (channel_id in messages_sent) and (user_id in messages_sent[channel_id]):
        # Get the original bot.
        computerbot = messages_sent[_my_channel_id][_my_user_id]
        message = computerbot.get_message_payload(f"<@{user_id}>! said:\n\t{text}")
        # Post the message in Slack
        response = web_client.chat_postMessage(**message)


if __name__ == "__main__":
    #logger = logging.getLogger()
    #logger.setLevel(logging.DEBUG)
    #logger.addHandler(logging.StreamHandler())
    ssl_context = ssl_lib.create_default_context(cafile=certifi.where())
    slack_token = os.environ["SLACK_BOT_TOKEN"]
    rtm_client = slack.RTMClient(token=slack_token, ssl=ssl_context)
    rtm_client.start()
