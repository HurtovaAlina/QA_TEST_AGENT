# Gemini gets requirements and generates test cases and returns in JSON format
from langchain_google_genai import ChatGoogleGenerativeAI
from app.config import gemini_api_key
import json

from app.prompts.prompts_loader import load_prompt


def generate_test_cases(requirements: str, feature_name: str):
    llm = ChatGoogleGenerativeAI(
        api_key=gemini_api_key,
        model="gemini-3.5-flash-lite",
        temperature=0.1
    )

    prompt_template = load_prompt("generate_test_cases.txt")

    prompt = prompt_template.format(
        requirements=requirements,
        feature_name=feature_name
    )

    response = llm.invoke(prompt)

    content = response.content

    if isinstance(content, list):
        content = "\n".join(
            item["text"]
            for item in content
            if item.get("type") == "text"
        )

    return json.loads(content)

# Gemini checks if requirements are covered by existing test cases
def check_test_coverage(requirement: str, fdd_content, existing_test_cases: str):
    llm = ChatGoogleGenerativeAI(
        api_key=gemini_api_key,
        model="gemini-3.5-flash-lite",
        temperature=0.1
    )

    prompt_template = load_prompt("check_test_coverage.txt")

    prompt = prompt_template.format(
        requirement=requirement,
        fdd_content=fdd_content,
        existing_test_cases=existing_test_cases
    )

    response = llm.invoke(prompt)

    content = response.content

    if isinstance(content, list): # if content is a list -> take only text
        content = "\n".join(
            item["text"]
            for item in content
            if item.get("type") == "text"
        )

    return json.loads(content) # return json -> to Python


def generate_missing_test_cases(requirements, existing_test_cases, feature_name):
    missing_test_cases = []

    for requirement in requirements:

        # 1. Check if requirement is covered
        coverage = check_test_coverage(
            requirement,
            existing_test_cases
        )

        print(f"\nRequirement: {requirement}")
        print(f"Coverage result: {coverage}")

        # 2. If covered - skip and go to the next
        if coverage["covered"]:
            print("SKIP: Requirement is already covered.")
            continue

        # 3. If not covered - generate new test cases
        print("GENERATE: Requirement is not covered.")

        new_test_cases = generate_test_cases(
            requirement,
            feature_name
        )

        missing_test_cases.extend(new_test_cases)

    return missing_test_cases