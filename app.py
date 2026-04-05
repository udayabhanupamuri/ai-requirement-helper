import streamlit as st
from datetime import datetime
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

st.set_page_config(page_title="AI Requirement Helper", page_icon="🧩", layout="wide")

# Initialize Gemini
api_key = os.getenv("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
    try:
        # Try to list available models and use the first available generative model
        available_models = [m for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        if available_models:
            model_name = available_models[0].name.replace('models/', '')
            model = genai.GenerativeModel(model_name)
            AI_ENABLED = True
        else:
            AI_ENABLED = False
    except Exception as e:
        st.warning(f"Could not initialize AI: {str(e)}")
        AI_ENABLED = False
else:
    AI_ENABLED = False

# Initialize session state for history
if "history" not in st.session_state:
    st.session_state.history = []

st.title("🧩 AI Requirement Helper")
st.caption("Transform your requirements into structured summaries, acceptance criteria, and test cases.")

def detect_requirement_type(req: str):
    req = req.lower()
    if "login" in req or "authentication" in req:
        return "Authentication"
    elif "upload" in req or "file" in req:
        return "File Handling"
    elif "data" in req or "report" in req or "analysis" in req:
        return "Data Processing"
    return "General"

def generate_outputs(requirement: str, priority: str):
    if AI_ENABLED:
        try:
            prompt = f"""You are an expert requirement analyst. Analyze this requirement and provide a detailed breakdown in JSON format.

Requirement: {requirement}
Priority: {priority}

Provide your response as valid JSON with this structure (no extra text, just JSON):
{{
  "req_type": "Type of requirement (Authentication/File Handling/Data Processing/etc)",
  "summary": "A concise 2-3 sentence summary of what this requirement does",
  "acceptance_criteria": [
    "Criterion 1",
    "Criterion 2",
    "Criterion 3",
    "Criterion 4",
    "Criterion 5"
  ],
  "test_cases": [
    "Test case 1",
    "Test case 2", 
    "Test case 3",
    "Test case 4",
    "Test case 5"
  ]
}}

Make the acceptance criteria and test cases specific, practical, and relevant to the requirement."""

            response = model.generate_content(prompt)
            response_text = response.text.strip()
            
            # Parse JSON response
            import json
            try:
                # Find JSON in response
                json_start = response_text.find('{')
                json_end = response_text.rfind('}') + 1
                if json_start >= 0 and json_end > json_start:
                    json_str = response_text[json_start:json_end]
                    data = json.loads(json_str)
                    
                    req_type = data.get("req_type", "General")
                    summary = data.get("summary", f"This requirement focuses on {requirement.strip()}.")
                    acceptance_criteria = data.get("acceptance_criteria", [])
                    test_cases = data.get("test_cases", [])
                else:
                    raise ValueError("No JSON found in response")
            except (json.JSONDecodeError, ValueError):
                # Fallback to rule-based if AI parsing fails
                return generate_outputs_fallback(requirement, priority)
            
            traceability_note = (
                f"Requirement Type: {req_type} | Priority: {priority} | "
                f"Generated on {datetime.now().strftime('%Y-%m-%d')} | "
                "This output can be linked to validation and testing artifacts."
            )
            
            return req_type, summary, acceptance_criteria, test_cases, traceability_note
        except Exception as e:
            st.warning(f"AI generation failed: {str(e)}. Using fallback method.")
            return generate_outputs_fallback(requirement, priority)
    else:
        return generate_outputs_fallback(requirement, priority)

def generate_outputs_fallback(requirement: str, priority: str):
    """Fallback rule-based generation when AI is not available"""
    req = requirement.lower()

    req_type = detect_requirement_type(req)
    
    # Better summary
    summary = f"This requirement focuses on enabling users to {requirement.strip()}. It is classified as a {req_type} requirement with {priority} priority."

    acceptance_criteria = [
        "The feature must work as described in the requirement.",
        "All error scenarios should be handled gracefully with appropriate user feedback.",
        "The implementation should follow security best practices."
    ]
    
    # Dynamic acceptance criteria based on keywords
    if "upload" in req:
        acceptance_criteria.extend([
            "User should be able to upload files successfully.",
            "System should validate file format, size, and integrity before processing.",
            "Users should receive clear feedback on upload progress and completion."
        ])
    if "login" in req or "authentication" in req or "sign" in req:
        acceptance_criteria.extend([
            "Users should be able to log in with valid credentials.",
            "System should reject invalid login attempts with clear error messages.",
            "User sessions should be secure and properly managed."
        ])
    if "delete" in req or "remove" in req:
        acceptance_criteria.extend([
            "Users should be able to delete items with confirmation.",
            "Deleted items should not be recoverable.",
            "Users should be notified of successful deletion."
        ])
    if "search" in req or "filter" in req:
        acceptance_criteria.extend([
            "Search/filter results should be accurate and relevant.",
            "Results should load within acceptable timeframes.",
            "Users should be able to refine their search/filter criteria."
        ])
    if "data" in req or "report" in req or "analysis" in req:
        acceptance_criteria.extend([
            "System should process data accurately and completely.",
            "Output should be consistent and reproducible.",
            "Data integrity should be maintained throughout processing."
        ])
    if "export" in req or "download" in req:
        acceptance_criteria.extend([
            "Exported/downloaded files should be in the correct format.",
            "File should contain all required data.",
            "Users should be able to easily access the downloaded content."
        ])

    # Generate contextual test cases
    test_cases = []
    
    if "upload" in req:
        test_cases.extend([
            "Upload a valid file and verify successful processing.",
            "Attempt to upload an invalid or corrupted file.",
            "Upload a file exceeding size limits.",
            "Verify upload progress indicator displays correctly.",
            "Test concurrent file uploads."
        ])
    elif "login" in req or "authentication" in req or "sign" in req:
        test_cases.extend([
            "Login with correct username and password.",
            "Login with incorrect password.",
            "Login with non-existent account.",
            "Verify password reset functionality.",
            "Test session timeout after inactivity."
        ])
    elif "delete" in req or "remove" in req:
        test_cases.extend([
            "Delete a single item and verify removal.",
            "Attempt to delete without confirmation.",
            "Delete multiple items in bulk.",
            "Verify deletion confirmation dialog appears.",
            "Test undo functionality if available."
        ])
    elif "search" in req or "filter" in req:
        test_cases.extend([
            "Search with valid keywords and verify results.",
            "Search with no matching results.",
            "Filter results by different criteria.",
            "Test search with special characters.",
            "Verify pagination of search results."
        ])
    else:
        test_cases.extend([
            "Test with typical valid input.",
            "Test with edge case inputs.",
            "Test error handling with invalid data.",
            "Verify user feedback and messaging.",
            "Performance test with large datasets."
        ])

    traceability_note = (
        f"Requirement Type: {req_type} | Priority: {priority} | "
        f"Generated on {datetime.now().strftime('%Y-%m-%d')} | "
        "This output can be linked to validation and testing artifacts."
    )

    return req_type, summary, acceptance_criteria, test_cases, traceability_note

def build_export_text(requirement, priority, req_type, summary, acceptance_criteria, test_cases, traceability_note):
    text = f"""AI Requirement Helper Output

Original Requirement:
{requirement}

Priority:
{priority}

Requirement Type:
{req_type}

Summary:
{summary}

Acceptance Criteria:
"""
    for item in acceptance_criteria:
        text += f"- {item}\n"

    text += "\nTest Cases:\n"
    for item in test_cases:
        text += f"- {item}\n"

    text += f"\nTraceability Note:\n{traceability_note}\n"
    return text

with st.form("requirement_form"):
    requirement = st.text_area(
        "Enter requirement",
        placeholder="Example: The system should allow users to upload a PDF and extract the document title."
    )
    priority = st.selectbox("Select priority", ["Low", "Medium", "High"])
    submitted = st.form_submit_button("Generate")

if submitted:
    if requirement.strip():
        req_type, summary, acceptance_criteria, test_cases, traceability_note = generate_outputs(requirement, priority)

        # Add to history
        history_item = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "requirement": requirement,
            "priority": priority,
            "req_type": req_type,
            "summary": summary,
            "acceptance_criteria": acceptance_criteria,
            "test_cases": test_cases,
            "traceability_note": traceability_note
        }
        st.session_state.history.insert(0, history_item)

        st.subheader("Requirement Type")
        st.write(req_type)

        st.subheader("Summary")
        st.write(summary)

        st.subheader("Acceptance Criteria")
        for item in acceptance_criteria:
            st.write(f"- {item}")

        st.subheader("Test Cases")
        for item in test_cases:
            st.write(f"- {item}")

        st.subheader("Traceability Note")
        st.info(traceability_note)

        export_text = build_export_text(
            requirement, priority, req_type, summary,
            acceptance_criteria, test_cases, traceability_note
        )

        st.download_button(
            label="Download Output as Text",
            data=export_text,
            file_name="requirement_output.txt",
            mime="text/plain"
        )
    else:
        st.warning("Please enter a requirement first.")

st.markdown("---")
st.subheader("📜 History")

if st.session_state.history:
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("🗑️ Clear History"):
            st.session_state.history = []
            st.rerun()
    
    for idx, item in enumerate(st.session_state.history):
        with st.expander(f"📝 {item['requirement'][:50]}... | {item['priority']} | {item['timestamp']}"):
            st.write(f"**Full Requirement:** {item['requirement']}")
            st.write(f"**Type:** {item['req_type']} | **Priority:** {item['priority']}")
            st.write(f"**Summary:** {item['summary']}")
            st.write("**Acceptance Criteria:**")
            for criteria in item['acceptance_criteria']:
                st.write(f"- {criteria}")
            st.write("**Test Cases:**")
            for test in item['test_cases']:
                st.write(f"- {test}")
else:
    st.info("No history yet. Generate a requirement to see it here!")