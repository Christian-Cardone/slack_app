import json
import slack


def get_client():
    with open("./tokens/keys.json") as file:
        bot_keys = json.load(file)

    client = slack.WebClient(token=bot_keys['API_TOKEN'])
    return client


def send_message(channel, message, client):
    response = client.chat_postMessage(
        channel=channel,
        text=message)
    assert response["ok"]


def job(u_channel, u_message):
    send_message(channel=u_channel, message=u_message, client=get_client())




# import requests
# import json
#
# url = "https://slack.com/api/chat.postMessage"
# headers = {
#   "Content-Type": "application/json",
#   "Authorization": "Bearer {0}".format(bot_token)
# }
#
#
# def send_message(message_text):
#     message = {
#         "channel": "#bot-test",
#         "text": message_text
#     }
#     requests.post(url, headers=headers, data=json.dumps(message))
#
#
# send_message("morning")