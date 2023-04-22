import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(BASE_DIR, "config.json")
CONFIG = json.loads(open(CONFIG_FILE).read())["rabbitpy"]

URL = CONFIG["URL"]
EXCHANGE = CONFIG["EXCHANGE"]
QUEUE = CONFIG["QUEUE"]
ROUTING_KEY = CONFIG["ROUTING_KEY"]
