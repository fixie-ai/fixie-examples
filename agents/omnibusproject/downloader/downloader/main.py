#!/usr/bin/env python3

# This tool downloads all episodes of the Omnibus Project podcast, and uses
# Deepgram to generate transcripts for each episode.

import datetime
import json
import os
import re
import tempfile
import yaml

import click
from deepgram import Deepgram
import feedparser
from rich.console import Console
from rich.progress import Progress
import requests
from google.cloud import storage


DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")
if not DEEPGRAM_API_KEY:
    raise ValueError("Please set the DEEPGRAM_API_KEY environment variable")

# The default RSS feed to process. This is for the Omnibus Project podcast.
RSS_FEED = "https://feeds.fireside.fm/omnibus/rss"

# The default GCS bucket to upload data (audio and transcripts) to.
GCS_BUCKET = "mdw-omnibus-project-audio"

console = Console()


class Episode:
    """Represents a single podcast episode.

    Args:
        rss_entry: The RSS entry for the episode.
        gcs_bucket: The GCS bucket to upload data to.
    """

    def __init__(self, rss_entry, gcs_bucket, skip_processing=False):
        self._entry = rss_entry
        self._gcs_bucket = gcs_bucket
        self._skip_processing = skip_processing

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
        self._bucket = self._storage_client.bucket(self._gcs_bucket)
        self._mp3_blob = self._bucket.blob(self._mp3_filename)
        self._transcript_blob = self._bucket.blob(self._transcript_filename)
        self._fulltext_blob = self._bucket.blob(self._fulltext_filename)

    def process(self):
        """Process this episode and return a signed URL for the full text."""
        if not self._skip_processing:
            self.download_mp3()
            self.transcribe()
            self.extract_text()
        return f"https://storage.googleapis.com/{self._gcs_bucket}/{self._fulltext_filename}"

    def upload_to_gcs(self, localfile, destfile):
        """Upload the given file to GCS."""
        storage_client = storage.Client()
        bucket = storage_client.bucket(self._gcs_bucket)
        blob = bucket.blob(destfile)
        print(f"Uploading {localfile} to {self._gcs_bucket}/{destfile}...")
        with console.status(
            f"Uploading {localfile} to {self._gcs_bucket}/{destfile}..."
        ):
            blob.upload_from_filename(localfile)

    def download_mp3(self):
        """Download the MP3 for the episode and store in GCS."""
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
        """Return a signed URL for the given GCS blob."""
        blob_url = blob.generate_signed_url(
            version="v4", expiration=datetime.timedelta(seconds=86400), method="GET"
        )
        return blob_url

    def transcribe(self):
        """Transcribe the episode and store the transcript in GCS."""
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
        """Extract the raw text from the transcript and store in GCS."""
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
                # Break each sentence onto its own line. The transcripts we get
                # from Deepgram don't do this for us, and having everything on one
                # single long line doesn't work well with our chunking logic.
                .replace(". ", ".\n")
            )

        with tempfile.NamedTemporaryFile(suffix=".txt") as tmpfile:
            with open(tmpfile.name, "w") as outfile:
                outfile.write(full_text)
            self.upload_to_gcs(tmpfile.name, self._episode + ".txt")


@click.command()
@click.option("--rss_feed", default=RSS_FEED, help="RSS feed to process.")
@click.option("--gcs_bucket", default=GCS_BUCKET, help="GCS bucket to store data.")
@click.option("--output", default="episodes.yaml", help="The output YAML file.")
@click.option('--skip_processing', is_flag=True)
def download(rss_feed, gcs_bucket, output, skip_processing):
    episodes = []
    feed = feedparser.parse(rss_feed)
    for entry in feed.entries:
        try:
            episode = Episode(entry, gcs_bucket, skip_processing)
            fulltext_url = episode.process()
            episodes.append(fulltext_url)
        except Exception as e:
            console.print(f"[red]Error processing {entry.title} - skipping: {e}")
    with open(output, "w") as outfile:
        yaml.dump({"episodes": episodes}, outfile)
    console.print(f"Processed {len(episodes)} episodes, Wrote output to {output}")


if __name__ == "__main__":
    download()
