import streamlit as st
from pathlib import Path
import google.generativeai as genai
import os  
api_key = st.secrets["google"]["api_key"]

genai.configure(api_key=api_key)

generation_config = {
  "temperature": 0.4,
  "top_p": 1,
  "top_k": 32,
  "max_output_tokens": 4096,
}


safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
]


system_prompt="""
As a highly ekilled medical practitioner specializing in image analysis, you are tasked with examining medical images for a renowned hospital. Your expertise is crucial in identifying any anomalies, diseases, or health issues that may be present in the images.

Your Responsibilities include:

1.Detailed Analysis: Thoroughly analyse each image, focussing on identifying any abnormal findings.
2.Findings Report: Document all observed anomalies or signs of disease. Clearly articulate the findings in a structured form.
3.Recommonadations and Next steps: Based on your analysis, suggest potential next steps, include further tests or treatments as applications
4.Treatment Suggestions: If appropriate, recommand possible treatment options or interventions.

Important Notes:

1.Scope of Response: Only respond If the image pertains to human health issues.
2.Clarity of Image: in caes where the image quality impedes clear analysis, note that certain aspects are "Unable to be determined based on the provided image."
3.Disclaimer: Accompany your analysis with the disclaimer: "Consult with a Doctor before making any decisions."

4.Your insights are invaluable in guiding clinical deecisions. Please proceed with the analysis, adhering to the structured approach outlined above

Please provide me an output respone with these 4 headings Detailed Analysis, Findings Report, Recommonadations and Next steps, Treatment Suggestions
"""

model = genai.GenerativeModel(model_name="gemini-1.5-flash",
                              generation_config=generation_config,
                              safety_settings=safety_settings)


st.set_page_config(page_title="VitalImage Analytics", page_icon=":robot:")

st.title("🤵🏻Vital❤Image 📷 Analytics 📊🤵🏻")

st.subheader("An application that can help users to identify medical images")

uploaded_file = st.file_uploader("Upload the medical image for analysis", type=["png","jpg","jpeg"])
if uploaded_file:
    st.image(uploaded_file,width=300,caption="Uploaded Medical Image")
submit_button = st.button("Generate the Analysis")

if submit_button:
    
  if uploaded_file is None:
    st.error("Please provide a medical image for analysis.")
  else:

    image_data = uploaded_file.getvalue()

    image_parts = [
        {
            "mime_type":"image/jpeg",
            "data":image_data
        },
    ]

    prompt_parts = [
        image_parts[0],
        system_prompt,
    ]

    
    
    response = model.generate_content(prompt_parts)
    if response:
        st.title("Here is the analysis based on your image: ")
        st.write(response.text)
st.markdown("**Developed by [Mahalakshmi](#)** ❤️**")
