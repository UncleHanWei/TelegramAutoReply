import time
from telethon import TelegramClient, events
import random

# sample API_ID from https://github.com/telegramdesktop/tdesktop/blob/f98fdeab3fb2ba6f55daf8481595f879729d1b84/Telegram/SourceFiles/config.h#L220
# or use your own
myFile = open('account.txt')
lines = myFile.readlines()
api_id = int(lines[0])
api_hash = lines[1].strip()

# fill in your own details here
phone = lines[2].strip()
username = lines[3].strip()
# password = 'YOUR_PASSWORD'  # if you have two-step verification enabled

# content of the automatic reply
receivedFile = open('received.txt', encoding='utf8')
messageFile = open('message.txt', encoding='utf8')
eatWhatFile = open('eatWhat.txt', encoding='utf8')
received = receivedFile.readlines()
message = messageFile.readlines()

for i in range(len(received)) :
    received[i] = received[i].strip()
    message[i] = message[i].strip()

eatWhat = eatWhatFile.readlines()
for i in range(len(eatWhat)) :
    eatWhat[i] = eatWhat[i].strip()

def main():
    # Create the client and connect
    client = TelegramClient(username, api_id, api_hash, update_workers=1, spawn_read_thread=False)
    client.start(phone)

    @client.on(events.NewMessage(incoming=True))
    def _(event):
        if event.is_private :
            # print(time.asctime(), '-', event.message)  # optionally log time and message
            # time.sleep(1)  # pause for 1 second to rate-limit automatic replies
            print('Receive message from:', event.message.from_id)
            event.message.message = ''.join(e for e in event.message.message if e.isalnum())
            print(event)
            for i in received :
                if i in event.message.message :
                    event.reply(message[received.index(i)])
        # print(event)
        if '幫我' in event.message.message and ('吃什麼' in event.message.message 
        or '吃啥' in event.message.message 
        or '吃甚麼' in event.message.message) :
            print('有人問吃啥')
            event.reply(eatWhat[random.randint(0, len(eatWhat))])

    print(time.asctime(), '-', 'Auto-replying...')
    client.idle()
    client.disconnect()
    print(time.asctime(), '-', 'Stopped!')

if __name__ == '__main__':
    main()