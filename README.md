# crowdin-helper

## Dev

install PDM: https://pdm-project.org/latest/#recommended-installation-method

```bash
# install dependencies
pdm install
# run
pdm dev
```

## Run

Crowdin Helper need 3 options to run:

| Option             | Required | Description        |
| ------------------ | -------- | ------------------ |
| OPENAI_API_KEY     | true     | OpenAI API Key     |
| OPENAI_BASE_URL    | false    | OpenAI Base URL    |
| CROWDIN_API_KEY    | true     | Crowdin API Key    |
| CROWDIN_PROJECT_ID | true     | Crowdin Project ID |

## Usage

### Cli Options

```bash
pdm dev --openai-api-key your_openai_api_key --openai-base-url your_openai_base_url --crowdin-api-key your_crowdin_api_key --crowdin-project-id your_crowdin_project_id
```

### Environment Variables

```bash
export OPENAI_API_KEY=your_openai_api_key
export OPENAI_BASE_URL=your_openai_base_url
export CROWDIN_API_KEY=your_crowdin_api_key
export CROWDIN_PROJECT_ID=your_crowdin_project_id
```

### Config File

```toml
OPENAI_API_KEY = "your_openai_api_key"
OPENAI_BASE_URL = "your_openai_base_url"
CROWDIN_API_KEY = "your_crowdin_api_key"
CROWDIN_PROJECT_ID = "your_crowdin_project_id"
```

```bash
pdm dev --config-file your_config_file_path
```

## TODO

- Use LangChain to optimize the translation process.

## LINCENE

[Apache 2.0](./LICENSE)
