# reverts DataFrame to Test cases
from typing import List
import pandas as pd

def extract_test_cases(df: pd.DataFrame) -> list:
    """
        Converts Excel DataFrame into a list of test cases.
        Each test case contains a title and its steps.
    """
    test_cases = []

    current_test_case = None

    for _, row in df.iterrows(): # go through each row in the DataFrame

        # New test case starts when Title is present
        if pd.notna(row["Title"]): # checks that title is not NaN

            if current_test_case is not None:
                test_cases.append(current_test_case)

            current_test_case = {
                "title": row["Title"],
                "steps": []
            }

        # Add step to current test case
        if current_test_case is not None and pd.notna(row["Test Step"]):

            current_test_case["steps"].append({
                "step": row["Test Step"],
                "action": row["Step Action"],
                "expected": row["Step Expected"]
            })

    # Add the last test case
    if current_test_case is not None:
        test_cases.append(current_test_case)

    return test_cases

# creates test cases as text to send to Gemini
def test_cases_to_text(test_cases: list) -> str:
    """
        Converts test cases into text format for LLM.
    """
    result = []

    for test_case in test_cases:
        result.append(f"Test Case: {test_case['title']}") # add title

        for step in test_case["steps"]: # gather steps in test case
            result.append(f"Step: {step['step']}:\n"
            f"Action: {step['action']}\n"
            f"Expected: {step['expected'] if pd.notna(step['expected']) else ''}"
        )

    return"\n\n".join(result)

