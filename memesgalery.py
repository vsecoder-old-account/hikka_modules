"""
                                _             
  __   _____  ___  ___ ___   __| | ___ _ __   
  \ \ / / __|/ _ \/ __/ _ \ / _` |/ _ \ '__|  
   \ V /\__ \  __/ (_| (_) | (_| |  __/ |     
    \_/ |___/\___|\___\___/ \__,_|\___|_|     

    Copyleft 2022 t.me/vsecoder                                                            
    This program is free software; you can redistribute it and/or modify 

"""
# meta developer: @vsecoder_m
# meta pic: https://img.icons8.com/ios/344/angry-face-meme.png


import random
import requests
from telethon.tl.types import Message

from .. import loader, utils
from ..inline.types import InlineQuery

from telethon import TelegramClient

@loader.tds
class MemsGaleryMod(loader.Module):
    """Sends mems pictures"""

    strings = {"name": "MemsGalery"}

    async def client_ready(self, client: TelegramClient, db):
        self.memes_bot = "@ffmemesbot"
        self._db = db
        self._client = client

    def __init__(self):
        self.config = loader.ModuleConfig(
            "upload_url",
            "https://0x0.st",
            lambda m: self.strings("cfg_searc_url", m),
        )
        self.name = self.strings["name"]

    async def photo(self) -> str:
        async with self._client.conversation(self.memes_bot) as conv:
            await conv.send_message("/start")
            phtmem = await conv.get_response()
            await conv.mark_read()
            f = await self._client.download_media(message=phtmem, file=bytes)
            oxo = await utils.run_sync(
                requests.post,
                self.config["upload_url"],
                files={"file": f},
            )

            return oxo.text

    async def memscmd(self, message: Message):
        """Send mems picture"""
        await self.inline.gallery(
            caption=lambda: f'<i>{random.choice(["Dev @vsecoder", "All memes from @ffmemesbot", "Thk @skillzmeow and @shadow_hikka"])}</i>',
            message=message,
            next_handler=self.photo,
            preload=5,
        )

    async def mems_inline_handler(self, query: InlineQuery):
        """
        Send mems
        """
        await self.inline.query_gallery(
            query,
            [
                {
                    "title": "🤣 MemsGalery",
                    "description": "Send mems photo",
                    "next_handler": self.photo,
                    "thumb_handler": self.photo,  # Optional
                    "caption": lambda: f'<i>{random.choice(["Dev @vsecoder", "All memes from @ffmemesbot", "Thk @skillzmeow and @shadow_hikka"])}</i>',  # Optional
                    # Because of ^ this lambda, face will be generated every time the photo is switched
                    # "caption": f"<i>Enjoy! {utils.ascii_face()}</i>",
                    # If you make it without lambda ^, it will be generated once
                }
            ],
        )
