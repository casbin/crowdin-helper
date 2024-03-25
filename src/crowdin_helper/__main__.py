import logging

import click
from crowdin_helper.config import settings
from crowdin_helper.log import init_logging
from crowdin_helper.crowdin import Translater


def run_translater():
    project_id = int(settings.CROWDIN_PROJECT_ID)
    langs: list[str] = settings.CROWDIN_LANGS.split(",")
    langs = [lang.strip(" ") for lang in langs]

    translater = Translater(project_id)

    for lang_id in langs:
        logging.info(f"Start translating to {lang_id}")
        translater.run(lang_id)
        logging.info(f"Finish translating to {lang_id}")


def show_settings():
    logging.info("Settings:")
    logging.info(f"OPENAI_BASE_URL: {settings.OPENAI_BASE_URL}")
    logging.info(f"OPENAI_MODEL: {settings.OPENAI_MODEL}")
    logging.info(f"CROWDIN_PROJECT_ID: {settings.CROWDIN_PROJECT_ID}")
    logging.info(f"CROWDIN_LANGS: {settings.CROWDIN_LANGS}")
    logging.info(f"BATCH_SIZE: {settings.BATCH_SIZE}")


@click.command()
@click.option("--openai-api-key", default=settings.OPENAI_API_KEY, help="OpenAI API Key")
@click.option("--openai-base-url", default=settings.OPENAI_BASE_URL, help="OpenAI Base URL")
@click.option("--openai-model", default=settings.OPENAI_MODEL, help="OpenAI Model")
@click.option("--crowdin-api-key", default=settings.CROWDIN_API_KEY, help="Crowdin API Key")
@click.option("--crowdin-project-id", default=settings.CROWDIN_PROJECT_ID, help="Crowdin Project ID")
@click.option("--crowdin-langs", default=settings.CROWDIN_LANGS, help="The languages to translate to")
@click.option("--batch-size", default=settings.BATCH_SIZE, help="batch size for translation")
@click.option("--config-file", default="", help="Config file path")
def main(**options):
    init_logging()

    openai_api_key = options.get("openai_api_key")
    openai_base_url = options.get("openai_base_url")
    openai_model = options.get("openai_model")
    crowdin_api_key = options.get("crowdin_api_key")
    crowdin_project_id = options.get("crowdin_project_id")
    crowdin_langs = options.get("crowdin_langs")
    batch_size = options.get("batch_size")
    config_file = options.get("config_file")

    settings.OPENAI_API_KEY = openai_api_key
    settings.OPENAI_BASE_URL = openai_base_url
    settings.OPENAI_MODEL = openai_model
    settings.CROWDIN_API_KEY = crowdin_api_key
    settings.CROWDIN_PROJECT_ID = crowdin_project_id
    settings.CROWDIN_LANGS = crowdin_langs
    settings.BATCH_SIZE = batch_size

    if config_file != "":
        settings.load_file(config_file)

    show_settings()
    run_translater()


if __name__ == "__main__":
    main()
