import logging

import click
from .config import settings
from log import init_logging
from crowdin import Translater
import json


def run_translater():
    project_id = int(settings.CROWDIN_PROJECT_ID)
    langs = json.loads(settings.CROWDIN_LANGS)
    translater = Translater(project_id)
    for lang_id in langs:
        logging.info(f"Start translating to {lang_id}")
        translater.run(lang_id)
        logging.info(f"Finish translating to {lang_id}")


def show_settings():
    print(f"OPENAI_API_KEY: {settings.OPENAI_API_KEY}")
    print(f"OPENAI_BASE_URL: {settings.OPENAI_BASE_URL}")
    print(f"OPENAI_MODEL: {settings.OPENAI_MODEL}")
    print(f"CROWDIN_API_KEY: {settings.CROWDIN_API_KEY}")
    print(f"CROWDIN_PROJECT_ID: {settings.CROWDIN_PROJECT_ID}")
    print(f"CROWDIN_LANGS: {settings.CROWDIN_LANGS}")


@click.command()
@click.option("--openai-api-key", default=settings.OPENAI_API_KEY, help="OpenAI API Key")
@click.option("--openai-base-url", default=settings.OPENAI_BASE_URL, help="OpenAI Base URL")
@click.option("--openai-model", default=settings.OPENAI_MODEL, help="OpenAI Model")
@click.option("--crowdin-api-key", default=settings.CROWDIN_API_KEY, help="Crowdin API Key")
@click.option("--crowdin-project-id", default=settings.CROWDIN_PROJECT_ID, help="Crowdin Project ID")
@click.option("--crowdin-langs", default=settings.CROWDIN_LANGS, help="The languages to translate to")
@click.option("--config-file", default="", help="Config file path")
def main(**options):
    init_logging()

    openai_api_key = options.get("openai_api_key")
    openai_base_url = options.get("openai_base_url")
    openai_model = options.get("openai_model")
    crowdin_api_key = options.get("crowdin_api_key")
    crowdin_project_id = options.get("crowdin_project_id")
    crowdin_langs = options.get("crowdin_langs")
    config_file = options.get("config_file")

    settings.OPENAI_API_KEY = openai_api_key
    settings.OPENAI_BASE_URL = openai_base_url
    settings.OPENAI_MODEL = openai_model
    settings.CROWDIN_API_KEY = crowdin_api_key
    settings.CROWDIN_PROJECT_ID = crowdin_project_id
    settings.CROWDIN_LANGS = crowdin_langs

    if config_file != "":
        settings.load_file(config_file)

    # show_settings()
    run_translater()


if __name__ == "__main__":
    main()
