# 🤖 VaaniVision AI

### Multimodal AI Assistant

VaaniVision AI is a multimodal AI assistant that allows users to interact with Artificial Intelligence using **text, voice, and images**.

The application uses **Google Gemini AI** to understand user inputs and generate intelligent responses. It also converts AI responses into speech using **Text-to-Speech** technology.

---

## ✨ Features

- 💬 **Text Input** – Ask questions using text.
- 🎤 **Voice Input** – Speak your question using a microphone.
- 🖼️ **Image Understanding** – Upload an image and get AI-powered analysis.
- 🤖 **Gemini AI Responses** – Receive intelligent AI-generated answers.
- 🔊 **AI Voice Response** – Convert AI responses into speech.
- 🎨 **Professional UI** – Simple and user-friendly Streamlit interface.
- 🔐 **Environment Variable Security** – API keys are stored securely using `.env`.

---

## 🧠 How It Works

```text
                    VAANIVISION AI
                          │
            ┌─────────────┼─────────────┐
            ↓             ↓             ↓
          TEXT          IMAGE         VOICE
            │             │             │
            ↓             ↓             ↓
       Text Input     Image Upload   Speech Input
            │             │             │
            └─────────────┼─────────────┘
                          ↓
                     GEMINI AI
                          ↓
                 Intelligent Response
                          │
                  ┌───────┴───────┐
                  ↓               ↓
             Text Response    Voice Response
                                  ↓
                              gTTS