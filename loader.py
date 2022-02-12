from aiogram import Dispatcher
from utils import WebhookModel, PollingModel
import argparse

__all__ = ['dp', 'engine']

parser = argparse.ArgumentParser("main.py")

parser.add_argument("--polling", "-p",
    help="Run the application is running in polling mode.",
    action="store_true"
)

parser.add_argument("--webhook", "-w",
    help="Run the application is running in webhook mode.",
    action="store_true"
)

args = parser.parse_args()

engine =  WebhookModel() if args.webhook else PollingModel()
dp = engine.get_dispatcher()
