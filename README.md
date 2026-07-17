# 🛡️ AI Hallucination Confidence Labeler

An AI-powered fact verification system that evaluates the reliability of AI-generated responses by validating them against trusted web sources.

Instead of blindly trusting an AI response, the application retrieves supporting evidence from reliable sources and assigns a confidence label with a clear explanation, helping users determine whether an answer is trustworthy.

---

## 📖 Problem Statement

Large Language Models (LLMs) can sometimes generate **hallucinations**—responses that sound convincing but are factually incorrect or unsupported.

This project addresses that challenge by introducing a **Confidence Labeling System** that verifies AI-generated answers using external evidence and classifies them into one of three reliability levels:

- 🟢 Certain
- 🟡 Uncertain
- 🔴 Needs Verification

---

## ✨ Features

- 🤖 Generate AI responses using Gemini
- 🔍 Retrieve trusted evidence using Tavily Search API
- 📚 Compare AI responses against retrieved evidence
- 🛡️ Assign reliability labels
- 💬 Provide clear explanations for every decision
- 📄 Display supporting evidence and source links
- ⚡ Fast and intuitive user interface

---

## 🏗️ System Architecture

```text
                User Question
                      │
                      ▼
           Tavily Search API
      (Retrieve Trusted Evidence)
                      │
                      ▼
          Gemini 2.5 Flash Model
       (Answer using Retrieved Evidence)
                      │
                      ▼
         Confidence Classification
                      │
                      ▼
        Certain / Uncertain / Needs Verification
                      │
                      ▼
       Explanation + Supporting Sources
```

---

## 🚀 Tech Stack

### Frontend
- React.js
- Vite
- Tailwind CSS
- Axios

### Backend
- Node.js
- Express.js

### AI & Search
- Google Gemini 2.5 Flash
- Tavily Search API

---

## 📂 Project Structure

```
AI-Hallucination-Confidence-Labeler/
│
├── frontend/
│   ├── src/
│   ├── components/
│   ├── pages/
│   └── App.jsx
│
├── backend/
│   ├── controllers/
│   ├── services/
│   ├── routes/
│   ├── utils/
│   └── server.js
│
├── README.md
└── .env
```

---

## ⚙️ Workflow

### Step 1

The user submits a question.

Example:

```
Who invented Python?
```

---

### Step 2

The backend retrieves relevant evidence from trusted sources using the Tavily Search API.

Example Sources:

- Python.org
- Britannica
- Wikipedia

---

### Step 3

The retrieved evidence is passed to Gemini.

Gemini is instructed to answer **only using the supplied evidence**, minimizing hallucinations.

---

### Step 4

The system evaluates the quality and consistency of the evidence and assigns one of the following labels:

| Label | Meaning |
|-------|---------|
| 🟢 Certain | Strong evidence supports the answer |
| 🟡 Uncertain | Evidence is limited or partially supports the answer |
| 🔴 Needs Verification | Evidence contradicts or does not support the answer |

---

### Step 5

The application displays:

- AI Answer
- Reliability Label
- Confidence Score
- Explanation
- Supporting Facts
- Source Links

---

## 🖥️ Sample Output

**Question**

```
Who invented Python?
```

**Answer**

```
Python was created by Guido van Rossum.
```

**Reliability**

```
🟢 Certain
```

**Confidence**

```
97%
```

**Reason**

```
The answer is consistently supported by multiple trusted sources including Python.org and Britannica.
```

---

## 📦 Installation

### Clone Repository

```bash
git clone https://github.com/yourusername/AI-Hallucination-Confidence-Labeler.git
```

### Navigate to Project

```bash
cd AI-Hallucination-Confidence-Labeler
```

### Install Frontend

```bash
cd frontend
npm install
```

### Install Backend

```bash
cd ../backend
npm install
```

---

## 🔑 Environment Variables

Create a `.env` file inside the backend folder.

```env
GEMINI_API_KEY=YOUR_GEMINI_API_KEY

TAVILY_API_KEY=YOUR_TAVILY_API_KEY
```

---

## ▶️ Run the Application

Backend

```bash
npm run dev
```

Frontend

```bash
npm run dev
```

---

## 🎯 Future Improvements

- Support document-based fact verification
- Multi-language verification
- Domain-specific verification (Medical, Legal, Finance)
- Source credibility scoring
- Fact-level highlighting within responses
- Historical verification reports

---

## 💡 Key Highlights

- Reduces AI hallucinations through Retrieval-Augmented Generation (RAG)
- Verifies AI-generated responses using trusted external evidence
- Improves transparency by explaining confidence decisions
- Encourages responsible and trustworthy AI interactions

---

## 👩‍💻 Team

Built for the **TCS Tech Day Hackathon** under the theme **Responsible Enterprise AI**.

---
