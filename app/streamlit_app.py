import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

# to run: streamlit run app/streamlit_app.py
import pandas as pd
import streamlit as st
from app.tools.testcases_loader import extract_test_cases, test_cases_to_text
from app.tools.search import search
from app.agents.test_generator import check_test_coverage, generate_test_cases
from app.tools.excel_writer import add_test_cases_to_excel


# --------------------------------
# Page configuration
# --------------------------------

st.set_page_config(
    page_title="QA Test Agent",
    page_icon="🧪",
    layout="wide"
)

# --------------------------------
# Session state
# --------------------------------
# saves interface statement
if "analysis" not in st.session_state:
    st.session_state.analysis = None

if "generated_test_cases" not in st.session_state:
    st.session_state.generated_test_cases = None

if "cancelled_test_cases" not in st.session_state:
    st.session_state.cancelled_test_cases = []

if "processed_test_cases" not in st.session_state:
    st.session_state.processed_test_cases = {}

# --------------------------------
# Header
# --------------------------------

st.title("🧪 QA Test Agent")

st.markdown(
    """
    AI-powered QA assistant

    Generates test cases based on FDD requirements
    Checks existing test coverage and adds missing test cases

    """
)

st.divider()

# --------------------------------
# 1. User provides requirement
# --------------------------------

st.subheader("📝 Enter Requirement")

requirement = st.text_area(
    "Requirement",
    placeholder="Example: Login to the application.",
    height=120
).strip()

# --------------------------------
# Generate button
# --------------------------------

if st.button("🚀 Generate Test Cases", type="primary", use_container_width=True):

    if not requirement:
        st.warning("⚠️ Requirement cannot be empty.")

    else:
        st.success("✅ Requirement received successfully.")

        # --------------------------------
        # 2. Search FDD in Pinecone
        # --------------------------------

        st.markdown("🔍 Searching FDD...")

        search_results = search(requirement)

        if not search_results:
            st.error("❌ No relevant FDD content found.")

        else:
            st.success(
                f"✅ Found {len(search_results)} relevant FDD result(s)."
            )

            # --------------------------------
            # 3. Determine feature
            # --------------------------------

            feature = search_results[0].metadata.get("feature")

            if not feature:
                st.error("❌ Feature was not found in FDD metadata.")

            else:

                # --------------------------------
                # 4. Get FDD content only from selected feature
                # --------------------------------

                fdd_content = "\n\n".join(
                    result.page_content
                    for result in search_results
                    if result.metadata.get("feature") == feature
                )

                # --------------------------------
                # 5. Show FDD search results
                # --------------------------------

                st.markdown("📄 FDD Search Results")

                fdd_results = []

                for i, result in enumerate(search_results, start=1):
                    result_feature = result.metadata.get("feature")
                    content = result.page_content

                    fdd_results.append(
                        {
                            "feature": result_feature,
                            "content": content
                        }
                    )

                    with st.expander(
                            f"📌 Result {i} — {result_feature}"
                    ):
                        st.markdown("Feature")
                        st.write(result_feature)

                        st.markdown("Content")
                        st.write(content)

                st.markdown("🎯 Selected Feature")
                st.success(f"✅ {feature}")

                # --------------------------------
                # 5. Load existing test cases from Excel
                # --------------------------------

                st.markdown("📊 Existing Test Cases")

                try:
                    df = pd.read_excel(
                        "data/testcases/Testcases.xlsx",
                        sheet_name=feature
                    )

                    test_cases = extract_test_cases(df)
                    existing_test_cases = test_cases_to_text(test_cases)

                    if existing_test_cases:
                        st.success(
                            f"✅ Found {len(test_cases)} "
                            f"existing test case(s)."
                        )

                        with st.expander("📋 Show Existing Test Cases"):
                            st.text(existing_test_cases)

                    else:
                        st.info(
                            "ℹ️ No existing test cases found "
                            "for this feature."
                        )

                except ValueError:
                    st.warning(
                        f"⚠️ Excel sheet '{feature}' "
                        "does not exist."
                    )

                    existing_test_cases = ""
                    test_cases = []

                # --------------------------------
                # 6. Coverage check
                # --------------------------------

                st.subheader("🔍 Coverage Check")

                coverage_result = check_test_coverage(
                    requirement,
                    fdd_content,
                    existing_test_cases
                )

                # Save analysis in session
                # so it survives Streamlit reruns
                st.session_state.analysis = {
                    "requirement": requirement,
                    "fdd_results": fdd_results,
                    "fdd_content": fdd_content,
                    "feature": feature,
                    "existing_test_cases": existing_test_cases,
                    "test_case_count": len(test_cases),
                    "coverage_result": coverage_result
                }

                # New requirement = new generation
                st.session_state.generated_test_cases = None

# --------------------------------
# Show saved analysis
# --------------------------------

