import httpx
import asyncio
import json
import time
import sys
import os
import aioconsole
from pydantic import ValidationError
from config import BOT_API_TOKEN, MAIN_CHANNEL_CHAT_ID
from model import TelegramgetMeResponse, TelegramMessage, TelegramPhoto, TelegramPoll, TelegramDocument, TelegramAudio, TelegramVideo
from tele import sendPhoto, sendMessage, sendDocument, sendPoll, getMe, sendAudio, sendVideo



print()
print('###################################################')
print('\33[95mTelegram System\33[0m')
print('\33[95mCopyright by Blegping\33[0m')
print('\33[95mMade by Muhammad Nizamuddin Aulia\33[0m')
print('###################################################')
print()


# TELEGRAM
URL = 'https://api.telegram.org/bot' + str(BOT_API_TOKEN)

# MAIN CHANNEL
# Main channel is used for controlling bot from Telegram such as restarting
main_channel_chat_id = MAIN_CHANNEL_CHAT_ID
'''Add your telegram bot into your channel. Do not forget to make your bot as admin that has access to read and post messages'''


# TELEGRAM UPDATES READER
async def getUpdates(offset):
    async with httpx.AsyncClient(http2=True) as tele:
        url = f"{URL}/getUpdates?offset={offset}"
        #url = URL + "/getUpdates?offset={}".format(offset)
        r = await tele.post(url)
        return r.json()


async def getUpdateId(updates):
    num_updates = len(updates['result'])
    last_update = num_updates - 1
    update_id = updates['result'][last_update]['update_id']
    return update_id


async def updateidandoffset():
    try:
        with open('update_id.txt', encoding="utf8") as u:
            update_id = str(u.read())
    except FileNotFoundError:
        update_id = '0'
    try:
        with open('offset.txt', encoding="utf8") as o:
            offset = str(o.read())
    except FileNotFoundError:
        offset = 0
    return update_id, offset


async def getpollanswer(pollid):
    while True:
        try:
            answer = answered
            return answer
        except NameError:
            await asyncio.sleep(1)
            try:
                with open(str(pollid) + '_answered.txt', encoding="utf8") as op:
                    answered = str(op.read())
                os.remove(str(pollid) + '_answered.txt')
            except FileNotFoundError:
                pass


async def welcome(chat_id):
    if not os.path.exists('Data/'+str(chat_id)):
        os.makedirs('Data/'+str(chat_id))
    await sendMessage(BOT_API_TOKEN=BOT_API_TOKEN, message=TelegramMessage(chat_id=chat_id, text="<b>Welcome to YG Information System</b>", parse_mode="HTML"))


async def restart(chat_id):
    choice = await getpollanswer(await sendPoll(BOT_API_TOKEN=BOT_API_TOKEN, poll=TelegramPoll(chat_id=chat_id, question="Are you sure?", options=json.dumps(["Yes", "No"]))))
    if choice == 'Yes':
        await sendMessage(BOT_API_TOKEN=BOT_API_TOKEN, message=TelegramMessage(chat_id=chat_id, text="Restarting bot.."))
        os.execv(sys.executable, ['python3'] + sys.argv)
    else:
        pass


