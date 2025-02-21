import gradio as gr
import requests
import random

# Backend URL
BACKEND_URL = "http://127.0.0.1:5000"

def get_random_group():
    try:
        response = requests.get(f"{BACKEND_URL}/groups")
        response.raise_for_status()
        data = response.json()
        groups = data.get("groups", [])
        if not groups:
            return None, "No groups found."
        random_group = random.choice(groups)
        group_id = random_group.get("id")
        # Try "group_name" first; if not available, use "name"
        group_name = random_group.get("group_name") or random_group.get("name", "Unknown")
        return group_id, f"Current Group: {group_name}"
    except Exception as e:
        return None, f"Error: {e}"

def fetch_random_word(current_group):
    try:
        # Fetch words only from the specified group.
        response = requests.get(f"{BACKEND_URL}/groups/{current_group}/words/raw")
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
    # Return a blank string for the answer input field.
    return english_word, "", correct_catalan, word_id

def init_game():
    group_id, group_text = get_random_group()
    if group_id is None:
        return None, group_text, "", "", "", ""
    english_word, blank, correct_catalan, word_id = generate_word(group_id)
    return group_id, group_text, english_word, blank, correct_catalan, word_id

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
        return study_session_id, []  # nothing to update
    if not study_session_id:
        # Use study_activity_id 2 for "Writing Practice"
        payload = {"group_id": current_group, "study_activity_id": 2}
        try:
            response = requests.post(f"{BACKEND_URL}/study-sessions", json=payload)
            response.raise_for_status()
            data = response.json()
            study_session_id = data["id"]
        except Exception as e:
            raise gr.Error(f"Failed to create study session: {e}")
    for item in review_items:
        payload = {"word_id": item["word_id"], "correct": item["correct"]}
        try:
            response = requests.post(f"{BACKEND_URL}/study-sessions/{study_session_id}/review", json=payload)
            response.raise_for_status()
        except Exception as e:
            raise gr.Error("Failed to save study session")
    gr.Info("💾 Study session saved!", duration=2)
    return study_session_id, []  # Clear review items after saving

with gr.Blocks() as demo:
    gr.Markdown("# English to Catalan Writing Practice")
    
    # States for study session, review items, and current group.
    study_session_state = gr.State(None)
    review_items_state = gr.State([])
    current_group_state = gr.State(None)
    current_group_display = gr.Markdown("Current Group: ", visible=True)
    
    with gr.Row():
        english_output = gr.Textbox(label="English Word", interactive=False)
        answer_input = gr.Textbox(label="Your Answer in Catalan")
    
    hidden_correct = gr.Textbox(visible=False)
    hidden_word_id = gr.Textbox(visible=False)
    
    result_success = gr.Markdown(visible=False)
    result_error = gr.Markdown(visible=False)
    
    with gr.Row():
        check_button = gr.Button("Check Answer")
        save_button = gr.Button("Save Study Session")
    
    # On page load, initialize the game.
    demo.load(fn=init_game, outputs=[current_group_state, current_group_display, english_output, answer_input, hidden_correct, hidden_word_id])
    
    # When "Check Answer" is clicked:
    # 1. Evaluate the answer and update review items.
    check_button.click(fn=check_answer,
                       inputs=[answer_input, english_output, hidden_correct, review_items_state, hidden_word_id],
                       outputs=[result_success, result_error, review_items_state])
    # 2. Immediately generate a new word.
    check_button.click(fn=generate_word,
                       inputs=current_group_state,
                       outputs=[english_output, answer_input, hidden_correct, hidden_word_id])
    
    # "Save Study Session": create a session if needed, then send recorded reviews.
    save_button.click(fn=save_study_session,
                      inputs=[study_session_state, review_items_state, current_group_state],
                      outputs=[study_session_state, review_items_state])
    # Optionally clear any error message after saving.
    save_button.click(lambda: gr.update(value="", visible=False), outputs=result_error)

demo.launch()
