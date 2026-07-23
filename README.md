

<div align="center">

# 🛡️ AI Hallucination Confidence Labeler

### Know when to trust AI.

An evidence-grounded AI verification system that evaluates responses against real-world sources and clearly communicates how reliable an answer is.

**Responsible Enterprise AI · TCS Tech Day Hackathon**

<br/>

![React](https://img.shields.io/badge/React-19-61DAFB?style=for-the-badge&logo=react&logoColor=white)
![Node.js](https://img.shields.io/badge/Node.js-Express-339933?style=for-the-badge&logo=nodedotjs&logoColor=white)
![Gemini](https://img.shields.io/badge/Google-Gemini-4285F4?style=for-the-badge&logo=google&logoColor=white)
![Tavily](https://img.shields.io/badge/Tavily-Web_Search-111827?style=for-the-badge)
![Tailwind](https://img.shields.io/badge/Tailwind-CSS-06B6D4?style=for-the-badge&logo=tailwindcss&logoColor=white)

</div>

---

## 💡 The Problem

Large Language Models are powerful, but they can **hallucinate** — generating information that sounds convincing while being inaccurate, unsupported, or completely fabricated.

The bigger problem?

> **AI often presents incorrect information with the same confidence as correct information.**

For users, there is often no simple way to distinguish between:

> ✅ *"This answer is backed by reliable evidence."*

and

> ⚠️ *"This sounds correct, but there isn't enough evidence to trust it."*

**AI Hallucination Confidence Labeler** is designed to bridge that trust gap.

---

## 🎯 Our Solution

Instead of asking users to blindly trust an AI response, our system grounds answers in **real-world evidence**.

For every question, the application:

1. 🔎 Searches the web for relevant evidence
2. 📚 Collects information from external sources
3. 🤖 Provides the evidence to Gemini
4. 🧠 Evaluates how strongly the evidence supports the response
5. 🛡️ Assigns an easy-to-understand reliability label
6. 💬 Explains *why* that label was assigned

The result is not just an AI answer — it is an **answer with evidence and context about its reliability**.

---

## 🛡️ Reliability Labels

| Label | Meaning |
| :--- | :--- |
| 🟢 **Certain** | Strong and consistent evidence supports the answer |
| 🟡 **Uncertain** | Evidence exists but is incomplete, limited, or partially supportive |
| 🔴 **Needs Verification** | Evidence is insufficient, conflicting, or does not support the answer |

This gives users an immediate visual indication of how much confidence they should place in the response.

---

## ⚙️ How It Works

```text
                         ┌─────────────────┐
                         │      USER       │
                         └────────┬────────┘
                                  │
                                  │ Question
                                  ▼
                    ┌──────────────────────────┐
                    │      REACT FRONTEND      │
                    └────────────┬─────────────┘
                                 │
                                 ▼
                    ┌──────────────────────────┐
                    │    NODE.JS / EXPRESS     │
                    │         BACKEND          │
                    └────────────┬─────────────┘
                                 │
                                 ▼
                    ┌──────────────────────────┐
                    │      TAVILY SEARCH       │
                    │                          │
                    │  Retrieve web evidence   │
                    └────────────┬─────────────┘
                                 │
                                 │ Evidence
                                 ▼
                    ┌──────────────────────────┐
                    │      GEMINI 2.5 FLASH    │
                    │                          │
                    │ Evidence-grounded        │
                    │ reasoning & generation   │
                    └────────────┬─────────────┘
                                 │
                                 ▼
                    ┌──────────────────────────┐
                    │  RELIABILITY ANALYSIS    │
                    │                          │
                    │ 🟢 Certain               │
                    │ 🟡 Uncertain             │
                    │ 🔴 Needs Verification    │
                    └────────────┬─────────────┘
                                 │
                                 ▼
                    ┌──────────────────────────┐
                    │ Answer + Reason + Sources│
                    └──────────────────────────┘
```

---

## 🧠 Why Evidence First?

A simple hallucination checker could ask an LLM:

> *"Is your previous answer correct?"*

But this still relies on the model's internal knowledge and can reproduce the same hallucination.

Our approach follows an **evidence-first architecture**.

```text
Question
   ↓
Retrieve Evidence
   ↓
Ground AI with Evidence
   ↓
Generate Answer
   ↓
Evaluate Reliability
```

Gemini is instructed to reason from the retrieved evidence rather than relying solely on its internal knowledge.

This makes the system more:

- 🔎 **Verifiable**
- 📚 **Evidence-grounded**
- 💡 **Explainable**
- 🛡️ **Trust-aware**

---

## 🔍 Example

### User Question

> **Who created the Python programming language?**

### Retrieved Evidence

The system searches external sources and retrieves evidence identifying **Guido van Rossum** as Python's creator.

### AI Response

> Python was created by Guido van Rossum.

### Reliability

> 🟢 **Certain — 96%**

### Why?

> Multiple relevant sources consistently support the claim that Guido van Rossum created Python.

The user receives not only an answer, but also an indication of **why that answer can be trusted**.

---

## ✨ Core Features

- 🤖 **AI-powered responses** using Google Gemini
- 🌐 **Real-time evidence retrieval** using Tavily Search
- 🛡️ **Three-level reliability classification**
- 📊 **Confidence indication**
- 💬 **Human-readable reasoning**
- 🔗 **Supporting source references**
- ⚡ **Fast response pipeline**
- 📱 **Responsive React interface**
- 🔐 **Secure API key handling through environment variables**

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
| :--- | :--- | :--- |
| 🎨 Frontend | React + Vite | Interactive user interface |
| 💅 Styling | Tailwind CSS | Responsive UI design |
| ⚙️ Backend | Node.js + Express | API and application logic |
| 🧠 AI | Gemini 2.5 Flash | Evidence-grounded reasoning |
| 🔎 Search | Tavily Search API | Real-time evidence retrieval |
| 🔄 Requests | Axios | Frontend/backend communication |

---

## 📁 Project Structure

```text
ai-hallucination-confidence-labeler/
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── services/
│   │   ├── App.jsx
│   │   └── main.jsx
│   │
│   ├── package.json
│   └── vite.config.js
│
├── backend/
│   ├── controllers/
│   ├── routes/
│   ├── services/
│   │   ├── geminiService.js
│   │   └── tavilyService.js
│   ├── server.js
│   └── package.json
│
├── .gitignore
└── README.md
```

---

## 🔄 Verification Pipeline

### 01 — Ask

The user enters a question.

```text
"What is the capital of Australia?"
```

### 02 — Retrieve

Tavily searches for relevant information and returns evidence from web sources.

### 03 — Ground

The retrieved evidence is supplied to Gemini as context.

Gemini is instructed to reason **only from the available evidence**.

### 04 — Evaluate

The system determines whether the evidence:

```text
Fully supports the response
        ↓
🟢 CERTAIN


Partially supports the response
        ↓
🟡 UNCERTAIN


Does not support / contradicts the response
        ↓
🔴 NEEDS VERIFICATION
```

### 05 — Explain

The user receives:

```text
AI Answer
    +
Reliability Label
    +
Confidence
    +
Reason
    +
Supporting Sources
```

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/ai-hallucination-confidence-labeler.git

cd ai-hallucination-confidence-labeler
```

### 2. Install Backend Dependencies

```bash
cd backend
npm install
```

### 3. Install Frontend Dependencies

```bash
cd ../frontend
npm install
```

### 4. Configure Environment Variables

Create a `.env` file inside the `backend` directory:

```env
GEMINI_API_KEY=your_gemini_api_key
TAVILY_API_KEY=your_tavily_api_key
PORT=5000
```

> ⚠️ Never commit your `.env` file or API keys to GitHub.

### 5. Start the Backend

```bash
cd backend
npm run dev
```

### 6. Start the Frontend

Open another terminal:

```bash
cd frontend
npm run dev
```

Open the local URL displayed by Vite in your browser.

---

## 🔌 API

### Analyze a Question

```http
POST /api/analyze
```

#### Request

```json
{
  "question": "Who created Python?"
}
```

#### Example Response

```json
{
  "question": "Who created Python?",
  "answer": "Python was created by Guido van Rossum.",
  "label": "Certain",
  "confidence": 96,
  "reason": "Multiple retrieved sources consistently support the answer.",
  "sources": [
    {
      "title": "Source title",
      "url": "Source URL"
    }
  ]
}
```

---

## 🔐 Security

API keys are stored only on the backend using environment variables.

```text
Frontend
   ↓
Backend
   ↓
Gemini / Tavily
```

The frontend never directly exposes Gemini or Tavily credentials.

---

## 🌍 Why This Matters

As AI becomes increasingly integrated into enterprise workflows, generating an answer is no longer enough.

AI systems also need to communicate:

> **"Why should you trust this answer?"**

AI Hallucination Confidence Labeler demonstrates how **retrieval, evidence grounding, confidence labeling, and explainability** can work together to create more responsible AI experiences.

---

## 🔮 Future Scope

- 📄 Verify answers against uploaded documents
- 🏢 Enterprise knowledge-base integration
- 🧩 Claim-by-claim verification
- 🌐 Multi-language fact verification
- 📊 Advanced source credibility scoring
- 🏥 Domain-specific verification for healthcare
- ⚖️ Legal and financial information verification
- 📜 Verification history and audit trails

---

## 🏆 Hackathon

Developed for the **TCS Tech Day Hackathon**

**Theme:** Responsible Enterprise AI  
**Problem:** AI Hallucination Confidence Labeler

---

<div align="center">

### 🛡️ Don't just generate. Verify.

**AI Hallucination Confidence Labeler**

Built with React · Node.js · Gemini · Tavily

</div>
