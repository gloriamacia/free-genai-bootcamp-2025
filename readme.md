# 🚀 Free Genai Bootcamp 2025

#### Weeks Of Free Online GenAI Training And Hands-on Programming created by Andrew Brown, the team of ExamPro and amazing instructors 

---

###  Fictional Theme of the Bootcamp

Our fictional startup is building an AI-powered language learning platform designed to teach Catalan to English-speaking learners. The vision is to create an immersive, playful, and highly interactive learning experience using cutting-edge Generative AI. 

🟢 Visual inspiration is drawn from Duolingo, as a respectful homage to their mission of making language learning accessible and free for everyone. However, Duolingo currently only supports learning Catalan from Spanish, which creates a barrier for the growing number of international residents, travelers, and students who come to Barcelona and Catalonia from around the world and want to integrate locally.

🌍 Our project bridges that gap—bringing Catalan learning directly to English speakers, empowering them to better connect with the language, culture, and people of Catalonia.

--- 

### Eager to learn Catalan? 

The Catalan learning platform is publicly accessible 

http://learncatalan.net

![alt text](readme-images/dashboard.png)

It offers four interactive study activities: **Writing Practice**, **Listening Practice**, **Song Practice**, and **Speaking Practice**,

![alt text](readme-images/study_activities.png)

Awesome! Here's a fully updated and improved version of your `### EC2 Deployment` section, now including Docker Compose, containerization, and EC2 security group setup:

---

### ☁️ EC2 Deployment  

The application is deployed on an **Amazon EC2 instance**, using **Docker Compose** to manage and run the full multi-service setup. A **custom domain** was purchased via **AWS Route 53**, which handles DNS routing to the EC2 instance's public IP.

Before deployment, the entire app was **containerized**, with each major component — backend (Flask), frontend (React), and individual study tools (Gradio, Streamlit, etc.) — built as separate **Docker services**. These were defined and orchestrated using a `docker-compose.yml` file to ensure smooth coordination between containers.

Here's a high-level breakdown of the setup:
- 🐳 **Docker Compose** manages multiple services:
  - `backend` (Flask API with SQLite DB)
  - `frontend` (React app served via Nginx)
  - Gradio/Streamlit-based apps: `writing-practice`, `listening-practice`, `song-vocabulary`, `speaking-practice`
  
- Each app is exposed on a unique port (e.g., 7860, 7861…) and isolated in its own container.
- Environment variables and secrets are passed securely using `.env` files for services that require API credentials (e.g., AWS, OpenAI).
- Data such as the SQLite database is mounted as a volume for persistence.

🛡️ **Security Group Configuration** on EC2:
To make the app publicly accessible and ensure each microservice runs properly, the EC2 instance was configured with an appropriate **security group**, allowing inbound traffic on the required ports:
- `5173` for the frontend (React)
- `5001` for the backend (Flask)
- `7860–7863` for individual AI practice tools
- `80` and `443` (optional, for HTTP/HTTPS)

🌐 **Custom Domain with Route 53**:
- A domain was purchased via **AWS Route 53**
- An **A Record** was created in the hosted zone to point the domain to the EC2 instance’s public IPv4 address

---

### ✍️ Writing Practice
This app helps learners reinforce vocabulary through active recall. The learner selects a word group (e.g., adjectives), and is presented with words to translate into Catalan. After each response, the app provides immediate feedback on accuracy.

Performance data is saved to the language portal database, showing how many times each word was translated correctly—both within the current session and across past sessions.

### 🎧 Listening Practice

This app lets learners choose a dialogue topic, then generates a Catalan conversation using Anthropic’s LLM through AWS Bedrock. The dialogue is voiced using AWS Polly for a natural listening experience.
After listening, learners answer a multiple-choice question to check their comprehension.


### 🎵 Song Practice
This app helps learners explore Catalan songs interactively using an LLM-powered agent. You simply enter the title of a Catalan song (optionally with the artist), and the agent takes over using three specialized tools:

* 🔍 Search Tool – Finds the full lyrics using DuckDuckGo.
* 🧠 Vocabulary Extractor – Identifies key or challenging Catalan words.
* 💬 Word Explainer – Provides clear English definitions and example sentences.

Behind the scenes, an autonomous language model agent from OpenAI coordinates all three tools to deliver a personalized and language-rich learning experience.

⚠️ **EC2 Deployment**: DuckDuckGo may occasionally block search requests originating from EC2 instances, which can cause the app to temporarily stop working.

### 🗣️ Speaking Practice

This app helps learners improve their spoken Catalan by presenting them with images of traditional Catalan scenes and asking them to describe what they see — all within one minute. The spoken response is transcribed using OpenAI Whisper and evaluated against the CEFR framework to provide a proficiency level.

⚠️ **EC2 Deployment**:
Due to [gradio limitations](https://discuss.huggingface.co/t/microphone-access-for-a-deployed-gradio-app-on-e2/108335), the microphone cannot capture capture audio when deployed on EC2 without HTTPS. Unfortunately, adding HTTPS in Flask can be complex, as its built-in development server isn’t intended for production use and lacks native HTTPS support. 

In retrospect, a different AWS deployment option might have been more suitable than EC2, but I was unaware of this limitation when I first set sail with it and I wished to keep it simple. That said, cloud deployment was not the main focus of the bootcamp — the app works perfectly in local environments, and instructions for running it locally are provided below.

### Run Locally 

TBD