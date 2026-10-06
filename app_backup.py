import streamlit as st
from dotenv import load_dotenv
from google import genai
from PIL import Image
import speech_recognition as sr
from gtts import gTTS
import os
import base64
import io


# =================================================
# LOAD API KEY
# =================================================

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("Gemini API key not found. Check your .env file.")
    st.stop()

client = genai.Client(api_key=api_key)


# =================================================
# PAGE SETTINGS
# =================================================

st.set_page_config(
    page_title="VaaniVision AI",
    page_icon="🤖",
    layout="wide"
)


# =================================================
# SESSION STATE
# =================================================

if "ai_response" not in st.session_state:
    st.session_state.ai_response = ""

if "voice_text" not in st.session_state:
    st.session_state.voice_text = ""


# =================================================
# TITLE
# =================================================

st.title("🤖 VaaniVision AI")
st.subheader("Multimodal AI Assistant")

st.write(
    "Ask questions using text, image, or voice."
)


# =================================================
# TEXT INPUT
# =================================================

st.header("💬 Ask a Question")

user_input = st.text_input(
    "Enter your question:"
)


# =================================================
# VOICE INPUT
# =================================================

st.header("🎤 Voice Input")

audio_input = st.audio_input(
    "Click here and speak your question"
)

voice_text = ""

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

        st.write("### 🗣️ You said:")
        st.write(voice_text)

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

        st.write(str(e))


# =================================================
# IMAGE INPUT
# =================================================

st.header("🖼️ Upload an Image")

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
        width=500
    )


# =================================================
# ASK VAANIVISION AI
# =================================================

if st.button("🚀 Ask VaaniVision AI"):

    # ---------------------------------------------
    # SELECT QUESTION
    # ---------------------------------------------

    final_question = user_input.strip()

    if not final_question:

        final_question = (
            st.session_state.voice_text.strip()
        )


    # ---------------------------------------------
    # CHECK INPUT
    # ---------------------------------------------

    if not final_question and not uploaded_image:

        st.warning(
            "Please enter a question, speak a question, "
            "or upload an image."
        )

    else:

        try:

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


            # =========================================
            # SAVE AI RESPONSE
            # =========================================

            st.session_state.ai_response = (
                response.output_text
            )


        except Exception as e:

            st.error(
                "Something went wrong."
            )

            st.write(str(e))


# =================================================
# DISPLAY AI RESPONSE
# =================================================

if st.session_state.ai_response:

    st.write(
        "### 🤖 VaaniVision AI Response"
    )

    st.write(
        st.session_state.ai_response
    )


    # =============================================
    # AI VOICE RESPONSE
    # =============================================

    st.write(
        "### 🔊 AI Voice Response"
    )

    if st.button("🔊 Play AI Voice"):

        try:

            tts = gTTS(
                text=st.session_state.ai_response,
                lang="en",
                slow=False
            )

            audio_file = "ai_response.mp3"

            tts.save(
                audio_file
            )

            st.success(
                "AI voice generated successfully!"
            )

            st.audio(
                audio_file,
                format="audio/mp3"
            )

        except Exception as e:

            st.error(
                "Could not generate AI voice."
            )

            st.write(str(e))