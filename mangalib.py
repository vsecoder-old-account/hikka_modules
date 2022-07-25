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
# meta pic:

__version__ = (1, 0, 1)

import logging
from aiogram.types import Message as AiogramMessage
from .. import loader
from ..inline.types import InlineCall

from selenium import webdriver
from selenium.webdriver.support.select import Select
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options

logger = logging.getLogger(__name__)


@loader.tds
class MangaLibMod(loader.Module):

    strings = {"name": "MangaLib"}

    async def client_ready(self, client, db):
        self._client = client
        self.db = db

        self.chrome_options = Options()
        self.chrome_options.add_argument("--headless")

        self.__doc__ = (
            "Модуль для чтения манги 👨‍💻[beta]\n\n🔗 Ссылка:"
            f" t.me/{self.inline.bot_username}?start=manga\n❗️ Установите Хромиум одной"
            " из команд для использования:\n ▪️ sudo apt install"
            " chromium-chromedriver\n ▪️ sudo apt-get install chromium-driver"
        )

    async def requests(self, data):
        driver = webdriver.Chrome(chrome_options=self.chrome_options)

        name = data["name"]
        volume = data["volume"]
        chapter = data["chapter"]
        page = data["page"]

        driver.get(f"https://mangalib.me/{name}/v{volume}/c{chapter}?page={page}")

        """
        Magic
        """
        driver.find_element(
            "xpath", "/html/body/div[3]/div/div/div[2]/div/button[2]"
        ).click()

        element = driver.find_element(
            "xpath", "/html/body/div[1]/div[3]/div/div[2]/div"
        )
        driver.execute_script("arguments[0].click();", element)

        all = BeautifulSoup(driver.page_source)

        imgs = all.find_all("div", class_="reader-view__wrap")[page - 1]
        modal = all.find_all("div", class_="modal__body")
        pages = (
            len(Select(driver.find_element("xpath", '//*[@id="reader-pages"]')).options)
            + 1
        )

        src = imgs.find_all("img")[0]["src"]

        arr = []
        for p in modal[3].find_all("a"):
            p = p.getText()
            p = p.replace("\n", "").replace("      ", "").replace("   ", " ")
            p = p.split(" ")

            arr.append(p)

        driver.close()

        return {
            "image": src,
            "page": f"{page} / {pages}",
        }

    async def aiogram_watcher(self, message: AiogramMessage):
        if self._client._tg_id == message.chat.id and message.text:
            if message.text == "/start manga":
                await self.inline.bot.send_message(
                    self._tg_id,
                    "👨‍💻 <b>Привет, чтобы продолжить введи <code>/read</code> с"
                    " параметром - названием манги, которое можно получить с сайта"
                    " https://mangalib.me, примеры:</b>\n\n ▪️ Наруто -"
                    " https://mangalib.me/naruto/v1/c0?page=1\n/read naruto\n\n ▪️ One"
                    " Piece - https://mangalib.me/one-piece/v1/c0?page=1\n/read"
                    " one-piece\n\n❗️ Аргумент - часть ссылки,"
                    " https://mangalib.me/<code>one-piece</code>/",
                )
            elif message.text.split(" ")[0] == "/read":
                args = message.text.split(" ")
                if len(args) != 2:
                    return await self.inline.bot.send_message(
                        self._tg_id, "❗️ Неправильно указан агрумент"
                    )

                data = {"name": args[1], "volume": 1, "chapter": 1, "page": 1}

                _markup = self.inline.generate_markup(
                    [
                        [
                            {
                                "text": "◀️",
                                "data": f"undo/{data['name']}/{data['volume']}/{data['chapter']}/{data['page']}",
                            },
                            {
                                "text": "▶️",
                                "data": f"next/{data['name']}/{data['volume']}/{data['chapter']}/{data['page']}",
                            },
                        ],
                        [
                            {
                                "text": "След.глава ⏭",
                                "data": f"next_chapter/{data['name']}/{data['volume']}/{data['chapter']}/{data['page']}",
                            }
                        ],
                        [
                            {
                                "text": "След.том ⏭",
                                "data": f"next_volume/{data['name']}/{data['volume']}/{data['chapter']}/{data['page']}",
                            }
                        ],
                    ]
                )

                r = await self.requests(data)
                await self.inline.bot.send_photo(
                    self._tg_id,
                    r["image"],
                    r["page"],
                    reply_markup=_markup,
                )

    async def feedback_callback_handler(self, call: InlineCall):
        args = call.data.split("/")

        data = {
            "name": args[1],
            "volume": int(args[2]),
            "chapter": int(args[3]),
            "page": int(args[4]),
        }

        if args[0] == "undo":
            data["page"] -= 1
        elif args[0] == "next":
            data["page"] += 1
        elif args[0] in {"next_chapter", "next_glava"}:
            data["chapter"] += 1
        elif args[0] in {"next_volume", "tom"}:
            data["volume"] += 1

        _markup = self.inline.generate_markup(
            [
                [
                    {
                        "text": "◀️",
                        "data": f"undo/{data['name']}/{data['volume']}/{data['chapter']}/{data['page']}",
                    },
                    {
                        "text": "▶️",
                        "data": f"next/{data['name']}/{data['volume']}/{data['chapter']}/{data['page']}",
                    },
                ],
                [
                    {
                        "text": "След.глава ⏭",
                        "data": f"next_chapter/{data['name']}/{data['volume']}/{data['chapter']}/{data['page']}",
                    }
                ],
                [
                    {
                        "text": "След.том ⏭",
                        "data": f"next_volume/{data['name']}/{data['volume']}/{data['chapter']}/{data['page']}",
                    }
                ],
            ]
        )

        r = await self.requests(data)
        await self.inline.bot.send_photo(
            self._tg_id, f"{r['image']}", f"{r['page']}", reply_markup=_markup
        )
