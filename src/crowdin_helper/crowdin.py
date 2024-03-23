from crowdin_api import CrowdinClient
from pathlib import Path
import json
from crowdin_helper.ai import completion
import logging
from crowdin_helper.config import settings


class FirstCrowdinClient(CrowdinClient):
    TOKEN = settings.CROWDIN_API_KEY  # Required, sets the API token
    TIMEOUT = 30  # Optional, sets http request timeout.
    RETRY_DELAY = 0.5  # Optional, sets the delay between failed requests
    MAX_RETRIES = 5  # Optional, sets the number of retries
    PAGE_SIZE = 100  # Optional, sets default page size


crowdin = FirstCrowdinClient()


class CrowdinFile:
    id: int
    project_id: int
    name: str
    path: str

    def __init__(self, project_id, _id, path):
        self.project_id = project_id
        self.id = _id
        self.path = path
        self.name = Path(path).name

    def __str__(self):
        return self.path


class CrowdinString:
    id: int
    file_id: int
    project_id: int
    text: str

    def __init__(self, project_id, file_id, _id, text):
        self.project_id = project_id
        self.file_id = file_id
        self.id = _id
        self.text = text

    def __str__(self):
        return self.text


class APIError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class ParseError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


PROMPT = """
Please translate the following texts enclosed in triple backticks into {lang}, following the rules below:
1. The text may contain code, which should be preserved as is.
2. The text may contain HTML tags or HTML escape characters, which should not be translated.
3. Please return the translated text or the original text in JSON format, containing a key-value pair, with the key as "translation" and the value as the translated or original text.
4. If there are multiple texts to be translated, please return them in an array format.
5. If you are unsure how to translate, please return the original text.

Please translate:
"""

"""
1. ```{text1}```
2. ```{text2}```
3. ```{text3}```
"""


