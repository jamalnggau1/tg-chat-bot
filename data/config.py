from environs import Env


env = Env()
env.read_env()
BOT_TOKEN = env.str("BOT_TOKEN")
ADMINS = env.list("ADMINS")
PATH = env.str("DB_PATH")
BD_ANON_ID = env.int("BD_ANON_ID")
ARCHIVE_ID = env.int("ARCHIVE_ID")


__all__ = [
    "ADMINS",
    "ARCHIVE_ID",
    "BD_ANON_ID",
    "BOT_TOKEN",
    "PATH",
    "env",
]
