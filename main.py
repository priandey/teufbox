import os

import googleapiclient.discovery
import googleapiclient.errors

from models import ExternalMusic

scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]

def search_engine(keep_going, youtube, keywords):
    while keep_going:

        request = youtube.search().list(
            part="snippet",
            maxResults=10,
            q=keywords
        )
        response = request.execute()
        response_list = []
        position = 0
        for proposition in response['items']:
            try:
                prop = ExternalMusic(name=proposition['snippet']['title'],
                                     channel=proposition['snippet']['channelTitle'],
                                     id=proposition['id']['videoId'])
                response_list.append(prop)
                print(f'{position}    -    {prop})')
                position += 1
            except KeyError:
                pass

        choice = input("DL one [0 - 9] or continue search (type search) or exit (type exit) ? : ")

        if choice.isnumeric():
            index = int(choice)
            try:
                response_list[index].download()
            except IndexError:
                print("Le chiffre doit être entre 0 et 9")

        elif choice == 'exit':
            keep_going = False
        else:
            keywords = choice

def main():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = os.getenv("GOOGLE_KEY")

    youtube = googleapiclient.discovery.build(api_service_name,
                                              api_version,
                                              developerKey=DEVELOPER_KEY)

    # Now that api is authenticated, start process
    keep_going = True
    keywords = input("Search for a video : ")
    search_engine(keep_going, youtube, keywords)

if __name__ == "__main__":
    main()
