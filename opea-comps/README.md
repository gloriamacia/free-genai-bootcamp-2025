# Running Ollama Third-Party Service

## Choosing a Model

You can get the model_id that ollama will launch from the [Ollama Library](https://ollama.com/library).

https://ollama.com/library/llama3.2

eg. LLM_MODEL_ID="llama3.2:1b"

### Getting the Host IP

#### Mac

```sh
docker compose up
```

### Ollama API

Once the Ollama server is running we can make API calls to the ollama API

https://github.com/ollama/ollama/blob/main/docs/api.md

## Download (Pull) a model

```bash
curl http://localhost:8008/api/pull -d '{
  "model": "llama3.2:1b"
}'
```

## Generate a Request

```bash
curl http://localhost:8008/api/generate -d '{
  "model": "llama3.2:1b",
  "prompt": "Why is the sky blue?",
  "stream":"false
}'
```