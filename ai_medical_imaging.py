import os 
from PIL import Image as PILImage
from agno.agent import Agent 
from agno.models.google import Gemini 
import streamlit as st 
from agno.tools.duckduckgo import DuckDuckGoTools 
from agno.media import Image as AgnoImage

if "GOOGLE_API_KEY" not in st.session_state:
    st.session_state.GOOGLE_API_KEY = None

with st.sidebar: 
    st.title(" Configuration ")

    if not st.session_state.GOOGLE_API_KEY:
        api_key = st.text_input(
            "Google API Key:",
            type="password"
        )
        st.caption(
            "Get you API Key form [Google AI Studio]"
        )
        if api_key:
            st.session_state.GOOGLE_API_KEY = api_key 
            st.success("API Key saved!")
            st.rerun()
    else:
        st.success("API Key is configured")
        if st.button("Reset API Key"):
            st.session_state.GOOGLE_API_KEY = None
            st.rerun()

    st.info(
        "This tool provides AI-powered analysis of medical imaging."
    )
    
    st.warning(
        "Used for educational purposes only."
    )

medical_agent = Agent(
    model=Gemini(
        id="gemini-2.0-flash",
        api_key=st.session_state.GOOGLE_API_KEY
    ),
    tools=[DuckDuckGoTools()],
    markdown=True
) if st.session_state.GOOGLE_API_KEY else None 

if not medical_agent: 
    st.warning("Please configure your API Key in the sidebar to continue.")





