from config import FOLDERS

class Router:
    def __init__(self, imap_client):
        self.imap_client = imap_client

    def route(self, uid, label):
        folder = FOLDERS.get(label, "INBOX")
        self.imap_client.move_email(uid, folder)
