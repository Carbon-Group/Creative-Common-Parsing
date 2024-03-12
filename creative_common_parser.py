import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]

def get_video_ids(query, api_service_name, api_version, max_results=10):
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'YOUR_CLIENT_SECRET_FILE.json', scopes)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    youtube = googleapiclient.discovery.build(api_service_name, api_version, credentials=creds)

    request = youtube.search().list(
        part='snippet',
        maxResults=max_results,
        q=query,
        type='video',
        license='creativeCommon'
    )
    response = request.execute()

    video_ids = []
    for search_result in response.get('items', []):
        if search_result['id']['kind'] == 'youtube#video':
            video_ids.append(search_result['id']['videoId'])

    return video_ids

if __name__ == "__main__":
    query = "смартфон обзор"
    api_service_name = "youtube"
    api_version = "v3"
    video_ids = get_video_ids(query, api_service_name, api_version)
    print("Video IDs:", video_ids)
