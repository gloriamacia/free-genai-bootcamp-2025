import gradio as gr
import requests
import random

# Backend URL
BACKEND_URL = "http://127.0.0.1:5000"

def start_study_session():
    # Create a study session using default values (adjust as needed)
    payload = {"group_id": 1, "study_activity_id": 1}
    try:
        response = requests.post(f"{BACKEND_URL}/study-sessions", json=payload)
        response.raise_for_status()
        data = response.json()
        session_id = data["id"]
        return session_id
    except Exception as e:
        raise gr.Error(f"Failed to create study session: {e}")

def fetch_random_word():
    try:
        # First, get the first page to determine total_pages
        response = requests.get(f"{BACKEND_URL}/words?page=1")
        response.raise_for_status()
        data = response.json()
        total_pages = data.get("total_pages", 1)
        # Choose a random page between 1 and total_pages
        random_page = random.randint(1, total_pages)
        # Fetch words from the chosen page
        response = requests.get(f"{BACKEND_URL}/words?page={random_page}")
        response.raise_for_status()
        data = response.json()
        words = data.get("words", [])
        if not words:
            return None, "🟡 No words found.", None
        random_word = random.choice(words)
        english = random_word.get("english", "Unknown")
        catalan = random_word.get("catalan", "Unknown")
        word_id = random_word.get("id", None)
        return english, catalan, word_id
    except requests.exceptions.RequestException as e:
        return None, f"❌ Error fetching data: {e}", None

def generate_word():
    english_word, correct_catalan, word_id = fetch_random_word()
    if not english_word:
        return "", "", correct_catalan, None
    # Return the new English word, clear the answer input, store the correct translation and the word id (both hidden)
    return english_word, "", correct_catalan, word_id

def check_answer(user_input, english_word, correct_catalan, review_items, current_word_id):
    # Compare user input with the correct answer (case-insensitive)
    correct = user_input.strip().lower() == correct_catalan.lower()
    if correct:
        message = f"<p style='color:green;'>✅ Correct! '{english_word}' in Catalan is '{correct_catalan}'.</p>"
    else:
        message = f"<p style='color:red;'>❌ Incorrect. '{english_word}' in Catalan is '{correct_catalan}'.</p>"
    # Update review items state
    review_items = review_items or []
    review_items.append({"word_id": current_word_id, "correct": correct})
    # Use gr.update on two Markdown components (one for success, one for error)
    if correct:
        return gr.update(value=message, visible=True), gr.update(value="", visible=False), review_items
    else:
        return gr.update(value="", visible=False), gr.update(value=message, visible=True), review_items

def save_study_session(study_session_id, review_items):
    messages = []
    for item in review_items:
        payload = {"word_id": item["word_id"], "correct": item["correct"]}
        try:
            response = requests.post(f"{BACKEND_URL}/study-sessions/{study_session_id}/review", json=payload)
            response.raise_for_status()
            messages.append(f"Saved word {item['word_id']}")
        except Exception as e:
            messages.append(f"Failed to save word {item['word_id']}: {e}")
    # Clear review_items after saving
    return "Study session saved: " + "; ".join(messages), []

with gr.Blocks() as demo:
    gr.Markdown("# English to Catalan Translation Game")
    
    # States to hold the study session id and the list of review items
    study_session_state = gr.State(None)
    review_items_state = gr.State([])
    
    with gr.Row():
        english_output = gr.Textbox(label="English Word", interactive=False)
        answer_input = gr.Textbox(label="Your Answer in Catalan")
    
    # Hidden fields to store the correct translation and the current word id
    hidden_correct = gr.Textbox(visible=False)
    hidden_word_id = gr.Textbox(visible=False)
    
    # Two Markdown components to display result messages:
    # result_success for correct answers, result_error for incorrect answers.
    result_success = gr.Markdown(visible=False)
    result_error = gr.Markdown(visible=False)
    
    with gr.Row():
        generate_button = gr.Button("Generate")
        check_button = gr.Button("Check Answer")
        save_button = gr.Button("Save Study Session")
    
    # On page load, create a study session and generate the first word.
    demo.load(fn=start_study_session, outputs=study_session_state)
    demo.load(fn=generate_word, outputs=[english_output, answer_input, hidden_correct, hidden_word_id])
    
    # "Generate" fetches a new word and clears previous answer and result messages.
    generate_button.click(fn=generate_word, outputs=[english_output, answer_input, hidden_correct, hidden_word_id])
    generate_button.click(
        lambda: (gr.update(value="", visible=False), gr.update(value="", visible=False)),
        outputs=[result_success, result_error]
    )
    
    # "Check Answer" evaluates the user's translation and updates review_items.
    check_button.click(
        fn=check_answer,
        inputs=[answer_input, english_output, hidden_correct, review_items_state, hidden_word_id],
        outputs=[result_success, result_error, review_items_state]
    )
    
    # "Save Study Session" sends each recorded review to the backend and then clears the review list.
    save_button.click(
        fn=save_study_session,
        inputs=[study_session_state, review_items_state],
        outputs=[result_success, review_items_state]
    )
    # Optionally clear any error message after saving.
    save_button.click(lambda: gr.update(value="", visible=False), outputs=result_error)

demo.launch()
