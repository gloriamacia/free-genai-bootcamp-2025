import gradio as gr
import json
import requests
from html2text import HTML2Text
from openai import OpenAI
from duckduckgo_search import DDGS
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

# Create a custom theme with dark mode settings:
theme = gr.themes.Default(font=[GoogleFont("Nunito")]).set(
    button_primary_background_fill="#55CD02",
    button_primary_background_fill_dark="#55CD02",
    body_background_fill_dark="#333333",
    button_primary_background_fill_hover_dark="#89E219"
)

# --- Helper Functions ---
def search_web(query: str) -> str:
    results = DDGS().text(query, max_results=10)
    if results:
        return [
            {"title": result["title"], "url": result["href"]}
            for result in results
        ]
    return []

def get_page_content(url: str) -> str:
    response = requests.get(url)
    h = HTML2Text()
    h.ignore_links = False
    content = h.handle(response.text)
    return content[:4000] if len(content) > 4000 else content

def extract_vocabulary(text: str) -> list:
    words = set(text.lower().split())
    vocabulary = [word for word in words if word.isalpha()]
    return sorted(vocabulary)

tools = [
    {
        "type": "function",
        "function": {
            "name": "search_web",
            "description": "Search the web for information.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The query to search the web for.",
                    },
                },
                "required": ["query"],
                "additionalProperties": False,
            },
            "strict": True,
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_page_content",
            "description": "Get the content of a web page.",
            "parameters": {
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "The URL of the web page.",
                    },
                },
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "extract_vocabulary",
            "description": "Extract new vocabulary from a text.",
            "parameters": {
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "The text to extract new vocabulary from.",
                    },
                },
                "required": ["text"],
                "additionalProperties": False,
            },
            "strict": True,
        },
    },
]

user_language = "English"
foreign_language = "Catalan"

def run_app(song_title: str, user_api_key: str):
    # Initialize the OpenAI client using the provided API key.
    client = OpenAI(api_key=user_api_key)
    
    messages = [
        {
            "role": "system",
            "content": f"""
You are a helpful language tutor. 
When the user provides a song title, search for the song lyrics and help them learn new vocabulary from it. 
First search for the lyrics, then extract vocabulary from them. 
Explain the meaning of new words in simple terms and provide example sentences. 
Use the user's native language to explain the meaning of new words.
Focus on words that would be valuable for a language learner.
The user's native language is {user_language}.
The language of the foreign song the user is learning is {foreign_language}.
            """,
        },
        {
            "role": "user",
            "content": f"help me learn about the song '{song_title}'",
        },
    ]
    goal_achieved = False
    limit = 10

    while not goal_achieved and len(messages) < limit:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            tools=tools,
        )
        messages.append(completion.choices[0].message)

        if completion.choices[0].message.tool_calls:
            for tool_call in completion.choices[0].message.tool_calls:
                arguments = json.loads(tool_call.function.arguments)
                if tool_call.function.name == "search_web":
                    result = search_web(arguments["query"])
                elif tool_call.function.name == "get_page_content":
                    result = get_page_content(arguments["url"])
                elif tool_call.function.name == "extract_vocabulary":
                    result = extract_vocabulary(arguments["text"])
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": str(result),
                })
        else:
            goal_achieved = True

    return messages[-1].content

# --- Gradio Blocks Interface ---
with gr.Blocks(js=js_func, theme=theme, css="""
.center {
    display: flex;
    justify-content: center;
    width: 100%;
    margin: 0 auto;
}
""") as demo:
    gr.Markdown("<h1 style='text-align:center;'>Learn Catalan with Songs 🎵</h1>")
    
    # Wrap the two columns in a row for a side-by-side layout.
    with gr.Row():
        # Left column with inputs and output.
        with gr.Column(scale=1):
            with gr.Row():
                song_title_input = gr.Textbox(label="Song Title", placeholder="Enter song title here")
                api_key_input = gr.Textbox(label="OpenAI API Key", placeholder="Enter your OpenAI API key here", type="password")
            submit_button = gr.Button("Submit", variant="primary")
            output_box = gr.Textbox(label="Output", interactive=False)
            
            submit_button.click(fn=run_app, inputs=[song_title_input, api_key_input], outputs=output_box)
        
        # Right column with the image.
        with gr.Column(scale=1):
            with gr.Row(elem_classes="center"):
                gr.Image(
                    value="oscar-sing.png", 
                    show_label=False,
                    show_download_button=False,
                    show_fullscreen_button=False,
                    container=False
                )

demo.launch(server_port=7862)
