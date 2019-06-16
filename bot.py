class BubbleTeaBot(object):
    """Constructs the bubble tea response message when called """

    def __init__(self, channel, user_id):
        self.channel = channel
        self.username = "bubbleteabot"
        self.user_id = user_id
        self.icon_emoji = ":robot_face:"
        self.timestamp = ""

    MESSAGE_BLOCK = {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": (
                "I see you have mentioned 'bubble' or 'tea' in your response! I want to let you know that today is Bubble Tea day! Please :+1: this message if you are planning to participate! :tea:"
            ),
        }
    }

    DIVIDER_BLOCK = {
        "type": "divider"
    }

    POLL_BLOCK =  {
		"type": "section",
		"text": {
			"type": "mrkdwn",
			"text": "Yes, I would like to participate!"
		},
		"accessory": {
			"type": "button",
			"text": {
				"type": "plain_text",
				"text": "Vote"
			},
			"value": "LMAO"
		}
	}

    # return the Block-based message format
    def get_message_payload(self):
        # print("responding to username: " + self.username)
        return {
            "ts": self.timestamp,
            "channel": self.channel,
            "username": self.username,
            "user_id": self.user_id,
            "icon_emoji": self.icon_emoji,
            "blocks": [
                self.MESSAGE_BLOCK
                # self.POLL_BLOCK
            ],
        }