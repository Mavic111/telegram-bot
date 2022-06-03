import aioconsole
import httpx
from model import TelegramMessage, TelegramPhoto, TelegramDocument, TelegramPoll, TelegramAudio, TelegramVideo
import aioconsole
import os


async def getMe(BOT_API_TOKEN: str):
    async with httpx.AsyncClient(http2=True) as tele:
        r = await tele.get(f"https://api.telegram.org/bot{BOT_API_TOKEN}/getMe")
        if r.json()["ok"] is True:
            return r.json()
        await aioconsole.aprint(r.text)


async def sendMessage(BOT_API_TOKEN: str, message: TelegramMessage):
    async with httpx.AsyncClient(http2=True) as tele:
        r = await tele.post(f"https://api.telegram.org/bot{BOT_API_TOKEN}/sendMessage", data=message.dict())
        if r.json()["ok"] is False:
            desc = r.json()["description"]
            await aioconsole.aprint(f"Failed to send message below:\n{message.text}\n{desc}")


async def sendPhoto(BOT_API_TOKEN: str, photo: TelegramPhoto, is_local: bool):
    async with httpx.AsyncClient(http2=True) as tele:
        try:
            if is_local:
                files = {
                    'photo': open(photo.photo, 'rb')
                }
                local_photo = TelegramPhoto.parse_obj(photo)
                del local_photo.photo
                r = await tele.post(f"https://api.telegram.org/bot{BOT_API_TOKEN}/sendPhoto", data=local_photo.dict(), files=files)
            else:
                r = await tele.post(f"https://api.telegram.org/bot{BOT_API_TOKEN}/sendPhoto", data=photo.dict())
            if r.json()["ok"] is False:
                await aioconsole.aprint(f"Failed to send photo below:\n{photo.photo}")
                await aioconsole.aprint(r.json()["description"])
        except FileNotFoundError:
            await aioconsole.aprint(f"Failed to send photo below:\n{photo.photo}\nFileNotFound: {photo.photo}")


async def sendDocument(BOT_API_TOKEN: str, document: TelegramDocument, is_local: bool):
    async with httpx.AsyncClient(http2=True) as tele:
        try:
            if is_local:
                files = {
                    'document': open(document.document, 'rb')
                }
                local_document = TelegramDocument.parse_obj(document)
                del local_document.document
                r = await tele.post(f"https://api.telegram.org/bot{BOT_API_TOKEN}/sendDocument", data=local_document.dict(), files=files)
            else:
                r = await tele.post(f"https://api.telegram.org/bot{BOT_API_TOKEN}/sendDocument", data=document.dict())
            if r.json()["ok"] is False:
                desc = r.json()["description"]
                await aioconsole.aprint(f"Failed to send document below:\n{document.document}\n{desc}")
        except FileNotFoundError:
            await aioconsole.aprint(f"Failed to send document below:\n{document.document}\nFileNotFound: {document.document}")


async def sendAudio(BOT_API_TOKEN: str, audio: TelegramAudio, is_local: bool):
    async with httpx.AsyncClient(http2=True) as tele:
        try:
            if is_local:
                files = {
                    'audio': open(audio.audio, 'rb')
                }
                local_audio = TelegramAudio.parse_obj(audio)
                del local_audio.audio
                r = await tele.post(f"https://api.telegram.org/bot{BOT_API_TOKEN}/sendAudio", data=local_audio.dict(), files=files)
            else:
                r = await tele.post(f"https://api.telegram.org/bot{BOT_API_TOKEN}/sendAudio", data=audio.dict())
            if r.json()["ok"] is False:
                desc = r.json()["description"]
                await aioconsole.aprint(f"Failed to send audio below:\n{audio.audio}\n{desc}")
        except FileNotFoundError:
            await aioconsole.aprint(f"Failed to send audio below:\n{audio.audio}\nFileNotFound: {audio.audio}")


async def sendVideo(BOT_API_TOKEN: str, video: TelegramVideo, is_local: bool):
    async with httpx.AsyncClient(http2=True) as tele:
        try:
            if is_local:
                files = {
                    'video': open(video.video, 'rb')
                }
                local_video = TelegramVideo.parse_obj(video)
                del local_video.video
                r = await tele.post(f"https://api.telegram.org/bot{BOT_API_TOKEN}/sendVideo", data=local_video.dict(), files=files)
            else:
                r = await tele.post(f"https://api.telegram.org/bot{BOT_API_TOKEN}/sendVideo", data=video.dict())
            if r.json()["ok"] is False:
                desc = r.json()["description"]
                await aioconsole.aprint(f"Failed to send video below:\n{video.video}\n{desc}")
        except FileNotFoundError:
            await aioconsole.aprint(f"Failed to send video below:\n{video.video}\nFileNotFound: {video.video}")


async def sendPoll(BOT_API_TOKEN: str, poll: TelegramPoll):
    async with httpx.AsyncClient(http2=True) as tele:
        r = await tele.post(f"https://api.telegram.org/bot{BOT_API_TOKEN}/sendPoll", data=poll.dict())
        if r.json()["ok"] is False:
            desc = r.json()["description"]
            await aioconsole.aprint(f"Failed to send poll below:\n{poll.question}\n{desc}")
        else:
            pollid = r.json()["result"]["poll"]["id"]
            if not os.path.exists('Poll'):
                os.makedirs('Poll')
            with open('Poll/' + str(pollid) + '_answer.txt', 'w') as sp:
                sp.write(str(pollid))
            return pollid
            
    