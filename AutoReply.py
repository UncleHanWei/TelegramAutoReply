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
received = ['太慢', '告你', '等', '嫩', '不行', '哈', '問']
message = ['快一點', '等著收傳票啦', '太慢了', '你才嫩', '你才不行', '笑屁', '不行']
eatWhat = ['學餐', '麥當勞', '小鼎', '黃切仔麵', '葉師傅', '夜市', '肯德基', '披薩',
    '八方', '華園', '悟饕', '永豆', '臺巴']

def main():
    # Create the client and connect
    client = TelegramClient(username, api_id, api_hash, update_workers=1, spawn_read_thread=False)
    client.start(phone)

    @client.on(events.NewMessage(incoming=True))
    def _(event):
        if event.is_private :
            # print(time.asctime(), '-', event.message)  # optionally log time and message
            time.sleep(1)  # pause for 1 second to rate-limit automatic replies
            print('Receive message from:', event.message.from_id)
            event.message.message = event.message.message.replace(' ', '')
            print(event)
            for i in received :
                if i in event.message.message :
                    event.reply(message[received.index(i)])
        # print(event)
        if '吃啥' in event.message.message or '吃什麼' in event.message.message :
            print('有人問吃啥')
            event.reply(eatWhat[random.randint(0, len(eatWhat))])

    print(time.asctime(), '-', 'Auto-replying...')
    client.idle()
    client.disconnect()
    print(time.asctime(), '-', 'Stopped!')

if __name__ == '__main__':
    main()