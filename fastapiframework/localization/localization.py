import json
from datetime import datetime
from typing import Any, Dict

from babel import dates, numbers
from strivelogger import StriveLogger


# Load translations from JSON files
class LocalizationHelper:
    _translations = {}

    def __init__(self, language_code: str = "en"):
        if not self._translations:
            raise Exception("Translations not loaded. Call LocalizationHelper.load_bundle() before creating an instance.")
        self.language_code = language_code

    @classmethod
    def load_bundle(cls, path: str):
       
        StriveLogger.info("Loading localization bundle from path: " + str(path))

        en_path = path / "en.json"
        fr_path = path / "fr.json"

        cls._translations["en"] = cls._load_messages(en_path)
        cls._translations["fr"] = cls._load_messages(fr_path)

        StriveLogger.info("Localization bundle loaded")

    @staticmethod
    def _load_messages(file_path):
        with open(file_path, "r") as f:
            return json.load(f)

    def get_message(self, key: str, args: Dict[str, Any] = {}) -> str:
        keys = key.split(".")
        translation = self._translations.get(self.language_code)
        if translation:
            message = translation
            for key in keys:
                if isinstance(message, dict):
                    message = message.get(key)
                else:
                    break
            if message:
                if message.find("{") != -1 and message.find("}") != -1:
                    return message.format(**args)
                else:
                    return message
            else:
                StriveLogger.error(key, args)
        return ""

    def format_number(self, number: float) -> str:
        formatted_number = numbers.format_number(number, locale=self.language_code)
        return formatted_number

    def format_date(self, date: datetime) -> str:
        formatted_date = dates.format_date(date, format="medium", locale=self.language_code)
        return formatted_date

    def format_number_with_currency(self, number: float) -> str:
        formatted_number = self.format_number(number)
        currency = "$"
        if self.language_code == "fr":
            return f"{formatted_number}{currency}"
        else:
            return f"{currency}{formatted_number}"

    def set_language_code(self, language_code: str):
        self.language_code = language_code
        if self.language_code not in self._translations:
            self.language_code = "en"
            StriveLogger.error(f"Unsupported language code: {language_code}. Falling back to English.")
