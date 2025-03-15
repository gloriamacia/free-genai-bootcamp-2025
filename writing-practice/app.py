import gradio as gr
import requests
import random
from gradio.themes import GoogleFont
import os

# Create a custom theme:
# - Use Nunito as the font.
# - Set primary button background to #55CD02 in both light and dark modes.
# - In dark mode, set the body background to #333333.
theme = gr.themes.Default(font=[GoogleFont("Nunito")]).set(
    button_primary_background_fill="#55CD02",
    button_primary_background_fill_dark="#55CD02",
    body_background_fill_dark="#333333"
)

# Backend URL
backend_url = os.getenv("BACKEND_URL")


def fetch_random_word(current_group):
    try:
        response = requests.get(f"{backend_url}/groups/{current_group}/words/raw")
        response.raise_for_status()
        data = response.json()
        words = data.get("words", [])
        if not words:
            return None, "🟡 No words found for this group.", None
        random_word = random.choice(words)
        english = random_word.get("english", "Unknown")
        catalan = random_word.get("catalan", "Unknown")
        word_id = random_word.get("id", None)
        return english, catalan, word_id
    except requests.exceptions.RequestException as e:
        return None, f"❌ Error fetching data: {e}", None

def generate_word(current_group):
    english_word, correct_catalan, word_id = fetch_random_word(current_group)
    if not english_word:
        return "", "", correct_catalan, None
    return english_word, "", correct_catalan, word_id

def init_game(request: gr.Request):
    params = dict(request.query_params)
    group_id = params.get("group_id")
    session_id = params.get("session_id")
    
    if not group_id:
        return session_id, None, "No group id provided.", "", "", None

    english_word, correct_catalan, word_id = fetch_random_word(group_id)
    return session_id, group_id, english_word, "", correct_catalan, word_id

def check_answer(user_input, english_word, correct_catalan, review_items, current_word_id):
    correct = user_input.strip().lower() == correct_catalan.lower()
    if correct:
        message = f"<p style='color:green;'>✅ Correct! '{english_word}' in Catalan is '{correct_catalan}'.</p>"
    else:
        message = f"<p style='color:red;'>❌ Incorrect. '{english_word}' in Catalan is '{correct_catalan}'.</p>"
    review_items = review_items or []
    review_items.append({"word_id": current_word_id, "correct": correct})
    if correct:
        return gr.update(value=message, visible=True), gr.update(value="", visible=False), review_items
    else:
        return gr.update(value="", visible=False), gr.update(value=message, visible=True), review_items

def save_study_session(study_session_id, review_items, current_group):
    if not review_items:
        return study_session_id, []
    if not study_session_id:
        payload = {"group_id": current_group, "study_activity_id": 1}
        try:
            response = requests.post(f"{backend_url}/study-sessions", json=payload)
            response.raise_for_status()
            data = response.json()
            study_session_id = data["id"]
        except Exception as e:
            raise gr.Error(f"Failed to create study session: {e}")
    for item in review_items:
        payload = {"word_id": item["word_id"], "correct_count": item["correct"]}
        try:
            response = requests.post(f"{backend_url}/study-sessions/{study_session_id}/review", json=payload)
            response.raise_for_status()
        except Exception as e:
            raise gr.Error("Failed to save study session")
    gr.Info("💾 Study session saved!", duration=2)
    return study_session_id, []

# Create Blocks with custom CSS to center content.
with gr.Blocks(theme=theme, css="""
.center {
    display: flex;
    justify-content: center;
    width: 50%;
}
""") as demo:
    gr.HTML("<h1> ✍🏼 English to Catalan Writing Practice </h1>")
    
    # States for study session, review items, and current group.
    study_session_state = gr.State(None)
    review_items_state = gr.State([])
    current_group_state = gr.State(None)
    
    with gr.Row():
        english_output = gr.Textbox(label="English Word", interactive=False)
        answer_input = gr.Textbox(label="Your Answer in Catalan")
    
    hidden_correct = gr.Textbox(visible=False)
    hidden_word_id = gr.Textbox(visible=False)
    
    result_success = gr.Markdown(visible=False)
    result_error = gr.Markdown(visible=False)
    
    with gr.Row():
        check_button = gr.Button("Check Answer", variant="primary")
        save_button = gr.Button("Save Study Session", variant="primary")
    
    demo.load(fn=init_game, outputs=[study_session_state, current_group_state, english_output, answer_input, hidden_correct, hidden_word_id])
    
    check_button.click(fn=check_answer,
                       inputs=[answer_input, english_output, hidden_correct, review_items_state, hidden_word_id],
                       outputs=[result_success, result_error, review_items_state])
    check_button.click(fn=generate_word,
                       inputs=current_group_state,
                       outputs=[english_output, answer_input, hidden_correct, hidden_word_id])
    
    save_button.click(fn=save_study_session,
                      inputs=[study_session_state, review_items_state, current_group_state],
                      outputs=[study_session_state, review_items_state])
    save_button.click(lambda: gr.update(value="", visible=False), outputs=result_error)
    
    gr.Markdown("Save progress and close the tab when finished.")
    with gr.Row(elem_classes="center"):
        gr.Image(
            value="writing-practice.png", 
            show_label=False,
            show_download_button=False,
            show_fullscreen_button=False,
            container=False
        )

demo.launch(server_name="0.0.0.0")
