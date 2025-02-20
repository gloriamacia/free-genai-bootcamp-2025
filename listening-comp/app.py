import streamlit as st
import boto3
import json
import os
from io import BytesIO
from pydub import AudioSegment

# Import Nunito font from Google Fonts.
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Nunito:wght@300;400;700&display=swap" rel="stylesheet">
<style>
    html, body, .stApp, .css-1d391kg, .css-18e3th9, * {
        font-family: 'Nunito', sans-serif !important;
    }
</style>
""", unsafe_allow_html=True)


# Initialize session state for dark mode if not already set.
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

# Use st.toggle for dark mode.
dark_mode_toggle = st.toggle("🌙", value=st.session_state.dark_mode)
st.session_state.dark_mode = dark_mode_toggle

# Set theme colors based on your simplified Tailwind values.
if st.session_state.dark_mode:
    background_color = "hsl(0, 0%, 20%)"     # Dark background
    text_color = "hsl(0, 0%, 98%)"           # Light text
    button_color = "hsl(96, 97%, 41%)"       # Duolingo Green (Primary)
    hover_color = "hsl(96, 97%, 45%)"        # Slightly lighter on hover
    input_background = "hsl(0, 0%, 96%)"     # Light input background for dark mode
else:
    background_color = "hsl(0, 0%, 100%)"    # White background
    text_color = "hsl(0, 0%, 29%)"           # Dark text
    button_color = "hsl(96, 97%, 41%)"       # Duolingo Green (Primary)
    hover_color = "hsl(96, 97%, 45%)"        # Slightly lighter on hover
    input_background = "hsl(0, 0%, 89.8%)"   # Input background for light mode

# Inject inline CSS based on the current theme and font.
css = f"""
<style>
/* Set main container background and font */
.stApp {{
    background-color: {background_color};
}}

/* Force text color for body, headings, labels, and question text */
body, h1, h2, h3, h4, h5, h6, label, .stMarkdown {{
    color: {text_color} !important;
}}

/* Fix for radio button text color (options) */
.stRadio label, .stRadio div div {{
    color: {text_color} !important;
}}

/* Button styles */
.stButton>button {{
    background-color: {button_color};
    color: black !important;  /* Ensure text stays black */
    border: none;
}}
.stButton>button:hover {{
    background-color: {hover_color};
    color: black !important;  /* Prevent hover from changing text color */
}}

/* Input field background */
input {{
    background-color: {input_background};
}}
</style>
"""
st.markdown(css, unsafe_allow_html=True)


# Configure AWS Polly client.
polly = boto3.client("polly", region_name="us-east-1")

# Set up data paths and topics.
DATA_PATH = "data/"
TOPICS = ["restaurant", "feina", "estudis", "vacances"]

st.title("Exercici de Comprensió Oral en Català 👂🏽")

# Layout: two columns – main content (col1) and image (col2).
col1, col2 = st.columns([2.5, 1.5])

with col1:
    inner_col1, inner_col2 = st.columns([1, 1])
    with inner_col1:
        topic = st.selectbox("Selecciona un tema per al diàleg:", TOPICS)

# Initialize session state for dialogue and answer tracking.
if "dialogue_data" not in st.session_state:
    st.session_state.dialogue_data = None
if "selected_answer" not in st.session_state:
    st.session_state.selected_answer = None
if "is_correct" not in st.session_state:
    st.session_state.is_correct = None

if st.button("Generar Diàleg"):
    file_path = os.path.join(DATA_PATH, f"{topic}.json")
    if not os.path.exists(file_path):
        st.error(f"No s'ha trobat el fitxer de diàleg: {file_path}")
    else:
        try:
            # Load dialogue data from JSON.
            with open(file_path, "r", encoding="utf-8") as file:
                st.session_state.dialogue_data = json.load(file)

            dialogue_script = st.session_state.dialogue_data["dialeg"]
            question = st.session_state.dialogue_data["pregunta"]
            options = st.session_state.dialogue_data["opcions"]
            correct_answer = st.session_state.dialogue_data["resposta_correcta"]

            # Reset answer-related session state.
            st.session_state.selected_answer = None
            st.session_state.is_correct = None

            # Synthesize speech using AWS Polly.
            audio_segments = []
            for line in dialogue_script:
                if line.startswith("[Veu 1]:"):
                    text_line = line[len("[Veu 1]:"):].strip()
                    voice_id = "Lucia"  # Female voice
                elif line.startswith("[Veu 2]:"):
                    text_line = line[len("[Veu 2]:"):].strip()
                    voice_id = "Enrique"  # Male voice
                else:
                    continue  # Skip lines that don't match.
                try:
                    response = polly.synthesize_speech(
                        Text=text_line,
                        OutputFormat="mp3",
                        VoiceId=voice_id,
                        LanguageCode="ca-ES"
                    )
                    audio_segments.append(response["AudioStream"].read())
                except Exception as e:
                    st.error(f"Error sintetitzant amb AWS Polly: {e}")

            # Combine audio segments into one MP3 file.
            if audio_segments:
                combined = AudioSegment.empty()
                for segment in audio_segments:
                    audio_segment = AudioSegment.from_file(BytesIO(segment), format="mp3")
                    combined += audio_segment

                combined_audio = BytesIO()
                combined.export(combined_audio, format="mp3")
                combined_audio.seek(0)

                with col1:
                    st.subheader("🎧 Escolta el diàleg:")
                    st.audio(combined_audio, format="audio/mp3")
        except Exception as e:
            st.error(f"Error carregant el diàleg: {e}")

with col2:
    st.image("lilly_call.png", use_container_width=True)

# If dialogue data is available, display the comprehension question.
if st.session_state.dialogue_data:
    question = st.session_state.dialogue_data["pregunta"]
    options = st.session_state.dialogue_data["opcions"]
    correct_answer = st.session_state.dialogue_data["resposta_correcta"]

    with col1:
        st.subheader("❓ Pregunta de comprensió:")
        st.write(question)

        # Radio button for answer selection.
        selected_option = st.radio("Escull una opció:", list(options.values()), key="user_selection")

        # Button to check the answer.
        if st.button("Comprovar resposta"):
            if selected_option:
                st.session_state.selected_answer = selected_option
                st.session_state.is_correct = (selected_option == options[correct_answer])
            else:
                st.warning("Si us plau, selecciona una resposta.")

# Display feedback based on the answer.
if st.session_state.selected_answer is not None:
    with col1:
        if st.session_state.is_correct:
            st.success("✅ Correcte! Bona feina!")
        else:
            st.error(f"❌ Incorrecte. La resposta correcta era: {options[correct_answer]}")
