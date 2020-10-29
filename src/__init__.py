# -*- coding: utf-8 -*-
import os

os.environ["API_VERSION"] = os.getenv("API_VERSION", "1.0")
os.environ["SERVER_PORT"] = os.getenv("SERVER_PORT", "5010")
os.environ["DEV_MODE"] = os.getenv("DEV_MODE", "1")
os.environ["ENABLE_CORS"] = os.getenv("ENABLE_CORS", "1")
os.environ["LOGGER_LEVEL"] = os.getenv("LOGGER_LEVEL", "debug")

API_VERSION = os.environ["API_VERSION"]
