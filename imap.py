import re

import pyzmail
from imapclient import IMAPClient


# context manager ensures the session is cleaned up
def read_mail(username: str, password: str, sender: str, subject: str):
    with IMAPClient(host="outlook.office365.com") as client:
        client.login(username, password)
        client.select_folder('INBOX', readonly=True)

        # search criteria are passed in a straightforward way
        # (nesting is supported)
        messages = client.search(['FROM', sender, 'SUBJECT', subject])

        # fetch selectors are passed as a simple list of strings.
        for msgid, data in client.fetch(messages, ['ENVELOPE', 'BODY.PEEK[]']).items():
            envelope = data[b'ENVELOPE']
            email = pyzmail.PyzMessage.factory(data[b'BODY[]'])

            # Process each email
            subject = email.get_subject()
            from_address = email.get_addresses('from')
            body_text = email.text_part.get_payload().decode(email.text_part.charset)

            print(f"Subject: {subject}")
            print(f"From: {from_address}")
            print(f"Body: {body_text}\n")
            code_pattern = r"\b\d{6}\b"

            # Search for the pattern in the email text
            match = re.search(code_pattern, body_text)

            # If a match is found, print it
            if match:
                code = match.group()
                print("Code found:", code)
                return code
            else:
                print("No code found.")
                raise 'No code found.'


if __name__ == '__main__':
    print(read_mail('bruhnseldent@hotmail.com', 'iCvLVl68', 'noreply@brightdata.com', 'Bright Data - Welcome'))
