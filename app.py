import streamlit as st
import json
from agent.triage_agent import run_triage_agent

# --- Page Configuration ---
st.set_page_config(page_title="AI Healthcare Triage Assistant", layout="centered")

# --- Sidebar Disclaimer ---
with st.sidebar:
    st.title("ℹ️ Disclaimer")
    st.warning("""
    **This AI triage assistant does NOT diagnose or prescribe.**  
    It provides general health guidance using trusted sources  
    (NHS, Mayo Clinic, MedlinePlus).  
    Always consult a qualified doctor for medical concerns.
    """)

# --- Title ---
st.title("🩺 AI Healthcare Triage Chat Assistant")
st.caption("Ask me about your symptoms, and I’ll help you understand what to do next.")

# --- Chat History ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- Display Chat History ---
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- User Input ---
user_input = st.chat_input("Describe your symptoms or ask a health-related question...")

if user_input:
    # Display User Message
    st.chat_message("user").markdown(user_input)
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    # Detect non-medical topics
    non_medical_keywords = [
        "code", "python", "sql", "movie", "game", "recipe",
        "football", "stocks", "car", "music", "politics", "book"
    ]

    if any(word in user_input.lower() for word in non_medical_keywords):
        bot_reply = (
            "🚫 This triage assistant cannot answer questions unrelated to health or medicine. "
            "If you have a medical-related query, please describe your symptoms."
        )
        st.chat_message("assistant").markdown(bot_reply)
        st.session_state.chat_history.append({"role": "assistant", "content": bot_reply})
    else:
        with st.chat_message("assistant"):
            with st.spinner("Analyzing your symptoms..."):
                result = run_triage_agent(user_input)

            # --- Parse JSON safely ---
            if isinstance(result, str):
                try:
                    result = json.loads(result)
                except json.JSONDecodeError:
                    result = {"Summary": result}

            # --- Build chatbot-style response ---
            response_parts = []

            if "Summary" in result:
                response_parts.append(f"🩺 **Summary:** {result['Summary']}")

            if "Possible_Causes" in result and result["Possible_Causes"]:
                causes = "; ".join(result["Possible_Causes"])
                response_parts.append(f"**Possible Causes:** {causes}")

            if "Triage_Recommendation" in result:
                response_parts.append(
                    f"**Triage Recommendation:** {result['Triage_Recommendation']}"
                )

            if "Next_Steps" in result and result["Next_Steps"]:
                steps = " ".join(result["Next_Steps"])
                response_parts.append(f"**Next Steps:** {steps}")

            if "References" in result and result["References"]:
                response_parts.append("**🔗 References:**")
                for ref in result["References"]:
                    if isinstance(ref, dict) and "name" in ref and "url" in ref:
                        response_parts.append(f"- [{ref['name']}]({ref['url']})")
            else:
                response_parts.append("**🔗 References:** Information unavailable")

            disclaimer = result.get(
                "Disclaimer",
                "⚠️ This is not medical advice. Consult a doctor for diagnosis and treatment.",
            )
            response_parts.append(f"**⚠️ Disclaimer:** {disclaimer}")

            final_output = "\n\n".join(response_parts)
            st.markdown(final_output)
            st.session_state.chat_history.append({"role": "assistant", "content": final_output})

        # --- Follow-up Message ---
        follow_up = "💬 Do you have any more questions about your health?"
        st.chat_message("assistant").markdown(follow_up)
        st.session_state.chat_history.append({"role": "assistant", "content": follow_up})
