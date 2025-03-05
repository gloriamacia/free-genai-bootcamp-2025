import gradio as gr
import soundfile as sf
import json
import random
import tempfile
import os
from dotenv import load_dotenv
from openai import OpenAI
from gradio.themes import GoogleFont

js_func = """
function refresh() {
    const url = new URL(window.location);
    if (url.searchParams.get('__theme') !== 'dark') {
        url.searchParams.set('__theme', 'dark');
        window.location.href = url.href;
    }
}
"""

theme = gr.themes.Default(font=[GoogleFont("Nunito")]).set(
    button_primary_background_fill="#55CD02",
    button_primary_background_fill_dark="#55CD02",
    body_background_fill_dark="#333333",
    button_primary_background_fill_hover_dark="#89E219"
)

css = """
#output_image {
      display: block;
      margin-left: auto;
      margin-right: auto;
      margin-top: 20px;
}
"""

# Load environment variables from the .env file
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)

# Load extra context from JSON file.
with open("catalan_traditions.json", "r") as f:
    traditions_data = json.load(f)

image_list = [
    "img_1.jpg",
    "img_2.jpg",
    "img_3.jpg",
    "img_4.jpg"
]

# Select a random image only once at page load.
random_image = random.choice(image_list)
extra_context = traditions_data[random_image]
extra_context_text = (
    f"This image represents the tradition '{extra_context['tradition_name']}'. "
    f"Expected context: {extra_context['phrase']}."
)

# Print logs for debugging.
print("Selected image:", random_image)
print("Extra context text:", extra_context_text)

def process_audio(audio_filepath, context_text):
    if audio_filepath is None:
        return "No audio recorded.", "No evaluation available."
    
    try:
        data, samplerate = sf.read(audio_filepath)
        duration = len(data) / samplerate
    except Exception as e:
        return f"Error processing audio: {e}", ""
    
    if duration > 60:
        data = data[:int(samplerate * 60)]
        temp_file = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
        sf.write(temp_file.name, data, samplerate)
        audio_to_transcribe = temp_file.name
    else:
        audio_to_transcribe = audio_filepath

    try:
        with open(audio_to_transcribe, "rb") as audio_file:
            transcript_response = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                language="ca",
                response_format="json"
            )
            transcription = transcript_response.text
    except Exception as e:
        return f"Error during transcription: {e}", ""
    
    # Build the evaluation prompt using the locked extra context.
    evaluation_prompt = (
        "Please evaluate the following Catalan speaking transcript based on these 3 categories: "
        "Fluency and Coherence, Lexical Resource, and Grammatical Range and Accuracy. "
        "For each category, write a short comment (one or two sentences) about how the speaker performed."
        "Then, based on the overall performance, assign an overall CEFR level for the speaker: A1, A2, B1, B2, C1, or C2. Include a brief explanation of the Catalan tradition at the end."
        "Ensure the total response does not exceed 300 words. "
        f"Transcript: {transcription}. "
        f"Extra Context: {context_text}"
    )
    
    try:
        evaluation_response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an expert language examiner."},
                {"role": "user", "content": evaluation_prompt}
            ]
        )
        evaluation = evaluation_response.choices[0].message.content.strip()
    except Exception as e:
        evaluation = f"Error during evaluation: {e}"
    
    return transcription, evaluation

def refresh_image():
    new_image = random.choice(image_list)
    new_context = traditions_data[new_image]
    new_context_text = (
        f"This image represents the tradition '{new_context['tradition_name']}'. "
        f"Expected context: {new_context['phrase']}."
    )
    print("Selected new image:", new_image)
    print("New extra context text:", new_context_text)
    # Return the new image path and extra context text.
    return f"images/{new_image}", new_context_text

with gr.Blocks(css=css, js=js_func, theme=theme) as demo:
    gr.Markdown("<h1 style='text-align:center;'>Catalan Speaking Practice</h1>")
    gr.Markdown("Look at the image below depicting a traditional Catalan celebration. Describe what you see in Catalan within 1 minute.")
    
    with gr.Row():
        # Left column: image on top, refresh button, and audio recording below.
        with gr.Column(scale=1):
            image_display = gr.Image(
                value=f"images/{random_image}", 
                label="Image to Describe", 
                interactive=False,
                show_download_button=False,
                show_share_button=False,
                show_fullscreen_button=False,
                show_label=False,
            )
            new_image_button = gr.Button("New Image", variant="primary")
            audio_component = gr.Audio(
                sources="microphone", 
                type="filepath", 
                label="Record your description (max 1 min)", 
                max_length=60
            )
        # Right column: transcript and feedback.
        with gr.Column(scale=1):
            gr.Markdown("**Transcription**")
            output_transcript = gr.Markdown("*Your transcription will be available here.*")
            gr.Markdown("**Feedback**")
            feedback = gr.Markdown("*Your performance evaluation will be shown here.*")
            image_display_2 = gr.Image(
                value="duolingo.png", 
                interactive=False,
                show_download_button=False,
                show_share_button=False,
                show_fullscreen_button=False,
                show_label=False,
                container=False,
                width=150,
                elem_id="output_image"
            )
    
    # Create a hidden state for the extra context.
    context_text_state = gr.State(extra_context_text)
    
    # New image button updates both the image display and the extra context.
    new_image_button.click(refresh_image, inputs=[], outputs=[image_display, context_text_state])
    
    # Update both transcription and evaluation feedback.
    audio_component.change(process_audio, inputs=[audio_component, context_text_state], outputs=[output_transcript, feedback])

demo.launch(server_port=7863)
