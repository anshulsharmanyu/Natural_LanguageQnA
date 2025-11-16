import requests

API_URL = "https://november7-730026606190.europe-west1.run.app/messages"
PAGE_SIZE = 100

def fetch_messages(limit=100):
    response = requests.get(API_URL, params={"page": 0, "limit": limit})
    if response.status_code == 200:
        data = response.json()
        return data.get("items", [])
    return []

def fetch_messages_for_member(member_name: str, max_pages=50):
    all_messages = []
    page = 0

    while page < max_pages:
        response = requests.get(API_URL, params={"page": page, "limit": PAGE_SIZE})
        if response.status_code != 200:
            break

        items = response.json().get("items", [])
        if not items:
            break

        member_msgs = [msg for msg in items if msg["user_name"].lower() == member_name.lower()]
        all_messages.extend(member_msgs)

        if len(all_messages) >= 5:
            break

        page += 1

    return all_messages