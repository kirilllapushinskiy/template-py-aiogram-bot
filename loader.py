from utils import WebhookModel, PollingModel
import argparse

__all__ = ['dp', 'engine', 'bot']

parser = argparse.ArgumentParser("main.py")

parser.add_argument("--mode", "-m", nargs=1,
                    help="Run the application in polling mode or webhook mode.",
                    default='polling',
                    choices=['polling', 'webhook']
                    )

args = parser.parse_args()
print(args.mode)
engine = WebhookModel() if args.mode[0] == 'webhook' else PollingModel()
dp = engine.get_dispatcher()
bot = engine.get_bot()
