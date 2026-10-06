import streamlit as st
from dotenv import load_dotenv
from google import genai
from PIL import Image
import speech_recognition as sr
from gtts import gTTS
import os
import base64
import io


# =========================================================
# LOAD API KEY
# =========================================================

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("Gemini API key not found. Please check your .env file.")
    st.stop()

client = genai.Client(api_key=api_key)


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="VaaniVision AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# SESSION STATE
# =========================================================

if "ai_response" not in st.session_state:
    st.session_state.ai_response = ""

if "voice_text" not in st.session_state:
    st.session_state.voice_text = ""

if "audio_data" not in st.session_state:
    st.session_state.audio_data = None


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

.stApp {
    background: linear-gradient(
        135deg,
        #f5f3ff,
        #eef4ff,
        #ffffff
    );
}

/* Sidebar */

[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #2563eb,
        #4f46e5,
        #6d28d9
    );
}

[data-testid="stSidebar"] * {
    color: white !important;
}

/* Main title */

.main-title {
    text-align: center;
    font-size: 44px;
    font-weight: 800;
    color: #4f46e5;
    margin-top: 10px;
}

.main-subtitle {
    text-align: center;
    font-size: 20px;
    color: #475569;
    margin-bottom: 25px;
}

/* Hero */

.hero-box {
    background: linear-gradient(
        135deg,
        #2563eb,
        #4f46e5,
        #7c3aed
    );

    padding: 30px;

    border-radius: 22px;

    text-align: center;

    color: white;

    margin-bottom: 30px;

    box-shadow:
        0 8px 25px rgba(79, 70, 229, 0.25);
}

.hero-box h2 {
    color: white;
    font-size: 28px;
    margin-bottom: 10px;
}

.hero-box p {
    color: #f8fafc;
    font-size: 16px;
    margin: 0;
}

/* Section headings */

h1, h2, h3 {
    color: #1e1b4b;
}

/* Text area */

textarea {
    border-radius: 12px !important;
}

/* File uploader */

[data-testid="stFileUploader"] {
    background: #ffffff;
    border-radius: 12px;
}

/* Buttons */

.stButton > button {

    background: linear-gradient(
        90deg,
        #2563eb,
        #4f46e5,
        #7c3aed
    );

    color: white;

    border: none;

    border-radius: 12px;

    padding: 12px 20px;

    font-weight: 600;

    font-size: 16px;

    transition: 0.2s;
}

.stButton > button:hover {

    transform: translateY(-2px);

    box-shadow:
        0 6px 15px rgba(79, 70, 229, 0.30);
}

/* Response */

.response-card {

    background: white;

    padding: 25px;

    border-radius: 20px;

    border-left: 6px solid #4f46e5;

    box-shadow:
        0 6px 20px rgba(79, 70, 229, 0.12);

    margin-top: 25px;

    margin-bottom: 20px;
}

/* Footer */

