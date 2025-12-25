# 🧠 AI Newsletter Automation

> Automated AI news aggregation and email delivery system powered by LangChain, LangGraph, and Tavily Search.

## ✨ Features

- **🔍 Smart News Aggregation** - Uses Tavily Search API to fetch the latest AI news, emerging technologies, and industry updates
- **🤖 AI-Powered Curation** - Structures and formats news using Gemini 2.5 Flash
- **📧 Beautiful HTML Emails** - Automatically generates professional newsletter emails with modern design
- **⏰ Scheduled Delivery** - Runs on a configurable schedule (default: every 5 minutes)
- **🎨 Mobile-Friendly Design** - Email templates optimized for all devices

## 🏗️ Architecture

```mermaid
%%{init: {'theme':'base', 'themeVariables': { 'primaryColor':'#f0f4f8','primaryTextColor':'#1a202c','primaryBorderColor':'#4299e1','lineColor':'#4299e1'}}}%%
graph TD
    A["⏰ Scheduler"] --> B["🔍 Search AI News"]
    B --> C["🤖 AI Processing"]
    C --> D["📧 Send Newsletter"]

    style A fill:#e3f2fd,stroke:#2196f3,stroke-width:2px,color:#1565c0
    style B fill:#f3e5f5,stroke:#9c27b0,stroke-width:2px,color:#6a1b9a
    style C fill:#e8f5e9,stroke:#4caf50,stroke-width:2px,color:#2e7d32
    style D fill:#fff3e0,stroke:#ff9800,stroke-width:2px,color:#e65100
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Gmail account with App Password enabled
- API Keys: Groq/Gemini, Tavily

### Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd email

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env with your API keys and email credentials
```

### Configuration

Create a `.env` file with the following:

```env
GEMINI_API_KEY=your_gemini_api_key
TAVILY_API_KEY=your_tavily_api_key
SENDER_EMAIL=your_email@gmail.com
SENDER_PASSWORD=your_app_password
```

### Usage

**Run once:**

```bash
python main.py
```

**Run on schedule:**

```bash
python run.py
```

## 📁 Project Structure

```
email/
├── main.py          # Core workflow logic with LangGraph
├── run.py           # Scheduler for automated execution
├── .env             # Environment variables (not committed)
└── requirements.txt # Python dependencies
```

## 🛠️ Tech Stack

| Component     | Technology            |
| ------------- | --------------------- |
| **LLM**       | Gemini 2.5 Flash      |
| **Workflow**  | LangGraph             |
| **Search**    | Tavily Search API     |
| **Email**     | Python smtplib (SMTP) |
| **Scheduler** | Python schedule       |

## 📧 Email Newsletter Preview

Each newsletter includes:

- 🎯 Catchy subject line
- 📰 Top 10 AI news stories
- 🔗 Direct links to sources
- 🎨 Modern card-based layout
- 📱 Mobile-responsive design