if st.session_state.analysis:

    analysis = st.session_state.analysis

    requirement = analysis["requirement"]
    fdd_results = analysis["fdd_results"]
    feature = analysis["feature"]
    existing_test_cases = analysis["existing_test_cases"]
    test_case_count = analysis["test_case_count"]
    coverage_result = analysis["coverage_result"]

    # --------------------------------
    # Show requirement
    # --------------------------------

    st.markdown("📋 Your Requirement")
    st.info(requirement)

    # --------------------------------
    # Show FDD search results
    # --------------------------------

    st.markdown("📄 FDD Search Results")

    for i, result in enumerate(fdd_results, start=1):
        result_feature = result["feature"]
        content = result["content"]

        with st.expander(f"📌 Result {i} — {result_feature}"):
            st.markdown("Feature")
            st.write(result_feature)
            st.markdown("Content")
            st.write(content)

    # --------------------------------
    # Show selected feature
    # --------------------------------

    st.markdown("🎯 Selected Feature")
    st.success(f"✅ {feature}")

    # --------------------------------
    # Show existing test cases
    # --------------------------------

    st.markdown("📊 Existing Test Cases")

    if existing_test_cases:
        st.success(
            f"✅ Found {test_case_count} "
            f"existing test case(s)."
        )

        with st.expander("📋 Show Existing Test Cases"):
            st.text(existing_test_cases)

    else:
        st.info(
            "ℹ️ No existing test cases found "
            "for this feature."
        )

    # --------------------------------
    # 6. Coverage check
    # --------------------------------

    st.subheader("🔍 Coverage Check")

    if coverage_result["covered"]:

        st.success(
            "✅ Requirement is already covered "
            "by existing test cases."
        )

        st.info(
            f"💡 {coverage_result['reason']}"
        )

    else:

        st.warning(
            "⚠️ No existing test case covers this requirement."
        )

        st.markdown("📌 What is missing?")

        st.info(
            f"💡 {coverage_result['reason']}"
        )

        # --------------------------------
        # Generate missing test cases
        # --------------------------------

        if st.button(
                "🚀 Generate Missing Test Cases",
                use_container_width=True
        ):
            with st.spinner("🤖 Generating missing test cases..."):
                missing_requirements = coverage_result.get(
                    "missing_requirements",
                    []
                )

                st.session_state.generated_test_cases = (
                    generate_test_cases(
                        "\n".join(missing_requirements),
                        feature
                    )
                )

                # Reset processed test cases for new generation
                st.session_state.cancelled_test_cases = []
                st.session_state.processed_test_cases = {}

        # --------------------------------
        # Show generated test cases
        # --------------------------------

        if st.session_state.generated_test_cases:
            st.success("✅ New test case(s) generated!")

            st.subheader("🧪 Generated Test Cases")

            for generated_test_case in st.session_state.generated_test_cases:

                test_case_id = generated_test_case["test_case_id"]

                # Skip processed test cases
                if test_case_id in st.session_state.processed_test_cases:
                    continue

                st.markdown(
                    f"### {test_case_id} — "
                    f"{generated_test_case['test_case_name']}"
                )

                steps = generated_test_case.get("steps", [])

                for step in steps:
                    step_number = step.get("step_number", "")
                    test_step = step.get("test_step", "")
                    expected_result = step.get("expected_result", "")

                    with st.container(border=True):
                        st.markdown(f"**Step {step_number}**")

                        st.markdown("**Test Step**")
                        st.write(test_step)

                        st.markdown("**Expected Result**")
                        st.write(expected_result)

                # --------------------------------
                # Test case actions
                # --------------------------------

                col1, col2 = st.columns(2)

                with col1:
                    if st.button(
                            "💾 Add to Excel",
                            key=f"add_{test_case_id}",
                            use_container_width=True
                    ):
                        add_test_cases_to_excel(
                            "data/testcases/Testcases.xlsx",
                            feature,
                            [generated_test_case]
                        )
                        st.session_state.processed_test_cases[test_case_id] = "added"

                        st.rerun() # if action was performed for the case, case should be moved to Processed

                with col2:
                    if st.button(
                            "❌ Cancel",
                            key=f"cancel_{test_case_id}",
                            use_container_width=True
                    ):
                        st.session_state.processed_test_cases[test_case_id] = "cancelled"

                        st.rerun() # if action was performed for the case, case should be moved to Processed

        # --------------------------------
        # Processed test cases
        # --------------------------------

        if st.session_state.processed_test_cases:

            st.subheader("📦 Processed Test Cases")

            for generated_test_case in st.session_state.generated_test_cases:

                test_case_id = generated_test_case["test_case_id"]

                status = st.session_state.processed_test_cases.get(test_case_id)

                if status == "added":

                    with st.container(border=True):
                        st.markdown(
                            f"### 🟢 {test_case_id} — "
                            f"{generated_test_case['test_case_name']}"
                        )

                        st.success("Added to Excel")

                elif status == "cancelled":

                    with st.container(border=True):
                        st.markdown(
                            f"### ⚪ {test_case_id} — "
                            f"{generated_test_case['test_case_name']}"
                        )

                        st.info("Cancelled")
