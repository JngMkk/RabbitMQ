import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(BASE_DIR, "config.json")
CONFIG = json.loads(open(CONFIG_FILE).read())["pika"]

USERNAME = CONFIG["USERNAME"]
PASSWORD = CONFIG["PASSWORD"]
HOST = CONFIG["HOST"]
PORT = CONFIG["PORT"]
EXCHANGE = CONFIG["EXCHANGE"]
QUEUE = CONFIG["QUEUE"]
ROUTING_KEY = CONFIG["ROUTING_KEY"]
