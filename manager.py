import json
import os

class MarketplaceManager:
    def __init__(self, filename="marketplace_data.json"):
        self.filename = filename
        self._load_data()

    def _load_data(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as f:
                    data = json.load(f)
                    self.listings = data.get('listings', [])
                    self.conversations = data.get('conversations', [])
                    self.next_item_id = data.get('next_item_id', 1)
            except (json.JSONDecodeError, ValueError):
                self._initialize_empty_data()
        else:
            self._initialize_empty_data()

    def _initialize_empty_data(self):
        self.listings = []
        self.conversations = []
        self.next_item_id = 1

    def _save_data(self):
        data = {
            'listings': self.listings,
            'conversations': self.conversations,
            'next_item_id': self.next_item_id
        }
        with open(self.filename, 'w') as f:
            json.dump(data, f, indent=4)

    # Create a listing (accept params instead of input)
    def create_listing(self, seller_username, item_name, description, price):
        listing = {
            "id": self.next_item_id,
            "seller": seller_username,
            "name": item_name,
            "description": description,
            "price": price
        }
        self.listings.append(listing)
        self.next_item_id += 1
        self._save_data()
        return listing

    # Get all listings (return data instead of print)
    def get_all_listings(self):
        return self.listings

    # Check for new messages for a user
    def check_for_new_messages(self, username):
        for convo in self.conversations:
            if username in convo['participants']:
                last_message = convo['messages'][-1]
                if last_message['unread'] and last_message['sender'] != username:
                    return True
        return False

    # Get conversations for a user
    def get_user_conversations(self, username):
        return [c for c in self.conversations if username in c['participants']]

    # Get conversation messages by conversation id or participants (simplify)
    def get_conversation_messages(self, item_id, user1, user2):
        convo = next(
            (c for c in self.conversations
             if c['item_id'] == item_id and user1 in c['participants'] and user2 in c['participants']),
            None)
        if convo:
            return convo['messages']
        else:
            return []

    # Add message to a conversation (or create new convo)
    def add_message(self, item_id, sender, recipient, content):
        convo = next(
            (c for c in self.conversations if c['item_id'] == item_id and sender in c['participants'] and recipient in c['participants']),
            None)
        if not convo:
            convo = {
                'item_id': item_id,
                'participants': [sender, recipient],
                'messages': []
            }
            self.conversations.append(convo)

        message = {'sender': sender, 'content': content, 'unread': True}
        convo['messages'].append(message)
        self._save_data()
        return message