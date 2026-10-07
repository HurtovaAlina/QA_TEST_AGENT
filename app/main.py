import pandas as pd
from app.tools.search import (search)
from app.agents.test_generator import (check_test_coverage, generate_test_cases)
from app.tools.testcases_loader import (extract_test_cases, test_cases_to_text)
from app.tools.excel_writer import add_test_cases_to_excel


if __name__ == "__main__":

    # --------------------------------
    # 1. User provides requirement
    # --------------------------------

    requirement = input("\nEnter requirement: ").strip()

    if not requirement:
        print("Requirement cannot be empty.")
        exit()

    # --------------------------------
    # 2. Search FDD in Pinecone
    # --------------------------------

    print("\n--- SEARCHING FDD ---")

    search_results = search(requirement)

    if not search_results:
        print("No relevant FDD content found.")
        exit()

    # --------------------------------
    # 3. Get feature from search result
    # --------------------------------

    print("\n--- FDD SEARCH RESULTS ---")

    for i, result in enumerate(search_results, start=1):

        feature = result.metadata.get("feature")
        content = result.page_content

        print(f"\nResult {i}")
        print(f"Feature: {feature}")
        print(f"Content:\n{content}")

    # --------------------------------
    # 4. Determine feature
    # --------------------------------

    feature = search_results[0].metadata.get("feature")

    if not feature:
        print("\nFeature was not found in FDD metadata.")
        exit()

    fdd_content = "\n\n".join(
        result.page_content
        for result in search_results
        if result.metadata.get("feature") == feature
    )

    print("\n--- SELECTED FEATURE ---")
    print(feature)

    # --------------------------------
    # 5. Load existing test cases
    #    from the corresponding Excel sheet
    # --------------------------------

    print("\n--- LOADING EXISTING TEST CASES ---")

    try:
        df = pd.read_excel("data/testcases/Testcases.xlsx", sheet_name=feature)
    except ValueError:

        print(f"\nExcel sheet '{feature}' does not exist.")
        print("No existing test cases found for this feature.")
        df = None

    # --------------------------------
    # 6. Convert existing test cases
    #    to text
    # --------------------------------

    if df is not None:
        test_cases = extract_test_cases(df)
        existing_test_cases = test_cases_to_text(test_cases)
    else:
        existing_test_cases = ""

    print("\n--- EXISTING TEST CASES ---")

    if existing_test_cases:
        print(existing_test_cases)
    else:
        print("No existing test cases found.")

    # --------------------------------
    # 7. Check requirement coverage
    # --------------------------------

    print("\n--- CHECKING REQUIREMENT COVERAGE ---")

    coverage = check_test_coverage(requirement, fdd_content, existing_test_cases)
    print("\nCoverage result:")
    print(coverage)

    # --------------------------------
    # 8. If requirement is already
    #    covered -> stop
    # --------------------------------

    if coverage["covered"]:

        print("\n========================================")
        print("REQUIREMENT IS ALREADY COVERED")
        print("========================================")

        print("\nNo new test cases will be generated.")
        print("No changes were made to Excel.")

        exit()

    # --------------------------------
    # 9. Requirement is missing
    #    Generate test cases
    # --------------------------------

    print("\n========================================")
    print("REQUIREMENT IS NOT COVERED")
    print("========================================")

    print("\nGenerating missing test cases...")

    missing_requirements = coverage.get("missing_requirements", [])

    new_test_cases = generate_test_cases(
        "\n".join(missing_requirements),
        feature
    )

    # --------------------------------
    # 10. Show generated test cases
    # --------------------------------

    print("\n--- GENERATED MISSING TEST CASES ---")
    print(new_test_cases)

    # --------------------------------
    # 11. Convert AI result
    #     to Excel writer format
    # --------------------------------

    test_cases_for_excel = []
    for test_case in new_test_cases:
        steps = []

        for step in test_case["steps"]:
            steps.append({
                "step": step["step_number"],
                "action": step["test_step"],
                "expected": step["expected_result"]
            })

        test_cases_for_excel.append({
            "title": feature,
            "steps": steps
        })

    # --------------------------------
    # 12. Add generated test cases
    #     to Excel
    # --------------------------------

    if test_cases_for_excel:
        add_test_cases_to_excel("data/testcases/Testcases.xlsx", feature, test_cases_for_excel)
        print("\n========================================")
        print("SUCCESS")
        print("========================================")

        print(
            f"\n{len(test_cases_for_excel)} "
            f"new test case(s) added to '{feature}'."
        )
    else:
        print("\nNo new test cases to add.")
