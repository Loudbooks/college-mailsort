import imaplib
import email

class IMAPClient:
    def __init__(self, host, user, password):
        self.mail = imaplib.IMAP4_SSL(host)
        self.mail.login(user, password)

    def fetch_unseen(self):
        self.mail.select("inbox")
        status, data = self.mail.search(None, "UNSEEN")
        email_ids = data[0].split()
        messages = []
        for e_id in email_ids:
            status, msg_data = self.mail.fetch(e_id, "(BODY.PEEK[])")
            msg = email.message_from_bytes(msg_data[0][1])
            subject = msg["subject"]
            from_ = msg["from"]
            body = ""
            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() == "text/plain":
                        body = part.get_payload(decode=True).decode(errors="ignore")
                        break
            else:
                body = msg.get_payload(decode=True).decode(errors="ignore")
            messages.append((e_id, subject, from_, body))
        
        return messages

    def move_email(self, e_id, folder):
        result, _ = self.mail.copy(e_id, folder)
        if result == "OK":
            self.mail.store(e_id, "+FLAGS", "\\Deleted")
            self.mail.expunge()
