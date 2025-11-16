from app.msg_client import fetch_messages, fetch_messages_for_member
from app.utils import extract_member_name, find_relevant_messages
from sentence_transformers import SentenceTransformer, util
from app.utils import extract_keywords, filter_by_keywords

model = SentenceTransformer("all-MiniLM-L6-v2")


def answer_question(question: str) -> str:
    try:
        first_page = fetch_messages(limit=100)
        known_names = list({msg["user_name"] for msg in first_page})

        member = extract_member_name(question, known_names)
        print(f"[DEBUG] Extracted member name: {member}")

        if not member:
            return "I couldn't find the member you're asking about."

        messages = fetch_messages_for_member(member)
        print(f"[DEBUG] Fetched {len(messages)} messages for {member}")

        relevant = find_relevant_messages(question, messages, member)
        print(f"[DEBUG] Found {len(relevant)} relevant messages")

        if relevant:
            # return relevant[0]["message"]
            return generate_answer(question, relevant, member)

        return f"I couldn't find any messages from {member} that answer your question."
    except Exception as e:
        print(f"[ERROR] {e}")
        return "Something went wrong while processing your question."

# all_messages = fetch_messages(limit=500)  # or fetch_all_messages()
# vikram_msgs = [m for m in all_messages if m["user_name"] == "Vikram Desai"]
# print(f"[DEBUG] Vikram messages found: {len(vikram_msgs)}")

def generate_answer(question: str, relevant_messages: list, member: str) -> str:
    if not relevant_messages:
        return f"I couldn’t find any messages from {member} that answer your question."

    top_msg = relevant_messages[0]["message"]

    # If the top message is itself a fallback message, don't attribute it to the member
    if top_msg.lower().startswith("i couldn’t find any messages from"):
        return top_msg

    return f"{member} said: \"{top_msg}\""


def extract_restaurant_name(text: str) -> str:
    # crude heuristic: extract name after "at"
    import re
    match = re.search(r'at ([A-Z][\w\s&]+)', text)
    return match.group(1).strip() if match else "a restaurant"




