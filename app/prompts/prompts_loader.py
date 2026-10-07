# reads prompts from files

from pathlib import Path


PROMPTS_DIR = Path(__file__).parent


def load_prompt(prompt_name: str) -> str:
    prompt_path = PROMPTS_DIR / prompt_name

    with open(prompt_path, "r", encoding="utf-8") as file:
        return file.read()

    