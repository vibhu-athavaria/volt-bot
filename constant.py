import os


SLACK_BOT_TOKEN = os.environ.get("SLACK_TOKEN")
BOT_ID = "U3ASS1SCQ"
AT_BOT = "<@{bot_id}>".format(bot_id=BOT_ID)

# Bot commands
COMMAND_HELP = "help"
COMMAND_EMPLOYEE = "who is "
COMMAND_TEAM_MEMBERS = "who is in "
COMMAND_ALL_TEAMS = "list all teams"
COMMAND_ALL_DEPARTMENTS = "list all departments"
COMMAND_UPCOMING_BIRTHDAY = "list upcoming birthdays"
COMMAND_LEAVE_CHANNEL = "leave this channel"

HELP_TEXT = """
    `who is` *John Doe*? \n
    `list all teams`. \n
    `list all departments`. \n
    `who is on` <team_name>. \n
"""

READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
