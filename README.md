# 🏥 Multi-Agent Healthcare Assistant

This project is a modular FastAPI-based application designed to simulate a real-world clinical assistant powered by multiple AI agents. It supports clinical note analysis, medical image interpretation, and structured SOAP note generation — all powered by large language and vision models.

![Multi-Agent Medical System](artifacts/multi-agent.png)
---

## 🚀 Features

- 🧠 **ICD-10 Code Extraction**  
  Extracts ICD-10 codes from free-text clinical notes using NLP models.

- 🖼️ **Medical Image Analysis**  
  Supports analysis of radiology images (X-ray, MRI, etc.) using multimodal models like MedGemma.

- 📋 **SOAP Note Generation**  
  Generates structured SOAP notes from raw clinical transcripts.

- 🧩 **Multi-Agent Architecture**  
  Built with modular agents for each task, easily extensible and integrated via `agentic_workflow.py`.

- 🔌 **FastAPI Backend**  
  Exposes an endpoint to upload both clinical text and medical images.

The user input goes through the router agent. The router agent analyzes the input, and routes the input to either icd10 code generation agent, soap generation agent or image analysis agent.

All the agents use MedGemma model as the LLM. The LLM is run locally via **Ollama**. In order to reduce the latency and memory usage, a quantized model is used. 


Here is an architecture diagram:

![Workflow Graph](artifacts/langgraph_workflow.png)

---

## 🎬 Demo

Watch a quick demo of the Multi-Agent Medical System in action:

[<video src="artifacts/demo.mp4" controls width="600"></video>
](https://github.com/user-attachments/assets/d5451b68-ee10-4f70-8876-39fdf3886654)


---

## 📊 Monitoring


The app is monitored using LangSmith (optional).

![Langgraph Runs](artifacts/runs.png)

---
## 📝 Requirements

- **OS**: Windows, macOS, or Linux
- **RAM**: 8 GB minimum (the quantized 4B model uses ~3 GB)
- **Ollama**: Download from [https://ollama.com](https://ollama.com)
- **Python**: 3.11+

---

## 📦 Installation

### 1. Install Ollama

Download and install Ollama from [https://ollama.com](https://ollama.com).

After installation, pull the MedGemma model:
```bash
ollama pull medgemma
```

> **Note:** The model will be automatically downloaded (~2.5 GB) on first use if you skip this step.

### 2. Clone the repo

```bash
git clone https://github.com/joyceannie/Multi_Agent_Medical_System.git
cd Multi_Agent_Medical_System
```

### 3. Setup Python environment
```bash
python -m venv venv

# Windows:
venv\Scripts\activate

# macOS/Linux:
# source venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Setup .env file (Optional — for LangSmith monitoring)
Create a `.env` file in the root directory:
```bash
LANGCHAIN_TRACING_V2="true"
LANGCHAIN_ENDPOINT="<your-langsmith-endpoint>"
LANGCHAIN_API_KEY="your-langsmith-api-key"
LANGCHAIN_PROJECT="your-langsmith-project"
```

> If you don't need LangSmith monitoring, you can skip this step. The app will work without it.

### 5. Start Ollama
Make sure Ollama is running before starting the app:
```bash
ollama serve
```

> On Windows, Ollama usually runs as a background service automatically after installation.

### 6. Run the app
```bash
uvicorn app.main:app --reload
```

Go to http://localhost:8000 and interact with the app.



