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

#Medical Analysis Query 
query = """
You are a highly skilled medical imaging expert with extensive knowledge in radiology and diagnostic imaging, Analyze the patient's medical image and structure your response as follows:

### 1. Image Type & Region
- Specify imaging modality (X-ray/MRI/CT/Ultrasound/etc.)
- Identify the patient's anatomical region and positioning 
- Comment on image quality and technical adequacy 

### 2. Key Findings
- List primary observations systematically
- Note any abnormalities in the patient's imaging with precise descriptions
- Include measurements and densities where relevant
- Describe location, size, shape, and characteristics
- Rate severity: Normal/Mild/Moderate/Severe

### 3. Diagnostic Assesment
- Provide primary diagnosis with confidence level 
- List differential diagnosis in order of likelihood 
- Support each diagnosis with observed evidence from the patient's imaging 
- Note any critical or urgent findings

### 4. Patient-Friendly Explanation 
- Explain the findings in simple, clear language that the patient can understand 
- Avoid medical jargon or provide clear definitions 
- Include visual analogies if helpful 
- Address common patient concerns related to these findings

### 5. Research Context 
IMPORTANT: Use the DuckDuck Go search tool to: 
- Find recent medical literature about similar cases 
- Search for standard treatment protocols 
- Provide a list of relevant medical links of them too 
- Reseach any relevant technological advances 
- Include 2-3 key references to support your analysis

Format your response using clear markdown headers and bullet points. Be concise yet thorough.  

"""

st.title("Medical Imaging Dianosis Agent")
st.write("Upload a medical image for professional analysis")

# Create containers for better organization 
upload_container = st.container()
image_container = st.container()
analysis_container = st.container()

with upload_container:
    uploaded_file = st.file_uploader(
        "Upload Medical Image",
        type=["jpg", "jpeg", "png", "dicom"],
        help="Supported formats: JPG, JPEG, PNG, DICOM"
    )