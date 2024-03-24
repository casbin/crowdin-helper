# crowdin-helper

Crowdin Helper is a tool to help you batch translate your Crowdin project using OpenAI's API.

## Dev

install PDM: https://pdm-project.org/latest/#recommended-installation-method

```bash
# install dependencies
pdm install
# run
pdm dev
# help
pdm dev --help
# build
pdm build
# install
pdm install # install to virtual environment
pip install dist/crowdin_helper-0.1.0-py3-none-any.whl # install from wheel
# run after install
python -m crowdin_helper
```

## Options

Crowdin Helper needs the following options to run:

| Option             | Required | Description                                | Default Value             |
| ------------------ | -------- | ------------------------------------------ | ------------------------- |
| OPENAI_API_KEY     | true     | OpenAI API Key                             |                           |
| OPENAI_BASE_URL    | false    | OpenAI Base URL                            | https://api.openai.com/v1 |
| OPENAI_MODEL       | false    | OpenAI Model                               | gpt-4                     |
| CROWDIN_API_KEY    | true     | Crowdin API Key                            |                           |
| CROWDIN_PROJECT_ID | true     | Crowdin Project ID                         |                           |
| CROWDIN_LANGS      | true     | The languages to translate to              |                           |
| BATCH_SIZE         | false    | The number of strings to translate at once | 30                        |

Useful links:

- OpenAI model list : https://platform.openai.com/docs/models/overview
- Crowdin languages list : https://developer.crowdin.com/language-codes/

## Usage

Warning: Sometimes, GPT's translation is unreliable. For some texts that should not be translated, the best way is to hide these texts in Crowdin.

### Config File

`config.toml`:

```toml
OPENAI_API_KEY = 'sk-xxx'
OPENAI_BASE_URL = "https://api.openai.com/v1"
OPENAI_MODEL = "gpt-4"
CROWDIN_API_KEY = "xxx"
CROWDIN_PROJECT_ID = "123456"
CROWDIN_LANGS = 'zh-CN, fr, de, ko, ru, ja'
BATCH_SIZE = 30
```

```bash
pdm dev --config-file your_config_file_path
```

### Environment Variables

```bash
export CH_OPENAI_API_KEY='sk-xxx'
export CH_OPENAI_BASE_URL="https://api.openai.com/v1"
export CH_OPENAI_MODEL="gpt-4"
export CH_CROWDIN_API_KEY="xxx"
export CH_CROWDIN_PROJECT_ID="123456"
export CH_CROWDIN_LANGS='zh-CN, fr, de, ko, ru, ja'
export CH_BATCH_SIZE=30
```

also support `.env` file:

```bash
CH_OPENAI_API_KEY='sk-xxx'
CH_OPENAI_BASE_URL="https://api.openai.com/v1"
CH_OPENAI_MODEL="gpt-4"
CH_CROWDIN_API_KEY="xxx"
CH_CROWDIN_PROJECT_ID="123456"
CH_CROWDIN_LANGS='zh-CN, fr, de, ko, ru, ja'
CH_BATCH_SIZE=30
```

then run:

```bash
pdm dev
# or
python -m crowdin_helper
```

### Cli

```bash
pdm dev --openai-api-key "sk-xxx" \
        --openai-base-url "https://api.openai.com/v1" \
        --openai-model "gpt-4" \
        --crowdin-api-key "xxx" \
        --crowdin-project-id "123456" \
        --crowdin-langs "zh-CN, fr, de, ko, ru, ja" \
        --batch-size 30
```

## TODO

- Use LangChain to optimize the translation process.

## LINCENE

[Apache 2.0](./LICENSE)
