import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow # type: ignore
from googleapiclient.discovery import build # type: ignore

# Define the scope: readonly allows us to view but not modify or delete emails.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

class GmailService:
    def __init__(self):
        """
        Initializes the Gmail service by handling authentication
        and building the API client.
        """
        self.creds = self._authenticate()
        self.service = build('gmail', 'v1', credentials=self.creds)

    def _authenticate(self):
        creds = None
        
        current_dir = os.path.dirname(os.path.abspath(__file__))
        root_dir = os.path.dirname(current_dir)
        
        # Join the root directory with the filenames
        token_path = os.path.join(root_dir, 'token.json')
        credentials_path = os.path.join(root_dir, 'credentials.json')

        if os.path.exists(token_path):
            creds = Credentials.from_authorized_user_file(token_path, SCOPES)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    credentials_path, SCOPES)
                creds = flow.run_local_server(port=0)
            
            with open(token_path, 'w') as token:
                token.write(creds.to_json())
        return creds

    def fetch_emails(self, limit=3):
        """
        Fetches a list of the latest emails and returns them as structured data.
        """
        try:
            # 1. Get the list of message IDs
            response = self.service.users().messages().list(
                userId='me', labelIds=['INBOX'], maxResults=limit
            ).execute()
            messages = response.get('messages', [])

            email_data = []
            for msg in messages:
                # 2. Fetch full message details
                full_msg = self.service.users().messages().get(
                    userId='me', id=msg['id']
                ).execute()
                
                # Extract headers for a more professional input for Gemini
                headers = full_msg.get('payload', {}).get('headers', [])
                subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'No Subject')
                sender = next((h['value'] for h in headers if h['name'] == 'From'), 'Unknown Sender')

                email_data.append({
                    "id": msg['id'],
                    "sender": sender,
                    "subject": subject,
                    "snippet": full_msg.get('snippet', '')
                })
            
            return email_data

        except Exception as error:
            print(f'An error occurred in GmailService: {error}')
            return []

if __name__ == '__main__':
    # This part allows you to still test this file independently
    gmail = GmailService()
    test_emails = gmail.fetch_emails(limit=2)
    for e in test_emails:
        print(f"DEBUG - From: {e['sender']} | Subject: {e['subject']}")