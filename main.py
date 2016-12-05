import re
import time
import html
from slackclient import SlackClient
from constant import *
from utils.managers import *

# # Turn off bytecode generation
# sys.dont_write_bytecode = True


# instantiate slack-client
slack_client = SlackClient(SLACK_BOT_TOKEN)


def process_department_list_command(channel):
    departments = get_department_list()
    response = "Here is the list of departments: \n```{}```".format("\n".join(departments))
    slack_client.api_call("chat.postMessage", channel=channel, text=response, as_user=True)


def process_upcoming_birthday_command(command, channel, user):
    pass


def process_team_list_command(channel):
    teams = get_team_list()
    response = "Here is the list of teams: \n```{}```".format("\n".join(teams))
    slack_client.api_call("chat.postMessage", channel=channel, text=response, as_user=True)


def _get_member_list(member_queryset, user, group_name):
    name_list = []
    member_names = member_queryset.values_list('first_name', 'last_name')
    for name in member_names:
        name_list.append(' '.join(name))

    response = "{user_name}, here is the list of employees in \"*{team_name}*\" team. \n ```{team_list}```".format(
        user_name=user,
        team_name=group_name,
        team_list="\n".join(name_list)
    )
    return response


def process_team_info_command(command, channel, user):
    team_name = command.replace(COMMAND_TEAM_MEMBERS, '').strip().title()
    team_name = re.sub("[?.]", "", team_name)

    team_members = get_team_info(team_name)

    if team_members.exists():
        response = _get_member_list(team_members, user, team_name)
    else:
        dept_members = get_dept_info(team_name)
        if dept_members.exists():
            response = _get_member_list(dept_members, user, team_name)
        else:
            response = "Sorry {user_name}, there is no team by name: \"{team_name}\"".format(
                user_name=user,
                team_name=team_name
            )
    slack_client.api_call("chat.postMessage", channel=channel, text=response, as_user=True)


def process_employee_info_command(command, channel, user):

    employee_name = command.replace(COMMAND_EMPLOYEE, '').strip().title()
    employee_name = re.sub("[?.]", "", employee_name)
    employees = get_employee_info(employee_name)
    if employees.exists():
        employee_list = []
        for emp in employees:
            info = "```Name: {full_name} \t Team: {team}\t Manager: {manager}```".format(
                full_name=(emp.first_name + " " + emp.last_name),
                team=emp.team.name if emp.team else "No Team",
                manager=(emp.manager.first_name + " " + emp.manager.last_name) if emp.manager else "No Manager"
            )
            employee_list.append({
                'avatar': emp.avatar_url,
                'info': info
            })

        if len(employee_list) > 1:
            response = "There are more than one \"*{}*\", here is their information.".format(employee_name)
        else:
            response = "Here is the information about \"*{}*\".".format(employee_name)

        slack_client.api_call("chat.postMessage", channel=channel, text=response, as_user=True)
        for emp in employee_list:
            slack_client.api_call("chat.postMessage", channel=channel, text=emp['avatar'], as_user=True)
            slack_client.api_call("chat.postMessage", channel=channel, text=emp['info'], as_user=True)
    else:
        response = "Sorry there is no employee by name \"{}\".".format(employee_name)
        slack_client.api_call("chat.postMessage", channel=channel, text=response, as_user=True)


def process_help_command(channel, user):
    response = """
            Howdy {user_name}, I am happy to help :-).
            I have very limited knowledge of english but I understand these commands:\n {help_text}""".format(
        user_name=user, help_text=HELP_TEXT
    )
    slack_client.api_call("chat.postMessage", channel=channel, text=response, as_user=True)


def handle_command(command, channel, user):
    """
        Receives commands directed at the bot and determines if they
        are valid commands. If so, then acts on the commands. If not,
        returns back what it needs for clarification.
    """

    if command.startswith(COMMAND_HELP):
        process_help_command(channel, user)
    elif command.startswith(COMMAND_TEAM_MEMBERS):
        process_team_info_command(command, channel, user)
    elif command.startswith(COMMAND_EMPLOYEE):
        process_employee_info_command(command, channel, user)
    elif command.startswith(COMMAND_ALL_TEAMS):
        process_team_list_command(channel)
    elif command.startswith(COMMAND_ALL_DEPARTMENTS):
        process_department_list_command(channel)
    elif command.startswith(COMMAND_LEAVE_CHANNEL):
        response = "ok bye bye!"
        slack_client.api_call("channels.leave", channel=channel)
    elif command.startswith(COMMAND_UPCOMING_BIRTHDAY):
        pass
    else:
        response = """
            Sorry {user_name}, I am not sure what do you mean. I can only understand following commands:\n{help_text}
        """.format(user_name=user_name, help_text=HELP_TEXT)
        slack_client.api_call("chat.postMessage", channel=channel, text=response, as_user=True)


def parse_slack_output(slack_rtm_output):
    """
        The Slack Real Time Messaging API is an events firehose.
        this parsing function returns None unless a message is
        directed at the Bot, based on its ID.
    """
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and AT_BOT in output['text']:
                # return text after the @ mention, whitespace removed
                return output['text'].split(AT_BOT)[1].strip().lower(), \
                       output['channel'], output['user']

    return None, None, None


if __name__ == "__main__":
    if slack_client.rtm_connect():
        print("StarterBot connected and running!")
        while True:
            command, channel, user = parse_slack_output(slack_client.rtm_read())
            if command and channel:
                command = html.unescape(command)
                user_name = "<@{user}>".format(user=user)
                print(command)
                handle_command(command, channel, user_name)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")


