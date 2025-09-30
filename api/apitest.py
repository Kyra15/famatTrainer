import dropbox
from dropbox import DropboxOAuth2FlowNoRedirect
import os
from dotenv import load_dotenv

load_dotenv()

APP_KEY = os.getenv("APP_KEY")
APP_SECRET = os.getenv("APP_SECRET")

def gen_refresh_token():
    auth_flow = DropboxOAuth2FlowNoRedirect(
        APP_KEY,
        APP_SECRET,
        token_access_type='offline',
        use_pkce=True
    )

    authorize_url = auth_flow.start()
    print("1. Go to:", authorize_url)
    print("2. Click 'Allow'.")
    print("3. Copy the authorization code.")

    auth_code = input("Enter the authorization code here: ").strip()
    oauth_result = auth_flow.finish(auth_code)

    print("Access token:", oauth_result.access_token)
    print("Refresh token:", oauth_result.refresh_token)
    print("Expires at:", oauth_result.expires_at)

    return oauth_result.refresh_token

gen_refresh_token()