async def texthandler(chat_id, text):
    try:
        if text == '/start':
            asyncio.ensure_future(welcome(chat_id))
        elif text == '/restart':
            asyncio.ensure_future(restart(chat_id))
        elif text == '/chatid':
            asyncio.ensure_future(sendMessage(BOT_API_TOKEN=BOT_API_TOKEN, message=TelegramMessage(chat_id=chat_id, text=chat_id)))
        elif text == '/sendmessage':
            asyncio.ensure_future(sendMessage(BOT_API_TOKEN=BOT_API_TOKEN, message=TelegramMessage(chat_id=chat_id, text="This is message")))
        elif text == '/sendphoto':
            asyncio.ensure_future(sendPhoto(BOT_API_TOKEN=BOT_API_TOKEN, photo=TelegramPhoto(chat_id=chat_id, photo='example-resources/bear.png', caption="This is photocaption"), is_local=True))
        elif text == '/senddocument':
            asyncio.ensure_future(sendDocument(BOT_API_TOKEN=BOT_API_TOKEN, document=TelegramDocument(chat_id=chat_id, document='example-resources/bear.png'), is_local=True))
        elif text == '/sendaudio':
            asyncio.ensure_future(sendAudio(BOT_API_TOKEN=BOT_API_TOKEN, audio=TelegramAudio(chat_id=chat_id, audio='example-resources/bensound-cute.mp3', caption="This is audio caption"), is_local=True))
        elif text == '/sendvideo':
            asyncio.ensure_future(sendVideo(BOT_API_TOKEN=BOT_API_TOKEN, video=TelegramVideo(chat_id=chat_id, video='example-resources/tailwind.mp4', caption="This is video caption"), is_local=True))
        else:
            pass
    except (ValueError, IndexError, AssertionError, KeyError):
        await aioconsole.aprint('TEXT HANDLING ERROR:', text)
        exc_type, exc_obj, exc_tb = sys.exc_info()
        await aioconsole.aprint(exc_type, exc_tb.tb_lineno)


async def pollanswerhandler(poll_id, answer):
    if os.path.exists('Poll/'+str(poll_id) + '_answer.txt'):
        with open('Poll/'+str(poll_id) + '_answered.txt', 'w') as sa:
            sa.write(str(answer))
        os.remove('Poll/'+str(poll_id) + '_answer.txt')
    else:
        await aioconsole.aprint('Poll is already answered:', poll_id)


