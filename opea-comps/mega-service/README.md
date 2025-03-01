# How to Run the LLM Service  

We use **Ollama**, delivered via **Docker Compose**, to run the LLM service.  

## Setting the LLM Service Port  

You can specify the port the LLM will listen on. The recommended port is **9000**, as it aligns with many default **OPEA megaservice** ports. If not set, it defaults to **8008**.  

Start the service using:  

```sh
LLM_ENDPOINT_PORT=9000 docker compose up
```

## Downloading (Pulling) a Model  

When you first start Ollama, it **does not include a pre-downloaded model**. You need to download a model via the Ollama API.  

Run the following command to download the **LLaMA 3.2 (1B model)**:  

```sh
curl -X POST http://localhost:9000/api/pull -d '{
  "model": "llama3.2:1b"
}'
```

## Accessing the Jaeger UI  

When you start Docker Compose, it should automatically launch **Jaeger** for tracing.  

You can access the **Jaeger UI** at:  

```sh
http://localhost:16686/
```

## Running the Mega Service Example  

To start the **Mega Service**, run:  

```sh
python app.py
```

## Testing the Application  

### Run a Sample Request  

Navigate to the **OPEA Mega Service directory**:  

```sh
cd opea-comps/mega-service
```

### Request 

To store the combined response chunks into a single file, run:  

```sh
curl -s -X POST http://localhost:9000/v1/example-service \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {"role": "user", "content": "When will humans land on Mars?"}
    ],
    "model": "llama3.2:1b",
    "max_tokens": 100,
    "temperature": 0.7,
    "stream": false
  }' 
```