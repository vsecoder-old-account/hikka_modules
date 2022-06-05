"""
                                _             
  __   _____  ___  ___ ___   __| | ___ _ __   
  \ \ / / __|/ _ \/ __/ _ \ / _` |/ _ \ '__|  
   \ V /\__ \  __/ (_| (_) | (_| |  __/ |     
    \_/ |___/\___|\___\___/ \__,_|\___|_|     

    Copyleft 2022 t.me/vsecoder                                                            
    This program is free software; you can redistribute it and/or modify 

"""

import os, random, requests, io

from .. import loader, utils, main
from ..inline.types import InlineQuery

from telethon import TelegramClient
from telethon.tl.types import Message
from telethon.tl.types import PeerUser, PeerChat, PeerChannel
from telethon.tl.functions.messages import GetHistoryRequest
from telethon.tl.types import MessageMediaPhoto, MessageMediaDocument
from telethon.tl.functions.channels import JoinChannelRequest

@loader.tds
class GifCatsMod(loader.Module):
    """Sends cats gifs and gallerys"""

    strings = {"name": "GifCats"}

    async def client_ready(self, client: TelegramClient, db):
        self.cats_ch = -1001554059668
        self._db = db
        self._client = client
        self._url = ''
        await client(JoinChannelRequest('simpampulki'))

    def __init__(self):
        self.config = loader.ModuleConfig(
            "upload_url",
            "https://0x0.st",
            lambda m: 'Upload api',
        )
        self.name = self.strings["name"]

    async def return_file(self):
        ch = await self._client.get_entity(PeerChannel(self.cats_ch))
        posts = await self._client(GetHistoryRequest(
            peer=ch,
            limit=3000,
            offset_date=None,
            offset_id=0,
            max_id=0,
            min_id=0,
            add_offset=0,
            hash=0
        ))
        for msg in posts.messages:
            message = random.choice(posts.messages)
            if message.media:
                gif = await self._client.download_media(message=message, file=bytes)
                return gif

    async def upload(self) -> str:
        gif = await self.return_file()
        oxo = await utils.run_sync(
            requests.post,
            self.config["upload_url"],
            files={"file": gif},
        )
        await self._client.send_message('me', oxo.text)
        self._url = oxo.text
        return oxo.text

    async def catsgifgallerycmd(self, message: Message):
        """ - send cats gif gallery"""
        await self.inline.gallery(
            caption=lambda: f'<b>🐈 GifCatsGallery</b>\n\n{self._url}',
            message=message,
            next_handler=self.upload,
            preload=0,
        )

    async def gifcatcmd(self, message: Message):
        """ - send cat gif"""
        await utils.answer(message, '<b>🕐 Loading...</b>')
        gif = io.BytesIO(await self.return_file())
        gif.name = "cat.gif"
        await self._client.send_message(
            utils.get_chat_id(message),
            file=gif,
            reply_to=getattr(message, "reply_to_msg_id", None),
        )
        await utils.answer(message, '<b>🐈 Gif cat:</b>')

    async def catsgif_inline_handler(self, query: InlineQuery):
        """ - send inline cats gif gallery"""
        await self.inline.query_gallery(
            query,
            [
                {
                    "title": "🐈 GifCatsGallery",
                    "description": "Send gif cats",
                    "next_handler": self.upload,
                    "caption": lambda: f'<b>🐈 GifCatsGallery</b>\n\n{self._url}',
                }
            ],
        )