async def main():
    await aioconsole.aprint()
    await aioconsole.aprint('\33[95mTelegram System STARTED\33[0m')
    try:
        bot = TelegramgetMeResponse.parse_obj(await getMe(BOT_API_TOKEN))
        await aioconsole.aprint("BOT INFORMATION")
        await aioconsole.aprint(f"ID      : {bot.result.id}")
        await aioconsole.aprint(f"Name    : {bot.result.first_name}")
        await aioconsole.aprint(f"Username: {bot.result.username}")
    except ValidationError:
        await aioconsole.aprint("Bot Configuration Error")
        sys.exit()
    await aioconsole.aprint()
    await sendMessage(BOT_API_TOKEN=BOT_API_TOKEN, message=TelegramMessage(chat_id=MAIN_CHANNEL_CHAT_ID, text=f"Telegram System ON\n{time.ctime(time.time())}"))
    # INITIAL CONDITIONS
    latest_update_id, offset = await updateidandoffset()
    # TELEGRAM UPDATES LOOP
    while True:
        try:
            while True:
                try:
                    updates = await getUpdates(offset)
                    offset = await getUpdateId(updates)
                    i = len(updates['result']) - 1
                    update_id = updates['result'][i]['update_id']
                    break
                except (KeyError, IndexError):
                    await aioconsole.aprint(updates)
                    await asyncio.sleep(1)
            # Only process new updates
            if update_id != latest_update_id:
                latest_update_id = update_id
                with open("update_id.txt", 'w') as u:
                    u.write(str(latest_update_id))
                with open("offset.txt", 'w') as o:
                    o.write(str(offset))
                try:
                    # MESSAGE
                    if updates['result'][i]['message']:
                        chat_id = updates['result'][i]['message']['chat']['id']
                        chat_type = updates['result'][i]['message']['chat']['type']
                        if not os.path.exists('Data/' + str(chat_id)):
                            os.makedirs('Data/' + str(chat_id))
                        try:
                            # TEXT
                            if updates['result'][i]['message']['text']:
                                text = updates['result'][i]['message']['text']
                                await aioconsole.aprint('Text', chat_id, chat_type, text)
                                asyncio.ensure_future(texthandler(chat_id, text))
                        except KeyError:
                            try:
                                # DOCUMENT
                                if updates['result'][i]['message']['document']:
                                    file_date = updates['result'][i]['message']['date']
                                    file_id = updates['result'][i]['message']['document']['file_id']
                                    mime_type = updates['result'][i]['message']['document']['mime_type']
                                    file_name = updates['result'][i]['message']['document']['file_name']
                                    try:
                                        # W/ CAPTION
                                        caption = updates['result'][i]['message']['caption']
                                        await aioconsole.aprint('Document', file_name, mime_type, file_id, caption)
                                    except KeyError:
                                        # W/O CAPTION
                                        await aioconsole.aprint('Document', file_name,mime_type, file_id)
                            except KeyError:
                                try:
                                    # POLL
                                    if updates['result'][i]['message']['poll']:
                                        poll_id = updates['result'][i]['message']['poll']['id']
                                        question = updates['result'][i]['message']['poll']['question']
                                        options = updates['result'][i]['message']['poll']['options']
                                        await aioconsole.aprint('Poll', poll_id, question, options)
                                except KeyError:
                                    try:
                                        # PHOTO
                                        if updates['result'][i]['message']['photo']:
                                            files = updates['result'][i]['message']['photo'][len(updates['result'][i]['message']['photo'])-1]
                                            file_id = files['file_id']
                                            width = files['width']
                                            height = files['height']
                                            try:
                                                # W/ CAPTION
                                                caption = updates['result'][i]['message']['caption']
                                                await aioconsole.aprint('Photo', file_id, width, height, caption)
                                            except KeyError:
                                                # W/O CAPTION
                                                await aioconsole.aprint('Photo', file_id, width, height)
                                    except KeyError:
                                        try:
                                            # AUDIO
                                            if updates['result'][i]['message']['audio']:
                                                file_name = updates['result'][i]['message']['audio']['file_name']
                                                mime_type = updates['result'][i]['message']['audio']['mime_type']
                                                title = updates['result'][i]['message']['audio']['title']
                                                file_id = updates['result'][i]['message']['audio']['file_id']
                                                try:
                                                    # W/ CAPTION
                                                    caption = updates['result'][i]['message']['caption']
                                                    await aioconsole.aprint('Audio', file_name, mime_type, title, file_id, caption)
                                                except KeyError:
                                                    # W/O CAPTION
                                                    await aioconsole.aprint('Audio', file_name, mime_type, title,file_id)
                                        except KeyError:
                                            try:
                                                # LOCATION
                                                if updates['result'][i]['message']['location']:
                                                    latitude = updates['result'][i]['message']['location']['latitude']
                                                    longitude = updates['result'][i]['message']['location']['longitude']
                                                    await aioconsole.aprint('Location', latitude, longitude)
                                            except KeyError:
                                                try:
                                                    # CONTACT
                                                    if updates['result'][i]['message']['contact']:
                                                        phone_number = updates['result'][i]['message']['contact']['phone_number']
                                                        first_name = updates['result'][i]['message']['contact']['first_name']
                                                        await aioconsole.aprint('Contact', phone_number, first_name)
                                                except KeyError:
                                                    await aioconsole.aprint('Unknown message type')
                                                    await aioconsole.aprint(updates)
                except KeyError:
                    try:
                        # CHANNEL POST
                        if updates['result'][i]['channel_post']:
                            chat_id = updates['result'][i]['channel_post']['chat']['id']
                            chat_type = updates['result'][i]['channel_post']['chat']['type']
                            try:
                                # TEXT
                                if updates['result'][i]['channel_post']['text']:
                                    text = updates['result'][i]['channel_post']['text']
                                    await aioconsole.aprint('Text', chat_id, chat_type, text)
                                    asyncio.ensure_future(texthandler(chat_id, text))
                            except KeyError:
                                try:
                                    # DOCUMENT
                                    if updates['result'][i]['channel_post']['document']:
                                        file_date = updates['result'][i]['channel_post']['date']
                                        file_id = updates['result'][i]['channel_post']['document']['file_id']
                                        mime_type = updates['result'][i]['channel_post']['document']['mime_type']
                                        file_name = updates['result'][i]['channel_post']['document']['file_name']
                                        try:
                                            # W/ CAPTION
                                            caption = updates['result'][i]['channel_post']['caption']
                                            await aioconsole.aprint('File', file_name, mime_type, file_date, caption)
                                        except KeyError:
                                            # W/O CAPTION
                                            await aioconsole.aprint('File', file_name,
                                                                    mime_type, file_date)
                                except KeyError:
                                    try:
                                        # POLL
                                        if updates['result'][i]['channel_post']['poll']:
                                            poll_id = updates['result'][i]['channel_post']['poll']['id']
                                            question = updates['result'][i]['channel_post']['poll']['question']
                                            options = updates['result'][i]['channel_post']['poll']['options']
                                            await aioconsole.aprint('Poll', poll_id, question, options)
                                    except KeyError:
                                        try:
                                            # PHOTO
                                            if updates['result'][i]['channel_post']['photo']:
                                                files = updates['result'][i]['channel_post']['photo'][
                                                    len(updates['result'][i]['channel_post']['photo']) - 1]
                                                file_id = files['file_id']
                                                width = files['width']
                                                height = files['height']
                                                try:
                                                    # W/ CAPTION
                                                    caption = updates['result'][i]['channel_post']['caption']
                                                    await aioconsole.aprint('Photo', file_id, width, height, caption)
                                                except KeyError:
                                                    # W/O CAPTION
                                                    await aioconsole.aprint('Photo', file_id, width, height)
                                        except KeyError:
                                            try:
                                                # AUDIO
                                                if updates['result'][i]['channel_post']['audio']:
                                                    file_name = updates['result'][i]['channel_post']['audio']['file_name']
                                                    mime_type = updates['result'][i]['channel_post']['audio']['mime_type']
                                                    title = updates['result'][i]['channel_post']['audio']['title']
                                                    file_id = updates['result'][i]['channel_post']['audio']['file_id']
                                                    try:
                                                        # W/ CAPTION
                                                        caption = updates['result'][i]['channel_post']['caption']
                                                        await aioconsole.aprint('Audio', file_name, mime_type, title,
                                                                                file_id, caption)
                                                    except KeyError:
                                                        # W/O CAPTION
                                                        await aioconsole.aprint('Audio', file_name, mime_type, title,
                                                                                file_id)
                                            except KeyError:
                                                try:
                                                    if updates['result'][i]['channel_post']['location']:
                                                        latitude = updates['result'][i]['channel_post']['location'][
                                                            'latitude']
                                                        longitude = updates['result'][i]['channel_post']['location'][
                                                            'longitude']
                                                        await aioconsole.aprint('Location', latitude, longitude)
                                                except KeyError:
                                                    try:
                                                        if updates['result'][i]['channel_post']['contact']:
                                                            phone_number = updates['result'][i]['channel_post']['contact'][
                                                                'phone_number']
                                                            first_name = updates['result'][i]['channel_post']['contact'][
                                                                'first_name']
                                                            await aioconsole.aprint('Contact', phone_number, first_name)
                                                    except KeyError:
                                                        await aioconsole.aprint('Unknown message type')
                                                        await aioconsole.aprint(updates)
                    except KeyError:
                        try:
                            # POLL ANSWER
                            if updates['result'][i]['poll']['id']:
                                poll_id = updates['result'][i]['poll']['id']
                                for option in updates['result'][i]['poll']['options']:
                                    if option['voter_count'] == 1:
                                        answer = option['text']
                                await aioconsole.aprint('Poll Answer', poll_id, answer)
                                asyncio.ensure_future(pollanswerhandler(poll_id, answer))
                        except KeyError:
                            await aioconsole.aprint('Unknown update_type')
                            await aioconsole.aprint(updates)
            else:
                pass
        except httpx.HTTPError as exc:
            await aioconsole.aprint(f"HTTP Exception for {exc.request.url} - {exc}")
            exc_type, exc_obj, exc_tb = sys.exc_info()
            await aioconsole.aprint(exc_type, exc_tb.tb_lineno)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print()
        print('Telegram System SHUTDOWN')
        asyncio.run(sendMessage(BOT_API_TOKEN=BOT_API_TOKEN, message=TelegramMessage(chat_id=MAIN_CHANNEL_CHAT_ID, text=f"YG System OFF\n{time.ctime(time.time())}")))
