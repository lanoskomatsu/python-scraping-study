import collections
import os
import logging
from typing import Dict, Iterator, List

from googleapiclient.discovery import build
from pymongo import MongoClient, ReplaceOne, DESCENDING
from pymongo.collection import Collection

YOUTUBE_API_KEY = os.environ['YOUTUBE_API_KEY']
logging.getLogger('googleapiclient.discovery_cache').setLevel(logging.ERROR) # 不要なログを出力しないようにする

def main():
    mongo_client = MongoClient('localhost', 27017)
    collection = mongo_client.youtube.videos

    for items_per_page in search_videos('手芸'):
        save_to_mongodb(collection, items_per_page)

    show_top_video(collection)


def search_videos(query: str, max_pages: int=5) -> Iterator[List[Dict]]:
    youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
    search_request = youtube.search().list(part='snippet', q=str, type='video', maxResults=50)

    i = 0
    while search_request and i < max_pages:
        search_response = search_request.execute()
        print(i)
    
        video_ids = [item['id']['videoId'] for item in search_response['items']]

        videos_response = youtube.videos().list(part='snippet,statistics', id=','.join(video_ids)).execute()

        yield videos_response['items']

        search_response = youtube.search().list_next(search_request, search_response)
        i += 1

def save_to_mongodb(collection: Collection, items: List[dict]):
    for item in items:
        item['_id'] = item['id']

        for key, value in item['statistics'].items():
            item['statistics'][key] = int(value)

    operaions = [ReplaceOne({'_id': item['id']}, item, upsert=True) for item in items]
    result = collection.bulk_write(operaions)
    logging.info(f'Upserted {result.upserted_count} documents.')

def show_top_video(collection: Collection):
    for item in collection.find().sort('statistics.viewCount', DESCENDING).limit(5):
        print(item['statstics']['viewCount'], item['snippet']['title'])

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main()
