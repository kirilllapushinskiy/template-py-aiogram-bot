from aiogram import Bot, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.webhook import SendMessage
from aiogram.utils.executor import start_webhook, start_polling

from loguru import logger as log

from abc import ABC, abstractmethod
from types import SimpleNamespace
import json

from utils.singletone import SingletonABC

class AbstactBot(SingletonABC):

    def __init__(self, config_file_name='projectconfig.json'):
        with open(config_file_name, "r") as file:
            self.config = json.loads(file.read(), object_hook=lambda data: SimpleNamespace(**data))
        self.bot = Bot(token=self.config.api.token)
        self.dispatcher = Dispatcher(self.bot)
        self.dispatcher.middleware.setup(LoggingMiddleware())

    @abstractmethod
    async def on_startup(self, _dispatcher):
        log.info("Bot startup...")
        pass

    @abstractmethod
    async def on_shutdown(self, _dispatcher):
        log.info("Closing storage...")
        await _dispatcher.storage.close()
        await _dispatcher.storage.wait_closed()
        log.info("Bot shutdown...")

    @abstractmethod
    def start(self):
        pass


class WebhookBot(AbstactBot):
    async def on_startup(self, _dispatcher):
        await super().on_startup(_dispatcher)
        await self.bot.set_webhook(self.config.webhook.host + self.config.webhook.path)

    async def on_shutdown(self, _dispatcher):
        await super().on_shutdown(_dispatcher)
        await self.bot.delete_webhook()

    def start(self):
        start_webhook(
            dispatcher=self.dispatcher,
            webhook_path=self.config.webhook.path,
            on_startup=self.on_startup,
            on_shutdown=self.on_shutdown,
            skip_updates=True,
            host=self.config.webapp.host,
            port=self.config.webapp.port,
        )


class PollingBot(AbstactBot):
    async def on_startup(self, _dispatcher):
        await super().on_startup(_dispatcher)

    async def on_shutdown(self, _dispatcher):
        await super().on_shutdown(_dispatcher)

    def start(self):
        start_polling(
            dispatcher=self.dispatcher,
            skip_updates=True
        )