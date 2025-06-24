import streamlit as st
import os
import sys
import io
from contextlib import redirect_stdout

# This import handling block ensures the app can find the 'src' modules.
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from src.agents.manager_agent import ManagerAgent

def load_business_profile():
    """A helper function to load the initial business profile."""
    try:
        profile_path = os.path.join(project_root, "data", "business_profile.txt")
        with open(profile_path, "r") as f:
            return f.read()
    except FileNotFoundError:
        return "Could not find data/business_profile.txt"

st.set_page_config(page_title="AI Marketing Agent", page_icon="🤖", layout="wide")

st.title("🤖 Autonomous AI Marketing Agent")
st.markdown("This tool uses a multi-agent system to help your business with its marketing tasks. You can edit the business profile below, provide a goal, and let the agents work.")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Business Profile")
    business_profile_content = load_business_profile()
    business_profile = st.text_area("Edit your business details here:", value=business_profile_content, height=300)

with col2:
    st.subheader("Marketing Goal")
    user_goal = st.text_input("What would you like the agent to do?", placeholder="e.g., 'create a post' or 'respond to reviews'")
    run_button = st.button("Run Agent")

st.subheader("Agent Live Output")
log_container = st.expander("Show Agent's Thought Process", expanded=False)
log_output = log_container.empty()
final_output_container = st.empty()

if run_button:
    if not user_goal:
        st.warning("Please enter a marketing goal.")
    elif not business_profile:
        st.warning("Please provide a business profile.")
    else:
        with st.spinner("The AI agents are collaborating... Please wait."):
            log_stream = io.StringIO()
            with redirect_stdout(log_stream):
                manager = ManagerAgent(business_profile=business_profile)
                final_result = manager.delegate_task(user_goal)

            log_output.code(log_stream.getvalue(), language='text')
            
            final_output_container.markdown("### Final Result")
            final_output_container.markdown(final_result)
