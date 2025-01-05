import streamlit as st
from gradio_client import Client
from PIL import Image
import shutil
import os
import time
from datetime import datetime

# Configuration and Setup
def initialize_app():
    st.set_page_config(
        page_title="AI Image Creator Studio",
        page_icon="🎨",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    
    # Custom CSS for better styling
    st.markdown("""
        <style>
        .main {
            padding: 2rem;
        }
        .stButton>button {
            width: 100%;
            border-radius: 8px;
            height: 3em;
            background-color: #FF4B4B;
            color: white;
            border: none;
            font-weight: bold;
        }
        .stButton>button:hover {
            background-color: #FF6B6B;
            border: none;
        }
        .sidebar .sidebar-content {
            background-color: #f5f5f5;
        }
        h1 {
            color: #1E1E1E;
            font-family: 'Helvetica Neue', sans-serif;
        }
        .status-box {
            padding: 1rem;
            border-radius: 8px;
            margin-bottom: 1rem;
        }
        .footer {
            position: fixed;
            bottom: 0;
            width: 100%;
            background-color: #f8f9fa;
            padding: 1rem;
            text-align: center;
        }
        </style>
    """, unsafe_allow_html=True)

def create_sidebar():
    with st.sidebar:
        st.header("💡 Creator Settings")
        st.markdown("---")
        
        # Advanced Settings
        st.subheader("🎛️ Advanced Configuration")
        api_name = st.text_input("API Endpoint", value="/predict", disabled=True)
        
        # Session Stats
        st.markdown("---")
        st.subheader("📊 Session Statistics")
        if 'generation_count' not in st.session_state:
            st.session_state.generation_count = 0
        st.metric("Images Generated", st.session_state.generation_count)
        
        # Help Section
        st.markdown("---")
        with st.expander("ℹ️ Help & Tips"):
            st.markdown("""
                - Be specific in your descriptions
                - Include details about lighting and style
                - Mention color schemes if important
                - Add artistic references if desired
            """)
    return api_name

def main_content(api_name):
    # Header
    col1, col2, col3 = st.columns([1,6,1])
    with col2:
        st.title("🎨 AI Image Creator Studio")
        st.markdown("""
            <p style='text-align: center; color: #666666; font-size: 1.2em;'>
            Transform your creative vision into stunning artwork using cutting-edge AI technology.
            </p>
        """, unsafe_allow_html=True)
    
    # Main Input Section
    st.markdown("---")
    prompt = st.text_area(
        "🖋️ Describe your vision",
        placeholder="e.g., A serene Japanese garden at sunset with cherry blossoms falling, painted in watercolor style",
        height=100
    )
    
    # Generation Section
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        generate_button = st.button("🚀 Create Masterpiece", use_container_width=True)
    
    if generate_button:
        if not prompt.strip():
            st.error("🎭 Please provide a description for your artwork.")
        else:
            try:
                # Progress Indication
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                # Generation Process
                for i in range(101):
                    time.sleep(0.01)
                    progress_bar.progress(i)
                    if i < 33:
                        status_text.info("🧠 Analyzing your description...")
                    elif i < 66:
                        status_text.info("🎨 Crafting your artwork...")
                    else:
                        status_text.info("✨ Adding final touches...")
                
                # API Call
                client = Client("Onoroyiza/text2img")
                result = client.predict(param_0=prompt, api_name=api_name)
                
                # Process Result
                output_path = f"generated_image_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
                shutil.copy(result, output_path)
                
                # Success Message
                status_text.success("🎉 Your masterpiece is ready!")
                progress_bar.empty()
                
                # Display Result
                st.markdown("---")
                col1, col2 = st.columns([3,1])
                with col1:
                    image = Image.open(output_path)
                    st.image(image, caption="Your Generated Artwork", use_container_width=True)
                
                with col2:
                    st.markdown("### 🎨 Artwork Details")
                    st.markdown(f"**Created:** {datetime.now().strftime('%Y-%m-%d %H:%M')}")
                    st.markdown("**Style:** AI-Generated")
                    
                    # Download Section
                    st.markdown("### 📥 Download Options")
                    with open(output_path, "rb") as file:
                        st.download_button(
                            label="Download JPG 📷",
                            data=file,
                            file_name=output_path,
                            mime="image/jpeg",
                        )
                
                # Update session stats
                st.session_state.generation_count += 1
                
            except Exception as e:
                st.error(f"🎭 Creation process encountered an issue: {str(e)}")
                
def footer():
    st.markdown("---")
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown("""
            <div style='text-align: center;'>
                <p>
                    🛠️ Crafted with passion by 
                    <a href="https://github.com/MrCalmz" target="_blank">Calmz Data Nexus</a>
                </p>
                <p style='font-size: 0.8em; color: #666666;'>
                    Powered by Streamlit & Hugging Face Spaces
                </p>
            </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    initialize_app()
    api_name = create_sidebar()
    main_content(api_name)
    footer()
