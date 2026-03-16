# 🇵🇪 GitHub Peru Analytics - Homework 2

Un completo sistema de gestión de datos y un panel de control para analizar el ecosistema de desarrolladores de GitHub en Perú. Este proyecto extrae datos de más de 1000 desarrolladores peruanos, clasifica sus repositorios por sectores mediante inteligencia artificial (GPT-4) y visualiza los resultados en un panel interactivo de varias páginas.

## 🚀 Project Overview

Esta herramienta identifica y analiza las tendencias técnicas, la distribución por sectores y las métricas de rendimiento de los desarrolladores, específicamente para los usuarios ubicados en Perú.
---

## 🥚 Huevo de Pascua
![Huevo de pascua](demo/Huevo%20de%20pascua.PNG)


### Características clave:
- **Extracción masiva de datos**: Obtiene los detalles completos del perfil de más de 1000 usuarios peruanos y sus repositorios más recientes.

- **Clasificación industrial con IA**: Utiliza GPT-4o-mini para categorizar proyectos según la Clasificación Industrial Internacional Uniforme (CIIU).

- **Métricas avanzadas**: Calcula el índice h, las puntuaciones de participación y la proporción de proyectos por año para todos los desarrolladores.

- **Panel interactivo**: Una aplicación Streamlit de 6 páginas con análisis detallados.

- **Agente de IA**: Un chatbot entrenado con datos del ecosistema para responder preguntas técnicas.
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

## 🛠️ Instrucciones de configuración

### 1. Requisitos
Asegúrese de tener Python 3.8 o superior instalado.

### 2. Configuración del entorno
1. Copie `.env.example` a `.env`.

2. Añada su **Token de Acceso Personal de GitHub** (`GITHUB_TOKEN`).

3. Añada su **Clave API de OpenAI** (`OPENAI_API_KEY`).

### 3. Instalación
```bash
pip install -r requirements.txt
```

---

## 📈 Ejecución del flujo de datos

Ejecute los scripts para construir el conjunto de datos:

1. **Extraer usuarios**: `python scripts/extract_users.py`
2. **Extraer repositorios**: `python scripts/extract_repos.py`
3. **Clasificar repositorios**: `python scripts/classify_repos.py`
4. **Finalizar métricas**: `python scripts/calculate_metrics.py`

---

## 📊 Ejecutar el panel de control

Iniciar la plataforma de análisis interactivo:
```bash
python scripts/run_dashboard.py
```
*O usar directamente streamlit:* `streamlit run app/main.py`
---

## 🤖 Agente de IA

Puedes interactuar con el Agente de IA de dos maneras:

### 1. Mediante el Panel de Control (GUI)
- Ejecuta `python scripts/run_dashboard.py`.

- Navega a la página **"06 AI Insights"** en la barra lateral.

- Escribe tus preguntas en la interfaz de chat.

### 2. Mediante la Terminal (CLI)
Ejecuta el script de chat:
```bash
python scripts/chat_with_agent.py
```

### Ejemplos de preguntas:
- "¿Cuáles son las 3 principales industrias para desarrolladores que usan Python en Perú?"

- "¿Qué ciudad tiene la comunidad de GitHub más activa?"

- "Dame un resumen de la madurez técnica del ecosistema peruano."

---

## 📺 Video Demonstration
A video tour of the project can be found at: [Link to Video] (User, please record your demo and update this link).

---

## 🎓 Author
**Julia** - *Homework 2 for Prompt Engineering Course*

