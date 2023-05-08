# The Omnibus Project

This is an Agent that answers questions about the hit podcast, 
[The Omnibus Project](https://www.omnibusproject.com/), by Ken Jennings and John Roderick.

## Downloading and transcribing the podcast audio

The code in `downloader` deals with downloading and transcribing the audio for all of the
Omnibus Project episodes. It checks the RSS feed for the podcast, downloads any new episodes, 
uses the Deepgram speech-to-text model to transcribe the audio, and stores the results in a
Google Cloud Storage bucket.

To use this tool, you need to do the following.

First, create a Google Cloud Storage project and GCS bucket. Edit `downloader/main.py` and
change the `GCS_BUCKET` variable to the name of your bucket.

Create a Service Account with `storage.read` and `storage.write` permissions on this bucket, 
and download the JSON key file.

Create an account on [Deepgram](https://www.deepgram.com/), and create an API key.

Create the file `.env` in the `downloader` directory, and add the following lines:

```
GOOGLE_APPLICATION_CREDENTIALS=<path to the JSON key file for your service account>
DEEPGRAM_API_KEY=<your Deepgram API key>
```

You can then run:

```
$ poetry install
$ poetry run ./downloader/main.py
```

This will download each episode, transcribe it, and write three files per episode to the
`GCS_BUCKET` bucket: 
* `NNN.mp3` - the MP3 file of the episode audio
* `NNN.json` - the raw JSON result from the Deepgram transcription
* `NNN.txt` - the full text extracted from the Deepgram result
where `NNN` is the episode number.

This process takes about 10 seconds per episode.

Using the Deepgram Nova model, it will cost about $0.25 per episode
to transcribe; as of May 2023 there are 546 episodes, so the $200
credit for new accounts should be enough to transcribe them all.
