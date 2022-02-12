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

class AbstactModel(SingletonABC):

    def __init__(self, config_file_name='projectconfig.json'):
        with open(config_file_name, "r") as file:
            self.config = json.loads(file.read(), object_hook=lambda data: SimpleNamespace(**data))
        self.__bot = Bot(token=self.config.api.token)
        self.__dispatcher = Dispatcher(self.__bot)
        self.__dispatcher.middleware.setup(LoggingMiddleware())

    def get_dispatcher(self):
        return self.__dispatcher

    @abstractmethod
    async def on_startup(self, _dispatcher):
        log.info("Bot startup...")
        log.warning("Running!")
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


class WebhookModel(AbstactModel):
    async def on_startup(self, _dispatcher):
        await super().on_startup(_dispatcher)
        await self._AbstactModel__bot.set_webhook(self.config.webhook.host + self.config.webhook.path)

    async def on_shutdown(self, _dispatcher):
        await super().on_shutdown(_dispatcher)
        await self._AbstactModel__bot.delete_webhook()

    def start(self):
        log.warning("The application is running in webhook mode.")
        start_webhook(
            dispatcher=self._AbstactModel__dispatcher,
            webhook_path=self.config.webhook.path,
            on_startup=self.on_startup,
            on_shutdown=self.on_shutdown,
            skip_updates=True,
            host=self.config.webapp.host,
            port=self.config.webapp.port,
        )


class PollingModel(AbstactModel):
    async def on_startup(self, _dispatcher):
        await super().on_startup(_dispatcher)

    async def on_shutdown(self, _dispatcher):
        await super().on_shutdown(_dispatcher)

    def start(self):
        log.warning("the application is running in polling mode")
        start_polling(
            dispatcher=self._AbstactModel__dispatcher,
            skip_updates=True,
            on_shutdown=self.on_shutdown,
            on_startup=self.on_startup
        )
        