# The Omnibus Project

This is an Agent that answers questions about the hit podcast, 
[The Omnibus Project](https://www.omnibusproject.com/), by Ken Jennings and John Roderick.
This podcast is a compendium of arcane trivia and esoteric knowledge, and is a perfect
demonstration use case for Fixie agents being able to take what is a complex,
meandering dialogue between two people and turn it into a useful knowledge base.

The agent works by downloading the audio for each episode, transcribing it using the
Deepgram speech-to-text AI model, and creating a Fixie agent using the resulting
transcripts.

[Try it yourself!](https://app.fixie.ai/agents/mdw/omnibusproject)

Try asking questions like:

* Why does John pronounce "England" as "Englang"?
* Summarize the episode about Rhinos in Europe
* Who was Magic Alex?

## Running the agent yourself

## Downloading and transcribing the podcast audio

The code in `downloader` deals with downloading and transcribing the audio for all of the
Omnibus Project episodes. It checks the RSS feed for the podcast, downloads any new episodes, 
uses the Deepgram speech-to-text model to transcribe the audio, and stores the results in a
Google Cloud Storage bucket.

To use this tool, you need to do the following.

First, create a Google Cloud Storage project and GCS bucket. Edit `downloader/main.py` and
change the `GCS_BUCKET` variable to the name of your bucket.

For now, the contents of the bucket need to be world-readable for Fixie to be able to fetch
the transcripts and answer questions. You can do this by running:

```
gsutil defacl set public-read gs://<your bucket name>
```

Next, create a Service Account with `storage.read` and `storage.write` permissions on this bucket, 
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

The script will write the file `episodes.yaml` to the local directory, which contains a list
of all of the `.txt` files. The Fixie agent code reads this file on startup to populate
the list of URLs it will use to answer questions.

Using the Deepgram Nova model, it will cost about $0.25 per episode
to transcribe; as of May 2023 there are 546 episodes, so the $200
credit for new accounts should be enough to transcribe them all.

## Deploying the Agent

After running the `downloader` and populating the GCS bucket, you can deploy the agent
using:

```
$ fixie deploy
```

from the `agents/omnibusproject` directory. This will create a new Fixie agent called
`omnibusproject`. It will take a while for the Agent to fully index all of the episode
transcripts, so be patient.

