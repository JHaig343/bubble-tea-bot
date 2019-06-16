import os
import logging
import slack
import ssl as ssl_lib
import datetime
import certifi
from bot import BubbleTeaBot
bubble_tea_nags = {}
# Hardcoded bot object because I can't be arsed to look it up
bubbleteabot = None

BOT_ID = 'BKN55L36K' 

def mention_bubble_tea(web_client: slack.WebClient, user_id: str, channel: str):
    global bubbleteabot
    # respond with bubble tea reminder
    bubbleteabot = BubbleTeaBot(channel, user_id)

    # get payload
    message = bubbleteabot.get_message_payload()

    # Post response in Slack
    response = web_client.chat_postMessage(**message)
    # print(response)
    # Save timestamp (will be used in later bot updates)
    bubbleteabot.timestamp = response["ts"]

    # Store message in bubble_tea_nags
    if channel not in bubble_tea_nags:
        bubble_tea_nags[channel] = {}
    bubble_tea_nags[channel][user_id] = bubbleteabot

# =======BubbleTea Mention Event======
# When user mentions "bubble", "tea" or "bubble tea" relentlessly remind them that Bubble Tea day exists
# TODO: linked to team_join for now, will update to respond to messages
@slack.RTMClient.run_on(event="message")
def bubble_tea_message(**payload):
    print(payload["data"])
    """Send a Bubble Tea reminder message whenever someone says absolutely anything """
    data = payload["data"]

    web_client = payload["web_client"]
    channel_id = data.get("channel")
    user_id = data.get("user")
    text = data.get("text")

    # TODO: check that the day is wednesday(2) before posting any responses
    if datetime.datetime.today().weekday() == 6 and user_id:
        # print("Oh look, its bubble tea day today!")
        # Mention the user, then reply with message
        # add a 'thread_ts' field with 'ts' value to send the message as reply to their message
        if "bubble" in text or "bubble" in text.lower() or "tea" in text or "tea" in text.lower():
            web_client.chat_postMessage(
                username="bubbleteabot",
                icon_emoji=":robot_face:",
                timestamp="",
                channel=channel_id,
                text=f"Hi <@{user_id}>!",
            )
            return mention_bubble_tea(web_client, user_id, channel_id)
    
# ==========Bubble Tea Msg Liked Event=======
# Reply that a user is going when the bot message is +1ed
@slack.RTMClient.run_on(event="reaction_added")
def mark_responders(**payload):
    print(payload["data"])
    """Mark anyone who thumbsups(+1s) the message as going"""
    data = payload["data"]
    web_client = payload["web_client"]
    reaction = data.get("reaction")
    user_id = data.get("user")
    item_user = data.get("item_user")
    item = data.get("item")
    channel_id = item.get("channel")
    thread_ts = item.get("ts")

    if reaction == "+1" and bubbleteabot.timestamp == thread_ts:
        web_client.chat_postMessage(
            username="bubbleteabot",
            icon_emoji=":robot_face:",
            timestamp="",
            channel=channel_id,
            text=f"<@{user_id}> is going to Bubble Tea Day!"
        )


if __name__ == "__main__":
    ssl_context = ssl_lib.create_default_context(cafile=certifi.where())
    slack_token = os.environ["SLACK_BOT_TOKEN"]
    rtm_client = slack.RTMClient(token=slack_token, ssl=ssl_context)
    rtm_client.start()