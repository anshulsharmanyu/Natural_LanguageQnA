#  Member Message QA Engine

This project is a FastAPI-based question-answering system that extracts relevant answers from a dataset of member messages. Users can ask natural language questions like “Where did Layla travel last month?” or “What is Vikram’s favorite restaurant?” and receive conversational responses grounded in actual message history.

---
## Hosted at https://natural-languageqna-1.onrender.com/
---
##  Features

- Semantic search using SentenceTransformers
- Robust fallback logic for low-similarity queries
- Conversational answer generation without LLMs
- Clean Swagger API with structured request/response models
- Dockerized for easy deployment

---

##  API Usage

**Endpoint:** `POST /ask`  
**Request Body:**
```json
{
  "question": "What's Layla's favorite restaurant?"
}

Response:

{
  "answer": "Layla Kawaguchi said: Secure a reservation at the chef’s table for six at Alinea."
}
```

The system uses member messages from this API, which contains over 3,000 timestamped entries from individuals like Layla Kawaguchi, Vikram Desai, and Sophia Al-Farsi.

---
### Design Notes

Several alternative approaches were considered before settling on the current architecture:

1. Exact Keyword Matching

✅ Simple to implement

❌ Fragile against typos, synonyms, and indirect phrasing

2. LLM-Based Answer Generation

✅ Highly fluent responses

❌ Overkill for short messages; introduces latency, cost, and dependency

3. Embedding-Based Semantic Search (Chosen)

✅ Handles indirect phrasing and typos

✅ Fast and scalable

✅ Works well with short, structured messages

❌ Requires careful threshold tuning and fallback logic

4. Hybrid Keyword + Embedding Scoring

✅ Boosts relevance for domain-specific cues (e.g., “reservation”, “trip”)

✅ Avoids hardcoding by blending question and keyword embeddings

---

###  Data Insights

After analyzing the dataset, several anomalies and inconsistencies were observed:

🔹 Inconsistent Timestamp Distribution

Some messages are dated in late 2024, while most are from 2025, suggesting either legacy data or future-dated entries.

🔹 Redundant or Overlapping Requests

Multiple users request similar services (e.g., “book a villa”, “reserve a table”) with slight variations, which can confuse semantic ranking.

🔹 Ambiguous Member Preferences

Some messages express preferences (e.g., “I prefer aisle seats”) without context, making it hard to answer questions like “What does Layla prefer when flying?”

🔹 Mixed Intent Types

Messages range from travel bookings to billing issues, profile updates, and thank-you notes. This diversity requires flexible semantic filtering to avoid false positives.

## Setup & Deployment

---
Local Development
---

git clone https://github.com/anshulsharmanyu/Natural_LanguageQnA
cd MemberDataQuestionAnswer
docker build -t fastapi-qa .
docker run -p 8000:8000 fastapi-qa

---
### Future Enhancements
---
- Multi-message summarization

- Named entity extraction for richer answers

- Optional LLM integration for rephrasing

- User feedback loop to improve relevance scoring


---
