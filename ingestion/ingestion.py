from dotenv import load_dotenv
from datetime import datetime
from botocore.exceptions import ClientError
import os
import requests
import boto3
import pandas as pd
import logging
import time

load_dotenv()

api_key = os.getenv("API_KEY")

top_artist_url = "https://ws.audioscrobbler.com/2.0/?method=chart.gettopartists&api_key={api_key}&format=json&page={page}"

top_tracks_url = "https://ws.audioscrobbler.com/2.0/?method=chart.gettoptracks&api_key={api_key}&format=json&page={page}"

artists_data = []
tracks_data = []


def extract_from_artist_api():
    """Extracts data from lastfm's api across all pages"""
    page = 1
    total_pages = 1

    while page <= total_pages:
        try:
            res = requests.get(top_artist_url.format(api_key=api_key, page=page))
            time.sleep(1)
            if res.status_code == 200:
                payload = res.json()["artists"]
                artists_data.extend(payload.get("artist", []))
                total_pages = int(payload["@attr"]["totalPages"])
                print(f"Fetched page {page}/{total_pages} - artist")
            else:
                print(res.status_code)
                break
        except Exception as e:
            logging.error(e)
            break

        page += 1


def extract_from_tracks_api():
    page = 1
    total_pages = 1

    while page <= total_pages:
        try:
            res = requests.get(top_tracks_url.format(api_key=api_key, page=page))
            time.sleep(5)
            if res.status_code == 200:
                payload = res.json()["tracks"]
                tracks_data.extend(payload.get("track", []))
                total_pages = int(payload["@attr"]["totalPages"])
                print(f"Fetched page {page}/{total_pages} - tracks ")
            else:
                print(res.status_code)
                break
        except Exception as e:
            logging.error(e)
            break

        page += 1


def upload_to_s3(FILE):
    """ Uploads file to S3 bucket, partitioned daily using a Hive-style dt= prefix"""
    dt = datetime.today().strftime("%Y-%m-%d")
    key = f"dt={dt}/{FILE}"
    BUCKET = os.getenv('BUCKET')
    s3 = boto3.client('s3')
    try:
        s3.upload_file(FILE, BUCKET, key)
    except ClientError:
        logging.error("Couldn't uplod to s3")

if __name__ == "__main__":
    extract_from_artist_api()
    extract_from_tracks_api()

    df = pd.json_normalize(artists_data)
    df.to_csv("artists.csv")

    df = pd.json_normalize(tracks_data)
    df.to_csv("tracks.csv")

    upload_to_s3("artists.csv")
    upload_to_s3("tracks.csv")