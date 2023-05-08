#!/usr/bin/env python3

import datetime
import json
import os
import re
import tempfile

from deepgram import Deepgram
import feedparser
from rich.console import Console
from rich.progress import Progress
import requests
from google.cloud import storage


DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")
if not DEEPGRAM_API_KEY:
    raise ValueError("Please set the DEEPGRAM_API_KEY environment variable")
RSS_FEED = "https://feeds.fireside.fm/omnibus/rss"
GCS_BUCKET = "mdw-omnibus-project-audio"

console = Console()


class Episode:
    def __init__(self, rss_entry):
        self._entry = rss_entry
        self._title = rss_entry.title
        self._mp3_url = self._entry.enclosures[0].href
        m = re.match("^Episode (\d+)", self._title)
        if not m:
            raise ValueError(f"Could not parse episode number from {self._title}")
        self._episode = m.group(1)
        self._mp3_filename = f"{self._episode}.mp3"
        self._transcript_filename = f"{self._episode}.json"
        self._fulltext_filename = f"{self._episode}.txt"

        self._storage_client = storage.Client()
        self._bucket = self._storage_client.bucket(GCS_BUCKET)
        self._mp3_blob = self._bucket.blob(self._mp3_filename)
        self._transcript_blob = self._bucket.blob(self._transcript_filename)
        self._fulltext_blob = self._bucket.blob(self._fulltext_filename)

    def process(self):
        self.download_mp3()
        self.transcribe()
        self.extract_text()

    def upload_to_gcs(self, localfile, destfile):
        storage_client = storage.Client()
        bucket = storage_client.bucket(GCS_BUCKET)
        blob = bucket.blob(destfile)
        print(f"Uploading {localfile} to {GCS_BUCKET}/{destfile}...")
        with console.status(f"Uploading {localfile} to {GCS_BUCKET}/{destfile}..."):
            blob.upload_from_filename(localfile)

    def download_mp3(self):
        if self._mp3_blob.exists():
            console.print(
                f"[yellow]Skipping download of {self._title} (already downloaded)"
            )
            return
        with tempfile.NamedTemporaryFile(suffix=".mp3") as tmpfile:
            with console.status(f"Downloading {self._title}..."):
                r = requests.get(self._mp3_url, allow_redirects=True, stream=True)
                with open(tmpfile.name, "wb") as outfile:
                    for chunk in r.iter_content(chunk_size=128):
                        outfile.write(chunk)
            self.upload_to_gcs(tmpfile.name, self._mp3_filename)

    def signed_url(self, blob):
        blob_url = blob.generate_signed_url(
            version="v4", expiration=datetime.timedelta(seconds=86400), method="GET"
        )
        return blob_url

    def transcribe(self):
        if self._transcript_blob.exists():
            console.print(
                f"[yellow]Skipping transcription of {self._title} (already transcribed)"
            )
            return

        with console.status(f"Transcribing {self._title}..."):
            dg = Deepgram(DEEPGRAM_API_KEY)
            MIMETYPE = "mp3"
            options = {"punctuate": True, "model": "general", "tier": "nova"}
            blob_url = self.signed_url(self._mp3_blob)
            console.print(f"Transcribing {self._title} from {blob_url}...")
            # source = {"url": blob_url, "mimetype": "audio/" + MIMETYPE}
            source = {"url": blob_url}
            res = dg.transcription.sync_prerecorded(source, options)
        with tempfile.NamedTemporaryFile(suffix=".json") as tmpfile:
            with open(tmpfile.name, "w") as transcript:
                json.dump(res, transcript)
            self.upload_to_gcs(tmpfile.name, self._transcript_filename)
        console.print(f"Saved transcript to {self._transcript_filename}")

    def extract_text(self):
        if self._fulltext_blob.exists():
            console.print(
                f"[yellow]Skipping extraction of {self._title} (already extracted)"
            )
            return
        if not self._transcript_blob.exists():
            raise ValueError(f"Transcript {self._transcript_filename} does not exist")
        with console.status(f"Extracting transcript from {self._title}..."):
            transcript_url = self.signed_url(self._transcript_blob)
            resp = requests.get(transcript_url)
            resp.raise_for_status()
            transcript = resp.json()
            full_text = (
                transcript.get("results", {})
                .get("channels", [{}])[0]
                .get("alternatives", [{}])[0]
                .get("transcript", "")
            )
        with tempfile.NamedTemporaryFile(suffix=".txt") as tmpfile:
            with open(tmpfile.name, "w") as outfile:
                outfile.write(full_text)
            self.upload_to_gcs(tmpfile.name, self._episode + ".txt")


feed = feedparser.parse(RSS_FEED)
for entry in feed.entries:
    episode = Episode(entry)
    episode.process()
