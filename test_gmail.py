import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def get_gmail_service():
    creds = None
    # Use absolute or relative paths carefully. 
    # If running from main.py in root, 'token.json' works.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return build('gmail', 'v1', credentials=creds)

def fetch_latest_emails(max_results=3):
    service = get_gmail_service()
    results = service.users().messages().list(userId='me', labelIds=['INBOX'], maxResults=max_results).execute()
    messages = results.get('messages', [])

    email_data = []
    for msg in messages:
        full_msg = service.users().messages().get(userId='me', id=msg['id']).execute()
        payload = full_msg.get('payload', {})
        headers = payload.get('headers', [])
        
        # Extract specific headers
        subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'No Subject')
        sender = next((h['value'] for h in headers if h['name'] == 'From'), 'Unknown Sender')
        snippet = full_msg.get('snippet', '')

        email_data.append({
            "id": msg['id'],
            "sender": sender,
            "subject": subject,
            "snippet": snippet
        })
    
    return email_data