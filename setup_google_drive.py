import os
import pickle
import tempfile
from google_auth_oauthlib.flow import InstalledAppFlow

def setup():
    """ONE-TIME setup to get Google Drive credentials"""
    
    print("=" * 70)
    print("GOOGLE DRIVE SETUP (ONE TIME ONLY)")
    print("=" * 70)
    print()
    
    # Use YOUR actual client ID and secret
    CLIENT_ID = "1936528-nspdgsobqd87.apps.googleusercontent.com"
    CLIENT_SECRET = "GOCSPX-xjLHYHFkq"
    
    print(f"Using Client ID: {CLIENT_ID}")
    print()
    
    # Create the flow
    flow = InstalledAppFlow.from_client_config(
        {
            "installed": {
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "redirect_uris": ["http://localhost:8080/"]
            }
        },
        scopes=['https://www.googleapis.com/auth/drive.file']
    )
    
    print("STEP 1: A browser window will open.")
    print("STEP 2: Log in with YOUR Google account")
    print("STEP 3: Grant 'Google Drive File' permissions")
    print()
    input("Press Enter to open browser...")
    
    # This will open browser for authentication
    creds = flow.run_local_server(port=8080)
    
    # Save the credentials
    token_path = os.path.join(tempfile.gettempdir(), 'drive_token.pickle')
    with open(token_path, 'wb') as token:
        pickle.dump(creds, token)
    
    print()
    print("=" * 70)
    print("✅ SUCCESS! Setup complete!")
    print("=" * 70)
    print()
    print(f"Token saved to: {token_path}")
    print(f"Authenticated as: {creds.client_id}")
    print(f"Refresh token: {'✅ Yes' if creds.refresh_token else '❌ No'}")
    print()
    print("Next steps:")
    print("1. This token will work forever (or until you revoke access)")
    print("2. Your app can now upload files to Google Drive")
    print("3. Files will go to folder with ID: {os.getenv('GOOGLE_DRIVE_FOLDER_ID', 'NOT SET')}")
    print()
    print("To test, run: python test_upload.py")

if __name__ == "__main__":
    setup()