# 🇵🇪 GitHub Peru Analytics - Homework 2

A comprehensive data pipeline and dashboard for analyzing the GitHub developer ecosystem in Peru. This project extracts data from over 1,000 Peruvian developers, classifies their repositories into industry categories using AI (GPT-4), and visualizes the results in a multi-page interactive dashboard.

## 🚀 Project Overview

This tool identifies and analyzes technical trends, industry distributions, and developer performance metrics specifically for users located in Peru.

### Key Features:
- **Massive Data Extraction**: Fetches full profile details for 1,000+ Peruvian users and their latest repositories.
- **AI-Powered Industry Classification**: Uses GPT-4o-mini to categorize projects based on the International Standard Industrial Classification (CIIU).
- **Advanced Metrics**: Calculates h-index, engagement scores, and project-per-year ratios for all developers.
- **Interactive Dashboard**: A 6-page Streamlit application with deep-dive analytics.
- **AI Insights Agent**: A chatbot trained on the ecosystem data to answer technical questions.

---

## 📂 Repository Structure

```
github-peru-analytics/
├── .env.example             # Template for API keys (REQUIRED)
├── .gitignore               # Standard Python gitignore
├── README.md                # This file
├── requirements.txt         # Project dependencies
├── streamlit_app.py         # Root entry point for Streamlit Cloud
│
├── app/                     # Streamlit Dashboard
│   ├── main.py              # Main entry point (Streamlit)
│   ├── pages/               # Dashboard sub-pages (Overview, Developers, etc.)
│   └── components/          # Reusable UI components
│
├── data/                    # Data Storage
│   ├── processed/           # Cleaned and classified CSVs
│   │   ├── users.csv
│   │   ├── repositories.csv
│   │   └── classifications.csv
│   └── metrics/             # Calculated performance files
│       └── user_metrics.csv
│
├── src/                     # Core Source Code
│   ├── extraction/          # GitHub API logic
│   ├── classification/      # OpenAI API logic
│   ├── metrics/             # Math & Calculation logic
│   └── agents/              # AI Insights Agent
│
└── scripts/                 # Easy-run Wrappers
    ├── extract_users.py
    ├── extract_repos.py
    ├── classify_repos.py
    ├── calculate_metrics.py
    └── run_dashboard.py
```

---

## 🛠️ Setup Instructions

### 1. Requirements
Ensure you have Python 3.8+ installed.

### 2. Environment Configuration
1. Copy `.env.example` to `.env`.
2. Add your **GitHub Personal Access Token** (`GITHUB_TOKEN`).
3. Add your **OpenAI API Key** (`OPENAI_API_KEY`).

### 3. Installation
```bash
pip install -r requirements.txt
```

---

## 📈 Data Pipeline Execution

Run the scripts in order to build the dataset:

1. **Extract Users**: `python scripts/extract_users.py`
2. **Extract Repos**: `python scripts/extract_repos.py`
3. **Classify Repos**: `python scripts/classify_repos.py`
4. **Finalize Metrics**: `python scripts/calculate_metrics.py`

---

## 📊 Running the Dashboard

Launch the interactive analytics platform:
```bash
python scripts/run_dashboard.py
```
*Or directly use streamlit:* `streamlit run app/main.py`

---

## 🤖 AI Insights Agent

You can interact with the AI Agent in two ways:

### 1. Through the Dashboard (GUI)
- Run `python scripts/run_dashboard.py`.
- Navigate to the **"06 AI Insights"** page in the sidebar.
- Type your questions in the chat interface.

### 2. Through the Terminal (CLI)
Run the dedicated chat script:
```bash
python scripts/chat_with_agent.py
```

### Example Questions:
- "What are the top 3 industries for developers using Python in Peru?"
- "Which city has the most active GitHub community?"
- "Give me a summary of the technical maturity of the Peruvian ecosystem."

---

## 📸 Antigravity AI Implementation

This project was built using **Antigravity AI**, showcasing an end-to-end agentic workflow including data engineering, AI integration, and front-end development.

> [!TIP]
> **Insert Screenshot Here**: (User, please take a screenshot of our conversation and the final dashboard and place it here as per assignment requirements).

---

## 📺 Video Demonstration
A video tour of the project can be found at: [Link to Video] (User, please record your demo and update this link).

---

## 🎓 Author
**Julia** - *Homework 2 for Prompt Engineering Course*

---

## 🥚 Huevo de Pascua
![Huevo de pascua](demo/Huevo%20de%20pascua.PNG)

