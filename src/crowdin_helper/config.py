from dynaconf import Dynaconf

settings = Dynaconf(
    envvar_prefix="CH",
    load_dotenv=True,
)

if settings.get("OPENAI_API_KEY") is None:
    settings.OPENAI_API_KEY = ""
if settings.get("OPENAI_BASE_URL") is None:
    settings.OPENAI_BASE_URL = ""
if settings.get("CROWDIN_API_KEY") is None:
    settings.CROWDIN_API_KEY = ""
if settings.get("CROWDIN_PROJECT_ID") is None:
    settings.CROWDIN_PROJECT_ID = ""
