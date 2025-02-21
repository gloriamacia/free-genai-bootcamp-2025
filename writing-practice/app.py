import gradio as gr
import requests
import random

# Backend URL
BACKEND_URL = "http://127.0.0.1:5000"

def fetch_random_word():
    try:
        groups_response = requests.get(f"{BACKEND_URL}/groups")
        groups_response.raise_for_status()
        groups_data = groups_response.json()
        groups = groups_data.get("groups", [])
        if not groups:
            return None, "❌ No groups found."
        random_group = random.choice(groups)
        group_id = random_group["id"]
        group_name = random_group["group_name"]
        words_response = requests.get(f"{BACKEND_URL}/groups/{group_id}/words/raw")
        words_response.raise_for_status()
        words_data = words_response.json()
        words = words_data.get("words", [])
        if not words:
            return None, f"🟡 No words found in group '{group_name}'."
        random_word = random.choice(words)
        catalan = random_word.get("catalan", "Unknown")
        english = random_word.get("english", "Unknown")
        return english, catalan
    except requests.exceptions.RequestException as e:
        return None, f"❌ Error fetching data: {e}"

def generate_word():
    english_word, correct_catalan = fetch_random_word()
    if not english_word:
        return "", "", correct_catalan
    # Return a new English word, clear the answer input, and store the correct translation (hidden)
    return english_word, "", correct_catalan

def check_answer(user_input, english_word, correct_catalan):
    if user_input.strip().lower() == correct_catalan.lower():
        success_message = f"<p style='color:green;'>✅ Correct! '{english_word}' in Catalan is '{correct_catalan}'.</p>"
        return gr.update(value=success_message, visible=True), gr.update(value="", visible=False)
    else:
        error_message = f"<p style='color:red;'>❌ Incorrect. '{english_word}' in Catalan is '{correct_catalan}'.</p>"
        return gr.update(value="", visible=False), gr.update(value=error_message, visible=True)

with gr.Blocks() as demo:
    gr.Markdown("# English to Catalan Translation Game")
    with gr.Row():
        english_output = gr.Textbox(label="English Word", interactive=False)
        answer_input = gr.Textbox(label="Your Answer in Catalan")
    
    # Hidden field to store the correct translation
    hidden_correct = gr.Textbox(visible=False)
    
    # Two Markdown components used for results:
    # result_success will show a success message (styled in green)
    # result_error will show an error message (styled in red)
    result_success = gr.Markdown(visible=False)
    result_error = gr.Markdown(visible=False)
    
    with gr.Row():
        generate_button = gr.Button("Generate")
        check_button = gr.Button("Check Answer")
    
    # When "Generate" is clicked, update the English word and clear the answer field.
    generate_button.click(fn=generate_word, outputs=[english_output, answer_input, hidden_correct])
    # Also clear any previous result messages when generating a new word.
    generate_button.click(
        lambda: (gr.update(value="", visible=False), gr.update(value="", visible=False)),
        outputs=[result_success, result_error]
    )
    
    # When "Check Answer" is clicked, update the result components accordingly.
    check_button.click(
        fn=check_answer,
        inputs=[answer_input, english_output, hidden_correct],
        outputs=[result_success, result_error]
    )
    
    # Automatically generate a word on page load.
    demo.load(fn=generate_word, outputs=[english_output, answer_input, hidden_correct])

demo.launch()
