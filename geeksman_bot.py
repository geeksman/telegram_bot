import requests
import datetime

ACCESS_TOKEN = '679326696:AAHZnAq5bLxLDnLrWBN-6vqFNPZk3g-kXBw'

class BotHandler:
  def __init__(self, token):
    self.token = token
    self.apiUrl = 'https://api.telegram.org/bot{}/'.format(token)

  def getUpdates(self, offset = None, timeout = 30):
    method = 'getUpdates'
    params = {'timeout': timeout, 'offset': offset}
    response = requests.get(self.apiUrl + method, params = params)
    return response.json()['result']

  def getLastUpdate(self):
    result = self.getUpdates()
    return result[-1] if len(result) > 0 else result[0]

  def sendMessage(self, chatId, message):
    method = 'sendMessage'
    params = {'chat_id': chatId, 'text': message}
    response = requests.post(self.apiUrl + method, data=params)

    return response


geekerBot = BotHandler(ACCESS_TOKEN)
greetingsType = ['hello', 'hi', 'hey', 'whta\'s up', 'howdy', 'yo']
now = datetime.datetime.now()


def main():
  newOffset = None
  today = now.day
  hour = now.hour

  while True:
      geekerBot.getUpdates(offset = newOffset)

      lastUpdate = geekerBot.getLastUpdate()

      lastUpdateId = lastUpdate['update_id']
      lastChatText = lastUpdate['message']['text']
      lastChatId = lastUpdate['message']['chat']['id']
      lastChatName = lastUpdate['message']['chat']['first_name']

      if lastChatText.lower() in greetingsType and today == now.day and 6 <= hour < 12:
          geekerBot.sendMessage(
              lastChatId, 'Good morning, {}'.format(lastChatName))
          today += 1

      elif lastChatText.lower() in greetingsType and today == now.day and 12 <= hour < 17:
          geekerBot.sendMessage(
              lastChatId, 'Good afternoon, {}'.format(lastChatName))
          today += 1

      elif lastChatText.lower() in greetingsType and today == now.day and 17 <= hour < 23:
          geekerBot.sendMessage(
              lastChatId, 'Good evening, {}'.format(lastChatName))
          today += 1

      newOffset = lastUpdateId + 1


if __name__ == '__main__':
  try:
    main()
  except KeyboardInterrupt:
    exit()