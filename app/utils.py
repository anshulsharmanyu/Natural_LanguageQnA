from sentence_transformers import SentenceTransformer, util
import re
from difflib import get_close_matches

import nltk

nltk.download('punkt_tab')
nltk.download('stopwords')


# import spacy

# nlp = spacy.load("en_core_web_sm")

# def extract_member_name(question: str):
#     doc = nlp(question)
#     people = [ent.text for ent in doc.ents if ent.label_ == "PERSON"]
#     # return first person name or list depending on your need
#     return people[0] if people else ""

def extract_member_name(question: str, known_names: list) -> str:
    question = question.replace("’", "'")
    words = re.findall(r"[A-Z][a-z]+(?:\s[A-Z][a-z]+)?", question)

    for word in words:
        match = get_close_matches(word, known_names, n=1, cutoff=0.6)
        if match:
            return match[0]

    for word in words:
        for name in known_names:
            if word.lower() in name.lower():
                return name
    return ""


model = SentenceTransformer("all-MiniLM-L6-v2")  # Fast and effective



def find_relevant_messages(question: str, messages: list, member: str) -> list:
    if not messages:
        return []

    message_texts = [msg["message"] for msg in messages]
    keywords = extract_keywords(question)
    filtered_msgs = filter_by_keywords(messages, keywords)

    if not filtered_msgs:
        print("[DEBUG] No keyword-matching messages. Falling back to full set.")
        filtered_msgs = messages

    filtered_texts = [msg["message"] for msg in filtered_msgs]
    # question_embedding = model.encode(question, convert_to_tensor=True)
    # message_embeddings = model.encode(filtered_texts, convert_to_tensor=True)
    # scores = util.cos_sim(question_embedding, message_embeddings)[0]

    question_embedding = model.encode(question, convert_to_tensor=True)
    keyword_embedding = model.encode(" ".join(keywords), convert_to_tensor=True)
    message_embeddings = model.encode(filtered_texts, convert_to_tensor=True)

    scores_q = util.cos_sim(question_embedding, message_embeddings)[0]
    scores_kw = util.cos_sim(keyword_embedding, message_embeddings)[0]

    # Blend scores: 70% question, 30% keywords
    scores = 0.7 * scores_q + 0.3 * scores_kw

    top_indices = scores.argsort(descending=True)
    for i in top_indices[:5]:
        print(f"[DEBUG] Score {scores[i]:.3f} → {filtered_texts[i]}")

    relevant = [
        {"message": filtered_texts[i]}
        for i in top_indices
        if scores[i] > 0.2
    ][:3]  # return top 3

    if not relevant and filtered_texts:
        best_index = scores.argmax().item()
        best_score = scores[best_index].item()
        if best_score > 0.3:
            return [{"message": filtered_texts[best_index]}]
        else:
            return [{"message": f"I couldn’t find any messages from {member} that answer your question."}]

    return relevant

def extract_keywords(question: str) -> list:
    import re
    from nltk.corpus import stopwords
    from nltk.tokenize import word_tokenize

    stop_words = set(stopwords.words("english"))
    words = word_tokenize(question.lower())
    keywords = [w for w in words if w.isalpha() and w not in stop_words]
    return keywords


def fuzzy_filter_keywords(keywords, message_text, threshold=0.8):
    message_words = message_text.lower().split()
    for kw in keywords:
        matches = get_close_matches(kw.lower(), message_words, n=1, cutoff=threshold)
        if matches:
            return True
    return False


def filter_by_keywords(messages: list, keywords: list) -> list:
    return [
        msg for msg in messages
        if fuzzy_filter_keywords(keywords, msg["message"])
    ]

