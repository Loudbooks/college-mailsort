import imaplib
import email

class IMAPClient:
    def __init__(self, host, user, password):
        self.mail = imaplib.IMAP4_SSL(host)
        self.mail.login(user, password)
        self.scanned_uids = set()

    def fetch_unseen(self):
        self.mail.select("inbox")
        status, data = self.mail.search(None, "UNSEEN")
        email_ids = data[0].split()
        messages = []

        for e_id in email_ids:
            status, msg_data = self.mail.fetch(e_id, "(BODY.PEEK[] UID)")
            if status != "OK":
                continue

            raw_email = msg_data[0][1]
            msg = email.message_from_bytes(raw_email)

            uid = msg_data[0][0].decode().split("UID ")[1].split()[0]

            if uid in self.scanned_uids:
                continue

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

            print(f"Fetched email UID: {uid}, Subject: {subject}")

            messages.append((uid, subject, from_, body))
            self.scanned_uids.add(uid)

        return messages

    def move_email(self, uid, folder):
        self.mail.select("inbox")

        result, _ = self.mail.uid('COPY', uid, folder)
        if result != "OK":
            print(f"Failed to copy email UID {uid} to {folder}")
            return

        self.mail.uid('STORE', uid, '+FLAGS', '\\Deleted')
        self.mail.expunge()

        print(f"Email UID {uid} moved to {folder} successfully.")
