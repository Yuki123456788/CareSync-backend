import json

import openai
from openai import OpenAI

from .prompts import PROMPT_TYPE
from .utils import get_system_message, get_openapi_key, get_audio_model, get_chat_model

VALID_FILE_TYPES = [".mp3", ".mp4", ".mpeg", ".mpga", ".m4a", ".wav", ".webm"]


class AIAssistanceService:
    def __init__(self):
        self._openai = None
        self.audio_model = get_audio_model()
        self.chat_model = get_chat_model()

    @property
    def openai(self):
        if self._openai is None:
            self._openai = OpenAI(api_key=get_openapi_key())
        return self._openai

    def _get_request_message(self, type: str, message: str) -> list:
        if type not in list(PROMPT_TYPE.values()):
            return "Invalid type"
        if message == "":
            return "Invalid message"

        message = [
            {"role": "system", "content": get_system_message(type)},
            {"role": "user", "content": message},
        ]
        return message

    def transcript_audio(self, audio_path: str) -> tuple[bool, str]:
        try:
            file = open(audio_path, "rb")
        except FileNotFoundError:
            return False, "File not found"

        # check file type
        if not audio_path.endswith(tuple(VALID_FILE_TYPES)):
            return False, "Invalid file type, Supported file types: " + ", ".join(VALID_FILE_TYPES)

        try:
            result = self.openai.audio.transcriptions.create(
                model=self.audio_model,
                response_format={"type": "json_object"},
                file=file,
                prompt="請使用繁體中文 (traditional Chinese) 進行語音轉文字。"
            )
        except openai.APIConnectionError as e:
            return (False, f"Failed to connect to OpenAI API: {e}")
        except openai.RateLimitError as e:
            return (False, f"OpenAI API request exceeded rate limit: {e}")
        except openai.APIError as e:
            return (False, f"OpenAI API returned an API Error: {e}")

        return True, result.text

    def get_audio_summary(self, audio_content: str) -> tuple[bool, dict]:
        if not audio_content:
            return False, "No audio content"

        try:
            response = self.openai.chat.completions.create(
                model=self.chat_model,
                response_format={"type": "json_object"},
                messages=self._get_request_message(
                    PROMPT_TYPE["GET_RECORD_SUMMARY"], audio_content
                ),
            )
        except openai.APIConnectionError as e:
            return (False, f"Failed to connect to OpenAI API: {e}")
        except openai.RateLimitError as e:
            return (False, f"OpenAI API request exceeded rate limit: {e}")
        except openai.APIError as e:
            return (False, f"OpenAI API returned an API Error: {e}")

        try:
            response_dict = json.loads(response.choices[0].message.content.replace("'", '"'))
        except json.JSONDecodeError as e:
            return (False, f"Failed to decode JSON response: {e}")

        def generate_precaution_detail(precaution: dict) -> str:
            if precaution and not isinstance(precaution, dict):
                return ""
            result = f"[{precaution.get('title')}]\n說明：{precaution.get('description')}\n"

            if precaution.get("steps") and isinstance(precaution.get("steps"), list):
                result += "執行步驟：\n"
                for index, step in enumerate(precaution.get("steps")):
                    result += f"{index + 1}. {step}\n"
            return result

        def generate_precautions(precautions: list) -> str:
            if precautions and not isinstance(precautions, list):
                return []
            result = ""
            for precaution in precautions:
                detail = generate_precaution_detail(precaution)
                if detail:
                    result += f"{detail}\n"
            return result

        result = {
            "symptom": response_dict.get("symptom", ""),
            "precautions": generate_precautions(response_dict.get("precautions", "")),
        }

        return True, result

    def get_precaution_detail(self, precaution: str):
        if not precaution:
            return False, "No precaution content"

        try:
            response = self.openai.chat.completions.create(
                model=self.chat_model,
                response_format={"type": "json_object"},
                messages=self._get_request_message(
                    PROMPT_TYPE["GET_PRECAUTION_DETAIL"], precaution
                ),
            )
        except openai.APIConnectionError as e:
            return (False, f"Failed to connect to OpenAI API: {e}")
        except openai.RateLimitError as e:
            return (False, f"OpenAI API request exceeded rate limit: {e}")
        except openai.APIError as e:
            return (False, f"OpenAI API returned an API Error: {e}")

        try:
            response_dict = json.loads(response.choices[0].message.content.replace("'", '"'))
        except json.JSONDecodeError as e:
            return (False, f"Failed to decode JSON response: {e}")

        result = {
            "description": response_dict.get("description", ""),
            "situation_judgment": response_dict.get("situation_judgment", ""),
            "steps": response_dict.get("steps", ""),
        }

        return True, result

    def get_medicine_info(self, prescription: str):
        if not prescription:
            return False, "No prescription content"

        try:
            response = self.openai.chat.completions.create(
                model=self.chat_model,
                response_format={"type": "json_object"},
                messages=self._get_request_message(PROMPT_TYPE["GET_MEDICINE_INFO"], prescription),
            )
        except openai.APIConnectionError as e:
            return (False, f"Failed to connect to OpenAI API: {e}")
        except openai.RateLimitError as e:
            return (False, f"OpenAI API request exceeded rate limit: {e}")
        except openai.APIError as e:
            return (False, f"OpenAI API returned an API Error: {e}")

        try:
            response_dict = json.loads(response.choices[0].message.content.replace("'", '"'))
        except json.JSONDecodeError as e:
            return (False, f"Failed to decode JSON response: {e}")

        def generate_medicine_info(medicine_info: dict) -> dict:
            FIELDS = [
                ("medicine_name", str, ""),
                ("appearance", str, ""),
                ("instruction", str, ""),
                ("precaution", str, ""),
                ("side_effect", str, ""),
            ]
            result = {}

            if not medicine_info or not isinstance(medicine_info, dict):
                for field, _, field_default in FIELDS:
                    result[field] = field_default
                return result
            for field, _, field_default in FIELDS:
                result[field] = medicine_info.get(field, field_default)
            return result

        def generate_take_medicine_info(take_medicine_info: dict) -> dict:
            FIELDS = [
                ("start_date", str, ""),
                ("interval_days", int, 1),
                ("duration", int, 0),
                ("medicine_time", list, []),
            ]
            result = {}

            if not take_medicine_info or not isinstance(take_medicine_info, dict):
                for field, _, field_default in FIELDS:
                    result[field] = field_default
                return result
            for field, _, field_default in FIELDS:
                result[field] = take_medicine_info.get(field, field_default)
            return result

        result = {
            "medicine_info": generate_medicine_info(response_dict.get("medicine_info", {})),
            "take_medicine_info": generate_take_medicine_info(
                response_dict.get("take_medicine_info", {})
            ),
        }

        return True, result
