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
        and building the API client. Falls back to Mock mode if credentials are missing.
        """
        self.creds = self._authenticate()
        
        if self.creds:
            self.service = build('gmail', 'v1', credentials=self.creds)
            self.is_mock = False
        else:
            self.service = None
            self.is_mock = True
            print("PRODUCTION WARNING: credentials.json not found. Operating in DEMO/MOCK mode with sample data.")

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
                try:
                    creds.refresh(Request())
                except Exception:
                    creds = None

            if not creds or not creds.valid:
                # CRITICAL CLOUD ISOLATION: If credentials.json is missing (e.g., on Render),
                # do not crash the app, return None to trigger safe Mock/Demo mode.
                if not os.path.exists(credentials_path):
                    return None
                    
                flow = InstalledAppFlow.from_client_secrets_file(
                    credentials_path, SCOPES)
                creds = flow.run_local_server(port=0)
            
            if creds:
                with open(token_path, 'w') as token:
                    token.write(creds.to_json())
                    
        return creds

    def fetch_emails(self, limit=3):
        """
        Fetches a list of the latest emails. If in mock mode or API fails,
        returns structured, high-quality sample data tailored for Bohemia Interactive presentation.
        """
        if self.is_mock:
            return self._get_mock_emails(limit)

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
            print(f'An error occurred in GmailService API: {error}. Falling back to demo data.')
            return self._get_mock_emails(limit)

    def _get_mock_emails(self, limit):
        """
        Returns high-quality, realistic tech/gaming emails for demonstration purposes.
        Ensures a fantastic presentation review without exposing private data.
        """
        mock_data = [
            {
                "id": "mock_msg_enfusion_001",
                "sender": "devops-alerts@bohemia-net.internal",
                "subject": "CRITICAL: Enfusion Engine Build Pipeline Blocked - Core Dump Detected",
                "snippet": "Alert triggered at 15:42 UTC. The automated nightly build for branch main failed on Linux target. Segmentation fault occurred during shader pre-compilation step in render_backend_v2.cpp. This is currently blocking 14 developers from merging features. Immediate engineering review required."
            },
            {
                "id": "mock_msg_aws_002",
                "sender": "billing@aws-amazon.com",
                "subject": "Amazon Web Services Invoice Available - Account 4920-XXXX",
                "snippet": "Your monthly AWS invoice for April 2026 is now available online. Total balance due: $14,250.42. This charge will be automatically processed via your primary payment method on file on May 18, 2026. Please review the Cost Explorer dashboard for regional server allocation breakdown."
            },
            {
                "id": "mock_msg_feedback_003",
                "sender": "michal.klinec@bohemia.cz",
                "subject": "Community Feedback Summary - DayZ Patch 1.26 Stability Issues",
                "snippet": "Hey Tadeas, I reviewed the player forums regarding yesterday's patch release. There is a small uptick in complaints about multiplayer desync and inventory duplication lag on European public servers. It is not breaking the core game, but we should schedule a quick sync tomorrow to discuss hotfix priorities."
            },
            {
                "id": "mock_msg_player_004",
                "sender": "frustrated-gamer99@gmail.com",
                "subject": "REFUND REQUEST: Lost all my inventory items due to server crash!!",
                "snippet": "I am demanding a full refund or restore of my digital items! I spent 40 hours looting on Server EU-03 and the server randomly crashed at 16:10 today. When I logged back in, my character was completely wiped. This is unacceptable, fix your game or I want my money back immediately!!"
            }
        ]
        return mock_data[:limit]

if __name__ == '__main__':
    gmail = GmailService()
    test_emails = gmail.fetch_emails(limit=2)
    for e in test_emails:
        print(f"DEBUG - From: {e['sender']} | Subject: {e['subject']}")