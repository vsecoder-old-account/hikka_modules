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
# meta pic: https://img.icons8.com/external-itim2101-lineal-color-itim2101/344/external-bot-education-and-learning-itim2101-lineal-color-itim2101.png

__version__ = (3, 0, 1)

import logging, time
import requests
from aiogram.types import Message as AiogramMessage
from .. import loader

logger = logging.getLogger(__name__)


@loader.tds
class SmartBotMod(loader.Module):

    strings = {
        "name": "SmartBot",
        "start": "✌️ Hi, I'm a smart bot, type in the message that you want to ask about my master!",
        "wait": "😒 You can send next question in {} second(-s)",
        "error": "🖍 Failed to respond to the user, check the token/text and token restrictions!"
    }

    strings_ru = {
        "start": "✌️ Привет, я умный бот, введите в сообщение, что вы хотите спросить о моём хозяине!",
        "wait": "😒 Вы сможете отправить новый вопрос через {}сек",
        "error": "🖍 Не удалось ответить пользователю, проверьте токен/текст и ограничения токена!"
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "ratelimit",
                "20",
                "Rate limit(in seconds)",
                validator=loader.validators.Integer(minimum=0),
            ),
            loader.ConfigValue(
                "token",
                "·····································",
                "HuggingFace token as https://huggingface.co/settings/tokens"
            ),
            loader.ConfigValue(
                "text",
                "Привет, я - none. В мои возможности входит none.",
                "The text about you, according to which the bot can be asked a question, I want to note that the text should be concise and accurate!"
            )
        )
        self.name = self.strings["name"]

    async def client_ready(self, client, db):
        self._client = client

        self._ratelimit = {}

        self.API_URL = "https://api-inference.huggingface.co/models/AndrewChar/model-QA-5-epoch-RU"
        

        self.__doc__ = (
            "Module from add smart bot 👨‍💻\n\n"
            "❌ Enter in .config your token and text!\n"
            "----------\n"
            "❌ Введите в .config токен и текст!\n"
            f"🔗 Link: t.me/{self.inline.bot_username}?start=smart\n\n"
            "P.S. Жалобы по поводу недопонимания ботом текста и неправильных ответов не выслушиваю, пытайтесь привести текст к более понятному варианту."
        )

    async def query(self, payload, headers):
        response = requests.post(self.API_URL, headers=headers, json=payload)
        return response.json()

    async def aiogram_watcher(self, message: AiogramMessage):
        if message.text == "/start smart":
            await message.answer(
                self.strings("start"),
            )
            return
        if message.text[0] != '/':

            if (
                message.from_user.id in self._ratelimit
                and self._ratelimit[message.from_user.id] > time.time()
            ):
                await message.answer(
                    self.strings("wait").format(
                        self._ratelimit[message.from_user.id] - time.time()
                    )
                )
                return

            headers = {
                "Authorization": f"Bearer {self.config['token']}"
            }

            self._ratelimit[message.from_user.id] = (
                time.time() + self.config["ratelimit"]
            )
            output = None
            try:
                output = await self.query(
                    {
                        "inputs": {
                            "question": message.text,
                            "context": self.config["text"]
                        }
                    },
                    headers
                )

                await message.answer(output["answer"])
            except:
                await self.inline.bot.send_message(
                    self._tg_id,
                    f"{self.strings('error')}\n\n{output}",
                )