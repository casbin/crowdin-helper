import click
from crowdin_helper import config


def show_settings():
    print(f"OPENAI_API_KEY: {config.settings.OPENAI_API_KEY}")
    print(f"OPENAI_BASE_URL: {config.settings.OPENAI_BASE_URL}")
    print(f"CROWDIN_API_KEY: {config.settings.CROWDIN_API_KEY}")
    print(f"CROWDIN_PROJECT_ID: {config.settings.CROWDIN_PROJECT_ID}")


@click.command()
@click.option("--openai-api-key", default=config.settings.OPENAI_API_KEY, help="OpenAI API Key")
@click.option("--openai-base-url", default=config.settings.OPENAI_BASE_URL, help="OpenAI Base URL")
@click.option("--crowdin-api-key", default=config.settings.CROWDIN_API_KEY, help="Crowdin API Key")
@click.option("--crowdin-project-id", default=config.settings.CROWDIN_PROJECT_ID, help="Crowdin Project ID")
@click.option("--config-file", default="", help="Config file path")
def main(openai_api_key, openai_base_url, crowdin_api_key, crowdin_project_id,config_file):
    if config_file != "":
        config.settings.load_file(config_file)

    if openai_api_key != "":
        config.settings.OPENAI_API_KEY = openai_api_key
    if openai_base_url != "":
        config.settings.OPENAI_BASE_URL = openai_base_url
    if crowdin_api_key != "":
        config.settings.CROWDIN_API_KEY = crowdin_api_key
    if crowdin_project_id != "":
        config.settings.CROWDIN_PROJECT_ID = crowdin_project_id
    # show_settings()


if __name__ == "__main__":
    main()