.footer {

    text-align: center;

    color: #64748b;

    padding: 30px 0 10px 0;

    font-size: 14px;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.title("🤖 VaaniVision AI")

    st.markdown("---")

    st.subheader("💡 About")

    st.write(
        "VaaniVision AI is a multimodal AI assistant "
        "that understands text, images and voice."
    )

    st.markdown("---")

    st.subheader("✨ Features")

    st.write("💬 Text-based questions")
    st.write("🎤 Voice input")
    st.write("🖼️ Image understanding")
    st.write("🤖 Gemini AI responses")
    st.write("🔊 AI voice responses")

    st.markdown("---")

    st.subheader("🛠️ Technologies")

    st.write("🐍 Python")
    st.write("🎨 Streamlit")
    st.write("🧠 Gemini AI")
    st.write("🎤 Speech Recognition")
    st.write("🔊 gTTS")

    st.markdown("---")

    st.caption("Multimodal AI Assistant")


# =========================================================
# MAIN HEADER
# =========================================================

st.markdown(
    '<div class="main-title">🤖 VaaniVision AI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="main-subtitle">Multimodal AI Assistant</div>',
    unsafe_allow_html=True
)


# =========================================================
# HERO SECTION
# =========================================================

st.markdown("""
<div class="hero-box">
    <h2>✨ Your Intelligent AI Assistant</h2>
    <p>
        Ask questions using text, voice or images
        and get intelligent AI-powered responses.
    </p>
</div>
""", unsafe_allow_html=True)


# =========================================================
# ASK SECTION
# =========================================================

st.header("✨ Ask VaaniVision AI")

st.write(
    "Choose any input method below."
)


# =========================================================
# TEXT INPUT
# =========================================================

st.subheader("💬 Text Question")

user_input = st.text_area(
    "Enter your question:",
    placeholder="Example: Explain artificial intelligence in simple words.",
    height=100
)


# =========================================================
# VOICE AND IMAGE COLUMNS
# =========================================================

col1, col2 = st.columns(2)


# =========================================================
# VOICE INPUT
# =========================================================

with col1:

    st.subheader("🎤 Voice Input")

    st.write(
        "Speak your question using your microphone."
    )

    audio_input = st.audio_input(
        "Record your question"
    )

    if audio_input:

        recognizer = sr.Recognizer()

        try:

            audio_bytes = audio_input.getvalue()

            with sr.AudioFile(
                io.BytesIO(audio_bytes)
            ) as source:

                audio = recognizer.record(source)

            voice_text = recognizer.recognize_google(
                audio
            )

            st.session_state.voice_text = voice_text

            st.success(
                "Voice recognized successfully!"
            )

            st.write("**You said:**")

            st.write(
                voice_text
            )

        except sr.UnknownValueError:

            st.error(
                "Sorry, I could not understand your voice."
            )

        except sr.RequestError:

            st.error(
                "Speech recognition service is unavailable."
            )

        except Exception as e:

            st.error(
                "Voice processing error."
            )

            st.write(
                str(e)
            )


# =========================================================
# IMAGE INPUT
# =========================================================

with col2:

    st.subheader("🖼️ Image Input")

    st.write(
        "Upload an image for AI analysis."
    )

    uploaded_image = st.file_uploader(
        "Choose an image",
        type=["jpg", "jpeg", "png"]
    )

    image_bytes = None

    if uploaded_image:

        image_bytes = uploaded_image.getvalue()

        image = Image.open(
            io.BytesIO(image_bytes)
        )

        st.image(
            image,
            caption="Uploaded Image",
            use_container_width=True
        )


# =========================================================
# ASK BUTTON
# =========================================================

st.write("")

ask_button = st.button(
    "🚀 Ask VaaniVision AI",
    use_container_width=True
)


# =========================================================
# PROCESS AI REQUEST
# =========================================================

if ask_button:

    final_question = user_input.strip()

    # Use voice question if text is empty
    if not final_question:

        final_question = (
            st.session_state.voice_text.strip()
        )

    # Check input
    if not final_question and not uploaded_image:

        st.warning(
            "Please enter a question, speak a question, "
            "or upload an image."
        )

    else:

        try:

            with st.spinner(
                "🤖 VaaniVision AI is thinking..."
            ):

                # =========================================
                # IMAGE + TEXT / VOICE
                # =========================================

                if uploaded_image:

                    if not final_question:

                        final_question = (
                            "Describe and explain this image in detail."
                        )

                    response = client.interactions.create(

                        model="gemini-3.5-flash-lite",

                        input=[

                            {
                                "type": "text",
                                "text": final_question
                            },

                            {
                                "type": "image",
                                "data": base64.b64encode(
                                    image_bytes
                                ).decode("utf-8"),
                                "mime_type": uploaded_image.type
                            }

                        ]
                    )

                # =========================================
                # TEXT / VOICE ONLY
                # =========================================

                else:

                    response = client.interactions.create(

                        model="gemini-3.5-flash-lite",

                        input=final_question

                    )

                # Save AI response
                st.session_state.ai_response = (
                    response.output_text
                )

                # Remove old audio
                st.session_state.audio_data = None

        except Exception as e:

            st.error(
                "Something went wrong while contacting AI."
            )

            st.write(
                str(e)
            )


# =========================================================
# DISPLAY AI RESPONSE
# =========================================================

if st.session_state.ai_response:

    st.markdown(
        '<div class="response-card">',
        unsafe_allow_html=True
    )

    st.subheader(
        "🤖 VaaniVision AI Response"
    )

    st.write(
        st.session_state.ai_response
    )

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )


    # =====================================================
    # AI VOICE
    # =====================================================

    st.subheader(
        "🔊 AI Voice Response"
    )

    st.write(
        "Convert the AI response into speech."
    )

    if st.button(
        "🔊 Play AI Voice",
        use_container_width=True
    ):

        try:

            with st.spinner(
                "🔊 Generating AI voice..."
            ):

                tts = gTTS(
                    text=st.session_state.ai_response,
                    lang="en",
                    slow=False
                )

                audio_file = "ai_response.mp3"

                tts.save(
                    audio_file
                )

                with open(
                    audio_file,
                    "rb"
                ) as f:

                    st.session_state.audio_data = (
                        f.read()
                    )

            st.success(
                "AI voice generated successfully!"
            )

        except Exception as e:

            st.error(
                "Could not generate AI voice."
            )

            st.write(
                str(e)
            )


    # =====================================================
    # AUDIO PLAYER
    # =====================================================

    if st.session_state.audio_data:

        st.audio(
            st.session_state.audio_data,
            format="audio/mp3"
        )


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    '<div class="footer">'
    '🤖 VaaniVision AI • Multimodal AI Assistant'
    '<br>'
    'Built with Python • Streamlit • Gemini AI'
    '</div>',
    unsafe_allow_html=True
)