import requests
import re
import time
from SlackAnalytics import SlackAnalytics

# Hubspot, sduane
API_TOKEN = '' #token here
# #ecopg-backroom
CHANNEL_ID = 'C3TU09YKW' 
EMOJI_REGEX = "\:[^\s]+\:"
DATE_EPOCH = 1527519380

def main():
    analytics = SlackAnalytics()

    fetchAndCountHistoryUntil(DATE_EPOCH, analytics)

    analytics.report()

def fetchAndCountHistoryUntil(dateEpoch, analytics):
    n = 0
    latest = int(time.time())
    hasMore = True
    while hasMore is True:
        print(f'Checking page {n} latest {latest}')
        page = fetchHistory(latest, dateEpoch)
        countPage(page, analytics)
        hasMore = page['has_more']
        n = n + 1
        if hasMore is True:
            latest = determineOldestMessage(page)

def determineOldestMessage(page):
    return page['messages'][-1]["ts"]

def fetchHistory(latest, oldest):
    #url = f'https://slack.com/api/groups.history?count=1000&channel={CHANNEL_ID}&token={API_TOKEN}&latest={latest}&oldest={oldest}'
    url = f'https://slack.com/api/channels.history?count=1000&channel={CHANNEL_ID}&token={API_TOKEN}&latest={latest}&oldest={oldest}'
    response = requests.post(url)
    json = response.json()
    if (json['ok'] is False):
        print(f'Bad request {json}')
        return {}
    return json

def countPage(page, analytics):
    # With the page in hand, we can start generating histories
    # We need to hold a map of what we want....
    for message in page['messages']:
        text = message['text']
        countTextEmojis(text, analytics)
        countReactionEmojis(message, analytics)

def countTextEmojis(text, analytics):
    emojis = re.findall(EMOJI_REGEX, text)
    for emoji in emojis:
        strippedEmoji = emoji.strip(':')
        analytics.incrementEmojiPostUsage(strippedEmoji, 1)

def countReactionEmojis(message, analytics):
    if 'reactions' not in message:
        return

    for reaction in message['reactions']:
        analytics.incrementEmojiReactionUsage(reaction['name'], reaction['count'])

main()
