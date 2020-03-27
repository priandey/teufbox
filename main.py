import os

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

from models import MusicProposition

scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]

def main():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "client_secret.json"

    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
    credentials = flow.run_console()
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)

    # Now that api is authenticated, start process
    keep_going = "y"
    while keep_going == "y":
        keywords = input("Search for a video : ")
        request = youtube.search().list(
            part="snippet",
            q=keywords
        )
        response = request.execute()
        response_list = []
        for proposition in response['items']:
            prop = MusicProposition(name=proposition['snippet']['title'],
                                    channel=proposition['snippet']['channelTitle'],
                                    id=proposition['id']['videoId'])
            print(prop)
        keep_going = input("Continue (y/n) ?")


if __name__ == "__main__":
    main()
