import streamlit as st
import boto3
import json
from io import BytesIO
from pydub import AudioSegment

# Configure AWS clients for Polly and Bedrock Runtime.
polly = boto3.client('polly', region_name='us-east-1')
bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')

st.title("Exercici de Comprensió Oral en Català 👂🏽")
st.write("Introdueix un tema per al diàleg")

# User input for the topic
topic = st.text_input("Tema del diàleg", "vacances")

if st.button("Generar Diàleg"):
    # Build the creative prompt for the dialogue.
    prompt = (
        f'Genera un diàleg d\'un minut sobre el tema "{topic}" en castellà'
        'El diàleg ha de tenir dues veus diferents, identificades com "[Veu 1]:" i "[Veu 2]:". '
        'Tradueix el diàleg al català i retorna només la versió en català.'
        'Cada línia ha de començar amb "[Veu 1]:" o "[Veu 2]:".'
    )
    
    # Define system prompt and message list per the docs.
    system_list = [
        {
            "text": (
                "Actua com a assistent creatiu de redacció de diàlegs en català."
            )
        }
    ]
    message_list = [
        {"role": "user", "content": [{"text": prompt}]}
    ]
    inf_params = {"maxTokens": 1024, "topP": 0.9, "topK": 20, "temperature": 0.7}
    
    request_body = {
        "schemaVersion": "messages-v1",
        "system": system_list,
        "messages": message_list,
        "inferenceConfig": inf_params,
    }
    
    # Use the model ID per the docs (here we use a Nova Lite model as an example).
    MODEL_ID = "us.amazon.nova-lite-v1:0"
    
    dialogue_script = ""
    try:
        response = bedrock.invoke_model_with_response_stream(
            modelId=MODEL_ID,
            body=json.dumps(request_body)
        )
        
        stream = response.get("body")
        if stream:
            # Process the response stream to accumulate the generated text.
            for event in stream:
                chunk = event.get("chunk")
                if chunk:
                    chunk_bytes = chunk.get("bytes")
                    if chunk_bytes:
                        chunk_json = json.loads(chunk_bytes.decode())
                        # Extract the delta text if present.
                        content_block_delta = chunk_json.get("contentBlockDelta")
                        if content_block_delta:
                            dialogue_script += content_block_delta.get("delta", {}).get("text", "")
        else:
            st.error("No response stream received.")
    except Exception as e:
        st.error(f"Error generant el diàleg amb Bedrock: {e}")
    
    if dialogue_script:
        # st.subheader("Diàleg generat:")
        # st.text(dialogue_script)
        
        # Split the dialogue into lines.
        lines = [line.strip() for line in dialogue_script.strip().split("\n") if line.strip()]
        
        # List to store audio segments.
        audio_segments = []
        
        # Synthesize each line with the appropriate voice.
        for line in lines:
            if line.startswith("[Veu 1]:"):
                text_line = line[len("[Veu 1]:"):].strip()
                try:
                    response = polly.synthesize_speech(
                        Text=text_line,
                        OutputFormat='mp3',
                        VoiceId='Lucia',       # Female voice
                        LanguageCode='ca-ES'
                    )
                    audio_segments.append(response['AudioStream'].read())
                except Exception as e:
                    st.error(f"Error sintetitzant amb Veu 1: {e}")
            elif line.startswith("[Veu 2]:"):
                text_line = line[len("[Veu 2]:"):].strip()
                try:
                    response = polly.synthesize_speech(
                        Text=text_line,
                        OutputFormat='mp3',
                        VoiceId='Enrique',     # Male voice
                        LanguageCode='ca-ES'
                    )
                    audio_segments.append(response['AudioStream'].read())
                except Exception as e:
                    st.error(f"Error sintetitzant amb Veu 2: {e}")
        
        # Combine all audio segments into one MP3 file.
        if audio_segments:
            combined = AudioSegment.empty()
            for segment in audio_segments:
                audio_segment = AudioSegment.from_file(BytesIO(segment), format="mp3")
                combined += audio_segment
            combined_audio = BytesIO()
            combined.export(combined_audio, format="mp3")
            combined_audio.seek(0)
            
            st.subheader("Reproducció del diàleg combinat:")
            st.audio(combined_audio, format='audio/mp3')
