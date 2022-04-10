import os
from slack import WebClient
from slack.errors import SlackApiError
from sqlite_utils import Database

db = Database("hipaabreach.db")
record = db.query("""SELECT * from breaches limit 1""")
settled = db.query("""SELECT * from breach_archive limit 1""")
ransom = db.query("""SELECT * from ransomware limit 1""")
#for row in record:
#  print(record)

client = WebClient()

slack_token = os.environ["SLACK_API_TOKEN"]
# print(slack_token)
client = WebClient(token=slack_token)

#try:
#  response = client.chat_postMessage(#
#    channel="slack-bots",
#    text="bot bot"
#  )

try:
  for row in record:
    response = client.chat_postMessage(
      channel="slack-bots",
      text=f"New breach reported by {row['Name of Covered Entity']} on {row['Breach Submission Date']} -- {row['Type of Breach']} affected {row['Individuals Affected']} people."
    )

    for row in settled:
        response = client.chat_postMessage(
        channel = "slack-bots",
        text=f"{row['Name of Covered Entity']} breach (reported {row['Breach Submission Date']}, {row['Individuals Affected']} people affected) resolved: \n> {row['Web Description']}"
        )

    for row in ransom:
        response = client.chat_postMessage(
        channel = "slack-bots",
        text=f":pirate_flag: Latest ransomware news! {row['Name of Covered Entity']}, {row['Individuals Affected']} people affected \npython > {row['Web Description']}"
        )


except SlackApiError as e:
  # You will get a SlackApiError if "ok" is False
  assert e.response["error"]