class Translater:
    project_id: int
    project_name: str
    target_langs: list[str]

    files: list[CrowdinFile] = []
    failed_file: set[str] = set([])
    error_count: int = 0

    def __init__(self, project_id: int):
        self.project_id = project_id
        data = crowdin.projects.get_project(project_id)["data"]
        self.project_name = data["name"]
        self.target_langs = data["targetLanguageIds"]

    def fetch_files(self):
        data = crowdin.source_files.list_files(self.project_id, limit=500)["data"]
        for f in data:
            cf = CrowdinFile(self.project_id, f["data"]["id"], f["data"]["path"])
            allow_types = (".md", ".json", "mdx")
            if cf.name.endswith(allow_types):
                self.files.append(cf)
        return self.files

    def fetch_strings(self, file_id: int) -> list[CrowdinString]:
        data = crowdin.source_strings.list_strings(self.project_id, file_id, limit=500)[
            "data"
        ]
        strings: list[CrowdinString] = []
        for s in data:
            # skip hidden strings
            if s["data"]["isHidden"]:
                continue

            string_id = s["data"]["id"]
            string_text: str = s["data"]["text"]

            """
            fix output json error
            Sometimes, when source text ends with \n, the output json will be invalid
            source text: "xxx\n"
            gpt output: ```
            {
                "translation": "xxx
            "
            }
            ```
            
            maybe LangChain can fix this
            """
            if string_text.endswith("\n"):
                string_text = string_text[:-1]

            cs = CrowdinString(self.project_id, file_id, string_id, string_text)
            strings.append(cs)

        return strings

    @staticmethod
    def list_parse(input: str) -> list[str]:
        lines = input.split("\n")
        res: list[str] = []
        for i, line in enumerate(lines):
            if line.startswith(f"{i + 1}. "):
                line = line[len(f"{i + 1}. ") :]
                if line.startswith("```") and line.endswith("```"):
                    line = line[3:-3]
                res.append(line)
            else:
                raise ParseError(f"Failed to parse GPT output")
        return res

    @staticmethod
    def json_parse(input: str) -> list[str]:
        try:
            json_res = json.loads(input)
        except Exception as e:
            raise ParseError(f"Failed to parse GPT output: {e}")

        if not isinstance(json_res, list):
            if json_res["translation"].startswith("```") and json_res["translation"].endswith(
                "```"
            ):
                json_res["translation"] = json_res["translation"][3:-3]
            
            return [json_res["translation"]]

        """
        Sometimes, the response enclosed in triple backticks
        """
        for trans in json_res:
            if trans["translation"].startswith("```") and trans["translation"].endswith(
                "```"
            ):
                trans["translation"] = trans["translation"][3:-3]

        res = [trans["translation"] for trans in json_res]

        return res

    @staticmethod
    def batch_translate(texts: list[str], lang: str) -> list[str]:
        append_text = "\n".join(
            [f"{num}. ```{text}```" for num, text in enumerate(texts)]
        )
        pmt = PROMPT.format(lang=lang) + append_text

        try:
            res = completion(pmt)
        except Exception as e:
            logging.exception(e)
            raise APIError(f"Failed to call OpenAI API: {e}")

        res = res.strip()

        logging.info(f"OpenAI response: \n{res}\n")
        
        if res.startswith("1"):
            return Translater.list_parse(res)
        else:
            return Translater.json_parse(res)

    def check_translation_if_existed(self, string_id, lang_id):
        res = crowdin.string_translations.list_string_translations(
            projectId=self.project_id, stringId=string_id, languageId=lang_id
        )
        if res["data"]:
            return True
        else:
            return False

    def get_file_progress(self, file_id, lang_id):
        res = crowdin.translation_status.get_file_progress(
            projectId=self.project_id, fileId=file_id
        )
        for item in res["data"]:
            if item["data"]["languageId"] == lang_id:
                return item["data"]["translationProgress"]

        return 0

    @staticmethod
    def get_lang_name(lang_id):
        res = crowdin.languages.get_language(languageId=lang_id)
        return res["data"]["name"]

    def submit_translation(self, string_id: int, lang_id: str, translation: str):
        try:
            crowdin.string_translations.add_translation(
                projectId=self.project_id,
                stringId=string_id,
                languageId=lang_id,
                text=translation,
            )
        except Exception as e:
            raise APIError(f"Failed to submit translation(string_id: {string_id}): {e}")

    def file_translate(self, file: CrowdinFile, lang_id: str, lang_name: str):
        logging.info(f"Now translating(id: {file.id}): {file.path}")
        ss = self.fetch_strings(file.id)

        # remove translated strings
        strings = [
            s for s in ss if not self.check_translation_if_existed(s.id, lang_id)
        ]

        logging.info(f"Strings need to be translated: {len(strings)}")

        batch_size = 30
        for i in range(0, len(strings), batch_size):
            # Sometimes, OpenAI API or Crowdin API will keep erroring
            # if the error count exceeds 5, stop translating
            if self.error_count > 5:
                logging.error(f"Too many errors, stop translating")
                self.print_failed_files()
                exit(-1)

            texts = [string.text for string in strings[i : i + batch_size]]
            try:
                translation = self.batch_translate(texts, lang_name)
            except Exception as e:
                self.failed_file.add(file.path)
                self.error_count += 1
                logging.error(f"Error: {e}")
                continue

            for j, trans in enumerate(translation):
                logging.info(f"Original text(id: {strings[i + j].id}):")
                logging.info(strings[i + j].text)
                logging.info(f"Translation:")
                logging.info(trans)
                try:
                    self.submit_translation(strings[i + j].id, lang_id, trans)
                except Exception as e:
                    self.failed_file.add(file.path)
                    self.error_count += 1
                    logging.error(f"Error: {e}")
                    continue

    def print_failed_files(self):
        if self.failed_file:
            logging.info("Failed files:")
            for file in self.failed_file:
                logging.info(file)

    def run(self, lang_id):
        self.fetch_files()
        if lang_id not in self.target_langs:
            logging.error(
                f"Language {lang_id} is not in {self.project_name} target languages"
            )
            return

        lang_name = self.get_lang_name(lang_id)
        logging.info(f"Start translate {self.project_name} to {lang_name}")

        for file in self.files:
            # skip 100% translated files
            if self.get_file_progress(file.id, lang_id) == 100:
                continue

            try:
                self.file_translate(file, lang_id, lang_name)
            except Exception as e:
                logging.error(f"Failed to translate file: {file.path}")
                logging.error(f"Error: {e}")
                self.failed_file.add(file.path)
                continue

        self.print_failed_files()
