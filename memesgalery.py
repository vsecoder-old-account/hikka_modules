"""
                                _             
  __   _____  ___  ___ ___   __| | ___ _ __   
  \ \ / / __|/ _ \/ __/ _ \ / _` |/ _ \ '__|  
   \ V /\__ \  __/ (_| (_) | (_| |  __/ |     
    \_/ |___/\___|\___\___/ \__,_|\___|_|     

    Copyleft 2022 t.me/vsecoder                                                            
    This program is free software; you can redistribute it and/or modify 

"""

import requests
from random import randrange
from telethon.tl.types import Message

from .. import loader, utils
from ..inline.types import InlineQuery


async def photo() -> str:
    return (
        await utils.run_sync(
            requests.get,
            "https://meme-api.herokuapp.com/gimme",
        )
    ).json()['preview'][2]


@loader.tds
class MemsGaleryMod(loader.Module):
    """Sends mems pictures"""

    strings = {"name": "MemsGalery"}

    async def client_ready(self, client, db):
        self._client = client

    async def memscmd(self, message: Message):
        """Send mems picture"""
        await self.inline.gallery(
            caption=lambda: f"<i>{utils.ascii_face()}\n\n@vsecoder</i>",
            message=message,
            next_handler=photo,
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
                    "next_handler": photo,
                    "thumb_handler": photo,  # Optional
                    "caption": lambda: f"<i>{utils.ascii_face()}\n\n@vsecoder</i>",  # Optional
                    # Because of ^ this lambda, face will be generated every time the photo is switched
                    # "caption": f"<i>Enjoy! {utils.ascii_face()}</i>",
                    # If you make it without lambda ^, it will be generated once
                }
            ],
        )