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
def myDel(message) :
    MOLi_list = open('MOLi_list.txt', mode = 'r+', encoding = 'utf8')
    allList = MOLi_list.readlines()
    MOLi_list.seek(0)
    for i in allList :
        if i.strip() != message :
            MOLi_list.write(i)
    MOLi_list.truncate()
    MOLi_list.close()

def myWrite(message) :
    MOLi_list = open('MOLi_list.txt', mode = 'a+', encoding = 'utf8')
    MOLi_list.write('\n' + message.replace('MOLi_new', '').replace(' ', ''))
    MOLi_list.close()


def myRead() :
    MOLi_list = open('MOLi_list.txt', mode = 'r', encoding = 'utf8')
    allList = MOLi_list.readlines()
    message = ''
    for i in allList :
        message = message + i
    MOLi_list.close()
    return message

def main():
    # Create the client and connect
    client = TelegramClient(username, api_id, api_hash, update_workers=1, spawn_read_thread=False)
    client.start(phone)
    
    @client.on(events.NewMessage(incoming=True))
    def _(event):
        if event.is_private :
            # print(time.asctime(), '-', event.message)  # optionally log time and message
            time.sleep(1)  # pause for 1 second to rate-limit automatic replies
            # print(event)
            print('Receive message from:', event.message.from_id)
            print('Message:', event.message.message)
            if event.message.message == 'MOLi_list' :
                event.reply('Here it is')
                client.send_message(event.message.from_id, myRead())
            if 'MOLi_new' in event.message.message :
                if event.message.message.replace('MOLi_new', '').replace(' ', '') not in myRead() :
                    myWrite(event.message.message)
                    event.reply('done')
                else :
                    event.reply('It\'s already in the list !')
            if 'MOLi_del' in event.message.message :
                if event.message.message.replace('MOLi_del', '').replace(' ', '') in myRead() :
                    myDel(event.message.message.replace('MOLi_del', '').replace(' ', ''))
                    event.reply('done')
                else :
                    event.reply('It\'s not in the list !')

    print(time.asctime(), '-', 'MOLi List Started...')
    client.idle()
    client.disconnect()
    print(time.asctime(), '-', 'Stopped!')

if __name__ == '__main__':
    main()