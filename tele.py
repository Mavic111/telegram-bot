import httpx
from model import TelegramMessage, TelegramPhoto, TelegramDocument, TelegramPoll, TelegramAudio, TelegramVideo
import aioconsole
import os


async def get_me(bot_api_token: str):
    async with httpx.AsyncClient(http2=True) as client:
        r = await client.get(f"https://api.telegram.org/bot{bot_api_token}/getMe")
        if r.json()["ok"] is True:
            return r.json()
        await aioconsole.aprint(r.text)


async def send_message(bot_api_token: str, message: TelegramMessage):
    async with httpx.AsyncClient(http2=True) as client:
        r = await client.post(f"https://api.telegram.org/bot{bot_api_token}/sendMessage", data=message.model_dump())
        if r.json()["ok"] is False:
            desc = r.json()["description"]
            await aioconsole.aprint(f"Failed to send message below:\n{message.text}\n{desc}")


async def send_photo(bot_api_token: str, photo: TelegramPhoto, is_local: bool):
    async with httpx.AsyncClient(http2=True) as client:
        try:
            if is_local:
                files = {
                    'photo': open(photo.photo, 'rb')
                }
                local_photo = TelegramPhoto.model_validate(photo)
                del local_photo.photo
                res = await client.post(f"https://api.telegram.org/bot{bot_api_token}/sendPhoto", data=local_photo.model_dump(), files=files)
                if res.json()["ok"] is False:
                    await aioconsole.aprint(f"Failed to send photo below:\n{local_photo.photo}")
                    await aioconsole.aprint(res.json()["description"])
            else:
                res = await client.post(f"https://api.telegram.org/bot{bot_api_token}/sendPhoto", data=photo.model_dump())
                if res.json()["ok"] is False:
                    await aioconsole.aprint(f"Failed to send photo below:\n{photo.photo}")
                    await aioconsole.aprint(res.json()["description"])
        except FileNotFoundError:
            await aioconsole.aprint("Photo file not found")


async def send_document(bot_api_token: str, document: TelegramDocument, is_local: bool):
    async with httpx.AsyncClient(http2=True) as client:
        try:
            if is_local:
                files = {
                    'document': open(document.document, 'rb')
                }
                local_document = TelegramDocument.model_validate(document)
                del local_document.document
                r = await client.post(f"https://api.telegram.org/bot{bot_api_token}/sendDocument", data=local_document.model_dump(), files=files)
                if r.json()["ok"] is False:
                    desc = r.json()["description"]
                    await aioconsole.aprint(f"Failed to send document below:\n{local_document.document}\n{desc}")
            else:
                r = await client.post(f"https://api.telegram.org/bot{bot_api_token}/sendDocument", data=document.model_dump())
                if r.json()["ok"] is False:
                    desc = r.json()["description"]
                    await aioconsole.aprint(f"Failed to send document below:\n{document.document}\n{desc}")
        except FileNotFoundError:
            await aioconsole.aprint("Document file not found")


async def send_audio(bot_api_token: str, audio: TelegramAudio, is_local: bool):
    async with httpx.AsyncClient(http2=True) as client:
        try:
            if is_local:
                files = {
                    'audio': open(audio.audio, 'rb')
                }
                local_audio = TelegramAudio.model_validate(audio)
                del local_audio.audio
                res = await client.post(f"https://api.telegram.org/bot{bot_api_token}/sendAudio", data=local_audio.model_dump(), files=files)
                if res.json()["ok"] is False:
                    desc = res.json()["description"]
                    await aioconsole.aprint(f"Failed to send audio below:\n{local_audio.audio}\n{desc}")
            else:
                res = await client.post(f"https://api.telegram.org/bot{bot_api_token}/sendAudio", data=audio.model_dump())
                if res.json()["ok"] is False:
                    desc = res.json()["description"]
                    await aioconsole.aprint(f"Failed to send audio below:\n{audio.audio}\n{desc}")
        except FileNotFoundError:
            await aioconsole.aprint(f"Audio file not found")


async def send_video(bot_api_token: str, video: TelegramVideo, is_local: bool):
    async with httpx.AsyncClient(http2=True) as client:
        try:
            if is_local:
                files = {
                    'video': open(video.video, 'rb')
                }
                local_video = TelegramVideo.model_validate(video)
                del local_video.video
                res = await client.post(f"https://api.telegram.org/bot{bot_api_token}/sendVideo", data=local_video.model_dump(), files=files)
                if res.json()["ok"] is False:
                    desc = res.json()["description"]
                    await aioconsole.aprint(f"Failed to send video below:\n{local_video.video}\n{desc}")
            else:
                res = await client.post(f"https://api.telegram.org/bot{bot_api_token}/sendVideo", data=video.model_dump())
                if res.json()["ok"] is False:
                    desc = res.json()["description"]
                    await aioconsole.aprint(f"Failed to send video below:\n{video.video}\n{desc}")
        except FileNotFoundError:
            await aioconsole.aprint("Video file not found")


async def send_poll(bot_api_token: str, poll: TelegramPoll):
    async with httpx.AsyncClient(http2=True) as client:
        res = await client.post(f"https://api.telegram.org/bot{bot_api_token}/sendPoll", data=poll.model_dump())
        if res.json()["ok"] is False:
            desc = res.json()["description"]
            await aioconsole.aprint(f"Failed to send poll below:\n{poll.question}\n{desc}")
        else:
            pool_id = res.json()["result"]["poll"]["id"]
            if not os.path.exists('Poll'):
                os.makedirs('Poll')
            with open('Poll/' + str(pool_id) + '_answer.txt', 'w') as sp:
                sp.write(str(pool_id))
            return pool_id
            
    