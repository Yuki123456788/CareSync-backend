import os
from dotenv import load_dotenv
from .prompts import PROMPT_TYPE, SYSTEM_MESSAGE_PROMPT

load_dotenv()


def get_system_message(type: str) -> str:
    if type not in list(PROMPT_TYPE.values()):
        return "Invalid type"

    return SYSTEM_MESSAGE_PROMPT[type]


def get_openapi_key() -> str:
    key = os.getenv("OPENAI_API_KEY")
    if key is None:
        raise ValueError("OPENAI_API_KEY is not set")
    return key


def get_audio_model() -> str:
    model = os.getenv("AUDIO_MODEL")
    if model is None:
        raise ValueError("AUDIO_MODEL is not set")
    return model


def get_chat_model() -> str:
    model = os.getenv("CHAT_MODEL")
    if model is None:
        raise ValueError("CHAT_MODEL is not set")
    return model
