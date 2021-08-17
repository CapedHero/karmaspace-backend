import environ

from dirs import PROJECT_ROOT


env = environ.Env()
env.read_env(str(PROJECT_ROOT / ".env"))
