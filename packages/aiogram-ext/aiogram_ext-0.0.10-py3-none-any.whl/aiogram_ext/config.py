from .env import env

BOT_TOKEN = env.str("BOT_TOKEN")
MONGO_DB = env.str("MONGO_DB")
MONGO_HOST = env.str("MONGO_HOST")
MONGO_USER = env.str("MONGO_USER", "root")
MONGO_PASSWORD = env.str("MONGO_PASSWORD")
TEXTS_PATH = env.str("TEXTS_PATH", "texts.toml")
