from typing import List, Optional
from urllib import request

import fixieai

BASE_PROMPT: str = (
    "I am an agent that answers questions about the TV show Futurama. "
    "User may have follow-up questions that refer to something mentioned before but I "
    "always do Ask Func[fixie_query_corpus] with a complete question, without any "
    "reference."
)

FEW_SHOTS: List[str] = []

URLS = [
    "https://en.wikipedia.org/wiki/Futurama",
    "https://en.wikipedia.org/wiki/Futurama_(season_1)",
    "https://en.wikipedia.org/wiki/Futurama_(season_2)",
    "https://en.wikipedia.org/wiki/Futurama_(season_3)",
    "https://en.wikipedia.org/wiki/Futurama_(season_4)",
    "https://en.wikipedia.org/wiki/Futurama_(season_5)",
    "https://en.wikipedia.org/wiki/Futurama_(season_6)",
    "https://en.wikipedia.org/wiki/Futurama_(season_7)",
]

CORPORA = [fixieai.DocumentCorpus(urls=URLS)]
agent = fixieai.CodeShotAgent(
    BASE_PROMPT,
    FEW_SHOTS,
    CORPORA,
    conversational=True,
)


@agent.register_corpus_func
def load_custom_corpus(request: fixieai.CorpusRequest) -> fixieai.CorpusResponse:
    """Load a custom corpus with auxilary content about the show.

    Note: This serves as an illustrative example, not a useful or efficient one."""
    if not request.partition:
        # The first request we receive will have no partition. We respond
        # with the two partitions we'd like to load, which may be loaded
        # in parallel. Subsequent requests will contain one of the two
        # partitions.
        # Other responses are able to add new partitions as well, but this
        # example doesn't use that capability.
        partition_names = ["movies", "private"]
        return fixieai.CorpusResponse(
            partitions=[
                fixieai.CorpusPartition(partition_name)
                for partition_name in partition_names
            ]
        )
    elif request.partition == "movies":
        return _handle_movies(request.page_token)
    elif request.partition == "private":
        return _handle_private(request.page_token)

    raise ValueError(f"Unexpected partition: {request.partition}")


def _handle_movies(page_token: Optional[str]) -> fixieai.CorpusResponse:
    if not page_token:
        # Since we didn't specify a first_page_token when the movies partition
        # was returned, our first request for this partition will have no page
        # token. We return two documents along with a token for page2 (purely
        # to demonstrate pagination).
        doc1 = _url_to_doc(
            "https://en.wikipedia.org/wiki/Futurama:_Bender%27s_Big_Score"
        )
        doc2 = _url_to_doc(
            "https://en.wikipedia.org/wiki/Futurama:_The_Beast_with_a_Billion_Backs"
        )
        return fixieai.CorpusResponse(page=fixieai.CorpusPage([doc1, doc2], "page2"))
    elif page_token == "page2":
        # The next request within the movies partition will have the page_token
        # we specified on the previous page. We return two more documents without
        # a new page token to indicate we've reached the end of this partition.
        doc3 = _url_to_doc("https://en.wikipedia.org/wiki/Futurama:_Bender%27s_Game")
        doc4 = _url_to_doc(
            "https://en.wikipedia.org/wiki/Futurama:_Into_the_Wild_Green_Yonder"
        )
        return fixieai.CorpusResponse(page=fixieai.CorpusPage([doc3, doc4]))

    raise ValueError(f"Unexpected page_token for movies partition: {page_token}")


def _url_to_doc(url: str) -> fixieai.CorpusDocument:
    page = request.urlopen(url)
    encoding = page.info().get_content_charset() or "utf-8"
    content_type = page.headers.get("Content-Type", "text/html")
    return fixieai.CorpusDocument(
        source_name=url,
        mime_type=content_type.split(";")[0].strip(),
        encoding=encoding,
        content=page.read(),
    )


def _handle_private(page_token: Optional[str]) -> fixieai.CorpusDocument:
    # Text content is easy to include as a document.
    doc1 = fixieai.CorpusDocument(
        source_name="favorite_episode.txt",
        content="""Mike's favorite episode is "The Devil's Hands
        are Idle Playthings" which is the final episode in season 4.""",
    )
    # Fixie can also automatically parse several other kinds of documents like
    # PDFs and Word docs. If you'd prefer to use your own parser, just execute
    # it here and return a text/plain document as above instead.
    with open("favorite_character.pdf", "rb") as f:
        doc2 = fixieai.CorpusDocument(
            source_name="favorite_character.pdf",
            content=f.read(),
            mime_type="application/pdf",
        )
    with open("favorite_movie.docx", "rb") as f:
        doc3 = fixieai.CorpusDocument(
            source_name="favorite_movie.docx",
            content=f.read(),
            mime_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        )
    return fixieai.CorpusResponse(page=fixieai.CorpusPage([doc1, doc2, doc3]))
