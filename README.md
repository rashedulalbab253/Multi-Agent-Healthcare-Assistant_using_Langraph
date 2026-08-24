# 🏥 Multi-Agent Healthcare Assistant

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688.svg?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![LangGraph](https://img.shields.io/badge/Orchestration-LangGraph-FF6F00.svg)](https://github.com/langchain-ai/langgraph)
[![Ollama](https://img.shields.io/badge/Inference-Ollama%20(MedGemma)-white.svg?logo=ollama)](https://ollama.com)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg?logo=docker&logoColor=white)](https://hub.docker.com/r/rashedulalbab1234/multi-agent-healthcare-assistant)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

An intelligent clinical assistant system powered by **LangGraph**, **FastAPI**, and **MedGemma** (running locally via Ollama). It coordinates specialized AI agents to extract ICD-10 diagnostic codes, perform multimodal radiology image interpretations, and synthesize structured SOAP notes from clinical encounters.

![Multi-Agent Medical System](artifacts/multi-agent.png)

---

## 📑 Table of Contents
- [Key Features](#-key-features)
- [Agentic Architecture](#-agentic-architecture)
- [Project Structure](#-project-structure)
- [🎬 Demo](#-demo)
- [Prerequisites](#-prerequisites)
- [Quick Start](#-quick-start)
- [Installation & Setup](#-installation--setup)
- [Docker Deployment](#-docker-deployment)
- [CI/CD — GitHub Actions](#-cicd--github-actions)
- [API Reference](#-api-reference)
- [Observability & Monitoring](#-observability--monitoring)
- [License](#-license)

---

## 🚀 Key Features

* 🧠 **Automated ICD-10 Extraction**: Parses free-text clinical transcripts and extracts relevant ICD-10 diagnostic codes along with clinical descriptions.
* 🖼️ **Multimodal Radiology Analysis**: Interprets medical imaging (X-rays, MRIs, CT scans) using multimodal vision-language models to report technique, findings, impressions, and recommendations.
* 📋 **Structured SOAP Generation**: Synthesizes Subjective, Objective, Assessment, and Plan (SOAP) clinical documentation from raw patient consultation transcripts.
* 🔀 **Intelligent Routing**: Employs a supervisor/router agent that dynamically analyzes inputs and dispatches tasks to the appropriate specialized sub-agent.
* 🔒 **Local & Privacy-Preserving**: Runs LLM inference locally using quantized **MedGemma** models via Ollama to safeguard sensitive clinical data.

---

## 🧩 Agentic Architecture

The system coordinates agents using a **LangGraph StateGraph**:

```
                  ┌────────────────────────┐
                  │      User Input        │
                  │ (Text Note and/or Img) │
                  └───────────┬────────────┘
                              │
                              ▼
                  ┌────────────────────────┐
                  │      Router Agent      │
                  └───────────┬────────────┘
                              │
         ┌────────────────────┼────────────────────┐
         ▼                    ▼                    ▼
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│   ICD-10 Agent  │  │   SOAP Agent    │  │ Image Analyzer  │
│ (Codes & Descs) │  │  (S-O-A-P Note) │  │(Radiology Report│
└────────┬────────┘  └────────┬────────┘  └────────┬────────┘
         │                    │                    │
         └────────────────────┼────────────────────┘
                              ▼
                  ┌────────────────────────┐
                  │    Unified Response    │
                  └────────────────────────┘
```

![LangGraph Workflow](artifacts/langgraph_workflow.png)

---

## 📂 Project Structure

```text
├── app/
│   ├── agents/                   # Specialized LangGraph agent definitions
│   │   ├── base_agent.py         # Base agent class
│   │   ├── router_agent.py       # Intent router (icd10, soap, image_analysis)
│   │   ├── icd10_agent.py        # ICD-10 extraction agent
│   │   ├── soap_generator_agent.py # SOAP note generator agent
│   │   └── image_analyzer_agent.py # Vision/radiology analysis agent
│   ├── api/                      # FastAPI routes & Pydantic response schemas
│   │   ├── analyze.py            # POST /api/analyze endpoint
│   │   └── schemas.py            # Response data models
│   ├── config/                   # Configuration & environment loader
│   ├── graph/                    # LangGraph StateGraph & workflow builder
│   │   ├── graph_builder.py      # Graph composition & routing logic
│   │   └── types.py              # State definitions
│   ├── static/                   # Frontend user interface (HTML/CSS/JS)
│   ├── utils/                    # Model loaders, image processors, and logger
│   └── main.py                   # FastAPI app entrypoint
├── evaluations/                  # Synthetic clinical datasets & benchmarks
├── experiments/                  # Jupyter notebooks for model experiments
├── artifacts/                    # Architecture diagrams, screenshots, demo media
├── .github/workflows/            # GitHub Actions CI/CD automation
├── Dockerfile                    # Container image specification
├── docker-compose.yml            # Multi-container orchestration (App + Ollama)
└── requirements.txt              # Project dependencies
```

---

## 🎬 Demo

Watch a quick demo of the Multi-Agent Healthcare Assistant in action:

https://github.com/user-attachments/assets/d5451b68-ee10-4f70-8876-39fdf3886654

---

## 📋 Prerequisites

* **OS**: Linux, macOS, or Windows
* **Python**: 3.11+
* **RAM**: 8 GB minimum (Quantized MedGemma requires ~3 GB VRAM/RAM)
* **Ollama**: [Download & install Ollama](https://ollama.com)

---

## ⚡ Quick Start

```bash
# 1. Pull the MedGemma model
ollama pull medgemma

# 2. Install dependencies
pip install -r requirements.txt

# 3. Start the application
uvicorn app.main:app --reload

# 4. Open in browser: http://localhost:8000
```

---

## 📦 Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/rashedulalbab253/Multi-Agent-Healthcare-Assistant_using_Langraph.git
cd Multi-Agent-Healthcare-Assistant_using_Langraph
```

### 2. Setup Python Environment
```bash
python -m venv venv

# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Configure Environment Variables (Optional)
To enable **LangSmith** monitoring and custom Ollama endpoints, create a `.env` file in the root directory:
```env
LANGCHAIN_TRACING_V2="true"
LANGCHAIN_ENDPOINT="https://api.smith.langchain.com"
LANGCHAIN_API_KEY="your-langsmith-api-key"
LANGCHAIN_PROJECT="healthcare-assistant"
OLLAMA_BASE_URL="http://localhost:11434"
```

> If you don't need LangSmith tracing, you can skip this step. The app runs fully offline by default.

### 4. Run Ollama Server
Ensure the Ollama service is active:
```bash
ollama serve
```

### 5. Launch the Server
```bash
uvicorn app.main:app --reload
```
Navigate to `http://localhost:8000` to interact with the application.

---

## 🐳 Docker Deployment

Run the complete multi-agent system and Ollama server with a single command using Docker Compose:

```bash
docker-compose up --build
```

This will:
1. Start the **Ollama** service and automatically pull the `medgemma` model on first launch (persisted in a Docker volume).
2. Start the **FastAPI** application container once Ollama passes health checks.
3. Expose the web application at **http://localhost:8000**.

To stop the containers:
```bash
docker-compose down
```

---

## 🔄 CI/CD — GitHub Actions

Every push to `main` automatically triggers a GitHub Actions workflow to build and publish the Docker image to Docker Hub.

* **Image:** [`rashedulalbab1234/multi-agent-healthcare-assistant`](https://hub.docker.com/r/rashedulalbab1234/multi-agent-healthcare-assistant)

### Required Repository Secrets
Configure the following secrets in **Settings → Secrets and variables → Actions**:

| Secret Name | Description |
|---|---|
| `DOCKERHUB_USERNAME` | Your Docker Hub username |
| `DOCKERHUB_TOKEN` | Docker Hub Access Token |

### Pull the Pre-Built Image
```bash
docker pull rashedulalbab1234/multi-agent-healthcare-assistant:latest
```

---

## 🔌 API Reference

### `POST /api/analyze`
Submits clinical notes, medical imagery, or both for automated analysis.

**Form Data Parameters:**
| Parameter | Type | Required | Description |
|---|---|---|---|
| `note` | `string` | Optional* | Free-text clinical transcript or encounter note |
| `image` | `file` | Optional* | Medical image (`.png`, `.jpg`, `.jpeg`) |

*\*At least one of `note` or `image` must be provided.*

#### Example Response (SOAP Agent):
```json
{
  "agent": "soap",
  "result": {
    "Subjective": "Patient reports persistent dry cough and mild fever for 3 days...",
    "Objective": "Vitals: BP 120/80, Temp 100.4F. Lungs clear to auscultation bilaterally...",
    "Assessment": "Acute upper respiratory tract infection...",
    "Plan": "Symptomatic treatment with rest, hydration, and OTC antipyretics..."
  }
}
```

#### Example Response (ICD-10 Agent):
```json
{
  "agent": "icd10",
  "result": [
    {
      "code": "J06.9",
      "description": "Acute upper respiratory infection, unspecified"
    }
  ]
}
```

---

## 📊 Observability & Monitoring

Agent execution chains, token metrics, and latency are monitored with **LangSmith**:

![LangSmith Tracing](artifacts/runs.png)

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
