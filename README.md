# 🔬 Research Analyst AI

> A multi-agent AI pipeline that searches, reads, writes, and critiques — delivering publication-ready research reports in seconds.

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.x-FF4B4B?style=flat-square&logo=streamlit)
![LangChain](https://img.shields.io/badge/LangChain-0.2+-00A67E?style=flat-square)
![Three.js](https://img.shields.io/badge/Three.js-r128-black?style=flat-square&logo=threedotjs)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

---

## ✨ Overview

**Research Analyst AI** is a fully autonomous, multi-agent research system built with LangChain and Streamlit. You give it a topic — it does everything else. Four specialized AI agents collaborate in a sequential pipeline to produce structured, cited, and critically evaluated research reports, complete with a quality score.

The UI features a fully animated Three.js background with DNA helices, neural particle clouds, and orbiting satellites — all running in real time inside the browser.

---

## 🤖 Agent Pipeline

```
User Input → [Search Agent] → [Reader Agent] → [Writer Chain] → [Critic Chain] → Report + Score
```

| Step | Agent | Role |
|------|-------|------|
| 01 | **Search Agent** | Queries the web for recent, reliable information on the topic |
| 02 | **Reader Agent** | Picks the most relevant URL and scrapes its full content |
| 03 | **Writer Chain** | Synthesizes search + scraped data into a structured report |
| 04 | **Critic Chain** | Evaluates the report and returns feedback with a score out of 10 |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- A Mistral API key (or swap for any LangChain-compatible LLM)

### Installation

```bash
git clone https://github.com/yourusername/research-analyst-ai.git
cd research-analyst-ai
pip install -r requirements.txt
```

### Environment Setup

Create a `.env` file in the root directory:

```env
MISTRAL_API_KEY=your_key_here
# Optional: add Tavily or SerpAPI key for the search agent
TAVILY_API_KEY=your_key_here
```

### Run

```bash
streamlit run app.py
```

Open `http://localhost:8501` in your browser.

---

## 🗂 Project Structure

```
research-analyst-ai/
├── app.py              # Streamlit UI + pipeline orchestration
├── agents.py           # Agent & chain definitions (LangChain)
├── requirements.txt    # Python dependencies
├── .env                # API keys (not committed)
└── README.md
```

---

## 🛠 Tech Stack

| Layer | Technology |
|-------|-----------|
| **LLM** | Mistral (via LangChain) |
| **Agents** | LangChain AgentExecutor |
| **Search Tool** | Tavily / SerpAPI |
| **Scraping Tool** | LangChain WebBaseLoader |
| **UI** | Streamlit |
| **3D Background** | Three.js (r128) |
| **Fonts** | Space Mono + Outfit (Google Fonts) |

---

## 🎨 UI Features

- Animated Three.js canvas — star fields, neural particle clouds, DNA helices, torus rings
- Real-time step tracker with active/done/waiting states
- Gradient progress bar
- Downloadable `.md` report
- Fully responsive dark theme

---

## 📦 Requirements

```
streamlit
langchain
langchain-mistralai
langchain-community
tavily-python
python-dotenv
```

---

## 🔮 Roadmap

- [ ] Add memory across research sessions
- [ ] Support PDF export
- [ ] Parallel agent execution
- [ ] Source citation linking in reports
- [ ] User-configurable LLM provider

---

## 📄 License

MIT License — free to use, modify, and distribute.

---

## 🙌 Contributing

Pull requests are welcome! Please open an issue first to discuss major changes.

---

<p align="center">Built with LangChain · Mistral · Streamlit · Three.js</p>
