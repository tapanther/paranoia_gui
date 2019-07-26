class ComputerBot:
    WELCOME_BLOCK = {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": (
                "Good day Troubleshooter!\n\n"
            ),
        },
    }  
    DIVIDER_BLOCK = {"type": "divider"}
    def __init__(self, channel):
        self.channel = channel
        self.username = "friend_computer"
        self.icon_emoji = ":minidisc:"
        self.timestamp = ""

    def get_message_payload(self):
        return {
            "ts": self.timestamp,
            "channel": self.channel,
            "username": self.username,
            "icon_emoji": self.icon_emoji,
            "blocks": [
                self.WELCOME_BLOCK,
                self.DIVIDER_BLOCK,
                *self._get_msg_block(),
            ],
        }

    def _get_msg_block(self):
        text = (
            "This is a test message."
            )
        return self._get_msg_block_content(text)

    @staticmethod
    def _get_msg_block_content(text):
        return [
            {"type": "section", "text": {"type": "mrkdwn", "text": text}}
        ]
    
